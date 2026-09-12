# 外部课程路线（按优先级）

> 位置：`ai/courses.md`，与 [landscape.md](./landscape.md)、[learning-path.md](./learning-path.md) 同属**横向入口**。
> 定位：本库（`ai/`）是**手册 + 原理 + 案例**；本页是**外部课进度表** —— 回答「先看哪门、看它图什么、看完往本库哪块写笔记」。
> 内容为**带日期的检索快照**（学期 / 公开材料批次 / 讲次都会变），核实日期 **2026-09-12**，文末列来源。
> **先看 §0 课程总表**（**已收录 5 门 + 候选池 10 门 = 15 门**，优先级 / 学期 / 状态一张表看全）；**要材料直接跳 §7**（讲义直链 / 录播 / 作业仓库 / 中文字幕搬运，逐条标注公开度）；每门课卡片的「公开材料」行只讲**有多少**，链接在 §7；**候选池详情与选课建议在 §8**。

## 排序原则

1. **按能否直接反哺手上的系统排**：正搭的是**代码沙盒 + 回测验证**，谁讲 Harness / 评测 / 沙盒，谁靠前。
2. **课只当主线，产出沉淀回本库**：看完一门 → 在本库对应专题补一节「课程对照 + 我的实现」，否则等于白看。
3. **按「能拿到什么材料」排，不按课名排**：公开度差异极大（有的全公开、有的只有 reading list），可自学性才是实际位次的决定因素。

---

## 0. 课程总表（已收录 5 门 + 候选池 10 门）

> 全页**唯一一张「课程」总表**（**15 门**）：**P0–P3 = 已收录**，下有详情节（§1–§4）；**C1–C3 = 候选池**，公开度 / 本库接口 / 「怎么排」见 §8。
> 公开度不在此列（各门差异极大且随周变，见每门课的「公开材料」段与 §7）。
> **课程官网链接一律挂在详情小节的课程名上**（§1–§4 的节标题、§8 的条目名）；总表里课名保持**纯文字**，只用 `§N` **锚点链接**跳到对应详情小节 —— 汇总表不放官网外链，避免两处维护。

