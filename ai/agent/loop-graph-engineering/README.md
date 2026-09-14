# 循环工程与图工程（Loop & Graph Engineering）

> 一句话：Agent 工程按层升级——**Prompt → Context → Harness → Loop → Graph**。人不做循环本身；图不取代循环——每个节点内部仍是一段循环。
>
> 目录名强调后两层（杠杆最大、最容易和前层混用）。前几层在本目录给**栈内口径**；技法细讲仍在 [环节 02](../环节02-提示与上下文工程详解.md)、[knowledge/context-engineering](../../knowledge/context-engineering/)、[harness/](../harness/)。
>
> 和 [Harness](../harness/) 的关系：Harness 是车（运行时外壳）；Loop 是怎么开（验证闭环）；执行图是立交怎么接；上下文图是地图（领域事实），**不是底盘**。
>
> 循环部分来源：Rahul《Loops: What Every AI Engineer Needs to Know in 2026》（2026-06-09）。图部分口径：执行图 vs 上下文图（2026 工程共识；综述 arXiv:2608.21156）。

本页是**总览索引**。

| 文档 | 主问题 | 读完能判断 |
|---|---|---|
| [prompt-engineering.md](./prompt-engineering.md) | 这一次怎么问清楚？ | 角色 / 任务 / 约束 / 格式；何时不再改提示 |
| [context-engineering.md](./context-engineering.md) | 窗口里该有什么？ | 选 / 砍 / 排序 / 预算；≠ 上下文图 |
| [harness-engineering.md](./harness-engineering.md) | 运行时外壳是什么？ | 工具 / 权限 / 验证门；车 ≠ 开法 |
| [loop-engineering.md](./loop-engineering.md) | 这一条何时算完？ | 五段循环、开闭环、舰队**定义**、验证器 |
| [graph-engineering.md](./graph-engineering.md) | 何时从 loop 转到 graph？ | 执行图 vs 上下文图；一张图一种东西 |
| [execution-graph.md](./execution-graph.md) | 多条谁先谁后？ | 边 / checkpoint / 人审 / 子图；舰队**接线** |
| [context-graph.md](./context-graph.md) | 系统知道什么？ | 构图管线、身份 / 时效 / 来源、GraphRAG 家族 |
| [mvp.py](./mvp.py) | 两张图怎么分工？ | 关键词漏政策；图路径走出不可退；退款停人审 |

最小 ReAct 循环见 [../mvp.py](../mvp.py)。运行本目录 MVP：`cd ai/agent/loop-graph-engineering && python3 mvp.py`。

---

## 一、整栈对照（先看这张）

```
Prompt（怎么问一次）                 ← prompt-engineering.md
  → Context（窗口里有什么）           ← context-engineering.md
    → Harness（运行时：工具 / 权限 / 验证门）  ← harness-engineering.md
      → Loop（同一条工作怎么转完）      ← loop-engineering.md
        → Graph                         ← graph-engineering.md
            ├─ 执行图（多条谁先谁后）   ← execution-graph.md
            └─ 上下文图（系统知道什么） ← context-graph.md
```

| | **提示** | **上下文** | **Harness** | **循环** | **执行图** | **上下文图** |
|---|---|---|---|---|---|---|
| 主问题 | 这一次怎么问？ | 窗口装什么？ | 外壳怎么跑？ | 这一条何时算完？ | 多条谁先谁后？ | 系统知道什么？ |
| 形状 | 一次 messages | 多源预算 | 工具 / 权限 / 产品 | 时间上的环 | 路由 / fan-out | 客户、合同、政策 |
| 杠杆 | 文案 | 编译窗口 | 底盘 | 完成定义 + 验证器 | 工作流边 | Schema / 本体 |
| 寿命 | 一次调用 | 一次调用 | 产品生命周期 | 一次任务 | 一次 run | 跨工作流 |
| 细讲 | [环节 02](../环节02-提示与上下文工程详解.md) | [knowledge/CE](../../knowledge/context-engineering/) | [harness/](../harness/) | 本目录 | [LangGraph](../langgraph/) · [环节 07](../环节07-编排与循环控制详解.md) | [RAG](../../knowledge/rag/) · [Memory](../../knowledge/memory/) |

