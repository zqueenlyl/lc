package main

// A2A 最小可用实现（Go 版，仅标准库，真实 HTTP + JSON-RPC 2.0 + SSE）。
//
// 运行：
//   go run . -mode client                          # 一条命令：自动拉起 server 子进程并完成一次委托
//   go run . -mode client -transport poll          # 用 tasks/get 轮询代替 SSE
//   go run . -mode client -skill unknown_skill     # 看 failed 分支
//   go run . -mode client -bill B-9999             # 看「账单不存在」分支
//
// 也可以手动分两个终端跑：
//   go build -o /tmp/a2a-server . && /tmp/a2a-server -mode server -addr 127.0.0.1:8899
//   go run . -mode client -server /tmp/a2a-server -addr 127.0.0.1:8899
//
// 与 Python 版 mvp.py 的区别：Python 版在同一进程内用对象模拟两端，
// 这个版本是**真的两个进程**走 HTTP——隔离不再靠约定，而是靠进程边界天然成立。

import (
	"flag"
	"fmt"
	"os"
)

func main() {
	mode := flag.String("mode", "client", "运行模式：server | client")
	addr := flag.String("addr", "127.0.0.1:8899", "监听/连接地址")
	transport := flag.String("transport", "sse", "等终态的方式：sse | poll")
	billID := flag.String("bill", "B-1001", "账单号")
	skill := flag.String("skill", "explain_charge", "要委托的技能 id")
	serverBin := flag.String("server", "", "server 二进制路径（client 模式，默认复用自身二进制）")
	flag.Parse()

	var err error
	switch *mode {
	case "server":
		err = runServer(*addr)
	case "client":
		err = runClient(*addr, *transport, *billID, *skill, *serverBin)
	default:
		fmt.Fprintf(os.Stderr, "unknown mode: %s\n", *mode)
		os.Exit(2)
	}
	if err != nil {
		fmt.Fprintln(os.Stderr, "error:", err)
		os.Exit(1)
	}
}
