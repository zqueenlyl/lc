# 执行图（Execution Graph）

> 多条循环**谁先谁后、如何汇合 / 重试 / 人审**。图层总览：[graph-engineering.md](./graph-engineering.md)。节点内部仍是五段循环 → [loop-engineering.md](./loop-engineering.md)。checkpoint ≠ 领域事实 → [context-graph.md](./context-graph.md)。

---

执行图 = 把五段循环**画成可版本化的状态机**。原语与 [环节 07](../环节07-编排与循环控制详解.md) 同构，这里只记相对循环的增量：

| 相对循环多出来的 | 作用 |
|---|---|
| **边（含条件边）** | 路由、fan-out / fan-in、按边重试、终止；人审是边上的节点 |
| **Checkpointer** | 崩溃续跑、回放。**不是**领域事实库 |
| **interrupt** | 高危操作暂停等人，State 保持、不重跑前面 |
| **子图 / Send** | 舰队在图上的接法 |

落地首选 [LangGraph](../langgraph/)。换框架前先写清节点契约：入参 State、出参部分更新、幂等。State / Node / Edge 讲义不在本篇重复。

**最常见混用**：把 checkpoint、会话记录、向量库当成「我们已经有领域模型了」。Checkpointer 能回答「这趟 run 跑到哪」；它不回答「CRM 和工单里的张三是不是同一个人」。那是 [上下文图](./context-graph.md) 的契约。

舰队：**定义**在 [循环](./loop-engineering.md)（每层仍是五段）；**接线**在本篇（哪条边连到哪个专家、失败走哪条补救边）。
