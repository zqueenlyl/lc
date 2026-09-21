# MiniMax-H3：按模块拆构成 + 训练全流程

> 配套总览：[《MiniMax-H3 全景与架构》](./MiniMax-H3全景与架构.md)（产品面 / 许可证 / 未披露表）｜ 部署：[本地部署与 API](./MiniMax-H3本地部署与API接入.md)
> 扩散数学底座：[图像扩散模型详解](../../foundation/generative/diffusion/图像扩散模型详解.md)｜ 视频时间维：[视频生成详解](../../foundation/generative/video/视频生成详解.md)｜ Transformer 块：[环节 07](../../foundation/transformer/环节07-Block堆叠与整体架构详解.md)
> **按 Transformer 环节拆读（推荐）**：[h3/环节00-总揽与环节导航.md](./h3/环节00-总揽与环节导航.md)（01–11 详解 + 各站 Notebook）。本文是同一套材料的单页压缩版。
> 手算合集（旧入口，内容已拆进各环节）：[MiniMax-H3模块与训练直觉演示.ipynb](./MiniMax-H3模块与训练直觉演示.ipynb)
>
> **口径（2026-09-21）**：官方完整 Tech Report **仍未发布**（2026-07-31 博客写 soon）。本文能钉死的数字来自官方博客、HF 模型卡、GitHub README，以及开源推理栈 [`vllm-omni` 的 `MiniMaxH3DiTArchConfig`](https://github.com/vllm-project/vllm-omni/blob/main/vllm_omni/diffusion/models/minimax_h3/minimax_h3_transformer.py)。训练数据配比、卡时、稀疏注意力具体模式、IR / Regenerator 参数量 **官方未披露**，文中一律标「未披露」。第三方评测 [arXiv:2609.18323](https://arxiv.org/abs/2609.18323) 是物理世界推理评测，**不是**官方技术报告。

---

## 0. 先建立一张总图

H3 **不是聊天模型**。MiniMax 的对话在 M 系；H 系（Hailuo / 海螺）是**音视频联合生成**。完整产品是三段系统，开源只给了中间那块：

```
用户丢进来：一句话 + 若干图 / 参考片 / 参考声
                    │
                    ▼
        ┌───────────────────────┐
        │ ① H3-Context-IR       │  托管，未开源
        │  把「关系」写成结构化 IR │  素材侧常 ~100K token 推理 → 平均 ~4K
        └──────────┬────────────┘
                    ▼
        ┌───────────────────────┐
        │ ② H3-Base（开源）      │  33B Omni Transformer
        │  packed 序列 → 联合去噪 │  默认短边 768、24 fps、32 kHz 立体声、4–15 s
        │  FL2VA 或 Ref2VA 二选一 │
        └──────────┬────────────┘
                    ▼
        ┌───────────────────────┐
        │ ③ H3-Regenerate-2K    │  托管，未开源
        │  768p 成片 + 原上下文   │  in-context 重生成，不是独立超分网络
        └───────────────────────┘
```

**一句话**：IR 负责「读懂你要什么」，Base 负责「在潜空间里同时画出画面和声音」，Regenerator 负责「带着原文再画一遍 2K」。

下面按**数据怎么进 → 每个模块干什么 → 损失怎么算 → 训练怎么排期**讲。

---

## 1. 模块 0：你到底在生成什么？（规格当约束）

把规格当成后面公式的边界条件，否则 token 账会对不上。

| 项 | 开源 Base 默认 | 完整产品 |
|----|----------------|----------|
| 时长 | 4–15 秒 | 同 |
| 帧率 | 24 FPS | 同 |
| 分辨率 | 短边 768（16:9 → 1344×768） | Regenerator → 2K |
| 音频 | 32 kHz 立体声，左右声道**同一套 VAE、独立编码再合并** | 同 |
| 对白 | 稳定 11 语；tokenizer 有 `<d>…</d>` 对白标记 | 同 |

两个任务族、**两份 Transformer 权重**（VAE / Encoder 可共享）：

| 权重 | 你在训练 / 推理什么 | 条件 |
|------|---------------------|------|
| **FL2VA** | 文生音视频 `t2va`；首/尾帧 `fl2va` | 0 / 1 / 2 张图 |
| **Ref2VA** | 参考生 `ref2va`（含 V2V 动作迁移） | 图 ≤9、视频 ≤3、音频 ≤3、文件合计 ≤12。开源日新闻写音频不能单独当输入；**现网 HF/GitHub 规格表未写**，见[全景](./MiniMax-H3全景与架构.md) |

实例：「参考视频 1 的希区柯克运镜，让图 2 的人唱歌，歌声跟音频 3」——这是 **Ref2VA**，不是第四个模型。

发布权重是 **CFG 蒸馏**的：推理没有 `negative_prompt` / `guidance_scale`，每步只跑一次前向。调度官方口径：视频 `flow_shift=12.0`，音频 `audio_flow_shift=3.0`。

---

## 2. 模块 1：H3-Context-IR（任务接口，不是 DiT）

### 2.1 它解决什么

前代视频模型把世界切成专家：T2V、I2V、首尾帧、主体参考、动作迁移、配音……H3 的主张是：**任务不要写死在模型头上，用自然语言写「上下文 ↔ 目标」的关系。**

IR 就是把这句话变成 Base 吃得下的**结构化中间表示**。官方把它叫 Contextual Omni Representation：caption 不再只描述目标画面，还要描述

1. 上下文和目标视频的关系；
2. 上下文内部元素之间的关系；
3. 音画、多镜头怎么对齐。

官方数字：**大部分素材需要约 100K token 的推理，压到平均约 4K token。** 这套管线「专用模型 + 全模态理解」，**结构未开源**。本地只跑 Base、丢一句短 prompt，不要期待对齐海螺 App。

### 2.2 实例（同一创意，三种写法）

用户意图：「这个产品瓶，用希区柯克运镜，女声哼一段与瓶身 Logo 同调的旋律。」

| 路径 | 实际进入 Base 的东西 | 后果 |
|------|----------------------|------|
| 裸 prompt | 「产品瓶 + 希区柯克 + 哼歌」十几 token | 运镜、口型、Logo 文字容易糊 |
| 自建预处理 | 仓库 skill `h3-prompt-writing`（`base-en.txt` / `ref-en.txt`）把参考编号、镜头、对白标签写清楚 | 接近官方，但仍缺 IR 的补全 |
| 官方 IR API | 多模态关联 + 时序 + 补未写清的语义 → ~4K 结构化文本 | 成片最稳；安全审核也在这一段 |

安全：用户提交的文/图/视频以及增强后的 prompt 会过自动审核。这不影响你本地合法微调。

---

## 3. 模块 2：三条编码器（把世界压成 packed 序列）

Base 不做像素空间扩散。三条路进 **同一条 packed 序列**，token 上打 `token_tags`：`0=video / 1=text / 2=audio`（padding 为 -1）。开源代码里 AdaLN 用

```
combined_index = inverse_timestep_index * 3 + clamp(token_tag, min=0)
```

同一时间步、三种模态，各拿一套 scale / shift / gate。

### 3.1 H3-Encoder（文本 + 视觉语义）

- 底座：**完整** Qwen3-VL-32B 预训练权重（Apache-2.0）。
- 取出的不是最后一层，而是 **第 50 层 hidden**（`text_dim = 5120`），LM head 闲置。
- 视觉参考（图、参考视频帧）**同时**走 Encoder（语义）和 VisualVAE（像素级 latent）。音频**不走** Encoder，只走 AudioVAE。
- tokenizer 加了 `<d>` 等特殊 token。对白要写成类似 `<d>[English] …</d>`。**必须用本仓 tokenizer**，不要换上游 Qwen 原版。

进 Transformer 前，文本 embedding 还要过一个 **2 层 Token Refiner**（标准 pre-norm 块，**没有** AdaLN、**没有** RoPE）——相当于给条件文本做一次「自己跟自己对齐」，再拼进 packed 序列。

### 3.2 H3-VisualVAE（画面的压缩信封）

官方记号 **`f16t4d24`**：

| 轴 | 压缩 | 含义 |
|----|------|------|
| 空间 | 16× | 768 高 → latent 高 48 |
| 时间 | 4× | 24 fps → latent 6 Hz（每 4 帧一个 latent 帧） |
| 通道 | 24 | 比 SD 的 4 通道「更厚、更短」 |

进 Transformer 前再按 `(time, height, width)` 做 **`1×2×2` patchify**。有效空间下采样变成 **32×**，时间仍 4×。每个视频 token 的输入维：

```
24 × 1 × 2 × 2 = 96
```

对应开源里的 `video_patch_proj: 96 → 5376`。

**数值实例**（Notebook §1 可复现）：10 秒、16:9、1344×768、24 fps

```
像素帧数 T = 10 × 24 = 240
VAE 后：T' = 240/4 = 60，H' = 768/16 = 48，W' = 1344/16 = 84
patch 后：H'' = 24，W'' = 42
视频 token 数 = 60 × 24 × 42 = 60 480
```

博客说换代 tokenizer 相对前代大约 **4× 有效序列长度收益**，这是敢做原生 2K 的前提之一。Encoder 训完后再训 **ViT decoder**：降解码成本、抬重建。时间上是 **causal** 视频自编码器（只看过去帧），有利于时序一致，细节未披露。

### 3.3 H3-AudioVAE（声音的压缩信封）

- 左右声道 **同一套编解码器、独立跑**，再拼成立体声。
- 每声道：32 kHz → **40 Hz** latent token。
- 开源 `audio_latents_dim = 32`，`audio_patch_proj: 32 → 5376`（音频不再做 2×2 空间 patch）。
- 自称受 **VA-VAE** 启发：重建要真，潜空间还要「好学」（别让 DiT 去拟合一团扭曲的 latent）。

**数值实例**：10 秒单声道 token = `10 × 40 = 400`。立体声独立编码，packed 时左右各一条或拼在序列里（布局以开源 `build_packed_sequence` 为准）；量级是 **百级 token**，对比视频的 **六万级**——所以联合去噪时，画面才是序列长度的绝对大头。

### 3.4 位置：三维 MM-RoPE `(t, h, w)`

Attention 本身看不见顺序。H3 用 **Multimodal RoPE**：把旋转拆到时间、高、宽三个轴（和 Qwen2-VL 的 M-RoPE 同一家族）。开源 `rope_inv_freq_len = 16`，`head_dim = 128`。

直觉（Notebook §4）：

- 同一物体下一帧：`t` 变、`h,w` 不变 → 时间轴旋转，空间轴不转；
- 同一帧里相邻 patch：`h/w` 变、`t` 不变；
- 文本 token 通常只转一维（序列下标），音频 token 主要转时间轴。

这样「第 3 秒画面左上角」和「第 3 秒的歌声」可以对上同一套时间坐标，而不需要单独的音画对齐网络。

---

## 4. 模块 3：H3-Omni-Transformer（单流去噪骨干）

### 4.1 开源钉死的骨架

来自 `MiniMaxH3DiTArchConfig`：

| 项 | 值 | 备注 |
|----|----|------|
| 层数 | 50 | 另有 2 层 text token refiner |
| hidden | 5376 | |
| 头数 × 头维 | 56 × 128 | `56×128=5376` |
| FFN 隐层 | 14336 | SwiGLU（`SiluAndMul`） |
| 稠密总参 | **33B** | 官方 |
| 其中 AdaLN | **~13B** | 纯推理可预计算后不加载 |
| 视频 latent 通道 | 24 | patch 后每 token 96 维 |
| 音频 latent 通道 | 32 | |
| 文本条件维 | 5120 | Qwen3-VL 第 50 层 |
| time embed | 256 → 5376 → **2688** | AdaLN 的条件向量 |

**Attention / FFN 没有模态分支。** 模态差只放在：输入投影、输出头、AdaLN。这就是「丢掉 Hailuo-02 那种过巧架构」的具体落地——任务泛化优先于专家结构。

参数账（Notebook §2）：

```
每层 AdaLN：2688 × (6 × 5376 × 3) ≈ 2.60×10⁸
50 层：≈ 1.30×10¹⁰   ← 官方「约 13B」对得上
```

推理时时间步 embedding 对同一 `t` 是固定的，AdaLN 的 6 组向量可以 **算一次、整步复用**，所以推理部署可以卸掉这 13B。微调必须留着：梯度还要流过这些调制。

### 4.2 一块里发生了什么（公式）

标准 DiT 块，只是 scale/shift/gate **按 token 的模态标签索引**：

\[
\begin{aligned}
(\gamma,\beta,g)_{\text{attn}},(\gamma,\beta,g)_{\text{mlp}}
&= \mathrm{AdaLN}(\mathrm{SiLU}(e_t))[m] \\
h &= \mathrm{Attn}\bigl(\mathrm{RMSNorm}(x)\odot(1+\gamma_{\text{attn}})+\beta_{\text{attn}}\bigr) \\
x &\leftarrow x + g_{\text{attn}}\odot h \\
h &= \mathrm{MLP}\bigl(\mathrm{RMSNorm}(x)\odot(1+\gamma_{\text{mlp}})+\beta_{\text{mlp}}\bigr) \\
x &\leftarrow x + g_{\text{mlp}}\odot h
\end{aligned}
\]

其中 \(m\in\{\text{video},\text{text},\text{audio}\}\)，\(e_t\) 是时间步嵌入。同一套 QKV，视频 token 和音频 token 在 **同一层 self-attention 里互相看得见**——这就是「原生同期声」而不是「先出片再配乐」。

末层：再做一次 AdaLN，然后 **两个头都作用在每一行上**，再靠 mask 取出：

- `video_out`: \(5376 \to 96\)（fp32）
- `audio_out`: \(5376 \to 32\)（fp32）

输入 / 输出投影、time embed 的若干线性层在 FSDP 路径上保持 **fp32**（SGLang 明确写：不为省那点精度去破坏数值）。

### 4.3 稀疏注意力（训练末段有，开源推理暂无）

官方：训练最后阶段引入 native sparse attention 降长序列成本；**首发开源只有全注意力推理**，稀疏实现标后续单独发。引入多模态上下文后，序列长度方差大约 **大了 3 倍**，理解负载和生成负载异质。这是训练基建问题，不是推理 API 行为。

### 4.4 一次前向的数据流（FL2VA 文生 10 秒）

```
噪声视频 latent [60, 24, 48, 84]  T,C,H,W  --patch 1×2×2-->  60480 × 96  --proj--> 60480 × 5376
噪声音频 latent [400, 32]  每声道 10s×40Hz；立体声 packed 以开源为准  --proj-->  ~400–800 × 5376
文本（第50层）[L, 5120] --condition_proj--> [L, 5376] --2层 refiner--> [L, 5376]

pack: [视频 | 文本 | 音频] + token_tags + (t,h,w) RoPE
        │
        ▼  50 × (AdaLN-RMS → Attn → AdaLN-RMS → SwiGLU)
        │
        ▼  final AdaLN + 双头
干净一点的视频速度 / 音频速度  →  scheduler 走一步
```

参考任务（Ref2VA）只是 **多 pack 进去若干「干净的」参考 token**（图/视频 VAE + Encoder，音频 VAE），目标段仍是噪声。V2V 动作迁移 = 参考视频 token 在序列里当条件，不是另一个网络。

---

## 5. 模块 4：生成目标（Rectified Flow，不是经典 DDPM）

仓库里的调度器名字、社区微调器（DiffSynth、`MiniMax-H3-FineTuning`）都按 **rectified flow / flow matching** 实现。官方未写损失函数的论文级公式；下面是与开源训练脚本一致的工作模型。经典 DDPM 见[图像扩散详解](../../foundation/generative/diffusion/图像扩散模型详解.md)，这里换成「直线运输」。

### 5.1 直线插值

数据 \(x_0\)（VAE latent），噪声 \(\varepsilon\sim\mathcal N(0,I)\)，时间 \(t\in[0,1]\)：

\[
x_t = (1-t)\,x_0 + t\,\varepsilon
\]

目标速度（从数据指向噪声，或反过来，取决于实现符号；社区脚本用 MSE 拟合这条直线的速度）：

\[
v = \varepsilon - x_0,\qquad
\mathcal L = \mathbb E\bigl\|u_\theta(x_t,t,c)-v\bigr\|^2
\]

H3 是 **联合损失**：视频 latent 一项 + 音频 latent 一项。社区最小 trainer 在没缓存真音频时会把音频损失置零——那是工程缺口，不是官方设定。

### 5.2 为什么视频 `flow_shift=12`、音频 `=3`

数字来自开源推理请求体（部署篇），**不是**官方论文公式。Flow matching 常用 shift 把均匀 \(t\) 拧偏；具体拧向干净端还是噪声端，取决于调度器把 \(t=1\) 定义成噪声还是数据。社区实现里视频用更大的 shift、音频用更小的 shift，常见解释是视频格子多、高噪更难学。这是 **两个独立 scheduler**，同一次 Transformer 前向、两套时间嵌入。方向解释标工作模型，不要当成官方机制。

### 5.3 CFG 蒸馏（你为什么调不了 guidance）

标准 CFG：

\[
u_{\text{guided}} = u_{\varnothing} + w\,(u_c - u_{\varnothing})
\]

要跑两次前向。H3 发布的是 **已经把 \(w\) 烤进权重** 的学生模型：推理 `w` 失效。微调若从蒸馏权重接着训，默认已经「只会听条件、不会无条件」。要恢复 CFG，需要官方未公开的教师权重或自己做蒸馏前的数据——**未披露**。

### 5.4 1 维玩具（Notebook §3）

把「一段 5 个数的小波」当 \(x_0\)，随机噪声当 \(\varepsilon\)，直线插值上训练一个两层 MLP。十几步后从纯噪声走 Euler 能回到波形。H3 做的是同一件事，只是 \(x_0\) 是 6 万视频 token + 几百音频 token，\(u_\theta\) 是 33B Transformer。

---

## 6. 模块 5：H3-Regenerate-2K（任务泛化的超分）

不是 Real-ESRGAN 那种专用 SR。官方说法：

1. 让 **H3 基模**以 in-context 方式重画自己的 768p 结果；
2. **再次看见原始多模态上下文**，把传统超分只能猜的小字、品牌细节补回来。

这也是他们论证「超分不必另养专家」的例子。模块未开源；对齐官方 2K 必须走 Regeneration API，或一键 `/video-generation-v2-create`。

本地 768p 和 App 2K **比的是系统，不是同一份权重**。

---

## 7. 训练全流程（能还原的阶段 + 明确未知）

官方没有放出 trainer。下面是把博客「预训练范式」+ 开源权重形态 + 社区微调器 **串成一条可执行的心智模型**。标了「官方」或「开源可见」或「社区/推断」。

```
真实自然数据（官方自称；配比未披露）
        │  清洗 / 切镜 / 音画对齐 / 多镜头
        ▼
┌─ A. Tokenizer 预训练 ─────────────────────────────────┐
│  VisualVAE：重建 + latent 可学性（f16t4d24）            │
│  encoder 训完后再训 ViT decoder（官方未写是否冻结）     │
│  AudioVAE：左右独立，32 kHz → 40 Hz，VA-VAE 风格       │
└────────────────────────────────────────────────────────┘
        │  此后像素不再进 DiT
        ▼
┌─ B. Caption / Omni Representation 管线（官方）─────────┐
│  专用理解模型：~100K token 素材 → 平均 ~4K caption     │
│  内容：目标 + 上下文关系 + 上下文内部关系 + 音画多镜头 │
│  语言当任务接口（不是固定 task id）                    │
└────────────────────────────────────────────────────────┘
        ▼
┌─ C. Omni Transformer 预训练（官方原则）────────────────┐
│  尽早混合、配比是关键（具体比例未披露）：               │
│    · T2I                                                    │
│    · T2V（联合原生立体声、原生多镜头）                   │
│    · T2A（人声 / 音效 / 音乐不拆任务）                   │
│    · 广义参考与编辑：I2I / I2V / A2A / AV2AV             │
│       关系用自然语言写，数据来自真实素材                │
│  损失：视频 flow MSE + 音频 flow MSE（开源生态一致）    │
│  基建：理解 / 生成 workload 拆开调度，样本间负载均衡     │
│        自称端到端吞吐 +~30%；序列长度方差 ×~3           │
│  末段：native sparse attention（开源推理暂无）          │
└────────────────────────────────────────────────────────┘
        ▼
┌─ D. 任务族分化（开源可见）─────────────────────────────┐
│  一份骨架 → 两份 DiT：FL2VA vs Ref2VA                  │
│  Qwen3-VL 条件器在 diffusers 布局里也可按任务分开       │
└────────────────────────────────────────────────────────┘
        ▼
┌─ E. CFG 蒸馏（开源可见结果）───────────────────────────┐
│  发布权重无 guidance；每步一次前向                      │
└────────────────────────────────────────────────────────┘
        ▼
┌─ F. 产品系统（部分未开源）─────────────────────────────┐
│  Context-IR 多模型编排 + 审核                           │
│  Regenerator：768p + 原上下文 in-context 2K             │
│  与 M 系融合、继续 Scale = 路线图，不是现网已交付       │
└────────────────────────────────────────────────────────┘
        ▼
┌─ G. 社区可做的后训练（非官方预训练）───────────────────┐
│  DiffSynth SFT / LoRA；fal People LoRA（rank 32）      │
│  官方许可证：禁止用 H3 或其输出蒸馏改进其它模型         │
└────────────────────────────────────────────────────────┘
```

### 7.1 阶段 A：先把信封训好

视频生成的第一生产力经常是 **VAE 好不好学**，不是 DiT 层数。H3 明确说同时优化重建和 learnability；VisualVAE 还多训一个 ViT decoder。音频独立成 VAE，避免「图像 VAE 硬塞频谱」。

### 7.2 阶段 B：语言当任务总线

这是 H3 相对「专家视频 DiT」最不像的一步。训练样本不是 `(task_id=I2V, image, prompt)`，而是一段自然描述：「把图 A 的人放到视频 B 的运镜里，音色像音频 C」。IR / caption 模型把这事在预训练前就做掉。**100K→4K 跑在哪套模型上，未披露。**

### 7.3 阶段 C：一个网络、多种噪声图

联合图+视频是视频 DiT 的老经验（图像 = 单帧视频，保空间质量）。H3 再叠：

- 音频与视频 **同一去噪环**；
- 参考/编辑不是后加 ControlNet，而是预训练任务；
- 硬件上把「读长上下文（理解）」和「写长视频 token（生成）」拆开利用率——所以序列方差变 3 倍还能吞吐 +30%。

优化器、全局 batch、token 总量、是否分分辨率课程学习：**未披露**。开源推理默认短边 768，2K 走 regen，合理推断预训练主分辨率在 768 桶，2K 是后一阶段的 in-context 任务，但官方没写死。

### 7.4 阶段 D–E：你下载到的两份 BF16

不要把 FL2VA 的 transformer 加载进 Ref2VA 请求。社区全参微调需要 DeepSpeed ZeRO-3 量级；实用路径是 LoRA 打在共享 `qkv_proj` / `out_proj` / FFN 上（fal 人像 LoRA 只打融合 QKV，一份文件挂 T2V/I2V/R2V）。

### 7.5 阶段 G：社区训练时四条会「静默毁掉权重」的约定

来自社区 trainer 的血泪总结（与官方数值设定对齐）：

1. 视频 / 音频两套 timestep，不要共用一个 `t`；
2. packed 布局必须用官方 `build_packed_sequence` / `build_row_timesteps`，不要自己 `cat`；
3. AdaLN 相关投影保持 fp32；
4. 蒸馏权重没有 CFG，不要在 loss 里再乘 guidance。

DiffSynth 文档：FL2VA 训练可把视频首尾帧自动当 `input_image/end_image`；Ref2VA 用 `metadata.json` 的 `references`（`image` / `video` / `audio` / `video_audio`）。参考图按短边策略缩放，参考视频裁到画布、24 fps 采样。

---

## 8. 推理一步 vs 训练一步（对照）

| | 训练一步 | 开源推理一步 |
|--|----------|----------------|
| 输入 \(x_t\) | 按随机 \(t\) 直线插值真 latent | 上一 scheduler 状态 |
| 条件 \(c\) | caption/IR 文本 + 可选参考 token | 同；本地常无 IR |
| 网络 | 完整 33B（含 AdaLN） | 可卸 ~13B AdaLN，调制预计算 |
| 前向次数 | 1（蒸馏后）或 2（蒸馏前，未披露） | **1** |
| 输出 | \(u_\theta\)，对 \(v\) 做 MSE | \(u_\theta\)，Euler/flow 积分 |
| 解码 | 通常不每步 decode | 积分结束后 VisualVAE + AudioVAE |

完整 2K 产品路径：`IR API → Base（本地或云）→ Regen API`。

---

## 9. 开源数据与第三方材料怎么用

| 来源 | 能当什么 | 不能当什么 |
|------|----------|------------|
| [官方博客 2026-07-31](https://www.minimax.io/blog/minimax-h3) | 设计原则、预训练任务清单、IR 100K→4K、吞吐 +30%、regen 动机 | 层配置、损失公式、数据配比 |
| [开源日新闻 2026-08-03](https://www.minimax.io/news/minimax-h3-open-source) | 三模块边界、双 checkpoint | 训练脚本 |
| HF `MiniMaxAI/MiniMax-H3` / GitHub `MiniMax-AI/MiniMax-H3` | 规格、编码路径、VAE 压缩比、33B/13B、MM-RoPE、CFG 蒸馏 | Tech Report |
| vLLM-Omni `minimax_h3_transformer.py` | **层数 / 宽度 / AdaLN 形状 / 双头 / token_tags** | 训练超参 |
| DiffSynth / 社区 FineTuning | 你怎么 SFT/LoRA | 官方预训练 |
| fal People LoRA | 176 条人像、rank 32、高分桶更重要 | 官方第四模块 |
| [arXiv:2609.18323](https://arxiv.org/abs/2609.18323) | 517 例物理推理，总成功率 41.97%；视频决策 56%，音频消歧 27.4% | 架构论文 |

官方完整 H3 Technical Report：**仍预告中**。

---

## 10. 把整条链收成一个「希区柯克唱歌」例子

1. **IR**：读懂「视频 1 = 运镜参考，图 2 = 人，音频 3 = 声」，补镜头运动描述、口型时序、对白语言标签，输出 ~4K IR。
2. **Encode**：IR 文本 → Qwen3-VL 第 50 层 → 2 层 refiner；图 2 与视频 1 → Encoder 语义 + VisualVAE；音频 3 → AudioVAE 左右独立 40 Hz。
3. **Pack**：参考 token（干净）+ 目标视频/音频 token（噪声）+ 三维 RoPE。
4. **去噪**：50 层单流 Transformer，AdaLN 按模态调制，联合预测视频速度与音频速度；`flow_shift` 视频 12、音频 3。
5. **Decode**：VisualVAE（ViT decoder）→ 768p 24 fps；AudioVAE 左右合并 → 32 kHz 立体声。
6. **Regen**（产品）：把 768p 片当新的上下文，连同原始图/视频/音频再生成 2K——Logo 小字靠的是「再看见原图」，不是从糊像素里超分猜。

本地开源停在第 5 步；缺第 1 步和第 6 步时，观感差距主要来自系统而不是你没调好 `guidance_scale`（那个参数本来就不存在）。
