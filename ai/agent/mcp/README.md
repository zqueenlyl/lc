# MCP · Model Context Protocol

> Agent 连接工具与数据源的开放标准。一句话：**MCP 是 AI 应用的 USB-C**——工具写一次，IDE / Agent / 聊天客户端都能插。

2024 年底由 Anthropic 开源，2025–2026 成为 Agent 栈的工具层事实标准。Cursor、Claude Desktop、ChatGPT、VS Code Copilot 等都以 MCP 暴露本地与远程能力。

配套 MVP：[mvp.py](./mvp.py)（stdio JSON-RPC 风格的最小 client/server，无外部依赖）。

---

## 一、技术讲解

LLM 本身不会查库、读文件、调内部 API。过去每个产品都自研「function calling」：OpenAI tools、LangChain tools、各家插件协议互不兼容，**N 个 Agent × M 个工具 = N×M 次对接**。

MCP 把这件事标准化成 **Client–Server**：

| 角色 | 谁扮演 | 做什么 |
|---|---|---|
| **Host** | Cursor / Claude Desktop / 你的 Agent 运行时 | 拉起并管理多个 MCP server，做权限与 UI |
| **Client** | Host 内的协议会话 | 与某一个 server 做 JSON-RPC |
| **Server** | 独立进程或远程服务 | 暴露 tools / resources / prompts |

传输：本地常用 **stdio**；远程用 **Streamable HTTP / SSE**。消息体是 JSON-RPC 2.0。

Server 三类能力：

1. **Tools**：可执行动作（`search_docs`、`create_issue`），对应模型的 function calling。
2. **Resources**：只读上下文（文件、ticket、schema），由 Host 决定何时塞进窗口。
3. **Prompts**：可复用的提示模板（「用公司风格写周报」）。

2026 年常见补充：**OAuth 2.1 + Dynamic Client Registration** 做远程鉴权；工具调用进 OpenTelemetry GenAI trace。

---

## 二、功能作用

- **解耦**：工具团队维护一个 MCP server，所有兼容 Host 立刻能用。
- **可发现**：`tools/list` 运行时枚举，模型按 schema 选工具，不必把工具写死在应用里。
- **权限边界**：Host 决定暴露哪些 server、是否要用户点确认；server 不感知「谁在编排」。
- **本地优先**：stdio 让「读本机文件 / 跑本机 git」不必开公网端口。
- **组合**：一个 Host 同时挂 GitHub、Postgres、浏览器、内部 RPC 多个 server。

它**不**规定 Agent 怎么思考、怎么记忆、怎么多步规划——那些留给 LangGraph / 循环工程。MCP 只负责「手和眼睛怎么接上」。

---

## 三、应用场景

| 场景 | 典型 server | 为什么用 MCP |
|---|---|---|
| 编码助手 | filesystem、git、language-server | IDE 统一插拔，不必为每个插件写 SDK |
| 企业内部 Agent | CRM / TAPD / 数仓只读查询 | 工具写一次，多套 Agent 复用 |
| 知识库 | 向量检索、图谱查询 | Resource + Tool 分离「读」和「搜」 |
| 运维 | 日志、指标、工单 | 危险写操作走 Host 确认 |
| 多产品入口 | 同一套 server 给桌面端 + 服务端 Agent | 避免重复对接 |

不适合：两个独立 Agent 互相委派任务（那是 [A2A](../a2a/)）；纯单次 JSON 输出（[structured-output](../../reliability/structured-output/) 就够）。

---

## 四、一次调用长什么样

```
Host                Client                 Server
 |-- spawn/connect -->|                       |
 |                    |-- initialize -------> |
 |                    | <-- capabilities ---- |
 |                    |-- tools/list -------> |
 |                    | <-- [{name, inputSchema}]
 |  (把 schema 交给模型)
 |  模型决定 call search
 |                    |-- tools/call -------> |
 |                    | <-- {content, isError}
 |  把结果塞回上下文，继续生成
```

`inputSchema` 就是 JSON Schema，和 OpenAI function calling 同构，所以从「厂商 tools」迁到 MCP 成本低。

---

## 五、与相邻技术

| 技术 | 关系 |
|---|---|
| Function Calling | MCP 的 tools 在模型侧就是 function calling；MCP 多了发现、传输、鉴权 |
| [A2A](../a2a/) | MCP = Agent→工具；A2A = Agent→Agent。生产栈通常两层都要 |
| LangChain Tools | 框架内抽象；可用适配器把 MCP server 映射成框架 tool |
| [Guardrails](../../reliability/guardrails/) | MCP 不管策略；危险 tool 必须在 Host / 护栏层拦 |
| [Agent Skills](../agent-skills/) | Skills 描述「怎么做事」；MCP 提供「能调用什么」 |

---

## 六、落地建议

1. **先本地 stdio**，跑通 list + call，再上远程 HTTP。
2. Tool 描述写清：何时用、入参约束、副作用（只读 / 会写库）。模型选工具几乎只看这段字。
3. 写操作默认 **人确认**；生产再加 OAuth 与审计 span。
4. 一个 server 只做一件领域的事（git、工单、检索），用 Host 组合，而不是巨型万能 server。
5. 错误用 `isError` + 可读信息返回，让模型能改参重试，不要直接进程崩溃。

---

## 七、延伸阅读

- 规范与 SDK：https://modelcontextprotocol.io
- 协议版本演进：[版本演进.md](./版本演进.md)（2024-11 → 2026-07 五个修订版的变更特性与迁移建议）
- Anthropic 公告与 Cursor / Claude Desktop 接入文档
- 对比：[A2A](../a2a/)、[structured-output](../../reliability/structured-output/)、[guardrails](../../reliability/guardrails/)

---

## 八、本目录 MVP

`mvp.py` 用标准库模拟 stdio 上的 JSON-RPC：一个 `DocsServer` 暴露 `search_docs` / `get_doc`，`Host` 完成 initialize → list → 按「用户问题」选工具 → call。不依赖真实 LLM，用来看清协议形状。
