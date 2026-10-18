package main

// MCP Host/Client：拉起 server 子进程，完成 initialize → tools/list → tools/call。
//
// 真实 Host（Cursor / Claude Desktop / 自研 Agent 运行时）做的三件事：
//   1. 拉起并管理 server 子进程（这里就是 exec）
//   2. 把 tools/list 拿到的 schema 交给模型，让模型选工具
//   3. 调 tools/call，把结果塞回上下文继续生成
// 第 2 步这里用 fakeLLMPick 规则模拟——MVP 不依赖真实 LLM，只为看清协议形状。

import (
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"strings"
)

type toolCall struct {
	tool string
	args map[string]any
}

// fakeLLMPickTools 模拟「模型选工具」这一步。
func fakeLLMPickTools(question string) []toolCall {
	if strings.Contains(strings.ToUpper(question), "A2A") {
		return []toolCall{
			{tool: "search_docs", args: map[string]any{"query": "A2A"}},
			{tool: "get_doc", args: map[string]any{"id": "a2a"}},
		}
	}
	return []toolCall{{tool: "search_docs", args: map[string]any{"query": question}}}
}

func runClient(question, serverBin string) error {
	// 默认复用自身二进制，用 -mode server 再启动一次，
	// 这样 `go run . -mode client` 一条命令就能演示真实的跨进程 stdio 通信。
	if serverBin == "" {
		self, err := os.Executable()
		if err != nil {
			return err
		}
		serverBin = self
	}

	cmd := exec.Command(serverBin, "-mode", "server")
	cmd.Stderr = os.Stderr // server 的日志直通到终端，不参与协议
	stdin, err := cmd.StdinPipe()
	if err != nil {
		return err
	}
	stdout, err := cmd.StdoutPipe()
	if err != nil {
		return err
	}
	if err := cmd.Start(); err != nil {
		return err
	}
	// 关闭 stdin = 告诉 server「我说完了」，它会读到 EOF 后自行退出
	defer func() {
		_ = stdin.Close()
		_ = cmd.Wait()
	}()

	conn := NewConn(stdin, stdout)

	// --- 1. initialize：握手，拿 server 能力与协议版本 ---
	var init InitializeResult
	resp, err := conn.Call("initialize", map[string]any{
		"protocolVersion": protocolVersion,
		"capabilities":    map[string]any{},
		"clientInfo":      map[string]any{"name": "mvp-host", "version": "0.1.0"},
	})
	if err != nil {
		return err
	}
	if resp.Error != nil {
		return fmt.Errorf("initialize failed: %s", resp.Error.Message)
	}
	if err := json.Unmarshal(resp.Result, &init); err != nil {
		return err
	}
	fmt.Printf("=== initialize ===\n")
	fmt.Printf("protocolVersion=%s serverInfo=%v capabilities=%v\n\n",
		init.ProtocolVersion, init.ServerInfo, init.Capabilities)

	// --- 2. notifications/initialized：握手收尾通知 ---
	if err := conn.Notify("notifications/initialized", nil); err != nil {
		return err
	}

	// --- 3. tools/list：运行时发现工具，而不是把工具写死在应用里 ---
	var list struct {
		Tools []ToolSpec `json:"tools"`
	}
	resp, err = conn.Call("tools/list", nil)
	if err != nil {
		return err
	}
	if resp.Error != nil {
		return fmt.Errorf("tools/list failed: %s", resp.Error.Message)
	}
	if err := json.Unmarshal(resp.Result, &list); err != nil {
		return err
	}
	fmt.Println("=== tools/list ===")
	for _, t := range list.Tools {
		fmt.Printf("  [docs] %s: %s\n", t.Name, t.Description)
	}
	fmt.Println()

	// --- 4. 模型选工具 → tools/call ---
	fmt.Printf("=== 用户问题: %s ===\n", question)
	for _, call := range fakeLLMPickTools(question) {
		resp, err := conn.Call("tools/call", CallToolParams{Name: call.tool, Arguments: call.args})
		if err != nil {
			return err
		}
		if resp.Error != nil {
			return fmt.Errorf("tools/call failed: %s", resp.Error.Message)
		}
		var out CallToolResult
		if err := json.Unmarshal(resp.Result, &out); err != nil {
			return err
		}
		text := ""
		if len(out.Content) > 0 {
			text, _ = out.Content[0]["text"].(string)
		}
		fmt.Printf("tools/call %s%v -> %s error=%t\n", call.tool, call.args, text, out.IsError)
	}
	return nil
}