**升级信号**

- 一次调用能稳住格式 → **停在提示**，不要上 Agent。
- 多源抢窗口、要压缩 / 缓存 → **上下文工程**。
- 要工具、权限、沙箱、产品形态 → **Harness**。
- 验证器能程序化、一条 Agent 转完 → **停在循环**，不要画图。
- 并行要汇合、人审必须是节点、失败要按边重试、多条循环不能共一段窗口 → **执行图**（不要在 while 里加 `if`）。
- 多个会话 / 系统必须对「同一个客户、同一版政策」读写一致 → **再加上下文图**。单线程编码、文件 + git + checkpoint 往往够，不必上 GraphRAG。

舰队：**定义**在 [循环](./loop-engineering.md)（每层仍是五段）；**接线**在 [执行图](./execution-graph.md)。

> Peter Steinberger：「你应该设计循环来提示你的代理。」又问：「还在谈 loop，还是已经转到 graph 了？」——**loop 还在转，graph 负责编排这些 loop，并（在需要时）给它们一份共享的领域事实。**

编码 Agent 还有第三张图，别和上面抢词：**代码图**（文件 / 符号 / 调用 / 依赖）给 Harness 当检索底座。

两个易混词：

| 名字 | 是 | 不是 |
|---|---|---|
| [上下文工程](./context-engineering.md) | 窗口预算 | 领域图 |
| [上下文图](./context-graph.md) | 实体 / 关系 / 时效 | 窗口裁剪 |

---

## 二、场景选型

| 场景 | 停在哪 | 为什么 |
|---|---|---|
| 分类 / 抽取 / 改写 | **提示** | 一次调用 + 格式校验 |
| 客服长会话、编码助手打开文件 | + **上下文工程** | 窗口预算，不必上循环 |
| 单线程编码：写 → 测 → 修 | **循环 + Harness** | 验证器是测试；文件 + git 够当进度 |
| 编码要并行子 Agent / 人审合入 | + 执行图（常再加代码图） | 汇合与审批是边 |
| 研究型多 Agent（搜 / 写 / 评） | + 执行图 | fan-out / fan-in，验证者与作者分离 |
| 企业知识：合同–条款–客户–事故 | + 上下文图 / GraphRAG | 多跳、全局总结、要引用路径 |
| 客服 / 理赔跨 CRM·工单·政策 | **执行图 + 上下文图** | 走路 vs 「同一客户」 |
| 长期记忆里的实体关系 | 上下文图（时序 KG） | Graphiti / Zep / Cognee |
| 步骤固定的审批 | 执行图，甚至普通工作流 | 不必 GraphRAG |

---

## 三、与相邻技术

| 技术 | 关系 |
|---|---|
| [环节 02](../环节02-提示与上下文工程详解.md) | Prompt + 窗口的技法讲义；栈内口径在本目录前两篇 |
| [knowledge/context-engineering](../../knowledge/context-engineering/) | 窗口预算本体；本目录 [context-engineering.md](./context-engineering.md) 只写它在栈里的位置 |
| [Harness](../harness/) | 车：工具、权限、验证门、产品形态。栈内口径：[harness-engineering.md](./harness-engineering.md) |
| [LangGraph](../langgraph/) · [环节 07](../环节07-编排与循环控制详解.md) | 执行图落地；State / Node / Edge 讲义在那边 |
| [环节 08](../环节08-多Agent协作详解.md) | 舰队的协作模式；接线仍用执行图 |
| [环节 01](../环节01-决策与推理范式详解.md) | ReAct 是微观骨架；五段是宏观阶段 |
| [RAG](../../knowledge/rag/) · [环节 06](../环节06-检索增强RAG详解.md) | GraphRAG 是 RAG 谱系一支；构图与契约在 [context-graph.md](./context-graph.md) |
| [Memory](../../knowledge/memory/) | 图式记忆 = 上下文图用在长期记忆上 |
| [知识库](../../knowledge/knowledge-base/) | 五维里的图存储 / Graph RAG / Ontology |
| [MCP](../mcp/) | 插件进循环；图库以 Tool / Resource 暴露 |
| [Eval](../../reliability/eval/) | 循环评验证器与轨迹；上下文图评多跳路径是否走对 |
| [structured-output](../../reliability/structured-output/) | 提示层的格式闭环 |

