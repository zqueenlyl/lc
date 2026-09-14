# 图工程（Graph Engineering）

> 循环之上的结构层：**执行图**管谁先谁后，**上下文图**管系统知道什么。总览：[README.md](./README.md)。节点内部仍是五段循环 → [loop-engineering.md](./loop-engineering.md)。

细则分两篇，不要合成一张 Schema：

| 文档 | 主问题 | 不是 |
|---|---|---|
| [execution-graph.md](./execution-graph.md) | 多条循环谁先谁后、汇合 / 重试 / 人审 | 领域本体 |
| [context-graph.md](./context-graph.md) | 跨会话、跨 Agent，客户 / 合同 / 政策是什么 | 窗口裁剪（那是 [上下文工程](./context-engineering.md)） |

---

## 一、这一层管什么

Loop 还在转。Graph 负责**编排这些 loop**，并在需要时给它们一份共享的领域事实。

| | **执行图** | **上下文图** |
|---|---|---|
| 主问题 | 多条谁先谁后、如何汇合 / 重试 / 人审？ | 跨会话、跨 Agent，系统知道什么？ |
| 形状 | Agent、工具、审批；路由 / fan-out | 客户、合同、政策；`OWNS` / `SUPERSEDES` |
| 状态 | checkpoint、分支结果 | 事实、来源、时效、决策痕迹 |
| 含义来自 | 工作流定义 | **应用自己的 Schema / 本体** |
| 寿命 | 一次 run / 一条 thread | 跨工作流、跨框架 |
| 落地 | [LangGraph](../case-studies/langgraph/) · [环节 07](../环节07-编排与循环控制详解.md) | [RAG · GraphRAG](../../knowledge/rag/) · [Memory](../../knowledge/memory/) |

**最常见混用**：把 checkpoint、会话记录、向量库当成「我们已经有领域模型了」。Checkpointer 能回答「这趟 run 跑到哪」；它不回答「CRM 和工单里的张三是不是同一个人」。

编码 Agent 还有第三张图，别和上面抢词：**代码图**（文件 / 符号 / 调用 / 依赖）给 Harness 当检索底座。

---

## 二、何时从循环升级到图

- 并行要汇合、人审必须是节点、失败要按边重试、多条循环不能共一段窗口 → **执行图**（不要在 while 里加 `if`）。
- 多个会话 / 系统必须对「同一个客户、同一版政策」读写一致 → **再加上下文图**。单线程编码、文件 + git + checkpoint 往往够，不必上 GraphRAG。

舰队：**定义**在 [循环](./loop-engineering.md)（每层仍是五段）；**接线**在 [执行图](./execution-graph.md)。

---

## 三、和上下文工程的分界

[上下文工程](./context-engineering.md) 决定这一跳窗口装什么。[上下文图](./context-graph.md) 决定系统里有哪些实体和边。图查询的结果仍要按 token 预算裁进窗口，两层接力，不是互相替代。
