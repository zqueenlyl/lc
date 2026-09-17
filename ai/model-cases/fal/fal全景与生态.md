# fal 全景与生态

> 调研时间：2026-09-17 ｜ 范围：Hugging Face 组织 [`fal`](https://huggingface.co/fal)、公司 [fal.ai](https://fal.ai)
> **不是 MiniMax。** MiniMax 官方权重组织是 [`MiniMaxAI`](https://huggingface.co/MiniMaxAI)；H3 基座见 [minimax/](../minimax/MiniMax-H3全景与架构.md)。
> 本页只定身份与边界。挂在 H3 上的人像适配器单点深挖见 [《MiniMax-H3 Realism People LoRA》](./MiniMax-H3-Realism-People-LoRA.md)。

---

## 一、摘要（TL;DR）

1. **fal 是生成媒体推理平台，不是模型实验室。** 组织卡原文：跑开源图 / 视频 / 音频 / 3D，「尽快」。HF 上带 Inference Provider 徽章。
2. **它做三件事。** ① 托管别人的开源模型（H3 模型页右侧 Inference Providers 写 fal，权属仍是 MiniMax）；② 提供按 step 计费的 trainer（H3 有 t2v / i2v / flf2v / ref2va 四套）；③ 自己发 LoRA、FlashPack、以及少量自研权重（AuraFlow）。
3. **和 MiniMax 的关系是「平台 × 基座」。** 基座 `MiniMaxAI/MiniMax-H3`；适配器 `fal/MiniMax-H3-Realism-People-LoRA`。不要把 fal 写成 MiniMax 子品牌，也不要把 People LoRA 写成 H3 第四模块。

**核心判断**：选型时 fal 和 MiniMax 不在同一列——MiniMax 决定「模型会什么」，fal 决定「这份开源权重在谁的 GPU 上跑、LoRA 怎么训」。本目录目前只深挖一条：H3 人像写实 LoRA。

---

## 二、组织页快照（2026-09-17）

| 项 | 口径 |
|----|------|
| HF | [`huggingface.co/fal`](https://huggingface.co/fal)，Verified |
| 官网 | [fal.ai](https://fal.ai) · 文档 / Serverless GPU · [model gallery](https://fal.ai/models) |
| 自称 | generative media platform for developers |
| 规模量级 | 组织页约 89 个模型、3 个 dataset、4 个 Space；Inference Provider 月请求量级见组织页（会变） |
| 和本库相关的权重 | [`MiniMax-H3-Realism-People-LoRA`](https://huggingface.co/fal/MiniMax-H3-Realism-People-LoRA)（约 61k 月下载，快照时） |

组织页还能看到、**本目录不展开**的线：

| 线 | 例子 | 为什么不展开 |
|----|------|----------------|
| 自研文生图 | AuraFlow v0.x（自称当时最大开源 T2I 之一） | 与 H3 案例无关 |
| 风格 LoRA | Kontext Dev LoRAs（水彩 / 波普 / 铅笔 / 马赛克） | 图像侧，挂 FLUX Kontext |
| 格式转换 | Wan2.2 / Qwen-Image 等 FlashPack | 打包格式，不是新基座 |

H3 的 Turbo LoRA（`larryvrh`、`drbaph`、Comfy-Org）收在 **MiniMax 的 H3 Collection** 里，发布方也不是 fal。社区适配器有多家，fal 只是其中一家。

---

## 三、和 MiniMax 怎么接（不要混）

```
MiniMaxAI org          fal org
  出模型                  托管推理 + 训/发适配器
     │                           │
     ▼                           ▼
MiniMax-H3 (33B Base)  ← LoRA — MiniMax-H3-Realism-People-LoRA
     │                           │
     └──── HF Inference Providers 显示 fal（跑的仍是左边这份权重）
```

| 你看到的 | 实际是 |
|----------|--------|
| H3 模型页右侧写 fal | MiniMax 权重、fal 渠道 |
| `fal/MiniMax-H3-Realism-People-LoRA` | fal 训的皮肤，底座仍要加载 MiniMax checkpoint |
| fal 的 H3 `/lora` 端点 | 可选托管，权重文件本身不绑这家 |

许可证：People LoRA **跟基座走 MiniMax H3 Community License**（领土排除、蒸馏禁令）。fal 的平台 TOS 是另一份，上线两份都要看。

---

## 四、未展开边界

| 项 | 状态 |
|----|------|
| fal 全量模型 gallery / 单价 | 迭代极快，本页不记；上线看 [fal.ai/models](https://fal.ai/models) |
| AuraFlow / Kontext LoRA / FlashPack | 未做案例 |
| H3 trainer 现价（美元/step） | 训练指南写看 trainer 页 |
| 与 Comfy-Org / larryvrh Turbo LoRA 的横向人评 | 未见 |

---

## 五、参考来源

- [Hugging Face · fal](https://huggingface.co/fal)
- [fal.ai](https://fal.ai)
- [How to Train a LoRA for MiniMax H3](https://fal.ai/learn/devs/how-to-train-a-lora-for-minimax-h3)（Lovis Odin，2026-08-10）
- 案例：[MiniMax-H3-Realism-People-LoRA.md](./MiniMax-H3-Realism-People-LoRA.md)
- 基座：[MiniMax-H3 全景与架构](../minimax/MiniMax-H3全景与架构.md)
