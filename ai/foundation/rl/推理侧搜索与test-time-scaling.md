# 推理侧搜索与 Test-time Scaling（横切主题 · 第三条缩放律）

> 定位：**横切主题**，不占环节编号。训练侧把「会想」写进权重（[环节 07](./环节07-GRPO与RLVR详解.md) / [环节 08](./环节08-AgenticRL与信用分配详解.md)）；本文讲**同一底座上，推理时多花算力换准确率**。两端合起来才是「推理模型」。
> 所属总揽：[环节00-总揽与环节导航.md](./环节00-总揽与环节导航.md)。目录入口见 [README.md](./README.md)。
> **不在本文**：GRPO / RLVR / R1 四阶段（→ 环节 07）；PRM 怎么引导 beam / MCTS（→ 环节 08 §6）；CoT / ReAct 当 prompt 剧本（→ [agent 环节 01](../../agent/环节01-决策与推理范式详解.md)）；Prefill / KV（→ [transformer 环节 10](../transformer/环节10-推理解码与KV缓存详解.md)）。
> 配套 MVP：[mvp-test-time-scaling.py](./mvp-test-time-scaling.py)（约束谜题上「预算 1 次失败、预算 5 次成功」，不调外部模型）。

代表产品形态：OpenAI o 系列、DeepSeek-R1 的显性 `<think>`、Claude extended thinking、各家 `reasoning_effort` / `think` 档。

---

## 0. 一句话定位

**预训练把模型做大，后训练把行为对齐，测试时算力让同一份权重「多想一会儿」。** 这是 2024–2026 的第三条缩放律。Chat 模型秒答；推理模型把串行思维链、并行采样、带验证的搜索花在难题上。

经验上准确率对「思考 token」近似对数增长——所以必须设预算，不能无限想。想太久还会过思考（绕远、改对为错）。

```
训练侧（环节 07/08）          推理侧（本文）
─────────────────          ─────────────────
蒸馏长 CoT / 纯 RL 涌现  →  权重里已经会「先想后说」
结果奖励 + 组相对优势    →  测试时再花 token / 搜索 / 校验
PRM 训练不划算           →  PRM 主场在推理时选路（环节 08 §6）
```

---

## 1. 三种测试时扩展

| 方式 | 做法 | 成本形态 | 何时更值 |
|---|---|---|---|
| **串行 CoT** | 一条越来越长的思考 | 延迟随长度线性增 | 步骤有依赖、需要自我纠正 |
| **并行采样** | n 条独立思路再投票 / 裁判 | 可横向扩 GPU | 答案可核对（数学、代码）；对应提示词版是 Self-Consistency |
| **带验证的搜索** | 生成 → 检查 → 失败则回溯 | 最稳，实现最重 | 有可执行 verifier（单测、数值、约束） |

和 [agent 环节 01](../../agent/环节01-决策与推理范式详解.md) 的差别：那边是**不改权重的外层剧本**；这里是**权重已经会想**之后，再把测试时算力花在哪条轴上。推理模型把「先想后说」训进权重，不只是加一句 “think step by step”。

MVP 走第三条的穷人版：先猜，可执行校验器判定，失败则在预算内换一条。

---

## 2. 思考是怎么进权重的（只讲故事）

1. **蒸馏 / SFT 思维轨迹**：用老师模型的长 CoT 教学生。小模型变强的便宜来源，见 [SLM](../slm/)、[PEFT / LoRA](../peft-lora/)。
2. **纯 RL 涌现**（R1-Zero）：不先喂人类思维链，结果奖励（题对了）+ GRPO 一类算法，模型自己长出反思、换解法、验算。算法与四阶段 → [环节 07](./环节07-GRPO与RLVR详解.md)。

产品上因此出现两档模型：普通 Chat（默认短答）vs 推理模型（默认或可开 thinking）。不是骨架不同，是后训练目标与推理策略不同。很多推理底座本身是 [MoE](../moe/)。

---

## 3. 产品旋钮与账单（指针，不记过期字段）

| 问题 | 去哪 |
|---|---|
| `reasoning_effort` / `think` / 隐藏 vs 可见 CoT、加密回传 | [providers/协议对比](../../model-cases/providers/模型服务API协议对比.md) |
| 思考 token 吃光 `max_tokens`、`content` 变空 | [local-inference](../../runtime/local-inference/)（Ollama / MLX / llama.cpp 均有实测） |
| 简单题走 Flash、难题才开 thinking | [model-routing](../../reliability/model-routing/) |
| 报告准确率必须带思考预算 | [eval](../../reliability/eval/) |
| 思考块落盘 / 敏感链 | [guardrails](../../reliability/guardrails/) |
| 通话中默认关 thinking | [voice-realtime](../../runtime/voice-realtime/) |

计费常识：思考 token 通常按**输出价**计；多轮若厂商要求回传 thinking item，漏传会丢推理连续性。

---

## 4. 何时开、何时关

| 适合 | 不适合 |
|---|---|
| 数学 / 逻辑 / 代码修复 | 寒暄、翻译、简单抽取 |
| 多步工具规划、排错 | 强实时语音 |
| 需要验算的财务 / 合规计算 | 只要流畅文案 |
| 作为 Agent 的 planner | 每条消息都开最大 thinking |

落地五条：

1. **默认关、按路由开**。
2. 设 `max_think_tokens` 与墙钟超时。
3. 可自动验证的题上 verifier，比盲目加长 CoT 更值。
4. 用户可见回复与思考分离；思考默认不进客服会话记录。
5. Agent 里「想一小段 → 调工具 → 再想」，不要先空想 2000 token。

---

## 5. 本目录 MVP

`python3 mvp-test-time-scaling.py`：猜满足「奇数、大于 20 小于 40、n≡3 (mod 7)」的整数。同一套校验器，`budget=1` 失败、`budget=5` 成功。展示 test-time compute ↔ 成功率。

训练侧最小演示仍是 [mvp.py](./mvp.py)（值迭代 → Q-learning → REINFORCE）。

---

## 6. 相关链接

- 训练侧：[环节 07 · GRPO 与 RLVR](./环节07-GRPO与RLVR详解.md) · [环节 08 · 推理时搜索](./环节08-AgenticRL与信用分配详解.md) §6
- 外层剧本：[agent 环节 01](../../agent/环节01-决策与推理范式详解.md)
- 解码成本：[transformer 环节 10](../transformer/环节10-推理解码与KV缓存详解.md)
- 课程缺口：Stanford CS329A 的 test-time compute 论文脉络 → 本文；训练时扩展 → 环节 07
