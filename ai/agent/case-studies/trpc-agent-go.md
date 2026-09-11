# tRPC-Agent-Go · Go 语言生产级 Agent 框架

> 一句话：**用 Go 原生技术栈把「Agent 运行时」做成一整套可观测、可评估、能自我进化的生产框架，相当于 Go 版的 LangGraph + 更多。**
>
> 仓库：https://github.com/trpc-group/trpc-agent-go ｜ Apache-2.0 ｜ 腾讯 tRPC 团队 ｜ 文档 `trpc-group.github.io/trpc-agent-go`

这是国内大厂里少见的、以 **Go** 为主的 Agent 框架，定位是「用 Go 原生技术栈构建生产级 Agent 系统」。对「后端是 Go、要并发强、可观测、易部署」的团队尤其对口。

---

## 一、执行流程：Runner 编排一切

```
Runner（编排执行流程，管 Session）
  → Agent（处理请求，调多个组件）
     → Planner（决定策略与工具选择）
     → Tools（执行具体任务）
     → Memory（维护上下文，从交互学习）
     → Knowledge（RAG 文档理解）
  → Evolution（复盘会话，发布可复用 Skills）
```

主包职责：

| 包 | 职责 |
|---|---|
| `agent` / `runner` | 核心执行单元 + 执行器（流式 Runner、上下文取消、服务友好 API） |
| `model` | 多 LLM 抽象（OpenAI、DeepSeek 等） |
| `tool` | Function / MCP / DuckDuckGo 等工具 |
| `session` / `memory` / `knowledge` | 会话状态、长期记忆、RAG 检索 |
| `planner` | 规划与推理 |
| `artifact` | 版本化文件（图片、报告）存取 |
| `skill` | 加载执行 `SKILL.md` 定义的 Agent Skills |
| `evolution` | **复盘会话 → 提取/审核/发布可复用 Skills** |
| `event` / `server` | 事件流、HTTP 服务（Gateway / AG-UI / A2A） |
| `evaluation` | 可插拔指标评估 Agent，存储结果 |
| `telemetry` | OpenTelemetry tracing + metrics |

---

## 二、核心能力

1. **GraphAgent**：类型安全的图工作流 + 多条件路由，官方自比「Go 版 LangGraph」。
2. **多 Agent 编排**：内置 `LLMAgent`、`ChainAgent`（链式）、`ParallelAgent`（并行）、`CycleAgent`（循环）四种组合。
3. **协议全家桶**：MCP（工具）、A2A（Agent 互操作）、AG-UI（前端流式协议）——对应本仓库 [mcp](../mcp/)、[a2a](../a2a/) 两个专题的工业实现。
4. **Agent Skills**：`SKILL.md` 工作流 + 安全执行，对应 [agent-skills](../agent-skills/)。
5. **自我进化（Evolution）**：基于会话复盘，自动提取、审核、发布可复用 Skills——这是它区别于多数框架的「元能力」。
6. **Prompt Caching**：自动优化成本，缓存内容可省约 90% 费用。
7. **评估 + 可观测**：Eval sets + Metrics + OpenTelemetry + Langfuse 示例，对应 [eval](../../reliability/eval/)。

---

## 三、它和本知识库的关系

tRPC-Agent-Go 几乎把本仓库的多个专题「打包成了一个框架」：

| 本仓库专题 | tRPC-Agent-Go 里的对应 |
|---|---|
| [langgraph](../langgraph/) | `graph` + `agent/graph`（GraphAgent，类型安全的图） |
| [mcp](../mcp/) | MCP 工具接入 |
| [a2a](../a2a/) | A2A server |
| [memory](../../knowledge/memory/) | `memory` 包（长期记忆、个性化） |
| [rag](../../knowledge/rag/) | `knowledge` 包（RAG 检索） |
| [agent-skills](../agent-skills/) | `skill` + `evolution`（技能 + 自我进化） |
| [eval](../../reliability/eval/) | `evaluation` 包 + OpenTelemetry |

所以读这个框架，等于看一遍「把编排层各零件拼成生产系统的 Go 实现」。

---

## 四、技术栈与存储

- **语言**：Go（要求 Go 1.21+），并发/部署是天然优势。
- **存储后端**：Session / Memory / Artifact / Knowledge 支持内存、Redis、S3/COS 等。
- **代码执行**：本地安全执行环境。
- **协议**：MCP、A2A、AG-UI。
- **可观测**：OpenTelemetry + Langfuse。

官方致谢里提到已在**腾讯元宝、腾讯视频、腾讯新闻、IMA、QQ 音乐**等业务验证，并致敬 ADK、Agno、CrewAI、AutoGen 等开源项目。

---

## 五、选型视角

| 你是什么团队 | 倾向 |
|---|---|
| Go 后端、要并发/可观测/易部署 | tRPC-Agent-Go 是首选之一 |
| Python 生态、要快速原型 | LangGraph / 各 Python 框架 |
| 看「Agent 自我进化」这个方向 | Evolution 包值得单独研究 |
| 已有腾讯云/tRPC 体系 | 生态天然契合 |

对比 [Pi](./pi.md)（极简、让你自己拼）和 [commerce-agents](./commerce-agents.md)（给业务 Agent 做安全范本），tRPC-Agent-Go 走的是**「大而全的生产框架」**路线：能力内建、协议齐全、可观测开箱。

---

## 六、落地建议

1. 先跑官方 Quick Start（三步：建模型 → 建工具 → 建 Agent/Runner），感受流式 + 工具调用 + 多轮记忆。
2. 重点看 `graph` 包的图工作流和 `evolution` 包的自我进化，这是它的差异化。
3. 生产先接 OpenTelemetry，把 trace 从第一天打起来（和 [agent 专题](../) 的落地建议一致）。

---

## 七、延伸阅读

- 文档：`trpc-group.github.io/trpc-agent-go/`（含 GraphAgent、AG-UI、Skills、Evaluation 等主题博客）
- 示例：仓库 `examples/` 下 15 类（tool / llmagent / multiagent / graph / memory / knowledge / telemetry / mcp / agui / evaluation / skills / evolution / artifacts / a2a / gateway）
- 相邻专题：[langgraph](../langgraph/)、[agent](../)、[mcp](../mcp/)、[a2a](../a2a/)、[eval](../../reliability/eval/)
- 三项目横向对比见本目录 [README](./README.md)