| 层 | 课程 | 学期 / 起止 · 状态（截至 2026-09-12） | 为什么排这个位次 |
|---|---|---|---|
| **P0** | **CMU 11-768 AI Agents**（[§1](#1-p0--cmu-11-768-ai-agents-fall-2026)） | Fall 2026 · 2026-08-25 ~ 12-03 · **进行中**（第 3 周） | 唯一 **Build → Evaluate → Train 三件套全讲、作业就是实现**；授课人 Neubig 是 OpenHands / SWE-agent 主线 |
| **P1** | **Stanford CS329Z Engineering AI Agents**（[§2](#2-p1--stanford-cs329z-engineering-ai-agents-fall-2026)） | Fall 2026 · 2026-09-23 ~ 12-11 · **未开课**（差 11 天） | 复合 AI 系统全谱系（组件 → 编排 → 优化 → 评测 → 安全）；HW1/HW2 与 P0 同构，**但评测更成体系**（4-tuple 可直接抄给回测） |
| **P2** | **Stanford CS329A Self-Improving AI Agents**（[§3](#3-p2--stanford-cs329a-self-improving-ai-agents-autumn-2025)） | Autumn 2025 那一轮 · 2025-09-22 ~ 12-12 · ✅ **已结课**，下一轮 2027 Spring | 自我改进：测试时算力 / 验证器 / 搜索 / 训练时 RL / 长时程评测；研讨课，**要先有 harness / eval 的对照物**才读得动 |
| **P3-a** | **Stanford CS146S The Modern Software Developer**（[§4.1](#41-stanford-cs146s-the-modern-software-developer)） | 上一轮 2025-26 Autumn ✅ **已结课**；**新一轮 2026-09-22 开课**（差 10 天） | AI 原生开发流程（MCP / Agent Skills / spec-driven / loop engineering）：与本库笔记**重叠度最高**，是流程而非实现视角 → 只补差距 |
| **P3-b** | **MIT MAS.S60 How to AI (Almost) Anything**（[§4.2](#42-mit-mass60-how-to-ai-almost-anything)） | Spring 2025 · 2025 春 · ✅ **已结课**（OCW 定版） | 多模态 / 跨模态生成与交互；能力面扩展，与 Harness / 沙盒 / 回测无直接接口 |
| **C1** | **CMU 10-414/714 Deep Learning Systems**（[§8.1](#81-第一梯队--直接反哺手上的四条线)） | Fall 2026 · 2026-08-25 开课 · ⭕ **进行中** | 造 mini 框架 **Needle**（自动微分 → CPU/CUDA 后端的 NDArray → CNN/RNN），补**沙盒下面那一层**；2022 版全套录像公开 |
| **C1** | **Harvard CS249r · MLSysBook（Machine Learning Systems）**（[§8.1](#81-第一梯队--直接反哺手上的四条线)） | **不是学期课** · 持续更新（2026-09 更新） | 把本库本地推理的实测结论升级成**可计算的公式**（Iron Law）；另含 TinyTorch 手写框架、MLSys·im 性能建模 CLI、StaffML 面试题库 |
| **C1** | **Berkeley LLM Agents MOOC**（f24 + S25 两期）（[§8.1](#81-第一梯队--直接反哺手上的四条线)） | 两期**均已结束** · 视频 / slides / quiz **全公开保留** | 与 CS329A 同题**但有全套录像** → 补 CS329A「只有论文清单」的短板；⚠️ 2026 秋是否再开未公布 |
| **C1** | **MIT 6.5940 TinyML and Efficient AI Computing**（[§8.1](#81-第一梯队--直接反哺手上的四条线)） | Fall 2026 · 2026-09-10 开课 · ⭕ **进行中** | 量化 / 剪枝稀疏 / 蒸馏 → **LLM 量化部署**与长上下文，**本地推理那条线最正的一课**；当季逐讲放，往年版本在 Previous Courses |
| **C2** | **Stanford CS336 Language Modeling from Scratch**（[§8.2](#82-第二梯队--补原理与实现但要留整块时间)） | Spring 2026（3/30–6/3）· ✅ **已结课** | 唯一「从 tokenizer 一路写到 RL 对齐」的公开课（Triton FA2 / 并行 / scaling law / RLVR）；**5 学分、实现量高一个数量级、要 GPU** |
| **C2** | **Stanford CS224N**（[§8.2](#82-第二梯队--补原理与实现但要留整块时间)） | Winter 2026（1/6–3/12）· ✅ **已结课** | 只取两处增量：**A4 = LLM benchmark 与评估** + 期末改手写精简版 GPT-2；⚠️ 作业每年变，做往年不给分 |
| **C2** | **Berkeley CS285 Deep RL**（[§8.2](#82-第二梯队--补原理与实现但要留整块时间)） | Spring 2026（1/19–5/1）· ✅ **已结课** | **HW4 = LLM RL、HW5 = Offline RL** + 期末项目可选 LLM RL → 把 RL 骨架补全（视频只有 Fall 2023，讲义全公开） |
| **C3** | **Hugging Face AI Agents Course**（[§8.3](#83-第三梯队--成本低见效快动手--讲座--别踩的坑)） | **无截止日期** · 随时可做 | 免费、证书也免费；**Bonus Unit 2 = Observability and Evaluation**；覆盖 smolagents / LlamaIndex / LangGraph |
| **C3** | **Stanford CS25 Transformers United V6**（[§8.3](#83-第三梯队--成本低见效快动手--讲座--别踩的坑)） | Spring 2026 · ✅ 已结课（讲座在 YouTube） | 每周一位顶级嘉宾，**用来扫面与挑专题**，不是系统课（想深入得回论文） |
| **C3** | **Karpathy《Neural Networks: Zero to Hero》**（[§8.3](#83-第三梯队--成本低见效快动手--讲座--别踩的坑)） | **常青**（YouTube 全公开） | backprop 手写 → 字符级 → GPT 的**最低成本入门**；⚠️ **LLM101n 至今未发布，别等** |

**三条可操作结论**

1. **材料已冻结且全公开的只有 MIT MAS.S60**（OCW 定版，不受学期影响）；CS329A / CS146S 的官网仍保留当轮课表与 reading。
2. **CS329A / CS146S 不是「结束了」，而是「上一轮结束 + 下一轮已排课」**：CS329A 等 **2027 Spring**（2027-03-29 ~ 06-02，周二 / 周四 18:30–19:50，Chowdhery + Mirhoseini 继续教）；**CS146S 新一轮就在 10 天后**（2026-09-22 ~ 12-04，周二/周四 17:30–18:20，370-370，Class #6380）—— 它 2025 秋的官网材料会被新学期覆盖，**想留档现在拷**。
3. **想跟「正在进行」的只有 CMU 11-768**（8-25 开课、12-03 结课；公开视频滞后 1–2 周，讲义先出）；CS329Z 9-23 才开课，本页对它只能先按 reading list 预习。

> ⚠️ 课程状态会变：斯坦福课表明确写 "schedule is tentative and subject to change"，上表日期取自 ExploreCourses / 官网快照，动手前回官方核一遍。
>
> 上表 **C1–C3 就是候选池**（10 门）：§8 只补**公开度 / 本库接口 / 官网入口 / 「怎么排」**（位次理由不重复）—— 含 2026 秋**正在开**的 MIT 6.5940 与 CMU 10-414。

---

## 1. P0 · [CMU 11-768 AI Agents](https://www.cmu-agents.com/) (Fall 2026)

| 项目 | 内容 |
|---|---|
| 课程号 / 学期 | 11-768 · **Fall 2026**（2026-08-25 ~ 12-03），CMU Language Technologies Institute |
| 历史轮次 | **Fall 2026 首开**（第一轮；官网无 archive / 往届材料）→ **没有往届录像可补课，只能跟当季**。⚠️ 别与 CMU **24-880「AI Agents for Engineers」**混淆（机械工程系，授课人 Amir Barati Farimani，是**另一门课**）；CMU **15-482「Autonomous Agents」**（CSD 系，2025 秋）也不是这个课号 |
| 授课 | **Graham Neubig**（OpenHands / SWE-agent 主线）+ **Daniel Fried**；周二 / 周四 15:30–16:50，Porter Hall 100 |
| 先修 | 有训练神经语言模型经验（推荐 11-667 / 11-711 / 10-202）→ **对纯应用者偏硬** |
| 算力赞助 | Fireworks、Modal（A1 的 sandbox 就跑在 Modal 上）、Prime Intellect、Sail |
| 主线 | **Build → Evaluate → Train**：先写 harness，再做 eval，最后做 RL 训练；后半学期团队研究项目 |

**作业结构（这是本课最值钱的部分）**

| 作业 | 占比 | 内容 |
|---|---|---|
| A1 Harness | 10% | 从零实现：`build_prompt` / `Agent.run`（ReAct + `step_limit` + `finished`）/ `execute_tool_calls`（并行调用，**malformed JSON 与未知工具转成可恢复 observation 而非抛异常**）/ Skills / `compact_context` / ChessAgent |
| A2 Eval | 15% | 设计评估框架，含 LLM-as-judge |
| A3 Training | 15% | SFT + RL 训练流程 |
| 团队研究项目 | 50% | proposal → check-in → poster → final report |
| Lecture highlights | 10% | 22 次机会取最好 20 次，**禁止用 AI**、24h 内交 |

**A1 的工程细节（可直接照搬的清单）**

- **Skills = 渐进披露**：每个目录一个 `SKILL.md`，解析 YAML frontmatter；system prompt 只暴露 `name` + `description`，完整内容靠 `invoke_skill` 按需加载。
- **上下文压缩**：`compact_context` 让模型生成 working memory 摘要旧 prefix，**保留 system / task 与最新一轮 tool step 原文**，触发阈值约 **6,000 token**；作业要求在真实 SWE-bench 实例上报告压缩前后 token 对比。
- **观测 A/B**：ChessAgent 的 `play_move` / `simulate_move` / `run_python`，对比 `board only` vs `board + legal moves` —— **按实验与证据评分，不按是否赢棋评分**。
- **默认模型**：`deepseek/deepseek-v4-flash-0731`（OpenAI 兼容端点）——呼应本库 `Model + Harness = Agent` 的说法，模型与 harness 协同演进。
- 起步仓库是 `uv` 项目 + Makefile + 内置 chess web app + 100 分 rubric；**私有测试与 reference patch 不公开**，跑通需自付 Modal / API 费用。

**讲座里与本库直接对应的三块**

- 能力面：Tool Use → Context Management（长上下文）→ Skills and Memory → Planning / 任务分解 / 多 Agent 协作
- 训练面：SFT → RL Basics → Advanced RL → **RL Systems（SkyRL、Miles）**
- 安全与框架：**Sandboxing and Credential Management**（Lecture 13）｜ Observability and Monitoring（Lecture 16）｜ OpenHands（14）｜ LangGraph（15）

**公开材料**：Neubig YouTube 频道分批上传（**滞后约 1–2 周**）；截至 2026-09-08 公开 **Lecture 1–4 视频（合计约 4h36m）+ Lecture 1–6 slides**；B 站有中英字幕搬运。注册学生另有 Piazza / Canvas、赞助算力、A2/A3 仓库与私有测试。

**读完往本库写哪儿**：[agent/harness/](./agent/harness/)（A1 的实现笔记）｜ [reliability/sandbox/](./reliability/sandbox/)（Lecture 13 + Modal）｜ [reliability/eval/](./reliability/eval/)（A2）｜ [agent/agent-skills/](./agent/agent-skills/)（SKILL.md 渐进披露）

---

## 2. P1 · [Stanford CS329Z Engineering AI Agents](https://cs329z.stanford.edu/) (Fall 2026)

| 项目 | 内容 |
|---|---|
| 课程号 / 学期 | CS329Z · **Fall 2026**（校方 Session 写作 `2026-2027 Autumn 1`；Class #27855，3 学分），周一 / 周三 13:30–14:50，Packard 101；**2026-09-23 首讲 ~ 12-11 期末 Demo Day（截至 09-12 未开课）** |
| 历史轮次 | **Fall 2026 首开**（Stanford「CS329 专题课号」本轮新用 Z 号；官网无 archive、材料尚未发布）→ **无往届录像 / 讲义**，提前准备只能读 reading list。对照：**CS329A（2025 秋 Self-Improving AI Agents）是同系列的另一专题**，不是它的上一轮 |
| 授课 | Diyi Yang、Michael Ryan、John Yang |
| 先修 | CS224N / CS224U / CS224V / CS336 或同等 NLP 背景 |
| 主题 | 从单体大模型 → **复合 AI 系统（compound AI systems）**：LLM + 检索器 + 工具 + 优化器 |
| 路径 | **先从零实现核心组件**（RAG、工具调用、agent loop），再学 DSPy 等框架如何抽象这些模式 |

**两份作业 = 与 P0 同构，但评测更系统**

| 作业 | 占比 | 内容 |
|---|---|---|
| HW1 Build an Agentic Harness | 10%（W3–6） | **禁用任何 agent 框架**，只用 chat-completion API 与自写代码：先做能检索真实企业邮件档案的 LLM pipeline，再扩成带工具、终端、记忆、human-in-the-loop 的完整 harness |
| HW2 Evaluate an Agent | 10%（W6–9） | 给定现成 agent，设计完整评测套件：**code grader + 至少一个 LLM-as-judge**，按 **4-tuple 框架**构建基准任务，并做错误分析 |
| HW quiz | 15% | 个人闭卷，口述设计决策与取舍 |

**必须记下来的：4-tuple 评测框架**

```
(request, environment, stopping criteria, scorer)
```

「任务请求 / 运行环境 / 终止条件 / 评分器」——**这就是回测验证系统的四要素**：一条回测 = 一个 request，行情与撮合规则 = environment，资金曲线或止损触发 = stopping criteria，收益/回撤/夏普 = scorer。把 HW2 当作「给回测系统设计评测套件」的模板用。

**关键讲次**：LLMs for Builders（结构化 I/O、上下文工程、成本延迟权衡）→ RAG → **Tool Use & Function Calling（REPL、MCP、沙箱、错误重试）** → Frameworks & Orchestration（DSPy / LangChain / LangGraph / LlamaIndex）→ Agent Design Patterns（ReAct、plan-and-execute、reflection）→ Memory & Multi-Agent → Optimization（GEPA / MIPROv2 / OPRO / TextGrad、test-time compute、LoRA、蒸馏、RLHF/DPO）→ Data for Agentic Systems（traces、数据飞轮、合成数据）→ Data Selection & Quality → Evaluation Fundamentals & Benchmark Design → LLM-as-Judge（三类 grader、偏差、**pass@k vs pass^k**）→ Safety & Guardrails → Coding Agents（SWE-agent、Claude Code、OpenHands、SWE-bench）→ Proactive Agents。

**公开材料**：**讲座录像不公开**（仅注册学生可看 Canvas）；但课表内 reading list 全为 arXiv / Anthropic Engineering Blog / BAIR / OpenReview 等**公开可访问**资源（Compound AI Systems、ReAct、DSPy、SWE-agent、MemGPT、MCP 规范等）→ **自学主打 reading list + 两份作业的公开描述**。

**读完往本库写哪儿**：[reliability/eval/](./reliability/eval/)（HW2 + 4-tuple + pass@k/pass^k）｜ [reliability/sandbox/](./reliability/sandbox/)（工具沙箱与错误重试）｜ [agent/mcp/](./agent/mcp/) ｜ [agent/langgraph/](./agent/langgraph/)（Orchestration 对比）

---

## 3. P2 · [Stanford CS329A Self-Improving AI Agents](https://cs329a.stanford.edu/) (Autumn 2025)

| 项目 | 内容 |
|---|---|
| 课程号 / 学期 | CS329A · **Autumn 2025**（2025-09-22 ~ 12-12，**已结课**）；下一轮 **2026-27 Spring**（2027-03-29 ~ 06-02）已排课，周二 / 周四 18:30–19:50 |
| 授课 | Aakanksha Chowdhery、Azalia Mirhoseini |
| 形式 | **研讨课**：读最新论文 + 课堂讨论 + 原创研究项目（3 次作业共 50%，项目 50%）；**不允许旁听** |
| 门槛 | 需要先能判断「这个 agent 为什么失败」——所以排在 harness / eval 之后 |

**内容主线**（= 自我改进的技术栈）

| 板块 | 讲次要点 |
|---|---|
| 自我改进基础 | Test-time Compute Scaling ｜ Robust Verification ｜ Learning from Feedback with Tools / Code |
| 推理与规划 | Multi-step Reasoning / Planning ｜ 记忆增强（Memory Augmentation） |
| 训练侧扩展 | Train-Time Scaling / Scaling RL ｜ Open-Ended Evolution of Self-Improving Agents |
| 搜索与研究型 agent | Self-Improvement with Search ｜ Deep Research Agents |
| 软件工程 agent | Agentic Frameworks for Software Engineering |
| 评测 | **Agentic Evaluations & Long-Horizon Tasks**（长时程任务评测） |
| 客座 | Google DeepMind（post-training 演化、LLM Reasoning、AlphaProof / AlphaGeometry / Gemini IMO 金牌）、Reflection AI、Physical Intelligence（机器人多模态） |

**公开材料**：官网**无视频、无讲义下载**，只有每周论文清单（附 arXiv 链接）。可复用的产出 = **它的 reading list + 客座讲题**。

**读完往本库写哪儿**：[foundation/reasoning/](./foundation/reasoning/)（test-time compute、训练时扩展）｜ [reliability/eval/](./reliability/eval/)（长时程评测）｜ [agent/loop-engineering.md](./agent/loop-engineering.md)（反思 / 验证器闭环）

---

## 4. P3 · 拓展（两门）

### 4.1 [Stanford CS146S The Modern Software Developer](https://themodernsoftware.dev/)

| 项目 | 内容 |
|---|---|
| 学期 | **2025-26 Autumn 首开（2025-09-22 ~ 12-05，已结课）**；**新一轮 2026-27 Autumn 已排课**：2026-09-22 ~ 12-04，周二 / 周四 17:30–18:20，370-370（Class #6380，Waitlist 3）→ 上一轮的官网材料可能被新学期覆盖 |
| 授课 | Mihail Eric；每周讲座 + 动手编码 + 业界嘉宾；期末项目展示现代开发实践 |
| 先修 | CS111 / CS161 同等编程经验（推荐 CS221 / 229） |
| 关键词 | **MCP** · **Agent Skills** · **Spec-driven development（规格驱动开发）** · **Loop engineering（循环工程）** · **The software factory（软件工厂）** |
| 学习目标 | 给 agent 正确上下文与能力；把产品需求转成可执行规格；设计人机共同「规划—构建—评估—改进」的迭代工作流 |
| 公开材料 | 官网未提视频 / 讲义；列出开源合作方（Browserbase、HeyGen、CopilotKit、Semgrep、OpenHands、Milvus、Marimo、pi.dev、CrewAI、Warp、Vercel、Arize Phoenix、Unsloth、Anyscale） |

**重叠度提示（为什么排 P3）**：MCP、Agent Skills、Loop engineering、软件工厂，本库都已有对应笔记（[agent/mcp/](./agent/mcp/)、[agent/agent-skills/](./agent/agent-skills/)、[agent/loop-engineering.md](./agent/loop-engineering.md)）。它是**流程与协作视角**，不提供 harness 实现 —— **只补差距，不重读**。

### 4.2 [MIT MAS.S60 How to AI (Almost) Anything](https://mit-mi.github.io/how2ai-course/spring2025/)

| 项目 | 内容 |
|---|---|
| 学期 | **Spring 2025（已结课）**；MIT OCW + 课程主页 **全公开**（12 讲，含中英字幕搬运） |
| 主题 | 跨模态 / 多模态：从语言到图像、音频、3D、机器人；人机共生（human-AI symbiosis） |
| 与本库对应 | [foundation/multimodal/](./foundation/multimodal/)、[foundation/generative/](./foundation/generative/) |
| 排序理由 | 与 Harness / 沙盒 / 回测**无直接接口**，属能力面扩展；材料最全、最易补，但优先级最低 |

---

## 5. 课程 → 本库模块映射（一张总表）

| 课程 | 直接对应本库模块 | 能补的具体缺口 |
|---|---|---|
| CMU 11-768 | [agent/harness/](./agent/harness/) · [reliability/sandbox/](./reliability/sandbox/) · [reliability/eval/](./reliability/eval/) · [agent/agent-skills/](./agent/agent-skills/) | harness 的分模块实现（prompt / loop / 并行工具 / 压缩）、Skill 渐进披露、上下文压缩阈值实测 |
| CS329Z | [reliability/eval/](./reliability/eval/) · [agent/langgraph/](./agent/langgraph/) · [agent/mcp/](./agent/mcp/) | **4-tuple 评测框架**、pass@k vs pass^k、三类 grader 与偏差、DSPy 系 prompt 优化 |
| CS329A | [foundation/reasoning/](./foundation/reasoning/) · [agent/loop-engineering.md](./agent/loop-engineering.md) | test-time compute / 训练时扩展的论文脉络、长时程任务评测 |
| CS146S | [agent/loop-engineering.md](./agent/loop-engineering.md) · [agent/agent-skills/](./agent/agent-skills/) | spec-driven development、软件工厂的流程与角色分工 |
| MIT MAS.S60 | [foundation/multimodal/](./foundation/multimodal/) · [foundation/generative/](./foundation/generative/) | 跨模态生成的完整讲次顺序 |

---

## 6. 与手上项目（代码沙盒 + 回测验证）的接口

| 手上的模块 | 直接对标 | 拿来即用的东西 |
|---|---|---|
| **代码沙盒** | 11-768 Lecture 13 Sandboxing & Credential Management + A1 的 Modal sandbox；CS329Z Tool Use（沙箱、错误重试） | 工具调用必须在沙箱内执行、凭据不进模型上下文；未知工具 / 坏 JSON 一律降级为**可恢复 observation** |
| **Agent 外壳** | 11-768 A1 + CS329Z HW1（都要求**不用框架从零实现**） | 两份作业都是本库 [agent/harness/](./agent/harness/) 的实践版；先写自己的，再对照 LangGraph |
| **回测验证系统** | CS329Z HW2 的 **4-tuple** + 11-768 A2 Eval | `(request, environment, stopping criteria, scorer)` 直接映射「策略任务 / 行情与撮合 / 终止条件 / 绩效指标」；LLM-as-judge 只用于**解释性维度**，数值指标仍用 code grader |
| **可重复性要求** | 本库 [reliability/eval/](./reliability/eval/) | 回测比 agent eval 门槛更硬：**固定 seed、固定数据快照、隔离环境**；agent eval 里的 `pass^k` 思想可借用（同一策略多次运行的稳定性） |

**一句话**：P0 解决「harness 怎么写」，P1 解决「评测怎么设计」，两者合起来正是把**量化数据 + 回测工具**封装成 Agent 技能所需的地基；P2 要等这套地基跑通再读，否则只是看论文。

---

## 7. 公开课材料获取入口（可直接点）

> **官网 ≠ 材料页。** 下表把「官网 / 讲义直链 / 录播 / 作业仓库 / 中文字幕搬运」分开列，并标公开度。
> 公开度四级：**① 全公开免登录**（讲义 PDF、MIT 全部）｜ **② 需注册**（Piazza / Canvas 内的录像与私有测试）｜ **③ 只有 reading**（讲座不公开，但论文清单公开）｜ **④ 官方作业仓库公开**（可拿来当 starter）。
> 下列链接**均在 2026-09-12 实测可达**（讲义 PDF 与 404 结论为实际请求结果）；标 ⚠️ 的是**第三方转述、未逐条验证**的项。

### 7.1 CMU 11-768 AI Agents

| 材料 | 链接 | 公开度 |
|---|---|---|
| 课程官网（时间 / 地点 / 教师 / 入口汇总） | https://www.cmu-agents.com/ | ① |
| **讲义 PDF 直链**（模式 `/slides/lecture-0N-<slug>.pdf`） | [L1 agents](https://www.cmu-agents.com/slides/lecture-01-agents.pdf)（实测可下）｜ [L5 planning](https://www.cmu-agents.com/slides/lecture-05-planning.pdf)（实测可下，约 18 MB）<br>其余按同一模式拼：`lecture-02-tool-use.pdf`、`lecture-03-long-context.pdf`、`lecture-04-memory-and-skills.pdf`、`lecture-06-coding-agents.pdf` | ① 无需登录 |
| **录播（YouTube 单集，截至 9-08 仅 L1–L4）** | L1 `https://www.youtube.com/watch?v=UwfjzyLnvMg` ｜ L2 `...?v=jXChFB4JSyw` ｜ L3 `...?v=AiwCCvFW1uE` ｜ L4 `...?v=6zigF2a-2Pw` | ① 滞后 1–2 周 |
| 播放列表 ⚠️ | https://www.youtube.com/playlist?list=PLSN0qpDfUvTM —— 该 ID 为第三方转述且**长度异常（疑似被截断）**，打不开就以单集链接或 Neubig 频道为准 | ① |
| **中文字幕搬运（B 站）** | 全课合集（4 条，对应 L1–L4）https://www.bilibili.com/video/BV1ynYt6MEcb/ ｜ 单讲双语 + 资料 https://www.bilibili.com/video/BV1oGYm6LELX/ | 第三方转载 |
| **作业 1 起步代码（官方）** | https://github.com/cmu-agents/assignment-1（公开：README / 说明 / 100 分 rubric；**私有测试与 reference patch 不公开**）｜ 配套应用 https://github.com/cmu-agents/chess-app | ④ 部分 |
| 第三方复盘仓库 ⚠️ | https://github.com/daniellaah/cmu-11-768-ai-agents（含 `assignments/03-training`） | 第三方 |
| 注册后才有的 | Piazza https://piazza.com/cmu/fall2026/11768/home ｜ Canvas https://canvas.cmu.edu/courses/55126 | ② |
| 讲师主页 | Graham Neubig https://www.phontron.com/ ｜ Daniel Fried https://dpfried.github.io/ | ① |
| 逐讲拆解（第三方，含各讲材料公开状态） | https://www.heyuan110.com/posts/ai/2026-09-08-cmu-11-768-ai-agents-course/ | 第三方 |

### 7.2 Stanford CS329Z Engineering AI Agents

| 材料 | 链接 | 公开度 |
|---|---|---|
| 课程官网 —— **单页站，日程 + 作业权重 + 全部 reading 都在这页** | https://cs329z.stanford.edu/ | ① |
| ⚠️ 无独立日程页（实测结论） | `https://cs329z.stanford.edu/schedule` 与 `/sitemap.xml` **均返回 404**（GitHub Pages），别再试；日程就在首页 | — |
| Stanford Online 课程页 | https://online.stanford.edu/courses/cs329z-engineering-ai-agents | ① |
| Bulletin 官方课程描述 | https://bulletin.stanford.edu/courses/2283761 | ① |
| 讲座录像 | **不公开**（仅注册学生，Canvas 内；官网原文：教室后方摄像头只录教师讲授部分，需登录 Canvas 访问） | ② |
| 课表核验（Stanford ExploreCourses） | 2026-27 学年 CS329Z：[catalog 查询](https://explorecourses.stanford.edu/search?q=CS329Z&view=catalog&academicYear=20262027)（Session 显示 `2026-2027 Autumn 1`，起止 9/23–12/11） | ① |

### 7.3 Stanford CS329A Self-Improving AI Agents

| 材料 | 链接 | 公开度 |
|---|---|---|
| 课程官网 —— **单页站，全部 reading 的 arXiv 直链就挂在日程里**（Test-time Compute / Robust Verification / ReAct / STaR / DAPO / AlphaEvolve / MemGPT / 长时程评测等） | https://cs329a.stanford.edu/ | ③（材料只有论文） |
| 讲师主页 | https://www.achowdhery.com/ ｜ http://azaliamirhoseini.com/ | ① |
| 视频 / 讲义 | **无**，官网未提供；也不允许旁听 | — |
| 课表核验（Stanford ExploreCourses） | 2026-27 学年 CS329A：[catalog 查询](https://explorecourses.stanford.edu/search?q=CS329A&view=catalog&academicYear=20262027)（已排 **Spring 2027**：2027-03-29 ~ 06-02，Chowdhery + Mirhoseini 继续教） | ① |

### 7.4 Stanford CS146S The Modern Software Developer

| 材料 | 链接 | 公开度 |
|---|---|---|
| 课程官网 | https://themodernsoftware.dev/ | ① |
| **作业仓库（官方）** | https://github.com/mihail911/modern-software-dev-assignments | ④ |
| 中文版作业 ⚠️ | https://github.com/ShouZhengAI/CS146S_CN ｜ https://github.com/CaptainRhett/CS146S-CN | 第三方 |
| 他人解答参考 ⚠️ | https://github.com/baoziwu2/CS146S ｜ https://github.com/WeizhengLiang/Stanford-CS146S-Assignments | 第三方 |
| Bulletin 官方课程描述 | https://bulletin.stanford.edu/courses/2274401 | ① |
| 课表核验（Stanford ExploreCourses） | 上一轮 2025-26 Autumn：[catalog 查询](https://explorecourses.stanford.edu/search?q=CS146S&view=catalog&academicYear=20252026)（2025-09-22 ~ 12-05，Class #28883）｜ 新一轮 2026-27 Autumn：[catalog 查询](https://explorecourses.stanford.edu/search?q=CS146S&view=catalog&academicYear=20262027)（**2026-09-22 ~ 12-04，Class #6380**） | ① |

### 7.5 MIT MAS.S60 How to AI (Almost) Anything

| 材料 | 链接 | 公开度 |
|---|---|---|
| OCW 课程页（12 讲，含讲义与视频） | https://ocw.mit.edu/courses/mas-s60-how-to-ai-almost-anything-spring-2025/ | ① |
| OCW 整课打包下载页 | https://ocw.mit.edu/courses/mas-s60-how-to-ai-almost-anything-spring-2025/download/ | ① |
| 课程主页 | https://mit-mi.github.io/how2ai-course/spring2025/ | ① |
| **日程页 —— 讲义 PDF + YouTube 录播链接都在这里** | https://mit-mi.github.io/how2ai-course/spring2025/schedule/ | ① |
| 讲义直链模式 | `.../spring2025/schedule/lec1%20-%20introduction.pdf` 这种形式，**文件名含空格，空格必须写成 `%20`**，否则 404 | ① |
| 中文字幕搬运（B 站，12 条） | https://www.bilibili.com/video/BV1nG8G6mExC/ | 第三方转载 |

### 7.6 材料找不到时怎么自己挖（复用方法）

| 手段 | 要点 |
|---|---|
| `site:` 语法反查真实路径 | 例：搜 `site:cmu-agents.com slides`，比猜 `/schedule`、`/lectures` 有效得多 |
| ⚠️ **识别 SPA 站点** | `cmu-agents.com` 是 **React 单页应用**，课表渲染在 JS bundle 里 —— 所以 `/schedule`、`/lectures`、`/sitemap.xml`、`/robots.txt` **全部 404（已实测）**，不必再试；静态资源（`/slides/*.pdf`）才是直链，**可自己拼路径** |
| 先探 `sitemap.xml` / `robots.txt` | 两者都 404 → 基本可判定为**单页站**，日程就在首页（CS329Z / CS329A 即此类） |
| 从讲师个人主页找 | `phontron.com` 这类个人站常放讲义与播放列表入口 |
| 中文搬运检索 | B 站搜「课程号 + 中英字幕」；搬运**滞后且可能截断**（本次 11-768 只搬了 4 讲） |
| 三处交叉核对 | 官网（有多少材料）→ 讲师社媒 / 个人主页（发布公告）→ 第三方复盘文（常给直链，但**必须自己点一遍**，本次靠此才挖到 `/slides/lecture-0N-*.pdf` 这个模式） |

---

## 8. 候选池：还没收录、但值得学的 AI 课程

> **位次 / 学期 / 状态见 §0（C1–C3 行），本节只补 §0 不写的三样** —— **公开度 / 本库接口 / 官网入口**（2026-09-12 快照；**⭕ = 当季**，材料随周更新）。
> 筛选口径 = **能否反哺手上的「agent harness + 代码沙盒 + 回测/评测 + 本地推理」**；纯入门课（CS229 / 6.S191）与偏视觉课（CS231n）不进池。

### 8.1 第一梯队 · 直接反哺手上的四条线

| 课程 | 公开度 | 本库接口 | 备注 / 坑 |
|---|---|---|---|
| **[CMU 10-414/714 Deep Learning Systems](https://dlsyscourse.org/)** ⭕ | 2022 版全套录像 YouTube 公开；当季录像走课程站、讲义每讲前发，**当季是否对公众开放未说明** | `agent/harness/`（工具执行底座）· `runtime/local-inference/`（算子与后端） | — |
| **[Harvard CS249r · MLSysBook（Machine Learning Systems）](https://mlsysbook.ai/)** | **全免费开源**（MIT Press 2026）：教材 HTML / PDF / EPUB + 仓库 `harvard-edge/cs249r_book` | `runtime/local-inference/benchmark.md`（正面对偶）· `reliability/eval/` | Iron Law 原文：`T = D/BW + O/(R·η) + L`；MLSys·im CLI 例 `mlsysim eval Llama3_70B H100 --batch-size 1`（区分 mem-bound / compute-bound）；另含 Marimo Labs |
| **[Berkeley LLM Agents MOOC](https://llmagents-learning.org/)**（f24 + S25） | **视频 + slides + quiz 全部保留公开**：f24 `rdi.berkeley.edu/llm-agents/f24` · S25 `llmagents-learning.org` | `foundation/reasoning/` · `reliability/eval/` | f24 课号 = CS294/194-196《Large Language Model Agents》；主题≈CS329A（推理时技术 / 后训练 / 搜索规划 / agentic workflow / 代码生成与验证 / 数学与定理证明 / agent 安全） |
| **[MIT 6.5940 TinyML and Efficient AI Computing](https://efficientml.ai/)** ⭕ | **目前只公开 L1**（视频 + 讲义），L2–L25 是占位符会逐讲放；直播入口 `live.efficientml.ai` | `runtime/local-inference/` · `runtime/speculative-decoding/` | 主题谱系：量化 / 剪枝稀疏 / NAS / 蒸馏 / MCUNet / TinyEngine → LLM 量化部署 / 后训练 / 长上下文 / ViT / diffusion → 分布式与端上训练；授课 **Han Song**（这条路线的源头） |

### 8.2 第二梯队 · 补原理与实现，但要留整块时间

| 课程 | 公开度 | 本库接口 | 备注 / 坑 |
|---|---|---|---|
| **[Stanford CS336 Language Modeling from Scratch](https://cs336.stanford.edu/)** | **YouTube 全套 + 19 讲讲义 + 5 个作业仓库全公开** | `foundation/transformer/`（与本库原理层同构，但它是真跑一遍） | ⚠️ **荣誉守则**：可问 LLM 低层编程 / 高层概念，**禁止用 AI 直接解题**、建议关掉 Cursor Tab；云 GPU 见官网（Modal / Lambda / RunPod 报价） |
| **[Stanford CS224N](https://web.stanford.edu/class/cs224n/)** | 2026 录像**只在 Canvas**；**公开的是 Spring 2024 全套 YouTube**；slides 与 4 个作业 zip 公开 | `reliability/eval/`（当「评测视角的一课」用，别从头刷） | 授课 **Diyi Yang + Yejin Choi** |
| **[Berkeley CS285 Deep RL](http://rail.eecs.berkeley.edu/deeprlcourse/)** | **视频只有 Fall 2023**；**25 讲讲义 PDF + HW1–5 + 期末项目说明全公开** | `foundation/reasoning/`（补 RL 骨架；CS336 A5 只算练手，这门是系统学） | 授课 **Sergey Levine** |

### 8.3 第三梯队 · 成本低、见效快（动手 / 讲座 / 别踩的坑）

> 三门都免费公开、无截止限制，因此本表**不设公开度列**（§0 已列），只记**本库接口**与**上手节奏 / 坑**。

| 对象 | 本库接口 | 节奏 / 坑 |
|---|---|---|
| **[Hugging Face AI Agents Course](https://huggingface.co/learn/agents-course)** | `agent/langgraph/` · `agent/agent-skills/`（把理论落成能跑的 agent）· `reliability/eval/`（对应 Bonus Unit 2 = Observability and Evaluation） | 官方建议每章 1 周、每周 3–4 小时 |
| **[Stanford CS25 Transformers United V6](https://web.stanford.edu/class/cs25/)** | `ai/` 全库扫面用（无单一模块，用来挑专题） | — |
| **[Karpathy《Neural Networks: Zero to Hero》](https://karpathy.ai/zero-to-hero.html)** | `foundation/transformer/`（建「从零」手感） | ⚠️ `LLM101n` 至今未发布（他 2026-05 已加入 Anthropic 做预训练研究）—— **别等** |

> ⚠️ **DeepLearning.AI / Anthropic 官方短课**（MCP、agent 评测、prompt caching 之类 1–3 小时专题）本轮**未逐条核实课程名与时效**，也没有画得出的入口链接 —— **不计入候选池 10 门**，要用时自行核一遍。

### 8.4 怎么排（与已收录 5 门的关系）

1. **当季能跟直播**：CMU 11-768（P0，进行中）+ MIT 6.5940（从 L1 开始）——两门材料都随周更新。
2. **低成本先补**：MLSysBook（免费，给 `runtime/local-inference/benchmark.md` 补理论层）→ 10-414（先刷 2022 录像，再决定做不做 HW）→ Berkeley LLM Agents MOOC（CS329A 的**有声版**，按主题挑讲）。
3. **大投入 / 明确不排**：CS336 最硬；CS224N、CS285 只挑增量（A4 评测 / HW4 LLM RL）；CS231n、CS229、6.S191 不排（与 harness / 沙盒 / 回测链路重叠少）。

---

## 数据来源（核实日期 2026-09-12）

| 对象 | 来源 |
|---|---|
| CMU 11-768 | https://www.cmu-agents.com/ （官方，含时间 / 教师，无日程）｜ 讲义直链、YouTube 单集、作业仓库、公开度状态来自第三方逐讲分析（2026-09-08）｜ 官网 404 结论（`/schedule`、`/lectures`、`/sitemap.xml`、`/robots.txt`）与两份讲义 PDF 为本轮**实测**结果 |
| CS329Z | https://cs329z.stanford.edu/ （官方 schedule / 作业权重 / 公开性）｜ https://online.stanford.edu/courses/cs329z-engineering-ai-agents ｜ https://bulletin.stanford.edu/courses/2283761 ｜ 无 `/schedule` 子页为**实测**结果 |
| CS329A | https://cs329a.stanford.edu/ （官方 schedule / 评分 / 旁听政策 / 全部 reading 直链）｜ 讲师主页 https://www.achowdhery.com/ |
| CS146S | https://themodernsoftware.dev/ ｜ 官方作业仓库 https://github.com/mihail911/modern-software-dev-assignments ｜ https://bulletin.stanford.edu/courses/2274401 |
| MIT MAS.S60 | https://ocw.mit.edu/courses/mas-s60-how-to-ai-almost-anything-spring-2025/ ｜ 课程主页 https://mit-mi.github.io/how2ai-course/spring2025/ ｜ **日程页（讲义 PDF + 录播）** https://mit-mi.github.io/how2ai-course/spring2025/schedule/ |
| 课程状态（已结课 / 进行中 / 未开课） | 斯坦福三门的学期与起止用 **ExploreCourses** 核验：https://explorecourses.stanford.edu/ （参数形式 `search?q=CSxxx&view=catalog&academicYear=20252026`，学年可换 `20262027`）｜ Bulletin https://bulletin.stanford.edu/ ｜ 11-768 用官网 https://www.cmu-agents.com/ ｜ 均为本轮**实测**查询 |
| 候选池（§8） | 10 门课的**官网入口已挂在 §8 表的课程名上**（链接只在 §8 一处维护）｜ 除 DeepLearning.AI / Anthropic 短课（§8.3 末注，未核实）外，均为 2026-09-12 **实测**抓取 |

> 版本提醒：**课程号、学期、公开材料批次都会变**。引用本页结论时带上「2026-09 快照」；重看前先回官网核一遍公开进度（尤其 11-768 的视频上传）。
> 材料链接的可用性同理：**SPA 站点的静态直链（如 `/slides/*.pdf`）通常稳定，但课程改版后路径会变**；标 ⚠️ 的第三方链接只作入口参考。
