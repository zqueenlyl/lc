# A2A · Agent-to-Agent Protocol

> 独立 Agent 之间发现、委托、回传结果的开放协议。一句话：**MCP 是手，A2A 是同事之间的工单。**

Google 与多家厂商推动，IBM ACP 于 2025 年并入 A2A；2026 年 A2A 1.0 带签名 Agent Card，成为跨框架委派的主流信封。

配套 MVP：[mvp.py](./mvp.py)。

---

## 一、技术讲解

单个 Agent 挂一堆 MCP 工具，能把「查库 + 写邮件」做完。但企业里常见的是：

- 客服 Agent 不该直接碰账务库，要委托给账务 Agent；
- 研发 Agent 和法务 Agent 分属不同团队、不同运行时、不同权限域；
- 你不想把对方的内部 tools 暴露给自己的模型。

A2A 解决的是 **对等委托**，不是工具调用：

| 概念 | 含义 |
|---|---|
| **Agent Card** | 可发现的名片：名字、技能、端点、鉴权要求，可 JWS 签名 |
| **Task** | 一次委托的生命周期：submitted → working → completed / failed |
| **Artifact** | 对方交回来的产物（报告、工单号、文件），不是对方的内部 state |
| **Message** | 任务过程中的对话 / 澄清 |

传输常见 JSON-RPC 2.0 over HTTP，流式用 SSE。身份走 OAuth；Card 签名防止伪造「我是你们财务 Agent」。

关键设计：**不规定 Agent 内部怎么想**。LangGraph、ADK、AutoGen、自研循环都可以当一端。协议只保证信封一致。

---

## 二、功能作用

- **跨团队 / 跨厂商协作**：对方不开放 MCP tools，只开放「能办哪些事」。
- **权限隔离**：委托方看不到被委托方的数据库连接和内部 prompt。
- **异步长任务**：对方可以 working 很久，用状态轮询或 SSE 推送。
- **可发现**：运行时读 Card，而不是硬编码对方 URL + 技能列表。
- **可审计**：每一 hop 是一条明确的 Task，方便 [Eval](../../reliability/eval/) 按 hop 打分。

---

## 三、应用场景

| 场景 | 委托关系 | 为何不是 MCP |
|---|---|---|
| 客服 → 账务 | 「查这张账单为何多扣」 | 账务有独立合规与人审 |
| 编码 Agent → 安全扫描 Agent | 「对这个 PR 做 SAST」 | 扫描栈是另一套运行时 |
| 研究 Agent → 写作 Agent | 「把结论写成对外公告」 | 两个产品、两个供应商 |
| 平台编排器 → 领域专家 Agent | 总控拆任务下发 | 专家 Agent 自己有工具面 |

**先别上 A2A 的信号**：你其实只有一个 Agent + 一堆工具。那是 MCP。给单 Agent 套 A2A 只是仪式。

---

## 四、一次委托

```
Orchestrator                         Specialist
 |-- GET /.well-known/agent.json --> |   # Agent Card
 |-- tasks/send {skill, input} ----> |
 | <-- task.id, state=working ------- |
 |-- (SSE) status / artifact ------->|
 | <-- state=completed, artifact ---- |
```

Card 示例字段：`name`、`description`、`url`、`skills[]`（id / 输入输出 schema）、`authentication`。

---

## 五、与相邻技术

| 技术 | 关系 |
|---|---|
| [MCP](../mcp/) | 互补：MCP 连工具，A2A 连 Agent |
| 多智能体（LangGraph） | 同进程图编排不必上 A2A；跨进程 / 跨组织才需要 |
| [Guardrails](../../reliability/guardrails/) | 发出去的 Task 入参、收回来的 Artifact 都要校验 |
| [Eval](../../reliability/eval/) | 按 hop 做 TaskCompletion，而不是只评最终一句回复 |

---

## 六、落地建议

1. 一个 Agent 先把 MCP 工具面做稳，再拆第二个 Agent。
2. Skill 粒度按「业务闭环」而不是按函数（`resolve_billing_dispute` 而不是 `select_from_bills`）。
3. Card 签名 + 最小权限 token；不要把内部 tool schema 写进 Card。
4. 超时、重试、幂等 task id 一开始就设计，长任务一定会断。
5. Trace 里打上 `A2A_CLIENT` / `A2A_SERVER` span，和 MCP、模型调用同一条链路。

---

## 七、延伸阅读

- A2A 规范与 Agent Card：Google A2A / a2a-protocol
- 2026 协议栈综述：MCP + A2A + OAuth + OTel GenAI
- 对比：[mcp](../mcp/)、[agent-skills](../agent-skills/)、[langgraph](../langgraph/)

---

## 八、本目录 MVP

`mvp.py` 实现内存版 Agent Card 发现、Task 状态机、客服 → 账务委托。账务 Agent 内部有「假数据库」，对外只回 Artifact。
