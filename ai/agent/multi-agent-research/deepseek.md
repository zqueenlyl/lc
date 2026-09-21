# DeepSeek · Multi-agent 资料

> 不写「如何编排」的产品长文。公开主线是开源 harness 里一套可崩溃恢复的 **Agent Teams**，再用 V4.1-Flash 报告给出长时程编码曲线。
>
> 检索日：2026-09-21（相对 09-19 再搜：无新的官方 Team 编排长文。WideSeek-R1 等第三方 MARL 论文不是 DeepSeek 出品，不收）。`my-kb` 已摄入 `agent-teams`、`deepseek-harness`、`dsh-agent-teams-architecture`、V3.2 / V4.1-Flash。

总判断见 [README](./README.md)。落地四段见 [sdlc.md](./sdlc.md)。

先分清三套会撞名的东西：

1. **官方 Agent Teams**（`dsh` experimental，默认关）
2. **普通 subagent**（一次性委托，结果回来就结束）
3. **社区插件** [NanmiCoder/dsh-agent-teams](https://github.com/NanmiCoder/dsh-agent-teams)（更早、有自动调度和 Web UI）

V3.2 报告里的「多 agent」是**训练数据合成流水线**，不是运行时。R1 / MLA / Engram 不是本页资料。

---

## 论文 / 报告

| 来源 | 关系 |
|---|---|
| [DeepSeek-V3.2](https://arxiv.org/abs/2512.02556)（2025-12） | Search：构题 / 异构作答 / 验证。General：环境合成 agent 造 1827 环境、85k prompt。判据：F2P、唯一答案、pass@100。 |
| [Cordis](https://arxiv.org/abs/2608.25512)（2026-08） | dsh 底层：可逆副作用 + 响应式 coeffects。Teams 挂 `ctx.agentTeams`。 |
| [V4.1-Flash](https://arxiv.org/abs/2609.19969)（2026-09） | **唯一给出官方 Team 实测。** 编码环境也用构造 → 质检 → 修复流水线。 |

V4.1-Flash 数字（dsh Agent Team，初步）：

- ProgramBench Almost@1：单 1h 12.79% → 8h **20.39%**；多 1h 13.59% → 8h **30.04%**
- FrontierSWE v2 Mean@5：单 10.50% → 20h **28.20%**；多 13.50% → 20h **32.90%**
- 每个 deadline 都赢，墙钟越长差距越大
- 奖励 = 任务分 + 协作奖励 + **derived-latency**（DAG 关键路径，不是 token 总量）

机制：Lead `spawn_teammate`（fresh / fork）、共享同一 checkout、持久 mailbox、任务板 + 建议性写域、**只有 Lead 能 interrupt**。与 Anthropic 电商结论不矛盾：紧耦合会话不拆，长时程可并行编码才拆。

---

## 博客 / 产品

- [Harness developer preview](https://www.deepseek.com/harness/en/)（2026-08）：一切皆插件。Standard 含 subagents / workflows；Code mode 用 TypeScript 编排多轮工具（计划在代码里）。
- [V3.2 发布](https://www.deepseek.com/en/news/deepseek-v3-2/)（2025-12）：讲合成规模，不讲 Team API。
- [V4.1-Flash 新闻](https://www.deepseek.com/en/news/deepseek-v4-1-flash/)（2026-09）：多 agent 数字只在技术报告。

---

## 开源与文档

| 地址 | 角色 |
|---|---|
| [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) | 官方 MIT。`npx @deepseek-ai/dsh web` |
| `@deepseek-ai/dsh-experimental-tool-agent-team` | 官方工具：spawn / list / send / followup / task_* / wait / interrupt。需加 profile，契约会变 |
| [NanmiCoder/dsh-agent-teams](https://github.com/NanmiCoder/dsh-agent-teams) | `team.json` + `inbox/*.jsonl`；`attempt_id`、60s 租约、Web DAG |
| [docs/subsystems/agent-team.md](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/agent-team.md) | 官方类型与 `ctx.agentTeams` |
| [deepseekharness.io/agent-teams](https://deepseekharness.io/agent-teams/) | 第三方深读（`my-kb` 未单独建页） |
| [架构文档](https://deepseek-harness.github.io/deepseek-harness/en/reference/) | Cordis + capability seams |

官方 Team 四件套：

| 原语 | 要点 |
|---|---|
| Roster | fresh 不带 Lead 历史，fork 带快照 |
| Mailbox | 先落盘再 ack；恢复 = queued − delivered |
| Task DAG | 整份快照 + `revision` CAS；`blockedBy` 无环 |
| Steer | `wait_agent` / `interrupt_agent` |

成员**共享同一 checkout**。`writeScopes` 是建议性路径前缀，不是锁。实验可跑 official experimental，不要绑生产流水线。

和一次性 subagent：后者「任务进、结果出、中途没通道」；Team 是持久名册，能互发信、等待、打断。

---

## 落到本目录的 SDLC

最可抄：**任务板 + CAS + 持久邮箱 + 建议写域**，以及 fresh worker 只带规格。不管跨仓契约单一 owner，也不做人签三级门——那一层用 [Multica](./multica.md) 的 issue，或自建 run 目录。
