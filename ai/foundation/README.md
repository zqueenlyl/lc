# foundation · 基模

> **定位**：模型**本体** —— 是什么、怎么造、怎么变强、怎么生成。
> **口诀**：「讲模型内部 / 权重 / 训练 / 生成范式」→ 归这。
> **挂靠规则**：没长成独立环节课的，不跟 `transformer` / `rl` 平级当「全链路原理」。变体/档位用薄手册；跨环节收口用横切文（不占环节号）。

上级索引：[../README.md](../README.md) ｜ 学习地图：[../learning-path.md](../learning-path.md)

---

## 骨架

| 入口 | 一句话 |
|---|---|
| [transformer/](./transformer/)（手册） | 自注意力骨架；RNN/LSTM 为何被取代；因果 vs 双向 |
| [环节00](./transformer/环节00-总揽与环节导航.md)（原理，01–11） | 一条主线 + 两个生命周期 |
| [模型评测与选型](./transformer/模型评测与选型方法详解.md)（横切） | 训练产出后怎么验、部署前怎么选 |
| [长上下文工程](./transformer/长上下文工程详解.md)（横切） | 位置 / 结构可见 / KV / 算力四条天花板 |
| [RNN知识整理](./transformer/RNN知识整理.md) | Attention 之前的历史 |

引擎怎么跑、本地怎么装 → [../runtime/](../runtime/)（环节 11 只讲服务化原理）。

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
| [diffusion/](./generative/diffusion/) | 图像扩散：DDPM → 潜空间 VAE → UNet/DiT |
| [video/](./generative/video/) | 视频 = 图 + 时间 |
| [audio-speech/](./generative/audio-speech/) | ASR / TTS / 端到端语音对话 |
| [world-models/](./generative/world-models/) | 预测世界如何演化，而不只是下一个 token |
| [multimodal/](./generative/multimodal/)（理解侧手册） | 原生吃图/音/视频，不再靠 OCR/ASR 胶水 |
| [多模态理解与统一模型详解](./generative/multimodal/多模态理解与统一模型详解.md) | CLIP → VLM 三代接入 → 统一模型 |

---

## 四条读法

- **骨架线**（须按序）：[transformer 环节00](./transformer/环节00-总揽与环节导航.md) → 01 … 11 → 横切（评测 / 长上下文）。
- **训练线**：[rl 环节00](./rl/环节00-总揽与环节导航.md) → 01 … 08 → [推理侧横切](./rl/推理侧搜索与test-time-scaling.md)；微调几何走 [peft-lora 环节00](./peft-lora/环节00-总揽与环节导航.md)。
- **模态线**：[00-AIGC总揽](./generative/00-AIGC总揽与多模态地图.md) → `diffusion` / `video` / `audio-speech` / `world-models` / `multimodal`。
- **变体**：按需跳 `moe` / `slm`；手册线也可从 [transformer/README](./transformer/) 建骨架再跳。

## 相邻大类

- 把模型编成系统 → [../agent/](../agent/)
- 塞什么进上下文窗口 → [../knowledge/](../knowledge/)
- 拦错 / 打分 / 隔离 / 路由 → [../reliability/](../reliability/)
- 跑得快 / 省 / 本地 → [../runtime/](../runtime/)
