package main

// MCP Server：暴露 tools，通过 stdio 与 Client 对话。
//
// 真实 MCP server 是独立进程，对这个文件来说 stdin/stdout 就是协议边界。
// 铁律：**stdout 只能出现协议消息**，日志一律写 stderr，否则会污染分帧。

import (
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"log"
	"os"
	"strings"
)

// docs 是示例领域数据（真实场景背后是数据库 / 内部 API）。
var docs = map[string]string{
	"mcp": "MCP 用 JSON-RPC 把 tools/resources/prompts 标准化，供 Host 发现并调用。",
	"a2a": "A2A 让两个独立 Agent 用 Agent Card 发现彼此并委托任务。",
	"rag": "RAG 在生成前检索外部知识，降低幻觉与知识过期。",
}

// ToolSpec 是 tools/list 返回给客户端的工具元数据。
// 这段描述是给**模型**看的：模型几乎只靠它决定要不要调、怎么传参。
type ToolSpec struct {
	Name        string         `json:"name"`
	Description string         `json:"description"`
	InputSchema map[string]any `json:"inputSchema"`
}

// Tool 是服务端内部定义：元数据 + 真正的执行体（handler 不导出，不会进 JSON）。
type Tool struct {
	ToolSpec
	handler func(args map[string]any) (string, error)
}

type InitializeResult struct {
	ProtocolVersion string         `json:"protocolVersion"`
	ServerInfo      map[string]any `json:"serverInfo"`
	Capabilities    map[string]any `json:"capabilities"`
}

type CallToolParams struct {
	Name      string         `json:"name"`
	Arguments map[string]any `json:"arguments"`
}

// CallToolResult 是 tools/call 的返回信封。
// 注意：**错误也走信封**（isError=true），而不是让进程崩掉或返回协议级 error——
// 这样模型能看到「我调错了」并改参重试。
type CallToolResult struct {
	Content []map[string]any `json:"content"`
	IsError bool             `json:"isError"`
}

type Server struct {
	name string
	// order 固定 tools/list 的返回顺序。
	// 规范（2026-07-28）建议 SHOULD 返回确定性顺序：利于客户端缓存与 LLM 提示缓存命中。
	order []string
	tools map[string]Tool
}

func NewDocsServer() *Server {
	return &Server{
		name:  "docs",
		order: []string{"search_docs", "get_doc"},
		tools: map[string]Tool{
			"search_docs": {
				ToolSpec: ToolSpec{
					Name:        "search_docs",
					Description: "按关键词搜索内部文档。当用户问「有哪些资料/某某是什么」时使用。",
					InputSchema: map[string]any{
						"type": "object",
						"properties": map[string]any{
							"query": map[string]any{"type": "string"},
						},
						"required": []string{"query"},
					},
				},
				handler: searchDocs,
			},
			"get_doc": {
				ToolSpec: ToolSpec{
					Name:        "get_doc",
					Description: "按文档 id 读取全文。id 必须来自 search_docs 的 hits。",
					InputSchema: map[string]any{
						"type": "object",
						"properties": map[string]any{
							"id": map[string]any{"type": "string"},
						},
						"required": []string{"id"},
					},
				},
				handler: getDoc,
			},
		},
	}
}

func searchDocs(args map[string]any) (string, error) {
	q, _ := args["query"].(string)
	q = strings.ToLower(q)
	hits := make([]string, 0, len(docs))
	for id, body := range docs {
		if strings.Contains(id, q) || strings.Contains(strings.ToLower(body), q) {
			hits = append(hits, id)
		}
	}
	if len(hits) == 0 {
		return "hits: (none)", nil
	}
	return "hits: " + strings.Join(hits, ", "), nil
}

func getDoc(args map[string]any) (string, error) {
	id, _ := args["id"].(string)
	body, ok := docs[id]
	if !ok {
		return "", fmt.Errorf("doc not found: %s", id)
	}
	return body, nil
}

// handle 分发一个请求；返回 nil 表示这是通知，不回包。
func (s *Server) handle(req *Request) *Response {
	switch req.Method {
	case "initialize":
		return &Response{
			JSONRPC: "2.0",
			ID:      req.ID,
			Result: mustJSON(InitializeResult{
				ProtocolVersion: protocolVersion,
				ServerInfo:      map[string]any{"name": s.name, "version": "0.1.0"},
				Capabilities:    map[string]any{"tools": map[string]any{}},
			}),
		}

	case "notifications/initialized":
		// 握手完成的通知，无需回包
		return nil

	case "tools/list":
		list := make([]ToolSpec, 0, len(s.tools))
		for _, name := range s.order {
			if t, ok := s.tools[name]; ok {
				list = append(list, t.ToolSpec)
			}
		}
		return &Response{JSONRPC: "2.0", ID: req.ID, Result: mustJSON(map[string]any{"tools": list})}

	case "tools/call":
		return s.handleCall(req)

	default:
		return &Response{
			JSONRPC: "2.0",
			ID:      req.ID,
			Error:   &RPCError{Code: -32601, Message: "method not found: " + req.Method},
		}
	}
}

func (s *Server) handleCall(req *Request) *Response {
	var p CallToolParams
	if len(req.Params) > 0 {
		if err := json.Unmarshal(req.Params, &p); err != nil {
			return &Response{JSONRPC: "2.0", ID: req.ID, Error: &RPCError{Code: -32602, Message: "invalid params"}}
		}
	}

	tool, ok := s.tools[p.Name]
	if !ok {
		// 未知工具：仍然回信封，让模型自己纠正
		return &Response{JSONRPC: "2.0", ID: req.ID, Result: mustJSON(CallToolResult{
			Content: []map[string]any{{"type": "text", "text": "unknown tool: " + p.Name}},
			IsError: true,
		})}
	}

	text, err := tool.handler(p.Arguments)
	if err != nil {
		return &Response{JSONRPC: "2.0", ID: req.ID, Result: mustJSON(CallToolResult{
			Content: []map[string]any{{"type": "text", "text": err.Error()}},
			IsError: true,
		})}
	}
	return &Response{JSONRPC: "2.0", ID: req.ID, Result: mustJSON(CallToolResult{
		Content: []map[string]any{{"type": "text", "text": text}},
	})}
}

// runServer 从 stdin 逐条读请求、向 stdout 写响应，直到 stdin 关闭（EOF）。
func runServer() error {
	dec := json.NewDecoder(os.Stdin)
	enc := json.NewEncoder(os.Stdout)
	srv := NewDocsServer()

	log.SetOutput(os.Stderr) // 日志绝不进 stdout
	log.Printf("[server] docs server started, protocolVersion=%s", protocolVersion)

	for {
		var req Request
		if err := dec.Decode(&req); err != nil {
			if errors.Is(err, io.EOF) {
				log.Print("[server] stdin closed, exiting")
				return nil
			}
			return err
		}

		resp := srv.handle(&req)
		if resp == nil {
			log.Printf("[server] <- notification %s", req.Method)
			continue
		}
		log.Printf("[server] <- %s (id=%v)", req.Method, req.ID)
		if err := enc.Encode(resp); err != nil {
			return err
		}
	}
}
