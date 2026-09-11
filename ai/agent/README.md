# Agent · 智能体知识整理

> **Agent = 有目标、能感知环境、能调工具、能根据反馈再试的循环系统。**
> 聊天机器人答一句就停；工作流按固定箭头走；Agent 在中间——箭头是自己选的，停不停看验证结果。

本页是总图：**怎么理解 Agent、什么时候该用**。环节主线（01–10 关卡地图）见 [环节00-总揽与环节导航.md](./环节00-总揽与环节导航.md)；MCP / 记忆 / Harness / 评测等细拆见文末导航，不要在这里找协议字段或框架 API。

配套 MVP：[mvp.py](./mvp.py)（ReAct：Thought → Action → Observation，规则策略当模型，无外部 API）。

---

## 一、先分清三件事

| | 聊天 Bot | 工作流 Workflow | **Agent** |
|---|---|---|---|
| 控制权 | 人问一句，模型答一句 | 人预先画死节点和边 | 模型（在约束内）选下一步 |
| 工具 | 可有，多半一次调用 | 每步绑死一个动作 | 按需选工具，可多轮 |
| 失败 | 换个说法再问 | 走异常分支或停 | **自己看观察结果再试** |
| 典型 | ChatGPT 闲聊 | 审批流、ETL | 修测试、查库退款、浏览器办事 |

不是所有「带 Function Calling 的 LLM」都叫 Agent。一次 `get_weather` 再生成回复，仍是工具增强的聊天。**转起来、能根据环境反馈改计划**，才进入 Agent 区。

自主程度可以看成一条谱，生产上大多数停在中段：

```
L0  纯生成          写邮件草稿，人发出
L1  建议            推荐下一步，人点确认
L2  受限循环        白名单工具 + 步数上限 + 验证门（默认该停在这）
L3  长程闭环        测红就改，直到绿或预算耗尽
L4  舰队            编排者拆任务，专家 + 子 Agent 并行
```

L4 没有 L2 的沙箱和验证，只是把幻觉放大。先闭环，再开放。见 [循环工程](loop-engineering.md)。

---

## 二、解剖：一层模型叠七块肉

```
              ┌──────── 目标 / 完成定义 ────────┐
              │  VISION · 测试命令 · 验收标准     │
              └────────────────┬─────────────────┘
                               ▼
┌──────────┐  选动作   ┌──────────────┐  副作用  ┌──────────┐
│  模型     │ ───────► │  Harness     │ ───────► │  环境     │
│ 推理/路由 │ ◄─────── │  组上下文     │ ◄─────── │ 仓库/API  │
└──────────┘  观察     │  工具/权限    │  结果    │ 浏览器    │
                       └──────┬───────┘          └──────────┘
          Skills / SOP        │  MCP 插工具
          Memory 读写         │  A2A 委托同事
          Guardrails 门禁     │  Computer Use 补无 API 的手
          Context 裁剪        ▼
                       验证：测试 / 断言 / 人审
                       不过 → 再转；过 → 交付
```

| 块 | 干什么 | 本仓库 |
|---|---|---|
| **模型** | 想、选工具、写产物 | [reasoning](../foundation/reasoning/)、[model-routing](../reliability/model-routing/) |
| **Harness** | 循环怎么转、默认工具、沙箱 | [harness](harness/) |
| **工具协议** | 手怎么接上 | [mcp](mcp/)、[structured-output](../reliability/structured-output/) |
| **技能 / SOP** | 这类任务按什么做 | [agent-skills](agent-skills/) |
| **记忆** | 这轮 / 这会话 / 跨会话记什么 | [memory](../knowledge/memory/) |
| **上下文** | 窗口里塞谁、砍谁 | [context-engineering](../knowledge/context-engineering/) |
| **知识** | 仓库外的事实从哪召回 | [rag](../knowledge/rag/)、[知识库](../knowledge/knowledge-base/) |
| **无 API 的环境** | 看屏幕点鼠标 | [computer-use](computer-use/) |
| **多 Agent** | 同事之间派工单 | [a2a](a2a/)、[langgraph 04](langgraph/04-多智能体与高级模式.md) |
| **治理** | 别把生产删了；分数要可复现 | [guardrails](../reliability/guardrails/)、[eval](../reliability/eval/) |

