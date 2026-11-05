# dual-assistant

一个 `trpc-agent-go` agent，同一条 `runner.Runner` 同时对外说两种协议：

- **AG-UI**：官方 `server/agui`（v1.12.0），`POST` JSON，响应 `text/event-stream`
- **ACP**：stdio 上的 JSON-RPC 2.0。v1.12.0 还没有 `server/acp`（[PR #2330](https://github.com/trpc-group/trpc-agent-go/pull/2330) 已关闭未合并），适配层在 `acp/`，形状跟那次提案一致

两条协议共用会话存储，用户 id 分开：AG-UI 用框架默认的 `user`，ACP 用 `acp`。

## 运行

```bash
cd lc/ai/agent/trpc-agent

# 不调模型。AG-UI 在 HTTP，ACP 占 stdin/stdout。日志在 stderr。
go run . -agent echo

# 只开其中一条
go run . -mode agui -address 127.0.0.1:8080 -path /agui
go run . -mode acp

# OpenAI 兼容模型。读 OPENAI_API_KEY，可选 OPENAI_BASE_URL。
export OPENAI_API_KEY="..."
go run . -agent llm -model deepseek-v4-flash
```

编辑器把 ACP 命令指到 `go run . -mode acp`（或 `-mode both`）。stdout 只走协议，不要往上面打日志。

AG-UI 试一次：

```bash
curl --no-buffer -X POST http://127.0.0.1:8080/agui \
  -H 'Content-Type: application/json' \
  -H 'Accept: text/event-stream' \
  -d '{"threadId":"t1","runId":"r1","messages":[{"role":"user","content":"ping"}]}'
```

`-agent echo` 时助手原文是 `echo: ping`。

## 验证

```bash
go test ./...
```

测试用 echo agent 走真实的 AG-UI SSE 和 ACP `initialize → session/new → session/prompt`。
