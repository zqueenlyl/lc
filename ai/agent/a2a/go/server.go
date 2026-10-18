package main

// A2A Server（被委托方 / Specialist）：对外只有三件事——
//   1. GET  /.well-known/agent.json   → Agent Card（可发现）
//   2. POST /                         → JSON-RPC：tasks/send、tasks/get
//   3. GET  /tasks/{id}/stream        → SSE 推送任务状态
//
// 对内它可以随便查库：BILLS 只存在于这个进程的内存里，
// 永远不会被写进 Artifact——这就是隔离发生的地方。

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"sync"
	"time"
)

// bills 是「账务侧的内部数据库」。委托方拿不到它，只能拿到 artifact 里的几个字段。
var bills = map[string]map[string]any{
	"B-1001": {"user": "u1", "amount": 128.0, "reason": "会员自动续费"},
	"B-1002": {"user": "u1", "amount": 36.0, "reason": "流量加油包"},
}

// 模拟长任务：真实场景里对方可能要跑几分钟、甚至要人工审批。
const specialistWorkDelay = 500 * time.Millisecond

type Server struct {
	card AgentCard

	mu    sync.Mutex
	tasks map[string]*Task
	subs  map[string][]chan []byte // taskID -> 订阅者（传的是已序列化的 Task）
}

func NewBillingAgent() *Server {
	return &Server{
		card: AgentCard{
			Name:        "billing-agent",
			Description: "处理账单查询与争议解释，不开放底层 SQL。",
			URL:         "http://127.0.0.1:8899",
			Version:     "1.0",
			Skills: []Skill{
				{
					ID:     "explain_charge",
					Name:   "解释一笔扣费",
					Input:  map[string]string{"bill_id": "string"},
					Output: map[string]string{"summary": "string"},
				},
			},
			Authentication:  map[string]any{"schemes": []string{"bearer"}},
			Signature:       "",
			SignatureStatus: "demo-unsigned（生产环境应为 JWS，否则任何人都能冒充财务 Agent）",
		},
		tasks: map[string]*Task{},
		subs:  map[string][]chan []byte{},
	}
}

func (s *Server) Handler() http.Handler {
	mux := http.NewServeMux()
	// 三个模式都带方法前缀：Go 的 ServeMux 里「带方法的宽路径」与「不带方法的窄路径」会冲突
	mux.HandleFunc("GET /.well-known/agent.json", s.handleCard)
	mux.HandleFunc("POST /", s.handleRPC)
	mux.HandleFunc("GET /tasks/{id}/stream", s.handleStream)
	return mux
}

func (s *Server) handleCard(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	_, _ = w.Write(mustJSON(s.card))
}

func (s *Server) handleRPC(w http.ResponseWriter, r *http.Request) {
	var req Request
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeRPC(w, &Response{JSONRPC: "2.0", ID: nil, Error: &RPCError{Code: -32700, Message: "parse error"}})
		return
	}

	switch req.Method {
	case "tasks/send":
		var p SendParams
		if len(req.Params) > 0 {
			_ = json.Unmarshal(req.Params, &p)
		}
		task := s.newTask(p.Skill, p.Input)
		go s.run(task) // 异步：调用方立刻拿回 task id + state=working
		writeRPC(w, &Response{JSONRPC: "2.0", ID: req.ID, Result: mustJSON(task)})

	case "tasks/get":
		var p GetParams
		if len(req.Params) > 0 {
			_ = json.Unmarshal(req.Params, &p)
		}
		s.mu.Lock()
		task := s.tasks[p.ID]
		s.mu.Unlock()
		if task == nil {
			writeRPC(w, &Response{JSONRPC: "2.0", ID: req.ID, Error: &RPCError{Code: -32602, Message: "task not found: " + p.ID}})
			return
		}
		writeRPC(w, &Response{JSONRPC: "2.0", ID: req.ID, Result: mustJSON(task)})

	default:
		writeRPC(w, &Response{JSONRPC: "2.0", ID: req.ID, Error: &RPCError{Code: -32601, Message: "method not found: " + req.Method}})
	}
}

