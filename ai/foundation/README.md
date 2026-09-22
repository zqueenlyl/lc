# foundation · 基模

> **定位**：模型**本体** —— 是什么、怎么造、怎么变强、怎么生成。
> **口诀**：「讲模型内部 / 权重 / 训练 / 生成范式」→ 归这。
> **挂靠规则**：
> 1. **全链路环节课**才平级：现在是 `transformer/`（文本接龙 / LLM）、`video/`（生视频）、`rl/`（对齐）、`peft-lora/`（低秩微调）。
> 2. **文件夹按机制命名，不按品类**。所以文本这条不叫 `llm/`：01–07 的 Attention / FFN / RoPE 是零件，[video 环节 07](./video/环节07-Omni-Block堆叠详解.md) 直接复用。对外可以说「LLM 环节课」，路径仍是 `transformer/`。
> 3. 还没长成 01–N 的（图像扩散、语音、世界模型、多模态理解）留在 [generative/](./generative/)，用薄手册 + 地图，不占骨架席。
> 4. 变体/档位（`moe/` `slm/`）用薄手册，零件正文回环节课。

上级索引：[../README.md](../README.md) ｜ 学习地图：[../learning-path.md](../learning-path.md)

---

## 两条生成全链路（骨架）

同一套「环节 00 → 01–11 + Notebook」：先认机器在干什么，再下钻零件。

| | 文本接龙（LLM） | 生视频 |
|--|----------------|--------|
| 目录 | [transformer/](./transformer/) | [video/](./video/) |
| 关卡地图 | [环节00](./transformer/环节00-总揽与环节导航.md) | [环节00](./video/环节00-总揽与环节导航.md) |
| 机器 | 猜下一个 token | 把噪声 latent 拉回干净音视频 |
| 循环 | 序列变长，+1 token | 序列长度冻结，\(t\) 往 0 走 |
| 01–07 | 零件正文（Tokenizer → Block） | 视频侧改造（VAE / pack / 3D-RoPE / AdaLN / 双向 DiT） |
| 08–11 | LM Head、CE、KV、Chat 服务 | 速度头、flow MSE、沿 \(t\) 积分、异步出片 |

文本横切（评测 / 长上下文 / RNN 前史）仍挂在 transformer 下：[选型](./transformer/模型评测与选型方法详解.md) · [长上下文](./transformer/长上下文工程详解.md) · [RNN](./transformer/RNN知识整理.md)。视频横切：[演化路线](./video/生视频模型演化路线与类型.md) · [时间维短文](./video/视频生成详解.md)。

引擎怎么跑、本地怎么装 → [../runtime/](../runtime/)（各课环节 11 只讲服务化原理）。

---

## 训练

| 入口 | 一句话 |
|---|---|
| [rl/](./rl/)（手册） | SFT 之后为什么要 RL：偏好 / 验证器 / 环境 |
| [rl 环节00](./rl/环节00-总揽与环节导航.md)（原理，01–08） | MDP → PPO → RLHF → DPO → GRPO / RLVR → Agentic RL |
| [推理侧搜索与 test-time scaling](./rl/推理侧搜索与test-time-scaling.md)（横切） | 第三条缩放律：推理时多花算力换准确率 |
| [peft-lora/](./peft-lora/)（手册） | 何时微调、r 怎么选、热插拔 |
| [peft-lora 环节00](./peft-lora/环节00-总揽与环节导航.md)（原理，01–04） | 低秩为什么够用：森林寻宝 → 秩 → `ΔW=BA` |

工程账（7B 显存、QLoRA）仍在 [transformer 环节 09](./transformer/环节09-训练管线详解.md) §4.3；对齐算法不在那边展开。

---

## 变体 / 档位（薄手册，按需跳）

| 入口 | 一句话 | 零件正文在哪 |
|---|---|---|
| [moe/](./moe/) | 总参大、每 token 只激活少数专家 | [transformer 环节 05](./transformer/环节05-FFN激活与MoE详解.md) |
| [slm/](./slm/) | 小模型与端侧：便宜、快、可私有化 | 端侧操作 → [runtime/local-inference](../runtime/local-inference/) |

---

## 模态

生成与理解共用一张地图，目录在 [generative/](./generative/)。

| 入口 | 一句话 |
|---|---|
| [generative/](./generative/)（手册） | 生成侧入口与工程横切（异步 / 步数账 / 审核） |
| [00-AIGC总揽与多模态地图](./generative/00-AIGC总揽与多模态地图.md) | 模态矩阵 + 两大范式 + 公共底座 |
| [diffusion/](./generative/diffusion/) | 图像扩散：DDPM → 潜空间 VAE → UNet/DiT（尚未独立环节课） |
| [audio-speech/](./generative/audio-speech/) | ASR / TTS / 端到端语音对话 |
| [world-models/](./generative/world-models/) | 预测世界如何演化，而不只是下一个 token |
| [multimodal/](./generative/multimodal/)（理解侧手册） | 原生吃图/音/视频，不再靠 OCR/ASR 胶水 |
| [多模态理解与统一模型详解](./generative/multimodal/多模态理解与统一模型详解.md) | CLIP → VLM 三代接入 → 统一模型 |

---

## 四条读法

- **生成全链路**（须按序，两条平行）：文本 [transformer 环节00](./transformer/环节00-总揽与环节导航.md) → 01 … 11；视频 [video 环节00](./video/环节00-总揽与环节导航.md) → 01 … 11。视频 01–07 遇到 Attn/FFN/RoPE 公式，回 transformer 对应站，不在 video 重讲。
- **训练线**：[rl 环节00](./rl/环节00-总揽与环节导航.md) → 01 … 08 → [推理侧横切](./rl/推理侧搜索与test-time-scaling.md)；微调几何走 [peft-lora 环节00](./peft-lora/环节00-总揽与环节导航.md)。
- **模态线**（还没成课的生成/理解）：[00-AIGC总揽](./generative/00-AIGC总揽与多模态地图.md) → `diffusion` / `audio-speech` / `world-models` / `multimodal`。
- **变体**：按需跳 `moe` / `slm`。

## 相邻大类

- 把模型编成系统 → [../agent/](../agent/)
- 塞什么进上下文窗口 → [../knowledge/](../knowledge/)
- 拦错 / 打分 / 隔离 / 路由 → [../reliability/](../reliability/)
- 跑得快 / 省 / 本地 → [../runtime/](../runtime/)
