# Multi-agent SDLC · 几十仓的评审 / 拆解 / 实现 / 验收

> 场景：复杂业务系统、几十个仓库、多套配置。要做的不是「先组一队 agent」，而是 **外层固定四段工作流，内层按正交性才拆人**。
>
> 依据：`my-kb` 的 Workflows vs Agents、Skills Not Subagents、Agent Teams、Swarm Flow、Agent Coordination as Distributed Systems。厂商原语对照见 [Anthropic](./anthropic.md) / [OpenAI](./openai.md) / [DeepSeek](./deepseek.md) / [Multica](./multica.md)。目录总判断见 [README](./README.md)。

---

## 一、默认不拆

紧耦合会话不要拆（Anthropic 电商）：子 agent 每次移交都是有损状态传递，还加 token 和延迟。长时程、可并行的编码才拆（DeepSeek Agent Teams）：墙钟越长、写域越正交，多 agent 越赚。

分野不在「要不要 multi-agent」，而在任务形态。四条判据：

| 判据 | 用技能 / 单 agent | 才拆子 agent |
|---|---|---|
| 上下文耦合 | 共享需求、契约、会话历史，拆开会丢状态 | 子任务只需要目标、写域、验收，不需要整段对话 |
| 并行收益 | 后一步吃前一步输出，拆了只会串行加税 | 多仓 / 多模块写域不重叠，墙钟能被并行吃掉 |
| 所有权 | 编排器还要主导、反复进出（delegation） | 领域方接管（hand-off），或 worker 做完只回紧凑答案 |
| 延迟与成本 | 人对齐、评审、问答，延迟敏感 | 实现、探索、扫仓，可容忍小时级墙钟 |

「几十个仓库」本身不是拆 50 个 agent 的理由。先按写域是否重叠、契约是否共享、人是否还在回路里分组。同一需求里「改订单契约」通常只能有一个 owner；「订单仓改接口 + 各端按契约改调用」才值得并行。

经验规则：1 个 Lead 管阶段；实现阶段按**互不重叠的写域** spawn，而不是按仓库数 spawn。

两个例外：深度研究子 agent（自己搜、自己撞墙，只回摘要）；已有独立合规面（支付 / 权限 / 生产配置）做 **hand-off**，不要委派来回传。

---

## 二、先选编排范式，再选协作结构

Anthropic 把智能系统分成两类：**Workflow** 是预定义代码路径，**Agent** 是模型自己决定下一步。复杂研发链路两边都要用——阶段顺序固定，阶段内怎么做可以动态。

五种工作流：

| 模式 | 做什么 | 何时用 | 对应阶段 |
|---|---|---|---|
| Chaining | 线性步骤，上一步输出喂下一步，中间可加 gate | 路径清晰，用延迟换精度 | 评审 → 拆解 → 实现 → 验收 |
| Routing | 先分类，再导向专门下游 | 输入类别明显不同 | 需求进业务域 / 仓库簇 / 配置系统 |
| Parallelization | 预定义子任务并行，再聚合 | 子任务独立，或要多视角提置信度 | 多仓按已知清单并行改；多评审员交叉读 |
| Orchestrator-Workers | 中央模型动态分解、委派、综合 | 子任务结构随输入变，无法预先枚举 | 实现：Lead 按影响面现场拆写域 |
| Evaluator-Optimizer | 一个生成、一个按标准评估，循环迭代 | 有明确评估标准且迭代有可测收益 | 验收、测试、契约回归 |

三种协作结构，不要混成一种：

| 结构 | 何时 | 做法 |
|---|---|---|
| **单 agent + 技能**（默认） | 评审、拆解、人对齐、跨仓影响分析 | 模块化靠 `SKILL.md`，不移交会话 |
| **Agent Teams**（实现期） | 长时程编码、共享 checkout、写域隔离 | Lead + 可续 teammate；roster / 任务板 DAG / mailbox |
| **Swarm Flow**（算子层） | 动态决定派几个 worker、置信度不够就停 | `budget` / `parallel` / `compact` / `pipeline` / `human` 可组合 |

Orchestrator-Workers ≠ Agent Teams。前者是一次性委派；后者是持久身份、CAS 任务板、可恢复邮箱。跨仓实现要后者；一次分类或一次摘要用前者就够。