func writeRPC(w http.ResponseWriter, resp *Response) {
	w.Header().Set("Content-Type", "application/json")
	_, _ = w.Write(mustJSON(resp))
}

func (s *Server) newTask(skill string, input map[string]any) *Task {
	t := &Task{
		ID:    fmt.Sprintf("task-%d", time.Now().UnixNano()),
		Skill: skill,
		Input: input,
		State: StateWorking,
	}
	s.mu.Lock()
	s.tasks[t.ID] = t
	s.mu.Unlock()
	log.Printf("[server] task %s created skill=%s state=%s", t.ID, skill, t.State)
	return t
}

// run 是「账务 Agent 内部的思考过程」——对外不可见。
func (s *Server) run(t *Task) {
	time.Sleep(specialistWorkDelay)

	if t.Skill != "explain_charge" {
		s.finish(t, StateFailed, nil, "unknown skill: "+t.Skill)
		return
	}
	billID, _ := t.Input["bill_id"].(string)
	row, ok := bills[billID]
	if !ok {
		s.finish(t, StateFailed, nil, "bill not found: "+billID)
		return
	}

	// 只挑需要的字段放进 artifact：内部细节（user 的完整账单、SQL、prompt）不外泄
	artifact := map[string]any{
		"summary": fmt.Sprintf("账单 %s 扣费 %v 元，原因：%v。", billID, row["amount"], row["reason"]),
		"user":    row["user"],
	}
	s.finish(t, StateCompleted, artifact, "")
}

func (s *Server) finish(t *Task, state string, artifact map[string]any, errMsg string) {
	s.mu.Lock()
	t.State = state
	t.Artifact = artifact
	t.Error = errMsg
	subs := s.subs[t.ID]
	delete(s.subs, t.ID) // 终态后不再有后续事件
	s.mu.Unlock()

	log.Printf("[server] task %s -> %s", t.ID, state)
	for _, ch := range subs {
		select {
		case ch <- mustJSON(t):
		default: // 订阅者不消费就丢弃，绝不阻塞 server
		}
	}
}

// handleStream 是 SSE：长任务的中间状态与终态都从这里推给委托方。
func (s *Server) handleStream(w http.ResponseWriter, r *http.Request) {
	id := r.PathValue("id")

	s.mu.Lock()
	task, ok := s.tasks[id]
	if !ok {
		s.mu.Unlock()
		http.NotFound(w, r)
		return
	}
	ch := make(chan []byte, 8)
	s.subs[id] = append(s.subs[id], ch)
	current := mustJSON(task) // 在锁内取快照，避免与 run() 的写入竞争
	s.mu.Unlock()

	defer func() {
		s.mu.Lock()
		remain := make([]chan []byte, 0, len(s.subs[id]))
		for _, c := range s.subs[id] {
			if c != ch {
				remain = append(remain, c)
			}
		}
		if len(remain) == 0 {
			delete(s.subs, id)
		} else {
			s.subs[id] = remain
		}
		s.mu.Unlock()
	}()

	w.Header().Set("Content-Type", "text/event-stream")
	w.Header().Set("Cache-Control", "no-cache")
	w.Header().Set("Connection", "keep-alive")
	w.WriteHeader(http.StatusOK)
	flusher, ok := w.(http.Flusher)
	if !ok {
		return
	}

	// 先推一次当前状态，避免订阅晚于状态变更时丢事件
	fmt.Fprintf(w, "event: current\ndata: %s\n\n", current)
	flusher.Flush()

	for {
		select {
		case data := <-ch:
			var t Task
			_ = json.Unmarshal(data, &t)
			fmt.Fprintf(w, "event: %s\ndata: %s\n\n", t.State, data)
			flusher.Flush()
			if isTerminal(t.State) {
				return
			}
		case <-r.Context().Done():
			return
		}
	}
}

func runServer(addr string) error {
	log.SetOutput(os.Stderr)
	srv := &http.Server{Addr: addr, Handler: NewBillingAgent().Handler()}
	log.Printf("[server] billing-agent listening on %s", addr)
	return srv.ListenAndServe()
}
