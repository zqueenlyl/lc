package main

// A2A Client（委托方 / Orchestrator）：
//   1. 运行时读 Agent Card 做发现（不硬编码对方 URL 与技能列表）
//   2. tasks/send 提交委托，立刻拿回 task id + state=working
//   3. 用 SSE 订阅或 tasks/get 轮询，等到终态
//   4. 只拿到 Artifact——对方的数据库、内部 prompt 一概看不见
//
// 关键点：**这个进程的内存里没有 BILLS 表**。账单数据只存在于 server 进程，
// 跨进程的边界就是权限边界，这正是 A2A 存在的理由。

import (
	"bufio"
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"os/exec"
	"strings"
	"time"
)

// rpc 打一次 JSON-RPC，解出 result 或 error。
func rpc(client *http.Client, base, method string, params any) (*Task, error) {
	body, err := json.Marshal(Request{JSONRPC: "2.0", ID: time.Now().UnixNano(), Method: method, Params: mustJSON(params)})
	if err != nil {
		return nil, err
	}
	resp, err := client.Post(base+"/", "application/json", bytes.NewReader(body))
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	var out Response
	if err := json.NewDecoder(resp.Body).Decode(&out); err != nil {
		return nil, err
	}
	if out.Error != nil {
		return nil, fmt.Errorf("%s: %s", method, out.Error.Message)
	}
	var t Task
	if err := json.Unmarshal(out.Result, &t); err != nil {
		return nil, err
	}
	return &t, nil
}

// waitReady 轮询 Card，直到 server 起来或超时。
func waitReady(client *http.Client, base string, timeout time.Duration) error {
	deadline := time.Now().Add(timeout)
	for time.Now().Before(deadline) {
		resp, err := client.Get(base + "/.well-known/agent.json")
		if err == nil {
			resp.Body.Close()
			if resp.StatusCode == http.StatusOK {
				return nil
			}
		}
		time.Sleep(50 * time.Millisecond)
	}
	return fmt.Errorf("server not ready at %s", base)
}

// subscribe 用 SSE 等终态，返回最后一个 Task。
func subscribe(client *http.Client, base, taskID string, timeout time.Duration) (*Task, error) {
	req, err := http.NewRequest(http.MethodGet, base+"/tasks/"+taskID+"/stream", nil)
	if err != nil {
		return nil, err
	}
	ctx, cancel := context.WithTimeout(context.Background(), timeout)
	defer cancel()

	resp, err := client.Do(req.WithContext(ctx))
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	var last *Task
	sc := bufio.NewScanner(resp.Body)
	var data string
	for sc.Scan() {
		line := sc.Text()
		if line == "" {
			if data != "" {
				var t Task
				if err := json.Unmarshal([]byte(data), &t); err == nil {
					fmt.Printf("  [SSE] state=%s\n", t.State)
					last = &t
					if isTerminal(t.State) {
						return last, nil
					}
				}
			}
			data = ""
			continue
		}
		if strings.HasPrefix(line, "data: ") {
			data += strings.TrimPrefix(line, "data: ")
		}
	}
	if err := sc.Err(); err != nil {
		return nil, err
	}
	if last == nil {
		return nil, io.ErrUnexpectedEOF
	}
	return last, nil
}

// poll 用 tasks/get 轮询等终态。
func poll(client *http.Client, base, taskID string, timeout time.Duration) (*Task, error) {
	deadline := time.Now().Add(timeout)
	for time.Now().Before(deadline) {
		t, err := rpc(client, base, "tasks/get", GetParams{ID: taskID})
		if err != nil {
			return nil, err
		}
		fmt.Printf("  [poll] state=%s\n", t.State)
		if isTerminal(t.State) {
			return t, nil
		}
		time.Sleep(150 * time.Millisecond)
	}
	return nil, fmt.Errorf("timeout waiting for task %s", taskID)
}

func runClient(addr, transport, billID, skill, serverBin string) error {
	base := "http://" + addr
	client := &http.Client{Timeout: 5 * time.Second}

	// 启动被委托方（默认复用自身二进制，一条命令即可演示跨进程委派）
	if serverBin == "" {
		self, err := os.Executable()
		if err != nil {
			return err
		}
		serverBin = self
	}
	cmd := exec.Command(serverBin, "-mode", "server", "-addr", addr)
	cmd.Stderr = os.Stderr
	if err := cmd.Start(); err != nil {
		return err
	}
	defer func() {
		_ = cmd.Process.Kill()
		_, _ = cmd.Process.Wait()
	}()

	if err := waitReady(client, base, 3*time.Second); err != nil {
		return err
	}

	// --- 1. 发现：运行时读 Agent Card ---
	var card AgentCard
	resp, err := client.Get(base + "/.well-known/agent.json")
	if err != nil {
		return err
	}
	if err := json.NewDecoder(resp.Body).Decode(&card); err != nil {
		resp.Body.Close()
		return err
	}
	resp.Body.Close()

	fmt.Println("=== Agent Card ===")
	fmt.Printf("%s @ %s (version %s)\n", card.Name, card.URL, card.Version)
	fmt.Printf("signature status: %s\n", card.SignatureStatus)
	for _, s := range card.Skills {
		fmt.Printf("skill: %s（%s） input=%v output=%v\n", s.ID, s.Name, s.Input, s.Output)
	}
	fmt.Println()

	// --- 2. 校验对方确实有这个技能（真实场景里这一步由 LLM 或路由规则完成）---
	supported := false
	for _, s := range card.Skills {
		if s.ID == skill {
			supported = true
		}
	}
	if !supported {
		return fmt.Errorf("card 上没有技能 %q，别硬发——这就是 Card 的价值", skill)
	}

	// --- 3. tasks/send：提交委托，立刻拿回 working ---
	fmt.Printf("=== 用户: 为什么扣了 %s 这笔？ ===\n", billID)
	sent, err := rpc(client, base, "tasks/send", SendParams{Skill: skill, Input: map[string]any{"bill_id": billID}})
	if err != nil {
		return err
	}
	fmt.Printf("tasks/send -> id=%s state=%s（异步：调用方不阻塞）\n", sent.ID, sent.State)

	// --- 4. 等终态：SSE 推送 or 轮询 ---
	var final *Task
	switch transport {
	case "sse":
		final, err = subscribe(client, base, sent.ID, 5*time.Second)
	case "poll":
		final, err = poll(client, base, sent.ID, 5*time.Second)
	default:
		return fmt.Errorf("unknown transport: %s", transport)
	}
	if err != nil {
		return err
	}

	// --- 5. 只用 Artifact ---
	if final.State == StateFailed {
		fmt.Printf("\n=== 委托失败 ===\n%s\n", final.Error)
		return nil
	}
	fmt.Printf("\n=== Artifact（对方交回的产物）===\n%v\n", final.Artifact["summary"])
	fmt.Printf("[客服转述] %v\n", final.Artifact["summary"])

	fmt.Println("\n=== 隔离检查：委托方看不到 BILLS ===")
	fmt.Println("client 进程内存里没有 bills 表：数据只存在于 server 进程，")
	fmt.Println("跨进程边界即权限边界；这里拿到的只有 Artifact 里的 summary 与 user 字段。")
	return nil
}
