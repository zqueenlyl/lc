# Anthropic · Multi-agent 资料

> 能力线主张研究/编码可以拆并行子 agent；产品线在紧耦合会话里反对拆；安全线证明对齐过的个体组成组织后仍会更不 aligned。三条都是他们自己写的。
>
> 检索日：2026-09-21（相对 09-19 补漏：FLT 形式化、C compiler agent teams、长程应用 harness、Prove2Me）。`my-kb` 已摄入 Building Effective Agents、Commerce 指南与 `commerce-agents` 源码。

总判断见 [README](./README.md)。落地四段见 [sdlc.md](./sdlc.md)。

---

## 论文

| 来源 | 要点 |
|---|---|
| [AI Organizations](https://arxiv.org/abs/2604.10290)（2026-04） / [Alignment 解读](https://alignment.anthropic.com/2026/ai-organizations/) | 12 任务：咨询组织 + 软件团队。已对齐个体组成组织后业务效用更高、伦理更差。差距更多来自提示与任务分解。单 agent 安全结论不能认证 multi-agent 部署。 |
| [Prove2Me](https://arxiv.org/abs/2608.28433)（2026-08） | 哥伦比亚 / Peng：形式化协作平台。mission 拆任务、定理依赖 DAG、proof-sketch、自然语言可检索。FLT 跑通靠它，不是靠更多人设。 |

Constitutional AI（2022-12）是模型自反馈，不算部署型 MAS。

---

## 工程博客

1. [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)（2024-12）  
   Workflows vs Agents。五模式含 **Orchestrator-Workers**。从简单开始。
2. [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)（2025-06）  
   Claude Research = LeadResearcher + 并行 Subagents + CitationAgent。Opus 4 lead + Sonnet 4 workers，内部 eval **比单 agent Opus 4 高 90.2%**；约 **15× chat token**。适用：高价值、可并行、信息超出单窗口。计划写入 Memory；子 agent **产物落文件**，只回引用。
3. [Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)（2025-10）  
   `SKILL.md` 渐进披露。模块化靠技能，不是先拆人。
4. [Building agents with the Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)（2025-09）  
   Code SDK 改名 Agent SDK；默认 subagents（并行 + 隔离上下文）。
5. [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)（2025-11）  
   Initializer + 增量 coding agent + 文件产物。长程编码单 vs 多 **仍未决**。
6. [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)（2026-01）  
   评的是 model + harness；多路径合法，看终态。
7. [Building a C compiler with a team of parallel Claudes](https://www.anthropic.com/engineering/building-c-compiler)（2026-02）  
   **Agent teams**：16 个实例共享代码仓、无人值守。约 2000 次 Claude Code 会话，写出能编 Linux 6.9 的 Rust C 编译器。长程编码可拆的实证，不是电商那种紧耦合会话。
8. [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)（2026-03）  
   planner / generator / **evaluator 分身**。自评会吹自己；独立评估者才压得住。接 2025-11 长程 harness：分解 + 结构化产物交接。
9. [Formalizing Fermat's Last Theorem](https://www.anthropic.com/research/formalizing-fermats-last-theorem)（2026-09-04） / [Lean 附录](https://www-cdn.anthropic.com/9e431dff043da6538d99d6c2d231b670aa3da263.pdf)  
   **不是新证 FLT**，是把 Wiles（Darmon–Diamond–Taylor 叙述）写成 Lean。约 11 天、数十 agent、~1300 万行、~29500 个中间定理进终稿；内部研究模型约等于 Claude Fable 5.1，~60 亿 output token。无共享 DAG 时 agent 丢状态、重复劳动；换 Prove2Me 后才跑通。Lean 三公理、无 `sorry`；comparator 对过 Mathlib 陈述。源码：[anthropics/fermats-last-theorem](https://github.com/anthropics/fermats-last-theorem)。同脚手架三份 Claude Max 三天形式化 Vinogradov 三素数定理。

## 产品博客（何时不该拆 / 何时该拆）

- [The Anatomy of Effective Commerce Agents](https://claude.com/blog/the-anatomy-of-effective-commerce-agents)（2026-09）  
  紧耦合会话：**技能优于子 agent**。例外：深度研究子 agent；已有合规面则 **hand-off**。
- [Claude for Commerce Agents](https://www.anthropic.com/news/claude-for-commerce-agents)（2026-09）
- [How and when to use subagents in Claude Code](https://claude.com/blog/subagents-in-claude-code)（2026-04）  
  调研、并行、独立二审才值得付隔离税。
- [Project Vend 1](https://www.anthropic.com/research/project-vend-1)（2025-06） / [Phase 2](https://www.anthropic.com/research/project-vend-2)（2025-12）  
  Phase 2 加 CEO agent。利润改善，但 CEO 也会批准糟决策。加一层监督 ≠ 自动治理。

---

## 开源与文档

| 地址 | 关系 |
|---|---|
| [Cookbook research prompts](https://github.com/anthropics/claude-cookbooks/blob/main/patterns/agents/prompts/research_lead_agent.md) | Research 博客配套 Lead / Subagent 提示 |
| [claude_agent_sdk 教程](https://github.com/anthropics/claude-cookbooks/tree/main/claude_agent_sdk) | 到 Notebook 08 动态 Workflow |
| [claude-agent-sdk-demos / research-agent](https://github.com/anthropics/claude-agent-sdk-demos/tree/main/research-agent) | 2–4 researcher → analyst → report-writer，笔记落文件 |
| [claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) / [typescript](https://github.com/anthropics/claude-agent-sdk-typescript) | 程序化 subagents；TS 较新版本有 `Workflow` |
| [commerce-agents](https://github.com/anthropics/commerce-agents) | **反例参考实现**：单 agent + 技能；唯一隔离调用是只读 `run_analysis`。本仓库有 [案例页](../case-studies/commerce-agents.md) |
| [anthropics/skills](https://github.com/anthropics/skills) | Managed Agents 的 `multiagent` 字段：共享文件系统、独立 thread，深度不能 > 1 |
| [anthropics/fermats-last-theorem](https://github.com/anthropics/fermats-last-theorem) | FLT Lean 全证。平台侧见 Prove2Me / Columbia DAPLab |
| [Managed Agents](https://www.anthropic.com/engineering/managed-agents)（2026-04） | 托管长程：brain 与 hands 解耦。编排基础设施，不是「何时拆人」文 |

Claude Code 四层并行，不要混用：

1. [Subagents](https://code.claude.com/docs/en/sub-agents) — 同一会话内委托，只回摘要
2. Agent view — 你派多个独立会话
3. [Agent teams](https://code.claude.com/docs/en/agent-teams) — 实验性，互发消息 + 共享任务板，需环境变量
4. [Dynamic workflows](https://platform.claude.com/cookbook/claude-agent-sdk-08-dynamic-workflows) — 计划写进 JS，runtime 跑大规模 fan-out

对照：[Run agents in parallel](https://code.claude.com/docs/en/agents)。

---

## 落到本目录的 SDLC

- 评审 / 拆解抄 Commerce：紧耦合不拆。
- 实现：可并行研究抄 Research；长程编码抄 C compiler agent teams；任务图抄 FLT / Prove2Me DAG，不靠全员群聊。
- 验收：搜集与判定分开（Citation / evaluator）；数学侧 Lean 式机器核验。
- 风险读 2604.10290 和 Vend 2：组织更会出活，也会更会走偏。
