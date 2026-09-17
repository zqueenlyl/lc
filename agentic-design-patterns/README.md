# Agentic Design Patterns · 模式对照笔记

> Antonio Gulli《[Agentic Design Patterns](https://github.com/evoiz/Agentic-Design-Patterns)》（Springer, 2025）：21 个可组合的 Agent 模式 + 配套 notebook。版税捐 [Save the Children](https://www.savethechildren.org/)。
> 本目录是**学习笔记**，与 [naval/](../naval/)、[game-theory/](../game-theory/) 同级；按书的四部重组，**不摘录正文**。书讲「积木叫什么」；`ai/agent` 的 [环节 01–10](../ai/agent/环节00-总揽与环节导航.md) 讲「一次请求怎么流」。两套索引正交，对完就能跳读。

一句人话：**模式是菜谱，环节是厨房流水线。** 会点菜不等于会出餐——Chaining / Routing / Reflection 可以在提示层做完，也可以长成执行图上的边；判断标准仍是 [agent/README §七](../ai/agent/README.md#七按栈升级从提示到图) 的升级信号。

- 仓库（PDF + notebook）：[evoiz/Agentic-Design-Patterns](https://github.com/evoiz/Agentic-Design-Patterns)
- notebook 目录：[chapter_notebooks/](https://github.com/evoiz/Agentic-Design-Patterns/tree/main/chapter_notebooks)
- 代码示例许可证：MIT；**书正文版权归作者，本库不入库 PDF**

---

## 目录结构

```
agentic-design-patterns/
├── README.md              # 本索引：21 模式总表 + 学习路线 + 与环节对照
├── 01-核心模式.md         # Part 1 · Ch1–7  链 / 路由 / 并行 / 反思 / 工具 / 规划 / 多 Agent
├── 02-适应与协议.md       # Part 2 · Ch8–11 记忆 / 学习 / MCP / 目标监控
├── 03-可靠与对齐.md       # Part 3 · Ch12–14 异常恢复 / 人审 / RAG
└── 04-规模化.md           # Part 4 · Ch15–21 A2A / 成本 / 推理 / 护栏 / 评测 / 优先级 / 探索
```

---

## 学习路线

```
只想补词汇（半天）
  本页总表 → 标「本库已有」的行跳过 → 只读增量四章（9 / 11 / 20 / 21）

按书走一遍（对照本库，不要重写）
  01 核心模式 ──► 02 适应与协议 ──► 03 可靠与对齐 ──► 04 规模化

动手（二选一，不要两套一起开）
  本库已有：case-studies/langgraph/demos/
  书配套：上游 notebook（大量 Google ADK / CrewAI / Gemini）
```

- **已经读完环节 01–10**：用本页总表当词汇表，只补 Ch9 / 11 / 20 / 21。
- **还没建立 Agent 坐标系**：先 [agent/README](../ai/agent/README.md) → [环节00](../ai/agent/环节00-总揽与环节导航.md)，再回来点菜。
- **想对照框架**：LangGraph 走本库 [langgraph](../ai/agent/case-studies/langgraph/)；ADK / CrewAI 走上游 notebook，本库不重复造 demo。

---

## 21 模式总表

> 「本库」列指向已经写过的原理 / 案例，不是「书可以不看」。书的价值是**命名稳定 + 跨框架示例**；本库的价值是**工程红线 + 和流水线的位置**。

| # | 模式 | 一句话 | 本库 | 笔记 |
|---|---|---|---|---|
| 1 | Prompt Chaining | 大任务拆成串，上一步输出当下一步输入 | [langgraph 01](../ai/agent/case-studies/langgraph/01-核心概念与快速上手.md) · [环节 07](../ai/agent/环节07-编排与循环控制详解.md) | [01](./01-核心模式.md#ch1) |
| 2 | Routing | 先分类，再走不同链 / 模型 / 工具 | [langgraph 02](../ai/agent/case-studies/langgraph/02-条件分支与循环.md) · [model-routing](../ai/reliability/model-routing/) | [01](./01-核心模式.md#ch2) |
| 3 | Parallelization | 扇出独立子任务，再汇合（或投票） | [langgraph demo 04](../ai/agent/case-studies/langgraph/demos/04_parallel_fanout.py) | [01](./01-核心模式.md#ch3) |
| 4 | Reflection | 生成 → 批评 → 改，直到过门或预算尽 | [环节 01 Reflexion](../ai/agent/环节01-决策与推理范式详解.md) | [01](./01-核心模式.md#ch4) |
| 5 | Tool Use | 模型出结构化调用，宿主执行后回填观察 | [环节 04](../ai/agent/环节04-工具调用详解.md) | [01](./01-核心模式.md#ch5) |
| 6 | Planning | 先出步骤清单，再逐条执行（可重规划） | [环节 01 Plan-and-Execute](../ai/agent/环节01-决策与推理范式详解.md) · [loop-graph](../ai/agent/loop-graph/) | [01](./01-核心模式.md#ch6) |
| 7 | Multi-Agent | 角色拆开，主管分发或流水线交接 | [环节 08](../ai/agent/环节08-多Agent协作详解.md) | [01](./01-核心模式.md#ch7) |
| 8 | Memory Management | 工作 / 会话 / 长期三层，默认不可见要召回 | [环节 03](../ai/agent/环节03-记忆与状态详解.md) · [memory](../ai/knowledge/memory/) | [02](./02-适应与协议.md#ch8) |
| 9 | Learning and Adaptation | 用轨迹 / 奖励 / 少量样本改策略，不只改 prompt | [rl](../ai/foundation/rl/) · [Agentic RL](../ai/foundation/rl/环节08-AgenticRL与信用分配详解.md) | [02](./02-适应与协议.md#ch9) |
| 10 | MCP | 工具发现与接入的标准插头 | [环节 05](../ai/agent/环节05-工具接入协议MCP详解.md) · [mcp](../ai/agent/mcp/) | [02](./02-适应与协议.md#ch10) |
| 11 | Goal Setting and Monitoring | 完成定义写进循环，过程对照目标纠偏 | [loop-engineering](../ai/agent/loop-graph/loop-engineering.md) | [02](./02-适应与协议.md#ch11) |
| 12 | Exception Handling | 工具失败当观察；重试 / 降级 / 兜底 | [环节 10](../ai/agent/环节10-生产级工程化详解.md) | [03](./03-可靠与对齐.md#ch12) |
| 13 | Human-in-the-Loop | 高风险步暂停等人，人的决定写回状态 | [langgraph 03](../ai/agent/case-studies/langgraph/03-持久化-流式-人机协同.md) | [03](./03-可靠与对齐.md#ch13) |
| 14 | Knowledge Retrieval (RAG) | 窗口外的事实按需召回，带引用 | [环节 06](../ai/agent/环节06-检索增强RAG详解.md) · [rag](../ai/knowledge/rag/) | [03](./03-可靠与对齐.md#ch14) |
| 15 | Inter-Agent Communication (A2A) | Agent 之间交换任务单，不交换内部工具 | [a2a](../ai/agent/a2a/) | [04](./04-规模化.md#ch15) |
| 16 | Resource-Aware Optimization | token / 延迟 / 模型档位当一等约束 | [环节 10](../ai/agent/环节10-生产级工程化详解.md) · [model-routing](../ai/reliability/model-routing/) | [04](./04-规模化.md#ch16) |
| 17 | Reasoning Techniques | CoT / 自洽 / 搜树 / 代码当推理器 | [环节 01](../ai/agent/环节01-决策与推理范式详解.md) · [test-time](../ai/foundation/rl/推理侧搜索与test-time-scaling.md) | [04](./04-规模化.md#ch17) |
| 18 | Guardrails / Safety | 输入过滤、工具门禁、输出校验，安全靠代码 | [guardrails](../ai/reliability/guardrails/) · [commerce-agents](../ai/agent/case-studies/commerce-agents.md) | [04](./04-规模化.md#ch18) |
| 19 | Evaluation and Monitoring | 轨迹级评测 + 在线回归，不是单轮 BLEU | [环节 09](../ai/agent/环节09-评测与可观测详解.md) · [eval](../ai/reliability/eval/) | [04](./04-规模化.md#ch19) |
| 20 | Prioritization | 多目标抢同一预算时显式排序 / 重排 | 本库偏薄，见笔记 | [04](./04-规模化.md#ch20) |
| 21 | Exploration and Discovery | 主动探未知，不是在已知解空间里优化 | 本库偏薄，见笔记 | [04](./04-规模化.md#ch21) |

**本库相对薄、值得按书补的四章**：Ch9 适应、Ch11 目标监控、Ch20 优先级、Ch21 探索。其余章优先当「命名 ↔ 已有文档」的 vis-à-vis。

---

## 和本库两套索引怎么叠

```
书：21 个命名模式（积木，可跳读）
环节 01–10：一次任务怎么流（流水线，按序读）
README §七：Prompt → Context → Harness → Loop → Graph（何时加层）
```

| 你卡在 | 先读 |
|---|---|
| 「这个功能业界叫什么」 | 本页总表 |
| 「它在一次请求的哪一段」 | [环节00](../ai/agent/环节00-总揽与环节导航.md) |
| 「该不该上图 / 上多 Agent」 | [agent/README §七](../ai/agent/README.md#七按栈升级从提示到图) |
| 「别人源码怎么拼」 | [case-studies](../ai/agent/case-studies/) |

常见错位：

- 把 **Chaining** 当成 Agent。线性链没有观察闭环，停在工作流。
- 把 **Planning** 当成 Loop。计划过时必须能重规划，否则是一次性 To-Do。
- 把 **Memory** 当成窗口里那串 messages。长期记忆默认不可见，要召回才进上下文。
- 把 **A2A** 和 **MCP** 当成二选一。MCP 是手，A2A 是工单。

---

## 附录（书 A–G，本库不单开章）

| 附录 | 干什么 | 本库去哪 |
|---|---|---|
| A 高级提示 | CoT / few-shot / 角色等提示技法 | [环节 02](../ai/agent/环节02-提示与上下文工程详解.md) |
| B GUI → 真环境 | 从点 UI 到操作真实世界 | [computer-use](../ai/agent/computer-use/) |
| C 框架速览 | LangChain / AutoGen / CrewAI / ADK 扫面 | [langgraph](../ai/agent/case-studies/langgraph/)（本库只深挖这一个） |
| D AgentSpace | Google 托管构建（产品页易过期） | 不入库；要动手走官方文档 |
| E CLI Agent | 终端里的编码 / 运维 Agent | [harness](../ai/agent/harness/) · [pi](../ai/agent/case-studies/pi.md) |
| F 推理引擎 | 模型内部怎么「想」 | [环节 01](../ai/agent/环节01-决策与推理范式详解.md) · [test-time](../ai/foundation/rl/推理侧搜索与test-time-scaling.md) |
| G Coding agents | SWE-bench 线上的那些外壳 | [harness](../ai/agent/harness/) · [mini-swe-agent](../ai/agent/case-studies/mini-swe-agent.md) |

另有 `Appendix_Pydantic.ipynb`：结构化输出校验，本库见 [structured-output](../ai/reliability/structured-output/)。

---

## 怎么用这本书（以及这份笔记）

1. **当菜谱，不当圣经。** 21 章可以跳读；生产系统通常只稳定组合其中 5–8 个。
2. **先完成定义，再点模式。** 没有验收命令 / 必填字段，Reflection 和 Multi-Agent 只会把幻觉放大。
3. **每加一个模式先问成本。** Parallelization 和 Multi-Agent 把账单乘上去；默认 L2（步数、超时、花费、循环检测）。
4. **notebook 当对照，不进本库。** 上游示例绑 Gemini / ADK / CrewAI，和本库「无外部 API 的 mvp.py」约定冲突。

一手读 PDF 或买纸书；本笔记负责把主张收成可检索的骨架，并指回 `ai/` 里已经写过的红线。

---

## 与本仓其它专题

- Agent 流水线 / 环节 / 案例 → [ai/agent](../ai/agent/)
- 外部课程（CS329Z 也讲 Design Patterns）→ [ai/courses.md](../ai/courses.md)
- 同级书 / 专题笔记 → [naval](../naval/) · [game-theory](../game-theory/)
