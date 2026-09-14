# 开源 Agent 项目与框架案例 · case-studies

> 把**四个开源 Agent 项目**当作落地案例读，看业界怎么把 [agent 专题](../) 里的理论变成可跑的生产系统（横向对照「安全哲学、形态、信任来源」）；再加**一个图编排框架 LangGraph**，以「4 篇教程 + 8 个可跑 demo」的形式完整读完。
>
> 两类条目不在同一层：前四个是「造出来的系统」，LangGraph 是「被 import 的编排库」——放在一起，正好能看清**框架给你什么、不给你什么**。

四个项目 + 一个框架，覆盖 Agent 落地的五种取向：

| 项目 / 框架 | 一句话 | 领域 | 安全哲学 | 语言/形态 |
|---|---|---|---|---|
| [commerce-agents](./commerce-agents.md) | 生产级电商 Agent 参考实现，安全靠代码强制 | 业务 Agent | 内建门禁 + 围栏 + 人审 | Python 库 + 多运行时 |
| [pi](./pi.md) | 极简编码 harness，最小核 + 自扩展 | 编码 Agent | 极简核 + 外部沙箱 | TypeScript CLI |
| [mini-swe-agent](./mini-swe-agent.md) | 约 100 行的编码 Agent：只有 bash、线性历史、无状态执行 | 编码 / 评测基线 | 换 Environment = 换隔离 | Python（最小核） |
| [trpc-agent-go](./trpc-agent-go.md) | Go 生产级 Agent 框架，大而全 | 通用 Agent | 框架内建能力 + 可观测 | Go 框架 |
| [langgraph](./langgraph/) | 图状态机编排框架：State / Node / Edge + checkpoint / interrupt | 编排层 | **不内建**：安全/隔离交给宿主 | Python 库（教程 + `demos/`） |

## 为什么单独开一个专题

`lc/ai` 的其它目录是「一种技术」（RAG、MCP、Harness…），本目录是「一个源码对象」——读的是**别人实际怎么写出来的**：

- **四个项目**：不是单一技术，而是把多个专题（agent / guardrails / skills / memory / mcp / a2a / eval）**组合成系统**的实例。读它们等于看「理论拼装成生产」的四种答案。
- **LangGraph**：一个具体框架的**完整实操**（4 篇教程 + 8 个 demo）。它和上面四个不同层——它是被 import 的库，不是造出来的系统——但它同样需要独立成册：一整套可跑的 demo，比散落在各专题里的代码片段好读得多；而且它正是 [trpc-agent-go](./trpc-agent-go.md) 那句「Go 版 LangGraph」的对照样本。

## 一条主线：Agent 的信任从哪来

四个项目最值得横向比的是同一个问题——**怎么让 Agent 值得被信任**：

```
commerce-agents  信任来自 executor 内建的门禁（fence / gate / approval），换运行时也不丢
Pi               信任来自极小的内核 + 把进程丢进容器/微虚拟机
mini-swe-agent   信任来自「一次动作 = 一次独立 subprocess」+ 完整轨迹可复现（隔离强度由 Environment 决定）
trpc-agent-go    信任来自框架内建的可观测 + 评估 + 进化，让你「看得见、测得到、可复盘」
```

没有对错，只有适配：业务要「人审 + 溯源」，编码要「隔离 + 审计」，评测/微调要「轨迹可复现」，平台要「可观测 + 可评估」。

**LangGraph 不在这条主线上**——它是编排库，只管「下一步跑谁、跑到哪了」，安全与隔离全交给宿主。这个缺席本身就是选型时最该记住的一点：选了它，等于这些都要你自己补。

## 怎么读

1. 先读本目录 [commerce-agents](./commerce-agents.md)（信息密度最高，安全方法论最完整）。
2. 再读 [pi](./pi.md) 体会「最小核」和 commerce-agents 的「重门禁」两种哲学。
3. 接着读 [mini-swe-agent](./mini-swe-agent.md)：同一个「最小核 + 靠环境隔离」取向的**另一端**——它把核压到只有一个 bash，换来轨迹可复现，代价是不能做长程协作。
4. 最后读 [trpc-agent-go](./trpc-agent-go.md)，看一个框架如何把 [mcp](../mcp/)、[a2a](../a2a/)、[langgraph](./langgraph/)、[eval](../../reliability/eval/) 打包成 Go 实现。
5. 想动手就翻 [langgraph](./langgraph/)：按 `README → 01 → 04` 的顺序读 4 篇教程，配 `demos/` 里 8 个脚本跑一遍。

> Pi 与 mini-swe-agent 都「不内建权限系统、靠环境隔离」，但上下文策略相反：Pi 是树状会话 + 压缩（长程人机协作），mini 是严格线性不压缩（评测 / 微调数据）。二选一时先看用途。

## 回到专题

读完案例，按层回跳：

| 你想搞懂 | 去 |
|---|---|
| Agent 循环与安全门禁的理论 | [agent](../)、[guardrails](../../reliability/guardrails/) |
| 编码 Agent 外壳的六款对照 | [harness](../harness/) |
| 沙箱 / 隔离与执行后端 | [sandbox](../../reliability/sandbox/) |
| Skills 的 SKILL.md 形态 | [agent-skills](../agent-skills/) |
| 图编排（Go 版 LangGraph） | [langgraph](./langgraph/) |
| 协议：MCP / A2A | [mcp](../mcp/)、[a2a](../a2a/) |
| 记忆 / 评估 | [memory](../../knowledge/memory/)、[eval](../../reliability/eval/) |

总索引见 [../README.md](../../README.md)。
