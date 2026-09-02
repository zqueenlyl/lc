# Eval · 评测与可观测

> 用 **你们自己的任务集 + 线上 trace** 衡量系统，而不是只报 MMLU。2026 年 Agent 栈把 eval 和 OpenTelemetry 级 tracing 当成独立一层。

配套 MVP：[mvp.py](./mvp.py)（用例集 + 规则裁判 + 按 P0/P1 汇总）。

---

## 一、技术讲解

公开榜单测的是模型通识，不是你的退款 SOP、也不是工具是否被乱调。生产 eval 有三块：

| 块 | 问题 | 手段 |
|---|---|---|
| **离线集** | 改 prompt / 换模型会不会回退 | 金标问答、工具轨迹、安全红队 |
| **裁判** | 没有唯一答案时怎么打分 | 规则 / 程序校验 / LLM-as-judge（需抽检） |
| **线上 trace** | 真实用户路径哪里挂 | span：LLM、MCP、A2A、护栏、检索 |

Agent 要比聊天多记：选了哪个工具、参数、重试次数、是否违反 skill。MCP 适合 per-tool 审计；A2A 适合 per-hop TaskCompletion。Realtime 要在流中途抽检，不能等整段结束。

好的用例是 **可执行的断言**，不是「回答要有帮助」这种散文。

---

## 二、功能作用

- **改动有闸门**：合并前跑回归，像单测。
- **选型有数**：模型 A/B、路由策略用同一套集。
- **事故可复盘**：trace id 串起模型输入、工具、护栏决策。
- **防评测作弊**：定期换隐藏集、防 prompt 过拟合公开题。

---

## 三、应用场景

| 场景 | 指标例子 |
|---|---|
| RAG | 引用是否在检索块内、答对率、空检索拒答率 |
| Agent | 任务完成率、多余工具调用、平均步数 |
| 护栏 | 攻击漏拦率、良性误拦率 |
| 路由 | 分流后质量不掉点的比例、成本 |
| Computer Use | 路径完成、非法域点击 |
| 结构化抽取 | 字段级 F1 |

---

## 四、用例怎么写

```
id: refund-missing-order
priority: P0
input: "帮我退款"
context: {}
expect:
  skill: refund
  status: blocked
  ask_contains: 缺字段
```

P0 不过不能发版；P1 允许已知失败但要记账。和本仓库 [agent-skills](../agent-skills/) MVP 的契约可以一一对应。

---

## 五、与相邻技术

| 技术 | 关系 |
|---|---|
| [Guardrails](../guardrails/) | 护栏决策应成为 span，进入同一条 trace |
| [Model Routing](../model-routing/) | 路由策略用 eval 证明「省钱且不掉点」 |
| [Reasoning](../reasoning/) | 报告准确率时必须带 thinking 预算 |
| LangSmith / Langfuse / Braintrust | 常见产品化实现 |
| 单测 | 确定性逻辑用单测；生成用 eval 集 |

---

## 六、落地建议

1. 先做 **20 条 P0 黄金路径**，再谈平台。
2. 能程序断言的不要上 LLM judge（数学、schema、是否调用某工具）。
3. Judge 要抽 5–10% 人工校准，否则分数会漂。
4. 线上采样 + 离线回放，两边同一 schema。
5. 失败用例自动入库，形成回归飞轮。

---

## 七、延伸阅读

- OpenTelemetry GenAI semantic conventions
- 各厂商 eval 指南；Agent 轨迹评测论文 / 产品
- 对比：[guardrails](../guardrails/)、[agent-skills](../agent-skills/)

---

## 八、本目录 MVP

`mvp.py` 对一个迷你 Agent（退款技能）跑 4 条用例，统计 P0/P1 通过率，失败打印期望 vs 实际。