记一句：**模型不会「自己变 Agent」**。缺循环、缺工具、缺验证，它只是会说话的补全器。

---

## 三、一圈怎么转（ReAct 及变体）

最小循环（ReAct，Yao et al. 2022）至今仍是默认骨架：

```
Thought  →  Action(tool, args)  →  Observation  →  再 Thought …
直到 Finish 或触达步数 / 预算上限
```

现代实现里 Thought 常常藏进 **tool call JSON**（不一定再输出「我应该…」散文），但信息流一样。

| 模式 | 怎么走 | 适合 | 坑 |
|---|---|---|---|
| **ReAct / Tool loop** | 走一步看一步 | 工具结果不确定、要探索 | 无验证会空转；上下文膨胀 |
| **Plan-and-Execute** | 先出步骤清单再逐条执行 | 任务结构清楚 | 计划过时，要能重规划 |
| **发现→规划→执行→验证→迭代** | [循环工程](loop-engineering.md) 五段 | 编码 / 研究等要「测过才算完」 | Token 贵，必须闭环预算 |
| **Supervisor** | 一个编排者分发给专家 | 角色边界清（研究 / 码 / 测） | 编排者变成单点，prompt 膨胀 |
| **Swarm / 对等交接** | Agent 之间移交控制权 | 探索、对话式转交 | 难审计、易 ping-pong |
| **Fleet（舰队）** | 每层都跑同一套五段循环 | 大目标可拆 | 成本数量级上升 |

编排落地常用图状态机：[LangGraph](langgraph/)（节点=动作，条件边=路由，checkpointer=记忆，interrupt=人审）。

---

## 四、单 Agent vs 多 Agent

先问「是不是真的要第二个大脑」，再问协议。

| 用一个就够 | 才拆多个 |
|---|---|
| 同一权限域、同一工具箱 | 权限必须隔离（客服碰不到账） |
| 任务短、工具 < 15 个 | 工具太多，模型选不过来（按角色裁剪工具集） |
| 验证能程序化 | 需要「作者 / 评审分离」（子 Agent 当验证者） |
| 延迟敏感 | 可并行的独立子任务 |

拆开之后的连接方式：

- **进程内图**：LangGraph 多个 node / 子图，状态共享，简单。
- **A2A**：跨团队、跨厂商，只交换 Task / Artifact，不交换对方内部工具。
- **子 Agent**：同一 Harness 里缩小工具集跑一段（Kimi 的 explore / plan / coder）。

MCP 解决「手」；A2A 解决「工单」。不是二选一。

---

## 五、环境、工具、验证（Agent 的物理世界）

没有环境的 Agent 只能自言自语。

| 环境 | 工具长什么样 | 验收 |
|---|---|---|
| Git 仓库 | `read` / `edit` / `bash` | 测试绿、lint、类型检查 |
| 浏览器 / 桌面 | click / type / DOM | 页面出现目标文本；禁止乱点支付 |
| 业务 API | MCP tools | 工单状态、幂等、对账 |
| 知识库 | 检索 + 引用 | 答案能在命中块里溯源 |
| 其他 Agent | A2A Task | Artifact schema、hop 超时 |