---

## 三、任务下发：写规格，不聊天

子 agent 不该从一段自然语言里自己猜范围。Lead 写入任务板的是一份可机器校验的规格；worker 认领、执行、回写状态。这是分布式系统的工作队列，不是群聊。

| 字段 | 必须写清 | 为什么 |
|---|---|---|
| `goal` | 这一票要改变的可观察结果 | 没有目标就无法验收 |
| `repos[]` | 允许读 / 允许写的仓库列表 | 防止扫全库或改错仓 |
| `writeScope` | 路径前缀，建议性隔离 | 重叠写域必须串行或合并 |
| `inputs` | 需求、契约、接口快照的路径 | 不靠上下文口头传达 |
| `acceptance` | 测试、diff 约束、禁止事项 | collect 时对规格而不是对感觉 |
| `blockedBy` | 依赖的 task id | DAG 无环，完成 blockers 才能开工 |
| `budget` | 墙钟 / token / 工具次数 | 防止探索任务吞掉整条链路 |

下发协议：

| 步骤 | 谁做 | 语义 |
|---|---|---|
| 1. Lead 创建任务 | 编排器 | 写入任务板，`revision` = CAS 版本 |
| 2. Worker 认领 | 子 agent | `pending → in_progress`，带 `attempt_id` |
| 3. 执行 | 子 agent | 只在 `writeScope` 内改；产物写约定路径 |
| 4. 回写完成 | 子 agent | `completed` + 产物清单；消费端幂等 |
| 5. Lead 等待变化 | 编排器 | `waitForChange`，而不是轮询聊天 |

三种不该用的下发：把整段需求粘进 20 个子 agent（移交税 + 漂移）；让 worker 互相私聊改契约（无单一真相）；按仓库数固定 spawn（多数仓与本次需求无关）。

先 Routing 再 spawn。映射表应是代码 / 索引（服务名 → 仓 → 配置源），不要每次让模型从几十个仓里重新发现。

---

## 四、产物：文件是真相，对话是草稿

多 agent 失败最常见的点不是推理差，而是结果散落在各自身份的上下文里，Lead 只能口头汇总。收集必须对路径和 schema。

| 机制 | 做法 |
|---|---|
| 共享工作区 | 同一需求一个 worktree / 分支族。实现 worker 共享可见 checkout，改动立刻可见，写域不能重叠 |
| 阶段契约目录 | `runs/<id>/review.md`、`plan.json`、`tasks/*.json`、`impl/<task>/`、`accept/report.md` |
| 机器可校验 schema | 任务、影响面、接口变更、验收结果用 JSON/YAML。Markdown 给人读 |
| 收集 = 校验 + 合并 | compact 空 / 越权 diff → 按仓出 PR → Lead 只读产物清单和失败项 |

跨仓产物：

| 产物 | 生产者 | 收集规则 |
|---|---|---|
| 影响面图 | 评审 / 拆解 | 服务 → 仓 → 配置项；缺映射则停 |
| 跨仓契约 diff | 拆解 Lead | 只允许一个 owner 改契约 |
| 单仓 patch / PR | 实现 worker | 必须落在声明的 `writeScope` |
| 配置变更 | 配置 worker | 与代码 PR 成对，禁止静默改生产 |
| 验收报告 | Evaluator | 对 `acceptance` 逐条；失败回写任务，不口头说不行 |

投递语义不要靠模型自觉：任务板 `revision`、mailbox 去重、崩溃重投 = at-least-once + 消费端幂等。同一 `attempt` 重跑不得重复开 PR、不得覆盖更新的 `revision`。

---

## 五、授权与不确定：门在 harness 里

自动协调不够时停，而不是让模型「先做了再说」。三级写进 harness，不要写进 prompt。

| 级别 | 谁拍板 | 典型动作 | 例子 |
|---|---|---|---|
| Auto | harness / CI | 只读探索、跑测试、生成草稿 | 扫仓、单测、预览环境部署 |
| Notify | 人可事后看 | 可逆、范围清楚的写操作 | 单仓实现 PR、文档、非生产配置草稿 |
| Approve | 必须等人 | 不可逆、跨边界、合规、花钱 | 需求目标、跨仓契约、生产配置、发版、权限 |

