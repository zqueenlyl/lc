# Video · 视频生成（时间维上的去噪 / 运货）

> 一句话：**工业主核把视频当成 4D 信号压进 VAE，再在 DiT 上整段去噪或沿直线运货。** 难点从「画得好看」变成「帧间一致 + 运动合理 + 步数 × 序列长度付得起」。
>
> 与 [transformer/](../transformer/) **平级的另一条全链路**（01–11）。那边是猜下一个 token；这边是沿 \(t\) 运噪声。Attention / SwiGLU / RMSNorm / RoPE **公式**回 transformer 对应站，本目录只讲视频必须改的那一截。
>
> 环节主线：[环节00-总揽与环节导航.md](./环节00-总揽与环节导航.md)。本页讲机制 / 类型 / 选型。类型全谱：[生视频模型演化路线与类型.md](./生视频模型演化路线与类型.md)。扩散数学：[../generative/diffusion/](../generative/diffusion/)。

经典开源标本：**MiniMax-H3 Base**（潜空间 flow + 音画同环）。产品 / 部署 / 许可证：[H3 全景](../../model-cases/minimax/MiniMax-H3全景与架构.md)。

---

## 一、技术讲解

视频是 \(T\times H\times W\) 的 4D 张量。逐帧当图生成必然闪。主流 D/E 核做同一件事：

```
条件（文 / 图 / 参考）──► 编码器 + pack
噪声视频 latent     ──► DiT（时空 patch → 双向注意力）── 逐步改 latent ──► VAE Decode ──► 帧
（可选）噪声音频     ──► 同一条序列、同一去噪环 ──────────────────────────► 波形
```

和图像生成的三条本质差异：

| 差异 | 后果 |
|---|---|
| **时间维要建模** | 必须一次看见整段，常用三维 RoPE `(t,h,w)` |
| **序列长度爆炸** | token 数 ≈ 压缩后的 \(T'\times H'\times W'\)，注意力 \(O(n^2)\) |
| **数据更贵更少** | 图像打底空间质量，视频数据补运动；常联合图+视频训 |

生成核不是一种（详见演化路线）：

| 核 | 一次前向 | 代表窗口 |
|---|---|---|
| A GAN | 对抗出短 clip | 2016–21 |
| B 时间膨胀 UNet | 文生图权 + temporal 层 | 2022–23 |
| C 离散 token | 下一个视觉 token | 2021– |
| D 潜空间 DiT 扩散 | 预测噪声 | 2024 |
| E 潜空间 flow DiT | 预测速度 | 2024–26（H3） |
| F 世界模型 | 动作条件下一状态 | 旁支 |

本目录环节按 **D/E** 拆。D 与 E 骨干可同构，换的是训练目标。

---

## 二、功能作用

- **文生 / 图生 / 参考生视频**：条件布局不同，骨干常是同一套 DiT。
- **音画同环**：口型与节奏在注意力里对齐，而不是后配 TTS。
- **延展 / 编辑**：干净参考 token pack 进序列，当条件不去噪。
- **世界模型雏形**：把「下一帧」加上动作，见 [../generative/world-models/](../generative/world-models/)。

---

## 三、应用场景

| 场景 | 要点 |
|---|---|
| 广告片头 / 动态素材 | 短、可控、风格一致 |
| 短视频 / 分镜预演 | 首帧 + 提示词，快速试错 |
| 电商产品演示 | 多参考图一致性 |
| 影视后期 | 控制与工作流（不只一条生成） |

---

## 四、怎么选（心智模型）

| 问题 | 看什么 |
|---|---|
| 出帧核是 D、E 还是 C？ | 采样旋钮、loss、能不能套图像 DiT 蒸馏经验 |
| 音频在不在同一个去噪环？ | 不在则口型是后处理；在则两套 \(t\) 和 loss 加权 |
| 任务是专家网还是语言+pack？ | 微调打在哪；缺的是权重还是 caption/IR |
| 成本 | \(\propto\) 步数 \(\times n^2\)（全注意力）；\(n\) 由时长 × 分辨率 × VAE 压缩比定死 |

2026 年新训基座几乎不会从 GAN 或纯时间膨胀 UNet 起手。C 还活在「当语言写视频 / 世界模型 token」里。线上成片主核是 D/E。

---

## 五、与相邻技术

| 技术 | 关系 |
|---|---|
| [../generative/diffusion/](../generative/diffusion/) | 数学底座：DDPM / 潜空间 / 条件注入 |
| [../transformer/](../transformer/) | Attn / FFN / RMSNorm / RoPE 公式；本目录只讲视频侧改造 |
| [../generative/audio-speech/](../generative/audio-speech/) | 后配音 vs 同环 AudioVAE |
| [../generative/world-models/](../generative/world-models/) | 同一套预测下帧，加动作与物理 |
| [../generative/multimodal/](../generative/multimodal/) | 理解侧：视频问答，不是出帧 |
| [../../reliability/guardrails/](../../reliability/guardrails/) | 深度伪造、肖像、版权 |

---

## 六、落地建议

1. **异步 + 队列**：分钟级任务，绝不同步阻塞 HTTP。
2. **成本从第一天按帧 × 步数算**，配低质快 / 高质慢。
3. **锁版本 + 灰度**：升级必跑时序一致性回归。
4. **审核在服务端**。
5. **按镜头选模型**，没有全能冠军。

---

## 七、延伸阅读与环节 Notebook

- 关卡地图：[环节00](./环节00-总揽与环节导航.md)
- 类型：[生视频模型演化路线与类型.md](./生视频模型演化路线与类型.md)
- 时间维短文：[视频生成详解.md](./视频生成详解.md)
- 前置：[图像扩散](../generative/diffusion/图像扩散模型详解.md) ｜ 上级 [../README.md](../README.md)
- 案例：[MiniMax-H3](../../model-cases/minimax/MiniMax-H3全景与架构.md) ｜ [fal 人像 LoRA](../../model-cases/fal/MiniMax-H3-Realism-People-LoRA.md) ｜ [豆包 Seedance](../../model-cases/doubao/豆包视频交互技术深度调研报告.md)

环节 01–11 各配一份 notebook（纯 Python 标准库，零依赖）：

| 环节 | Notebook | 一句话 |
|---|---|---|
| 01 规格 | [演示](./环节01-规格与任务族演示.ipynb) | 时长 × 画幅如何变成整除合同 |
| 02 条件 | [演示](./环节02-Context-IR演示.ipynb) | 关系三元组；100K→4K 在压什么 |
| 03 VAE | [演示](./环节03-双VAE演示.ipynb) | 10 秒 16:9 → 60480 视频 token |
| 04 Packed | [演示](./环节04-Encoder与Packed序列演示.ipynb) | token_tags 与 AdaLN 索引 |
| 05 MM-RoPE | [演示](./环节05-MM-RoPE演示.ipynb) | 相对位移相同则点积相同 |
| 06 AdaLN | [演示](./环节06-AdaLN演示.ipynb) | 13B 参数账；推理可卸 |
| 07 Block | [演示](./环节07-Omni-Block堆叠演示.ipynb) | 结构相同 ≠ 参数共享 |
| 08 Flow 目标 | [演示](./环节08-双头与Flow训练目标演示.ipynb) | 直线插值 + shift |
| 09 训练 | [演示](./环节09-训练管线演示.ipynb) | 阶段清单；早融合配比是旋钮 |
| 10 采样 | [演示](./环节10-Flow采样与推理演示.ipynb) | Euler 步数 vs 误差 |
| 11 服务化 | [演示](./环节11-系统与服务化演示.ipynb) | 开源 vs 托管模块；显存账 |