---

## 四、落地建议

1. **先写完成定义，再写循环。** 哪条命令绿、哪个字段必填，写不出来就不要上 Agent。一次调用能交差就停在提示。
2. **验证者与执行者分离。** 模型说「已修好」不算完。
3. **默认闭环 + L2 护栏**：步数、超时、花费、重复动作检测。
4. **按栈升级，不要跳级**：提示稳了再管窗口，窗口稳了再上 Harness，循环跑绿再画执行图，最后才决定要不要上下文图。
5. **一张图只表示一种东西。** 工作流节点不要和「客户」节点混 Schema。上下文工程 ≠ 上下文图。
6. **抽取要可增量**；来源和置信度分开存；图查询默认只读。
7. **构图账单单列。** GraphRAG 的钱常常花在抽取，不在问答。
8. **循环加速的是你已理解的工作。** 两套相同循环，一套放大理解、一套逃避理解——循环不区分，人要区分。

---

## 五、面试速记

1. 提示工程和循环工程差在哪？→ 提示打磨一次输出；循环打磨反馈与停止条件，人退出调度。
2. 提示工程和上下文工程差在哪？→ 措辞 vs 窗口里选什么、砍什么。
3. 上下文工程和上下文图差在哪？→ 窗口预算 vs 领域事实；图召回之后仍要裁。
4. 五段里哪一段最不能省？→ VERIFY；省了就是开环。
5. 舰队是不是另一种循环？→ 不是。每层还是五段；变的是复制份数。接线归执行图。
6. 什么时候从 loop 升级到 graph？→ 并行汇合 / 人审节点 / 按边重试 / 共享领域事实。
7. Harness 和循环是不是一回事？→ 循环是设计；Harness 是带工具和权限的运行时。Loop + 执行图是外壳要交付的；上下文图是地图。
8. 执行图和上下文图差在哪？→ 控制流 vs 领域事实；checkpoint ≠ 本体。
9. 什么时候上 GraphRAG？→ 有跨实体多跳或全局总结的失败案例；先 Hybrid + Rerank。
10. 为什么持久化了还对不齐客户？→ 缺稳定 ID、时效、来源和冲突规则。

---

## 六、本目录 MVP

[mvp.py](./mvp.py) 演示执行图与上下文图如何分工（规则抽取，不调模型）：

1. 从三份短文档抽出「订单 / 客户 / 政策」属性图。
2. **关键词检索**答「订单 8821 为什么拒退」会漏掉政策节点。
3. **图上局部遍历**走出 `订单 → 许可证 → 不可退条款`。
4. **迷你执行图**：关键词不够就走图检索；退款是写操作，停在人审。

```bash
cd ai/agent/loop-graph-engineering
python3 mvp.py
```

要点：checkpoint 能记下这条 run；条款本身住在上下文图，不在 State 里。细则见 [execution-graph.md](./execution-graph.md)、[context-graph.md](./context-graph.md)。

---

## 七、延伸阅读

- 提示 / 窗口技法：[环节 02](../环节02-提示与上下文工程详解.md) · [knowledge/context-engineering](../../knowledge/context-engineering/)
- 循环原文：Rahul, *Loops: What Every AI Engineer Needs to Know in 2026* → [loop-engineering.md](./loop-engineering.md)
- 图综述：arXiv:2608.21156；GraphRAG（Microsoft 2024）；LightRAG / HippoRAG / LazyGraphRAG → [context-graph.md](./context-graph.md)
- 时序图式记忆：Zep Graphiti、Cognee
- 实现：[Harness](../harness/) · [LangGraph](../langgraph/) · [环节 07](../环节07-编排与循环控制详解.md)
- 零件：[Skills](../agent-skills/) · [MCP](../mcp/) · [Memory](../../knowledge/memory/) · [RAG](../../knowledge/rag/) · [Eval](../../reliability/eval/)
- 上级：[Agent 总图](../README.md) ｜ 总索引 [../../README.md](../../README.md)
