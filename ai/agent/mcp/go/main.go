package main

// MCP 最小可用实现（Go 版，仅标准库，真实 stdio JSON-RPC 传输）。
//
// 运行：
//   go run . -mode client                    # 一条命令：自动拉起 server 子进程并走完整个流程
//   go run . -mode client -question "RAG 是什么？"
//
// 也可以手动分两个终端跑（更接近真实部署形态）：
//   go build -o /tmp/mcp-server . && /tmp/mcp-server -mode server   # 终端 A：从 stdin 读请求
//   go run . -mode client -server /tmp/mcp-server                   # 终端 B
//
// 与 Python 版 mvp.py 的区别：Python 版用进程内对象模拟消息传递，
// 这个版本是**真的跨进程 stdio**，消息格式与真实 MCP 一致（一行一个 JSON-RPC 消息）。

import (
	"flag"
	"fmt"
	"os"
)

func main() {
	mode := flag.String("mode", "client", "运行模式：server | client")
	question := flag.String("question", "A2A 是干什么的？", "用户问题（client 模式）")
	serverBin := flag.String("server", "", "server 二进制路径（client 模式，默认复用自身二进制）")
	flag.Parse()

	var err error
	switch *mode {
	case "server":
		err = runServer()
	case "client":
		err = runClient(*question, *serverBin)
	default:
		fmt.Fprintf(os.Stderr, "unknown mode: %s\n", *mode)
		os.Exit(2)
	}
	if err != nil {
		fmt.Fprintln(os.Stderr, "error:", err)
		os.Exit(1)
	}
}
