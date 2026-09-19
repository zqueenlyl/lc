# OpenAI · Multi-agent 资料

> 几乎没有一篇对标 Anthropic Research 系统的工程长文。LLM 时代反复讲两个原语：**Handoff（转交对话所有权）** 与 **Agents as tools（经理把专家当工具）**，再用 Swarm → Agents SDK → Codex / Agents API 收成产品。
>
> 检索日：2026-09-19。`my-kb` 几乎没有 OpenAI 专题页，只有 2026-09-13 周报提到 Agents API 和万级 agent 证明。

总判断见 [README](./README.md)。落地四段见 [sdlc.md](./sdlc.md)。先分清两代：2018–2019 是 MARL（辩论、捉迷藏、Dota Five）；2024–2026 才是 LLM 编排。

---

## 论文 / 白皮书

| 年份 | 来源 | 关系 |
|---|---|---|
| 2018 | [AI safety via debate](https://arxiv.org/abs/1805.00899) / [博客](https://openai.com/index/debate/) | 两个 agent 对辩、人当裁判。对齐用自博弈。 |
| 2019 | [Emergent Tool Use](https://arxiv.org/abs/1909.07528) | 捉迷藏自博弈长出策略和工具使用。 |
| 2019 | [Dota 2 with large scale DRL](https://openai.com/index/dota-2-with-large-scale-deep-reinforcement-learning/) | OpenAI Five。 |
| 2023 | [Practices for Governing Agentic AI Systems](https://cdn.openai.com/papers/practices-for-governing-agentic-ai-systems.pdf) | 任务适配、动作约束、审批、日志、可中断。 |

没有「AI Organizations」那种组织对齐论文。LLM 编排写在指南和 SDK 里。

---

## 博客与产品（LLM 主线）

1. [Orchestrating Agents: Routines and Handoffs](https://developers.openai.com/cookbook/examples/orchestrating_agents)（已归档）  
   Swarm 概念原文：handoff = 电话转接，对方看得见全部对话。
2. [New tools for building agents](https://openai.com/index/new-tools-for-building-agents/)（2025）  
   Responses API + Agents SDK。SDK 是 Swarm 的生产演进。
3. [A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)  
   **先单 agent。** 要拆只有 Manager（`as_tool`）和 Handoff。
4. [Deep Research](https://openai.com/index/introducing-deep-research/) / [Operator](https://openai.com/index/introducing-operator/) / [ChatGPT agent](https://openai.com/index/introducing-chatgpt-agent/)  
   产品更像统一长循环，不是对外拆解的 Lead+Workers 文。
5. [The next evolution of the Agents SDK](https://openai.com/index/the-next-evolution-of-the-agents-sdk/)  
   Sandbox harness：MCP、skills、`AGENTS.md`、shell、apply_patch。
6. [Unrolling the Codex agent loop](https://openai.com/index/unrolling-the-codex-agent-loop/)  
   Codex harness 怎么管上下文。Agents API 的底本。
7. [Introducing the Agents API](https://openai.com/index/introducing-the-agents-api/)（2026-09）  
   托管 Codex harness：compaction、programmatic tool calling、原生并行 subagents。
8. [On the Navier–Stokes Millennium Prize Problem](https://openai.com/index/navier-stokes-solution/)（2026-09）  
   约 1 万并发 agent、分组通信、Codex 交叉授粉、Lean 形式化。优先权有争议。当「编排上限 + 可验证产物」样本读，不要当已结案科学结论。

---

## 开源与文档

| 仓库 / 页 | 用途 |
|---|---|
| [openai/swarm](https://github.com/openai/swarm) | 教育用。生产请迁 SDK。 |
| [openai-agents-python](https://github.com/openai/openai-agents-python) | handoffs、`as_tool`、guardrails、HITL、sessions、tracing |
| [examples/agent_patterns](https://github.com/openai/openai-agents-python/tree/main/examples/agent_patterns) | **最该读**：routing、agents_as_tools、parallelization、llm_as_a_judge、human_in_the_loop |
| [openai-agents-js](https://github.com/openai/openai-agents-js) | TypeScript |
| [openai/codex](https://github.com/openai/codex) | 开源 coding harness。Agents API 底层即此 |
| [multi-agent-emergence-environments](https://github.com/openai/multi-agent-emergence-environments) | 捉迷藏环境。历史 MARL |

官方第一问：**这一步谁对用户说话？**

- **Handoff**：专家接管回复。对应 Anthropic hand-off。
- **Agents as tools**：Manager 综合专家输出。对应 Orchestrator-Workers。

入口：[Orchestration](https://developers.openai.com/api/docs/guides/agents/orchestration) · [SDK multi_agent](https://openai.github.io/openai-agents-python/multi_agent/) · [Parallel Agents](https://developers.openai.com/cookbook/examples/agents_sdk/parallel_agents) · [Codex Subagents](https://developers.openai.com/codex/subagents) · [三档选型](https://developers.openai.com/api/docs/guides/agents)

Codex 默认要显式要求才 spawn；内置 `worker` / `explorer`；自定义 TOML 在 `.codex/agents/`。

---

## 落到本目录的 SDLC

- 评审 / 拆解：Manager 保持所有权（agents-as-tools），不要 Handoff 来回传。
- 实现：专家当 tool / subagent；HITL 与 guardrails 在 SDK 示例里现成。
- 跨域合规面才 Handoff。
- NS 实验提醒：分组、交叉授粉、**产物可机器核验** 比多做人设重要。