**验证者不要等于执行者。** 模型说「已修好」不算完；`pytest`、schema、人审才算。这是 Agent 评测难于 LLM 评测的原因：考的是模型 × Harness × 环境。见 [eval](../reliability/eval/)、[SWE-bench](https://www.swebench.com/)。

工具设计要点：

1. 名字和 schema 让模型能选对（含「何时不要用」）。
2. 失败返回**可行动的观察**（缺字段、权限拒绝），不要只丢栈。
3. 写操作要幂等或带确认；删除 / 转账进 [Guardrails](../reliability/guardrails/) L2。
4. 工具一多就分组：Skill 规定本组、或拆子 Agent。

---

## 六、常见死法（比模型笨更常见）

| 死法 | 看起来像 | 处理 |
|---|---|---|
| **空转** | 同一工具同一参数连打 | 循环检测 + 步数上限 |
| **目标漂移** | 修 bug 修成重构半个仓 | 完成定义写进循环；diff 门禁 |
| **假装成功** | 「测试应该过了」 | 程序验收，禁止自评 |
| **上下文中毒** | 早期错误观察一直留在窗口 | 摘要、丢弃失败尝试、[上下文工程](../knowledge/context-engineering/) |
| **工具幻觉** | 编造不存在的 API 结果 | 只把真实 Observation 写进状态 |
| **权限过大** | 一次 `bash` 能干掉生产 | 目录 / 命令白名单、人审 |
| **账单爆炸** | 舰队 × 推理模型 × 无缓存 | Flash 打下手、路由、缓存前缀 |
| **评测自欺** | 公开榜第一，自家仓不会修 | 自己的 P0 上机集 |

---

## 七、什么时候不要上 Agent

- 步骤固定、无分支：写成工作流或脚本，更稳更便宜。
- 数据在库里、问题是查询：RAG / Text-to-SQL，不必让模型自己探索文件系统。
- 一次性文案：聊天 + 人改即可。
- 合规要求每步可预先审计：预定义路径（闭环工作流）优于开放 ReAct。

选型梯子（贵的后上）：

```
提示 → 单次 tool call → RAG
  → 有验证的短循环（L2）
    → Harness + Skills + Memory
      → 多 Agent / A2A
        → Computer Use（实在没有 API）
```

每一步用 [Eval](../reliability/eval/) 证明有增益再加层。

---

## 八、产品侧（你每天打开的那些）

编码：[Claude Code](harness/)、Codex、Cursor Agent、Kimi Code、Pi、OpenClaw——比的是 Harness，不是聊天窗。办公：千问办公、豆包、Copilot Agent 模式。通用：ChatGPT / Claude / Gemini 里的「深度研究 / 电脑使用」。

地图见 [landscape §4.2](../landscape.md#42-编程-agent--ide2026-主战场)。公开干活榜看 [SWE-bench](https://www.swebench.com/) 和 [AA Coding Agents](https://artificialanalysis.ai/?coding-agents=execution-time)，记住坐标要写全：模型 + 外壳 + 环境。

---

## 九、术语

| 词 | 意思 |
|---|---|
| **ReAct** | 推理与行动交错的循环 |
| **Tool / Function calling** | 模型按 schema 发起一次调用 |
| **Observation** | 环境或工具返回、写进下一轮上下文的事实 |
| **Trajectory** | 一整段 Thought/Action/Observation 记录，评测要用 |
| **Harness** | 运行时外壳 |
| **Subagent** | 缩小权限的子循环 |
| **HITL** | Human in the loop，关键步暂停等人 |
| **Autonomy** | 无人干预能走多远；不是越高越好 |
| **% Resolved** | 上机题测绿的比例（SWE-bench） |

---

## 十、本仓库怎么读

按角色选入口：

| 你想搞懂 | 去 |
|---|---|
| Agent 是什么、何时用（本页） | [agent/](./) |
| 全链路环节主线（01–10 关卡地图） | [环节00-总揽与环节导航.md](./环节00-总揽与环节导航.md) |
| 循环怎么设计 | [loop-engineering.md](loop-engineering.md) |
| 图画出来怎么跑 | [langgraph/](langgraph/) |
| 工具插头 | [mcp/](mcp/) |
| Agent 互委托 | [a2a/](a2a/) |
| 菜谱 | [agent-skills/](agent-skills/) |
| 编码外壳 | [harness/](harness/) |
| 记忆 | [memory/](../knowledge/memory/) |
| 知识外挂 | [rag/](../knowledge/rag/) |
| 看屏幕动手 | [computer-use/](computer-use/) |
| 上线别炸 / 怎么打分 | [guardrails/](../reliability/guardrails/)、[eval/](../reliability/eval/) |

---

## 十一、落地建议

1. 先写 **完成定义**（哪条命令绿、哪个字段必填），再写循环。
2. 工具从只读开始，写操作加确认；生产凭证不要进模型上下文。
3. 默认 L2：步数、超时、花费、循环检测四条上限。
4. Trace 从第一天打：每次 tool 的参数、观察、耗时，否则无法 [eval](../reliability/eval/)。
5. 模型可换，循环和验收不要绑死在一家 API 上。

---

## 十二、本目录 MVP

`mvp.py` 用规则策略扮演模型，跑标准 ReAct：查订单 → 看到金额 → 退款 → `finish`。打印每一步的 Thought / Action / Observation，并演示「缺单号就停、不编造」。
