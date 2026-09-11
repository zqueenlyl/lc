# SLM · 小语言模型与端侧

> 参数从十亿到十亿级以内（以及强量化后的稍大模型），跑在手机、PC、网关或便宜云批次上。一句话：**不是所有请求都配得上前沿大模型。**

代表：Llama / Qwen / Gemma 小尺寸、Phi、Gemini Flash / GPT nano 一类快模型、端侧 NPU（Apple / Qualcomm / Pixel）上的本地生成。

配套 MVP：[mvp.py](./mvp.py)（规则化的「大小模型分流」+ 端侧离线兜底）。

---

## 一、技术讲解

2023 年叙事是「越大越好」。2026 年默认架构是 **舰队**：

- **前沿大模型**：难推理、开放对话、高风险决策；
- **SLM**：分类、抽取、改写、路由、工具参数填充、离线草稿；
- **特化小模型**：rerank、embedding、ASR、安全分类。

SLM 变强的来源：更好的数据与蒸馏（尤其从 [推理模型](../reasoning/) 蒸思维）、量化（4/8-bit）、端侧 NPU、以及「任务足够窄」。

端侧还多三个约束：**内存、电量、隐私**。权重量化 + KV 量化 + 短上下文是常规；[MoE](../moe/) 端侧要专家卸载，仍偏研究/高端机。

---

## 二、功能作用

- **成本**：简单请求便宜一个数量级。
- **延迟**：本地或小云模型，适合输入补全、键盘、实时预分类。
- **隐私**：数据不出设备（企业办公、医疗初筛、个人助手）。
- **可用**：断网仍能草稿、分类、模板填充。
- **给大模型减负**：SLM 做 [routing](../../reliability/model-routing/)、护栏初筛、工具选择。

---

## 三、应用场景

| 场景 | 为何 SLM 够用 |
|---|---|
| 意图分类 / 槽位填充 | 封闭标签集 |
| 日志脱敏、PII 打标 | 可蒸馏、可离线 |
| IDE 补全、commit message | 低延迟，错了人能改 |
| 边缘网关预决策 | 再决定上不上云 |
| 手机系统助手 | NPU + 隐私 |
| RAG 重写 query | 不必上最强模型 |

不够用：开放域复杂推理、长文档法律意见、高风险医疗结论（可 SLM 起草 + 大模型 / 人审）。

---

## 四、和「小而专」怎么做

1. **提示 + 约束解码** 往往先于微调。
2. 不够再 [LoRA](../peft-lora/) 一个领域。
3. 从教师模型蒸馏标签或 CoT，而不是从零堆数据。
4. 量化后必须回归 [Eval](../../reliability/eval/)，4-bit 可能把安全分类打穿。

---

## 五、与相邻技术

| 技术 | 关系 |
|---|---|
| [Model Routing](../../reliability/model-routing/) | SLM 是路由表里的默认廉价档 |
| [PEFT / LoRA](../peft-lora/) | 让 SLM 变领域专家 |
| [Reasoning](../reasoning/) | 蒸馏源；端侧很少开满 thinking |
| [Speculative Decoding](../../runtime/speculative-decoding/) | SLM 常当草稿模型 |
| [Guardrails](../../reliability/guardrails/) | 端侧先挡一层，上云再细审 |

---

## 六、落地建议

1. 列一张 **请求类型 → 模型档位** 表，用一周线上日志估节省。
2. 端侧先上「分类 / 补全」，再生「长文」。
3. 版本冻结：端侧模型更新要走应用商店 / MDM，不能当云 API 热更。
4. 失败上送策略写清楚：置信度低 / 用户点「问云端」。
5. 评测用设备档位矩阵（内存 4/8/16 GB），不要只在开发机上跑。

---

## 七、延伸阅读

- 各家 Flash / nano / mini 产品线；llama.cpp / MLX / ONNX Runtime
- 对比：[model-routing](../../reliability/model-routing/)、[peft-lora](../peft-lora/)、[speculative-decoding](../../runtime/speculative-decoding/)

---

## 八、本目录 MVP

`mvp.py` 三类请求（闲聊分类、槽位抽取、开放难题）分别走 tiny / small / frontier 模拟器，并演示断网时拒绝上送、只用本地 tiny。
