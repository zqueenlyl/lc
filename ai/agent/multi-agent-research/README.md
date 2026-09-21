# Multi-agent Research · 实验室对照与落地判断

> 三家实验室一手资料 + Multica 工作区，用来回答：**何时拆、怎么下发、产物怎么收、不确定谁拍板**。
> 关卡讲义仍读 [环节 08](../环节08-多Agent协作详解.md)；跨进程工单读 [a2a](../a2a/)。本目录是资料库，不是又一篇「怎么拆团队」。

整理日期：2026-09-21（补漏 FLT / Prove2Me、C compiler teams、Symphony）。场景锚点：复杂业务系统、几十个仓库、多套配置——需求评审 → 任务拆解 → 实现 → 验收。

---

## 一、和本目录其它页怎么分工

| 去哪 | 干什么 |
|---|---|
| [环节 08](../环节08-多Agent协作详解.md) | 关卡：主管-下属 / 流水线 / 辩论，该不该上 |
| [a2a](../a2a/) | 协议：跨团队委托的信封 |
| [langgraph 04](../case-studies/langgraph/04-多智能体与高级模式.md) | 框架：图画出来怎么跑 |
| **本目录** | 实验室实际发了什么、开源在哪、怎么落到多仓 SDLC |

落地主文：[sdlc.md](./sdlc.md)（何时拆、下发、产物、门控、四段配法）

厂商分册：[Anthropic](./anthropic.md) · [OpenAI](./openai.md) · [DeepSeek](./deepseek.md) · [Multica](./multica.md)（源码阅读：[multica-architecture.md](./multica-architecture.md)）

---

## 二、总判断

**阶段之间用固定工作流，阶段内部才决定拆不拆人。**

- 评审、拆解、人对齐：单 agent + 技能。上下文紧耦合，拆开会交「移交税」。
- 实现：按**互不重叠的写域** spawn，worker 数 ≠ 仓库数。
- 验收：对拆解时写下的 `acceptance` 跑，不按实现者自评。失败回原 owner。

判断拆不拆，四条就够：上下文是否必须共享、写域是否重叠、对话所有权在谁、能不能容忍小时级墙钟。「仓库多」本身不是拆 50 个 agent 的理由。

所有权：

| 模式 | 谁对用户说话 | 结果 |
|---|---|---|
| **Hand-off** | 领域方接管 | 干净（支付 / 权限 / 生产配置） |
| **Delegation** | 编排器主导，单轮反复进出 | 每次交换掉质量 |

---

## 三、下发、产物、门控

**下发的是规格，不是聊天记录。** Lead 写入任务板，worker 认领。字段至少有：`goal`、`repos[]`、`writeScope`、`inputs`（文件路径）、`acceptance`、`blockedBy`、`budget`。实现 worker 用 fresh，不带 Lead 聊天史。

**文件是真相，对话是草稿。** 一次需求一个 run 目录（`review.md` / `plan.json` / `tasks/*.json` / `impl/<task>/` / `accept/report.md`）。收集 = 校验 schema 与写域 → compact 空结果 → 按仓出 PR → Lead 只读产物清单。配置变更和代码 PR 成对。投递按 at-least-once + 消费端幂等，同一 `attempt` 不得重复开 PR。

**门在 harness 里，不在 prompt 里。**

| 级别 | 谁拍板 | 例子 |
|---|---|---|
| Auto | harness / CI | 只读探索、跑测试、草稿 |
| Notify | 人事后看 | 单仓可逆 PR |
| Approve | 必须等人 | 目标、跨仓契约、生产配置、发版、密钥 |

不确定就停，并列选项和证据：影响面不清 → 停在拆解门；契约两解 → 人签一个再 spawn；测试红像环境 → 标 flaky 回任务板；权限不够 → scoped token 或 `blocked`；写域冲突 → CAS 失败后合并或串行。

人签的是目标与边界，不是每个 diff。

---

## 四、四段 SDLC

完整配法（模式表、字段、run 目录、不确定协议、最小系统）见 **[sdlc.md](./sdlc.md)**。这里只留骨架：

1. **评审**：单 agent + 技能；必要时一个研究子 agent 扫仓。人签「做不做」。
2. **拆解**：仍是一个 Lead。契约变更唯一 owner。人签范围。
3. **实现**：这里才用 Team / Manager。共享 worktree，不共享生产凭据。
4. **验收**：Evaluator 对 `acceptance` 跑，不按实现者自评。上线单独签。

---

## 五、三家实验室一句话

| | 核心原语 | 何时拆 | 开源可跑 | 量化 |
|---|---|---|---|---|
| [Anthropic](./anthropic.md) | Skills vs subagents；Research = Lead + 并行 workers；FLT = Prove2Me DAG | 紧耦合会话不拆；可并行研究/长程编码/形式化才拆 | Cookbook prompts、`research-agent`、`commerce-agents`、FLT Lean | 内部 research eval +90.2%；FLT ~11 天 / ~60 亿 token |
| [OpenAI](./openai.md) | Handoff vs agents-as-tools；Symphony = issue 调度 | 先单 agent；合同/工具/策略变了再拆；人盯会话会爆则上看板 | Swarm → Agents SDK `agent_patterns` → Codex / Symphony | 万级 NS（有争议） |
| [DeepSeek](./deepseek.md) | 持久 roster + 任务板 + mailbox | 长时程可并行编码；共享 checkout + 建议写域 | `dsh` experimental Team；社区 `dsh-agent-teams` | ProgramBench 8h 30.04% vs 单 20.39% |

[Multica](./multica.md) 不是实验室论文，是人机看板：issue 是真相，daemon 在你机器上跑已有 CLI。管「工作系统」，不管「模型怎么推理」。

---

## 六、建议阅读顺序

1. 本页第二～三节，钉死总判断。
2. [sdlc.md](./sdlc.md) 走完四段：下发字段、run 目录、门控、最小系统。
3. 对照要抄的原语：DeepSeek 任务板 / Anthropic 研究子 agent / OpenAI Manager。
4. 若要上工作区而不是自建队列，读 [Multica](./multica.md)；逛源码按 [multica-architecture.md](./multica-architecture.md)。
5. 环节 08 仍用来讲模式名；上线评测回 [环节 09](../环节09-评测与可观测详解.md)。
