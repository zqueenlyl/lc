# MiniMax-H3 全景与架构

> 调研时间：2026-09-16（架构）／2026-09-17 对照官方 HF 模型卡再核 ｜ 范围：MiniMax **官方**仓库 [`MiniMaxAI/MiniMax-H3`](https://huggingface.co/MiniMaxAI/MiniMax-H3)（海螺 / Hailuo 线），不是 M 系对话模型，也不是 fal 的 LoRA
> 三线总图：[《MiniMax 全景与产品线》](./MiniMax全景与产品线.md)（文本 M3 / 本页视频 / 音频 Speech·Music3）。本文基于官方发布博客、Hugging Face 模型卡、GitHub README 与 Community License 整理；**完整 H3 Tech Report 官方预告，2026-09-18 仍未见独立论文。**
> 接入、本地部署、端点与坑见 [《MiniMax-H3 本地部署与 API 接入》](./MiniMax-H3本地部署与API接入.md)。挂在本基座上的 fal 人像 LoRA 见 [`fal/`](../fal/fal全景与生态.md)。原理对照：[视频生成详解](../../foundation/generative/video/视频生成详解.md)。M 系见 [M3 篇](./MiniMax-M3全景与架构.md)；接口速查 [providers · MiniMax](../providers/各大厂商代表模型总览.md#36-minimax)。

---

## 一、摘要（TL;DR）

1. **H3 是视频生成系统，不是聊天模型。** MiniMax 把对话 / Agent 放在 **M 系列**（如 `MiniMax-M3`），把音视频生成放在 **H 系列**（Hailuo 01 → Hailuo 02 → **H3**）。仓库 `MiniMaxAI/MiniMax-H3` 对应后者。
2. **完整系统 = 三模块，开源只给了中间那块。** `H3-Context-IR`（多模态指令 → 结构化中间表示）与 `H3-Regenerate-2K`（768p + 原上下文 → 2K）仍走托管 API；开源的是 **H3-Base**，默认短边 768、24 fps、原生 32 kHz 立体声，时长 4–15 秒。
3. **H3-Base 是 33B 稠密单流 Omni Transformer**，约 13B 在 AdaLN 分支——纯推理可预计算/不加载这 13B。注意力与 FFN **没有**模态专用结构；视频 / 音频在**同一次去噪循环**里联合预测，没有独立 vocoder。
4. **两个任务族、两份权重，不要混。** `FL2VA` = 文生 / 首尾帧生音视频；`Ref2VA` = 图 / 视频 / 音频参考。发布权重是 **CFG 蒸馏**的：没有 `negative_prompt` / `guidance_scale`，每步只跑一次前向。
5. **2K 不是专用超分。** 官方用基模对自己的 768p 结果做 **in-context regeneration**，再吃一遍原始多模态上下文——用来还原传统超分只能「猜」的小字和细节。这套还没开源。

**核心判断**：H3 的主张不是「又一个更强的文生视频专家」，而是把 T2V / I2V / 首尾帧 / 主体参考 / 动作迁移 / 音色参考 / 视频编辑 **收成同一套预训练任务**，用自然语言描述「上下文和目标的关系」。开源落地时要接受一个工程事实——**本地只能复现 768p Base；官方 2K 观感仍依赖托管 IR + Regeneration**。

---

## 二、产品面与版本时间线

| 日期 | 事件 | 要点 | 来源 |
|------|------|------|------|
| 更早 | Hailuo 01 / 02 | 01 从 0 到 1；02 抠架构效率、数据与规模。H3 **主动丢掉 Hailuo-02 架构**，因为它不利于任务泛化 | 官方博客 |
| 2026-07-31 | **H3 正式发布** | 全模态上下文理解 + 原生立体声音视频，最高 15s / 2K；宣称指令遵循、品牌文字、V2V 动作迁移 | 官方博客 |
| 2026-08-02 | **Community License / 权重开源日** | HF `MiniMaxAI/MiniMax-H3`；许可证日期即此日。Encoder 另走 Qwen3-VL-32B 的 Apache-2.0 | 官方 LICENSE |
| 2026-08-10 | fal H3 LoRA 训练指南 | 四套 trainer；176 人像素材、十六组人评。当时胜出配方后来被现网权重替换 | [fal People LoRA](../fal/MiniMax-H3-Realism-People-LoRA.md) |
| 2026-09-16 | 开源形态已稳定为双 checkpoint | `FL2VA/` + `Ref2VA/`；SGLang / vLLM / diffusers / ComfyUI 均有官方菜谱。完整 Tech Report **尚未见到** | 官方仓库 / 模型卡 |
| 2026-09-17 | fal 人像 LoRA 快照 | `fal/MiniMax-H3-Realism-People-LoRA`：现网 rank 32 / 1500 / 高分桶。**不是**官方第四模块 | [fal/](../fal/fal全景与生态.md) |

### 三条产品面（不要混规格）

| 面 | 入口 | 你实际拿到什么 |
|----|------|----------------|
| **C 端 App** | 全球 [hailuoai.video](https://hailuoai.video/tools/minimax-h3) ｜ 国内 [hailuoai.com](https://hailuoai.com/)；桌面 Hub `hub.minimax.io` / `hub.minimaxi.com` | 完整三模块体验（含 2K） |
| **开放平台 API** | 全球 [platform.minimax.io](https://platform.minimax.io/docs/api-reference/video-generation-v2-create) ｜ 国内 [platform.minimaxi.com](https://platform.minimaxi.com/docs/api-reference/video-generation-v2-create) | 一键 2K，或拆成 IR / Base / Regen 三段 |
| **开源权重** | Hugging Face `MiniMaxAI/MiniMax-H3`；ModelScope `MiniMax/MiniMax-H3` | **仅 H3-Base**，768p + 立体声 |

> **选型坑**：拿开源 768p 去和官方 API 的 2K 片比画质，比的是系统而不是同一份权重。H3 模型页 Inference Providers 显示 fal，只说明托管渠道；平台与适配器见 [`fal/`](../fal/fal全景与生态.md)。

### 输入 / 输出规格（模型卡口径）

| 项 | 规格 |
|----|------|
| 输出时长 | **4–15 秒**（diffusers 侧因 VAE 帧对齐写成 5–15 秒，见部署篇） |
| 宽高比 | 含 21:9、16:9、4:3、1:1、3:4、9:16 等 |
| 分辨率 | 默认短边 **768**（16:9 → 1344×768）；2K 走 Regenerator |
| 帧率 | **24 FPS** |
| 音频 | **32 kHz 立体声**（左右声道独立编解码再合并） |
| 对白语言 | 稳定 11 语：阿 / 中 / 英 / 法 / 德 / 意 / 日 / 韩 / 葡 / 俄 / 西；其它语种程度不等 |

| 变体 | 模式 | 输入上限 |
|------|------|----------|
| **H3-Base-FL2VA** | 首尾帧 | 0 / 1 / 2 张图：无图 = T2VA；一张 = 首帧或尾帧；两张 = 首尾帧 |
| **H3-Base-Ref2VA** | 全参考 | 图 ≤9；视频 ≤3 段、每段 2–15s、总时长 ≤15s；音频 ≤3 段、**每段 2–15s、总时长 ≤15s**，且必须配图或视频、不能单独作为输入；全类型文件合计 ≤12 |

V2V 动作迁移是 **Ref2VA 的一种用法**，不是第四个任务名。

---

## 三、设计纲领：打破任务边界

官方把前代视频模型的问题概括为**任务墙**：图侧 T2I / 编辑 / 主体 / 动作 / 风格各养一个专家；声侧人声 / 音效 / 音乐分家；视频侧再切文生、图生、首尾帧、参考、编辑。墙既限制创作者，也限制预训练泛化。

H3 预训练刻意早融合：

- 文生图 / 文生视频（**联合原生立体声**、原生多镜头）
- 文生音频（人声、音效、音乐**不拆任务**）
- 广义参考与编辑：图→图、图→视频、音频→音频、音视频→音视频；关系用**自然语言**写，而不是固定任务头
- 数据口径自称「完全由真实自然数据构成」，以换扩展性

应用侧的变化：用户不再只丢一句画面 prompt，而是描述**上下文与目标视频的关系**。官方示例：「参考视频 1 的希区柯克镜头运动，让图 2 中的人物唱歌，歌声参考音频 3」。

后续方向（官方自陈，非已交付）：H 系列下一版与 **M 系列能力融合**；模型规模还要 Scale；部分场景精细度仍不够。完整 **H3 Tech Report 仍标「后续发布」**（2026-09-16 快照未见独立论文）。

---

## 四、三模块拆解

```
自由多模态输入（文 / 图 / 视频 / 音频）
        │
        ▼
┌───────────────────┐     托管，未开源
│  H3-Context-IR    │  指令解析 · 跨模态关联 · 时序 · 推理
│  → Context IR     │  素材侧常需 ~100K token 推理，压到平均 ~4K
└─────────┬─────────┘
          ▼
┌───────────────────┐     开源（两份 BF16 checkpoint）
│  H3-Base          │  packed 多模态序列 → Omni Transformer
│  → 768p + 立体声  │  联合预测 video / audio latent
└─────────┬─────────┘
          ▼
┌───────────────────┐     托管，未开源
│ H3-Regenerate-2K  │  768p 结果 + 原始上下文 → in-context 重生成 2K
└───────────────────┘
```

### 4.1 H3-Context-IR

托管式预处理 / 编排。把「文本、图像、音频、参考视频之间的关系，以及它们和目标成片的关系」序列化成 Base 吃得下的结构化表示；在不偏离原意的前提下可以补未写清的语义。

官方强调：**IR 对成品质感至关重要**——本地只跑 Base、用短 prompt，不要期待对齐海螺 App。可选项：调 IR API，或按仓库「提示词指导」自建预处理（GitHub 内置 skill `h3-prompt-writing`）。

安全：用户提交的文本 / 图 / 视频以及增强后的 prompt 会过自动审核；拦违法、色情、侵权。官方承认无法消掉误拦 / 漏拦。这不影响许可证里被许可方自己的合法使用义务。

### 4.2 H3-Base（开源主体）

**编码进 packed 序列**

| 模态 | 谁编码 |
|------|--------|
| 文本 | **H3-Encoder**（Qwen3-VL-32B **完整预训练权重**，取第 **50** 层 hidden，而不是最后一层；LM head 闲置）。仓库 tokenizer 加了 `<d>` 等特殊 token（对白示例写作 `<d>[English] …</d>`），**必须用本仓 tokenizer**，不要换上游 Qwen 原版 |
| 视觉 | Encoder + **H3-VisualVAE** |
| 音频 | 仅 **H3-AudioVAE**（不经 Encoder） |

序列用 RoPE / **MM-RoPE**（三维 `(t, h, w)`）再进 Omni Transformer；Transformer **联合预测**视频 latent 与音频 latent，再分别 decode。没有单独的声码器、没有「先出片再配乐」的后处理通道。

**H3-VisualVAE**

- 时间因果视频自编码器：**空间 16×、时间 4×、24 通道**，记 `f16t4d24`
- 进 Transformer 前再按 `(time, height, width)` 做 `1×2×2` patchify → 有效空间下采样 **32×**，时间仍 4×
- Encoder 训完后另训 **ViT decoder**，降解码成本、抬重建
- 博客口径：H3 换代 tokenizer 相对前代，高压缩带来约 **4× 序列长度收益**，是「敢做原生 2K」的关键之一

**H3-AudioVAE**

- 左右声道 **同一套编解码器、独立跑**，再拼成立体声
- 每声道：32 kHz → **40 Hz** latent token
- 自称受 VA-VAE 启发，在重建与「好学」之间折中

**H3-Omni-Transformer**

| 项 | 官方口径 |
|----|----------|
| 规模 | **33B 稠密单流**；约 **13B 在 AdaLN 相关分支** |
| 推理 | AdaLN 调制可预计算缓存，**纯推理可不加载这 13B**；完整权重仍放出以便微调 |
| 模态专用参数 | 只在 **输入/输出层 + AdaLN**；Attention / FFN 无模态分支 |
| 位置 | 三维 **MM-RoPE** `(t, h, w)` |
| 稀疏注意力 | 训练末段引入，**降低长序列成本**；**首发开源只有全注意力推理**，稀疏实现标「后续单独发」 |

博客补充：引入多模态上下文后，序列长度方差约 **大了 3 倍**，理解 / 生成 workload 异质化。训练侧把理解与生成拆开调硬件利用率，并做样本间负载均衡，自称端到端训练吞吐 **+~30%**。这是训练基建，不是推理 API 行为。

### 4.3 H3-Regenerate-2K

不用专用超分网络，而让 **H3 基模以 in-context 方式重画自己的低分结果**，并再次看见原始多模态上下文。官方给出的理由：

1. 最大程度复用基模已经会的生成能力；
2. 能还原传统超分无法从低分里「猜」回来的信息（小字、品牌细节）。

官方同时把它当成「任务泛化」的例子：超分不再是另一个专家模型。**模块本身尚未开源**，验证走 Regeneration API。

---

## 五、四项技术选择（博客口径）

| 名称 | 要解决什么 | 机制（官方叙述） | 未披露 |
|------|------------|------------------|--------|
| **Contextual Omni Representation** | Caption 不能只写目标画面 | 还要写「上下文↔目标」「上下文内部元素」关系，且音视频、多镜头联合描述；语言当可泛化的任务接口 | 专用 caption 模型结构、数据配比 |
| Caption 管线成本 | 素材太长 | 「大部分素材需要消耗 **100K token** 的推理，最终得到平均约 **4K** token」 | 这 100K 跑在哪套模型上 |
| **H3-VAE** | 序列太长、2K 太贵 | 换代 tokenizer：重建 + 易学性 + 约 4× 有效序列 | 与 Hailuo-02 tokenizer 的逐项对比表 |
| **Omni Transformer** | 任务墙 / 架构过巧 | 丢掉 Hailuo-02 架构；Attention/FFN 通用，模态差放在 AdaLN | 层数 / 头数 / hidden size |
| **In-context Regeneration** | 2K 细节 | 低分结果 + 原上下文再生成，而非独立 SR | 2K 的具体像素规格、步数、是否另有蒸馏权重 |

博客定价叙事（**未给绝对价，仅相对口径**）：默认提供 2K；2K 每秒价格不到「主流模型」的 1/3，768p 不到主流 720p 的 1/2。上线请以开放平台价目为准。

---

## 六、与相邻路线怎么放

| 对照 | H3 的位置 |
|------|-----------|
| 经典视频 DiT（先出静音再配乐） | H3 是 **单 Transformer、单去噪环、音画联合**；更接近「原生 A/V」而不是两段流水线。原理层仍是潜空间去噪，见 [视频生成详解](../../foundation/generative/video/视频生成详解.md) |
| 字节 Seedance 2.0 | 同属「一次前向出画+声」赛道；Seedance 以 API / 产品为主、权重未开。案例见 [doubao](../doubao/豆包视频交互技术深度调研报告.md) |
| 可灵 / Veo / Wan | 仍是「按镜头选模型」的 2026 格局；H3 的差异化是 **开源 Base + 多模态参考上限写进模型卡** |
| MiniMax **M 系列** | 对话 / Agent / 代码；协议是 `chatcompletion_v2` + OpenAI 兼容。H3 走 **视频异步任务 API**（`/v1/videos` 或 `video-generation-v2-*`），两套不要共用客户端假设 |

---

## 七、许可证（工程必读，非法务意见）

`MiniMax H3 Community License`（2026-08-02）。许可方主体：**Nanonoble Pte. Ltd.**。要点：

| 条款 | 含义 |
|------|------|
| 适用领土 | **全球，排除美国、欧盟、英国、韩国**。排除区要商用 / 部署须另洽授权；模型卡链了 [申请表](https://huggingface.co/MiniMaxAI/MiniMax-H3)（License 节 Application form，仅美 / 欧 / 英 / 韩） |
| 费用 | 领土内 royalty-free；年营收超过 **2000 万美元**的商业产品须事先书面授权（`api@minimax.io`，标题 `MiniMax H3 licensing - authorization request`） |
| 品牌 | 使用 H3 的商业产品 UI **须显著展示「MiniMax H3」** |
| 蒸馏禁令 | **不得用 H3 或其输出去改进其它 AI 模型**（含蒸馏、中间表示、合成数据训练） |
| 托管义务 | 对外提供生成服务须落实与 AUP 相当的内容防护、举报与处置 |
| Encoder | Qwen3-VL-32B 部分走 **Apache-2.0**，与 H3 Community License 叠在同一套权重里 |
| 准据法 | 香港特别行政区法律与法院 |

完整文本：[HF LICENSE](https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/LICENSE)。上线前法务以原文为准。

---

## 八、未披露边界

| 项 | 状态 |
|----|------|
| 完整 H3 Tech Report | 官方预告，本快照未见 |
| Hailuo-02 被抛弃的具体结构 | 只说「会带来额外复杂性」 |
| Context-IR / Regenerator 的模型规模与是否蒸馏 | 未开源、未给参数量 |
| 训练数据构成、token 量、卡时 | 未披露 |
| 绝对单价（元/秒） | 只有相对「主流」的倍数叙事 |
| 稀疏注意力的模式 / 块大小 | 「后续单独发布」 |
| 开源权重是否含全部 33B（含 AdaLN） | 官方说「发布完整权重以便微调」；推理时可丢掉 ~13B AdaLN。以实际 checkpoint 为准 |

---

## 九、参考来源

**官方**

- [MiniMax H3：打破任务和模态的边界](https://www.minimaxi.com/blog/minimax-h3)（2026-07-31）
- [MiniMax H3: An Open Model Breaking the Boundaries…](https://www.minimax.io/blog/minimax-h3)
- [Open General Intelligence: MiniMax H3 Is Now Open Source](https://www.minimax.io/news/minimax-h3-open-source)
- [Hugging Face · MiniMaxAI/MiniMax-H3](https://huggingface.co/MiniMaxAI/MiniMax-H3)
- [GitHub · MiniMax-AI/MiniMax-H3](https://github.com/MiniMax-AI/MiniMax-H3)
- [MiniMax H3 Community License](https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/LICENSE)

**相邻**

- 部署与 API：[MiniMax-H3本地部署与API接入.md](./MiniMax-H3本地部署与API接入.md)
- fal 平台与人像适配器：[fal全景](../fal/fal全景与生态.md) · [People LoRA](../fal/MiniMax-H3-Realism-People-LoRA.md)
- 视频原理：[视频生成详解](../../foundation/generative/video/视频生成详解.md)
- 产业层：[landscape.md](../../landscape.md) §4.5
- 三线总图：[MiniMax全景与产品线.md](./MiniMax全景与产品线.md) ｜ 文本：[M3](./MiniMax-M3全景与架构.md) ｜ 音频：[Speech 与 Music3](./MiniMax音频线Speech与Music3.md)
- M 系接口：[providers · 各大厂商代表模型总览](../providers/各大厂商代表模型总览.md)
