package main

// JSON-RPC 2.0 消息层 + stdio 分帧。
//
// MCP 的本地传输就是 stdio：父进程（Host/Client）拉起 server 子进程，
// 双方各写一个 JSON 消息一行（\n 分隔），不做 Content-Length 分帧。
// 所以这里用 json.Encoder / json.Decoder 直接对着 pipe 读写即可。

import (
	"encoding/json"
	"io"
	"sync"
)

// protocolVersion 是本 MVP 实现的规范版本。
// 注意 2026-07-28 起握手被移除、版本改由每请求 _meta 承载；
// 这里保持和 Python 版 mvp.py 一致的 2025-03-26 形状，便于对照阅读。
const protocolVersion = "2025-03-26"

// Request 是一个 JSON-RPC 请求或通知。ID 为 nil 即为通知（不需要回包）。
type Request struct {
	JSONRPC string          `json:"jsonrpc"`
	ID      any             `json:"id,omitempty"`
	Method  string          `json:"method"`
	Params  json.RawMessage `json:"params,omitempty"`
}

// Response 是一个 JSON-RPC 响应，Result 与 Error 二选一。
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

func (r *Response) String() string {
	if r.Error != nil {
		return "error: " + r.Error.Message
	}
	return string(r.Result)
}

func mustJSON(v any) json.RawMessage {
	b, err := json.Marshal(v)
	if err != nil {
		// MVP：所有结构都是静态已知的，序列化失败属于代码 bug
		panic(err)
	}
	return b
}

// Conn 是 Client 侧对某一条 stdio 连接的会话封装。
// 对应 README 里的「Client = Host 内对某一个 server 的协议会话」。
type Conn struct {
	enc *json.Encoder
	dec *json.Decoder

	mu sync.Mutex
	id int64
}

func NewConn(w io.Writer, r io.Reader) *Conn {
	return &Conn{enc: json.NewEncoder(w), dec: json.NewDecoder(r)}
}

// Call 发一个请求并同步等它的响应（stdio 是有序单流，id 严格递增即可）。
func (c *Conn) Call(method string, params any) (*Response, error) {
	c.mu.Lock()
	defer c.mu.Unlock()

	c.id++
	req := Request{JSONRPC: "2.0", ID: c.id, Method: method}
	if params != nil {
		req.Params = mustJSON(params)
	}
	if err := c.enc.Encode(req); err != nil {
		return nil, err
	}

	var resp Response
	if err := c.dec.Decode(&resp); err != nil {
		return nil, err
	}
	return &resp, nil
}

// Notify 发一个通知：没有 id，server 不回包。
func (c *Conn) Notify(method string, params any) error {
	c.mu.Lock()
	defer c.mu.Unlock()

	req := Request{JSONRPC: "2.0", Method: method}
	if params != nil {
		req.Params = mustJSON(params)
	}
	return c.enc.Encode(req)
}