不确定时：

| 情况 | 禁止 | 正确动作 |
|---|---|---|
| 影响面不清 | 按「常见仓」开改 | 输出候选映射 + 证据，停在拆解门 |
| 契约有两种解法 | worker 各自选一种实现 | Lead 列选项 / 代价，人签一个再 spawn |
| 测试红像环境 | 改生产配置碰运气 | 验收报告标 flaky / env，回任务板 |
| 权限或密钥不够 | 复用他人凭证、绕过 | 申请 scoped token，或把任务标 `blocked` |
| 两个 worker 写域冲突 | 后写覆盖先写 | CAS 失败 → 合并任务或串行化 |

人签的是目标与边界，不是每个 diff。评审门签「做不做、为什么做、成功长什么样」。实现门签「跨仓契约和写域」。验收门签「能否上线」。中间交给 Evaluator + CI。

---

## 六、四段工作流，只在实现段拆人

外层 Chaining + 人工门，内层按阶段换结构。不要一上来做全职 agent 集群互相开会。

### 1. 需求评审 — 单 agent + 技能

紧耦合：要同时看业务目标、现有服务、配置约束、历史事故。拆子 agent 会丢共享上下文。技能里放仓库索引、配置系统说明书、领域禁区。

| 项 | 做法 |
|---|---|
| 模式 | 单 agent + 只读工具；必要时一个深度研究子 agent 扫仓 |
| 下发 | 不 spawn 实现者；只产出 `review.md` + 影响面候选 |
| 产物 | 目标、非目标、风险、涉及仓 / 配置、待人确认的问题 |
| 门 | Approve：人签「做不做、成功标准」。没签不准拆解 |

### 2. 任务拆解 — Orchestrator，但仍是一个 Lead

Lead 把已批准的需求切成写域不重叠的任务。可以并行做只读调研，契约变更必须先收敛成一份。

| 项 | 做法 |
|---|---|
| 模式 | Routing（映射到仓簇）+ 动态拆任务；契约任务唯一 owner |
| 下发 | 写入 `tasks/*.json`：`repos`、`writeScope`、`acceptance`、`blockedBy` |
| 产物 | 任务 DAG、跨仓接口草案、配置变更清单 |
| 门 | Approve：人签契约与范围。不确定就列选项，禁止默认一种 |

### 3. 实现 — 这里才用 Agent Teams

Lead spawn 可续 teammate，共享 worktree，任务板协调。worker 数量 = 互不重叠的写域数，不是仓库总数。配置变更与代码成对，但不共用生产凭据。

| 项 | 做法 |
|---|---|
| 模式 | Orchestrator-Workers 的持久化形态（roster + DAG + mailbox） |
| 下发 | 认领 task；fresh 模式不带 Lead 聊天史，只带规格与输入路径 |
| 产物 | 每任务一个 PR 或 patch 目录 + 自测日志；越权 diff 直接拒收 |
| 门 | Notify：普通 PR。Approve：跨仓契约落地、生产配置、密钥 |

抄 DeepSeek 的任务板 / 建议写域；跨域合规面才用 OpenAI Handoff。

### 4. 验收 — Evaluator-Optimizer，对人负责

评估者按拆解时写下的 `acceptance` 跑，不按实现者的自我描述。失败回写任务板让原 owner 修，而不是另起一个「修复 agent」改别人的仓。

| 项 | 做法 |
|---|---|
| 模式 | Evaluator-Optimizer；跨仓回归可并行，发布门串行 |
| 下发 | 验收任务引用 impl 产物路径和原 `acceptance` |
| 产物 | 逐条通过 / 失败、回归范围、残留风险、是否建议上线 |
| 门 | Approve：上线。Auto：单测 / 契约测试。不确定标 `blocked` 而不是绿 |

---

## 七、最小系统，先于「20 个人设」

1. 服务 → 仓库 → 配置源的索引（Routing 的地基）
2. 一次需求一个 run 目录（产物契约）
3. 任务板 + 写域（下发与隔离）
4. 三级门控（auto / notify / approve）
5. 实现阶段才允许 spawn

技能先写「怎么找仓、怎么改配置、怎么验收」。工作区不想自建队列时，看板用 [Multica](./multica.md) 的 issue，判断仍按本页。
