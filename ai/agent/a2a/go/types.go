package main

// A2A 的数据模型 + JSON-RPC 2.0 信封。
//
// A2A 传输是 HTTP 上的 JSON-RPC 2.0（流式用 SSE），身份走 OAuth，
// Card 可 JWS 签名。这个 MVP 只实现信封与状态机，鉴权与签名留占位字段。

import "encoding/json"

type Request struct {
	JSONRPC string          `json:"jsonrpc"`
	ID      any             `json:"id,omitempty"`
	Method  string          `json:"method"`
	Params  json.RawMessage `json:"params,omitempty"`
}

type Response struct {
	JSONRPC string          `json:"jsonrpc"`
	ID      any             `json:"id"`
	Result  json.RawMessage `json:"result,omitempty"`
	Error   *RPCError       `json:"error,omitempty"`
}

type RPCError struct {
	Code    int    `json:"code"`
	Message string `json:"message"`
}

func mustJSON(v any) json.RawMessage {
	b, err := json.Marshal(v)
	if err != nil {
		panic(err)
	}
	return b
}

// Skill 是 Card 上公布的「我能办哪些事」。
// 粒度按业务闭环（explain_charge），不是按数据库操作（select_from_bills）。
type Skill struct {
	ID     string            `json:"id"`
	Name   string            `json:"name"`
	Input  map[string]string `json:"input"`
	Output map[string]string `json:"output"`
}

// AgentCard 是可发现的名片。注意：这里**不**放内部 tool schema 或连接串。
type AgentCard struct {
	Name            string         `json:"name"`
	Description     string         `json:"description"`
	URL             string         `json:"url"`
	Version         string         `json:"version"`
	Skills          []Skill        `json:"skills"`
	Authentication  map[string]any `json:"authentication"`
	Signature       string         `json:"signature,omitempty"` // 生产里放 JWS
	SignatureStatus string         `json:"signatureStatus"`
}

// Task 是一次委托的生命周期。
type Task struct {
	ID       string         `json:"id"`
	Skill    string         `json:"skill"`
	Input    map[string]any `json:"input"`
	State    string         `json:"state"`
	Artifact map[string]any `json:"artifact,omitempty"`
	Error    string         `json:"error,omitempty"`
}

// TaskState 常量。
const (
	StateSubmitted = "submitted"
	StateWorking   = "working"
	StateCompleted = "completed"
	StateFailed    = "failed"
)

func isTerminal(state string) bool {
	return state == StateCompleted || state == StateFailed
}

type SendParams struct {
	Skill string         `json:"skill"`
	Input map[string]any `json:"input"`
}

type GetParams struct {
	ID string `json:"id"`
}
