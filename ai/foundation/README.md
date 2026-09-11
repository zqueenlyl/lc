# foundation · 基模

> **定位**：模型**本体** —— 是什么、怎么造、怎么变强、怎么生成。
> **口诀**：「讲模型内部 / 权重 / 训练 / 生成范式」→ 归这。

上级索引：[../README.md](../README.md) ｜ 学习地图：[../learning-path.md](../learning-path.md)

## 专题

| 专题 | 一句话 | 入口 |
|---|---|---|
| **Transformer（手册 + MVP）** | 自注意力骨架；RNN/LSTM 为何被取代；因果 vs 双向 | [transformer/](./transformer/) |
| **Transformer 全链路（原理）** | 一条主线 + 两个生命周期，11 环节关卡地图 | [总揽](./transformer/环节00-总揽与环节导航.md) |
| **模型评测与选型（原理）** | 训练产出后「怎么验」、部署前「怎么选」 | [详解](./transformer/模型评测与选型方法详解.md) |
| **强化学习与模型对齐（原理）** | SFT 之后为什么要 RL：RLHF → DPO → GRPO → RLVR | [详解](./transformer/强化学习与模型对齐详解.md) |
| **RNN** | Attention 之前的历史：串行、长距离难题 | [RNN知识整理](./transformer/RNN知识整理.md) |
| **Reasoning** | 推理模型 + 测试时算力缩放（第三条缩放律） | [reasoning/](./reasoning/) |
| **MoE** | 稀疏专家混合：总参大、激活小 | [moe/](./moe/) |
| **Multimodal** | 文本 / 图 / 音 / 视频原生一体 | [multimodal/](./multimodal/) |
| **多模态理解与统一模型（原理）** | CLIP 对齐 → VLM 三代接入 → 统一模型 | [详解](./multimodal/多模态理解与统一模型详解.md) |
| **SLM** | 小模型与端侧：便宜、快、可私有化 | [slm/](./slm/) |
| **PEFT / LoRA** | 只训少量参数就能适配领域 | [peft-lora/](./peft-lora/) |
| **Generative（手册）** | 生成侧入口：扩散 / 视频 / 语音 / 世界模型 | [generative/](./generative/) |
| **AIGC 总揽（原理）** | 模态矩阵 + 两大生成范式 + 公共底座 | [总揽](./generative/00-AIGC总揽与多模态地图.md) |
| **Diffusion** | 图像扩散：DDPM → 潜空间 VAE → UNet/DiT | [diffusion/](./generative/diffusion/) |
| **Video** | 视频 = 图 + 时间：时空 patch / 3D VAE / DiT | [video/](./generative/video/) |
| **Audio / Speech** | ASR / TTS 三代演化 / 端到端语音对话 | [audio-speech/](./generative/audio-speech/) |
| **World Models** | 预测「世界如何演化」，而不只是下一个 token | [world-models/](./generative/world-models/) |

## 三条读法

- **手册线**（可跳读）：`transformer/README.md` 建骨架 → 按需跳 `reasoning` / `moe` / `slm` / `peft-lora`。
- **原理线**（须按序）：[`环节00-总揽与环节导航`](./transformer/环节00-总揽与环节导航.md) → `环节01` … `环节11` → 横切两篇（模型评测与选型 / 强化学习与模型对齐）。
- **生成线**：[`generative/README`](./generative/) → `00-AIGC总揽与多模态地图` → `diffusion` / `video` / `audio-speech` / `world-models`。

## 相邻大类

- 把模型编成系统 → [../agent/](../agent/)
- 塞什么进上下文窗口 → [../knowledge/](../knowledge/)
- 跑得快 / 省 / 本地 → [../runtime/](../runtime/)
