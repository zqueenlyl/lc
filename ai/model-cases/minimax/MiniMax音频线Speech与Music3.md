# MiniMax 音频线：Speech 与 Music3

> 调研时间：2026-09-18 ｜ 范围：MiniMax **语音 TTS** 与 **文生音乐**，不是 H3 片内立体声、不是 M3 的文本回复
> 产品线地图：[《MiniMax 全景与产品线》](./MiniMax全景与产品线.md)。原理对照：[音频与语音](../../foundation/generative/audio-speech/README.md)。

---

## 一、摘要（TL;DR）

音频在 MiniMax 里是**两条产品**，只共享部分声学想法（Flow-VAE）：

| | **Speech（说话）** | **Music3（唱歌/成曲）** |
|--|-------------------|------------------------|
| 输入 | 文本（+ 音色 / 情绪 / 停顿标记） | **歌词** + **音乐描述**（caption） |
| 输出 | 人声朗读 / 克隆 | 最多约 **5 分钟** 的完整歌曲（人声+编曲） |
| 主入口 | 开放平台 `POST /v1/t2a_v2`（HTTP / WebSocket） | 开源权重 [`MiniMaxAI/MiniMax-Music3`](https://huggingface.co/MiniMaxAI/MiniMax-Music3) |
| 论文 | **有**：[MiniMax-Speech](https://arxiv.org/abs/2505.07916)（2025-05） | 模型卡级；Flow-VAE 改编自 Speech 再为音乐重训 |
| 本地 | 研究演示 / Collection；旗舰体验在 API | SGLang-Omni、diffusers Modular、ComfyUI |

H3 的 32 kHz 立体声是**视频联合去噪**出来的同期声，既不是 TTS 也不是 Music3。三套音频不要互相比「像不像 MiniMax 的声音」。

---

## 二、Speech：TTS 与克隆

### 2.1 研究底座（2025-05）

[技术报告页](https://minimax-ai.github.io/tts_tech_report/) / [arXiv:2505.07916](https://arxiv.org/abs/2505.07916) / HF Collection [`MiniMax-Speech`](https://huggingface.co/collections/MiniMaxAI/minimax-speech)。

自回归 Transformer TTS。要点：

- **可学习 speaker encoder**：从参考音频抽音色，**不要求参考音频的转写** → 零样本克隆。
- **Flow-VAE** 提重建。
- 宣称 32 语；客观克隆指标（WER / Speaker Similarity）与当时 TTS Arena 位置见论文，本页不抄过期榜。
- 扩展（不改基座）：情绪 LoRA、文本描述出音色（T2V）、专业克隆 PVC（再微调音色特征）。

这是**论文模型**。线上档位已经迭代到 Speech-02 / 2.6 / **2.8**，能力与延迟以 API 文档为准，不要用 2025-05 的 Arena 名次给 2.8 报价。

### 2.2 开放平台档位（2026-09-18 文档枚举）

来源：[T2A HTTP](https://platform.minimax.io/docs/api-reference/speech-t2a-http)。`model` 枚举含：

`speech-2.8-hd`、`speech-2.8-turbo`、`speech-2.6-hd`、`speech-2.6-turbo`、`speech-02-hd`、`speech-02-turbo`、`speech-01-hd`、`speech-01-turbo`。

WebSocket 指南对 2.8/2.6/02 的一句话定位：2.8-hd 偏拟真与 sound tags；2.8-turbo 偏流畅；2.6 偏低延迟 / Agent；02 偏节奏稳定与复刻相似度。具体延迟毫秒**未在本页实测**。

工程约束（文档）：

- 文本 &lt; **10000** 字；&gt;3000 字建议流式。
- 停顿：`<#x#>`，x ∈ [0.01, 99.99] 秒，插在可念文本之间，不能连用。
- 鉴权 Bearer；国际 `api.minimax.io`，国内域名按控制台。克隆走单独的 `/v1/voice_clone`（先传音频）。

**未披露**：线上 2.8 是否仍是论文那套 speaker encoder、参数量、是否与开源 Collection 同权。

---

## 三、Music3：歌词到整曲

### 3.1 它做什么

条件：歌词（可带 `[Verse]` / `[Chorus]` 等**独占一行**的结构标签）+ 详细音乐描述。输出：最长约五分钟、主题/人声/编曲能撑过长结构的立体声。模型卡推荐 Structured Caption 三段：Global Metadata（曲风 BPM 调性）/ Vocal Details / Arrangement。

可用 `npx skills add MiniMax-AI/MiniMax-Music3 --skill music-caption-rewriter` 把短描述扩成结构化 caption。

### 3.2 架构（模型卡 / GitHub README）

层次自回归 + 连续隐状态合成，**不是**「HF 控件上写的 2B 一个数」那么简单：

```
歌词 + caption
        │
        ▼
┌─ Global LLM 8B（Qwen3-8B 初始化）── 逐帧预测 RVQ 第 1 个语义 codebook（16384 词表）
└─ Local LLM 0.6B ──────────────── 帧内补其余 7 个声学 codebook（各 1024）
        │ 融合两路最后隐状态
        ▼
   Flow Matching 2.4B → Flow-VAE latent → Decoder 123M → 32 kHz / 16-bit 立体声 WAV
```

Tokenizer 训练用 8 层 RVQ；**推理出波形不走离散 tokenizer 解码器**，而走融合隐状态。Flow-VAE 从 MiniMax-Speech 改编、按音乐动态范围重训。

HF 仓库 Safetensors 摘要仍可能显示 **2B params**——那是托管页统计/切片，与上面 8B+0.6B+2.4B 的模块表不一致。引用规模时写模块表，并标注控件数字。

diffusers 文档有一处写成 DAC 解码 **44.1 kHz**，模型卡/README 写 **32 kHz**。以你实际 `pipe.sampling_rate` / 文件头为准。

### 3.3 怎么跑

```bash
hf download MiniMaxAI/MiniMax-Music3 --local-dir /path/to/minimax_ttm
sgl-omni serve --model-path MiniMaxAI/MiniMax-Music3 --port 8000
```

复用 **speech** 风格端点：`POST /v1/audio/speech`。`input` = 歌词，`instructions` = 音乐描述。`max_new_tokens` = 声学帧上限，**25 fps**；9000 帧是硬顶（文档；约六分钟量级，产品文案仍写五分钟）。

diffusers：`ModularPipeline.from_pretrained("MiniMaxAI/MiniMax-Music3")`。官方片段称整精度约 24GB；CPU offload ~22GB；再对 LM 做 leaf offload 可进 8GB（更慢）。合并前需按模型卡指定的 diffusers commit 安装。

限制（模型卡）：只要 CUDA；当前**非流式**；文本 prompt ≤ 5000 token；结构标签是生成控制不是乐谱保证——BPM/调性/歌词未必逐条命中。

---

## 四、工程坑

1. **Speech API ≠ Music3 本地服务。** 一个是 `t2a_v2` + `voice_setting`，一个是 `/v1/audio/speech` + `instructions`。
2. **H3 同期声 ≠ 这两条。** 视频里的对白/环境声来自 H3-AudioVAE 联合去噪。
3. **论文 Speech ≠ 线上 2.8。** 选型、报价、语种以平台文档为准。
4. **歌词标签必须独占行。** 标签和词写在同一行会被丢掉（Music3 输入契约）。
5. **Music3 规模不要抄 HF 的 2B。** 用 8B / 0.6B / 2.4B / 123M。
6. **采样率两套文档。** 先看输出 WAV 头。
7. 声音克隆、整曲人声涉及肖像与版权；Speech 论文的零样本克隆尤其要授权链路。

---

## 五、参考来源

- [MiniMax-Speech 论文](https://arxiv.org/abs/2505.07916) · [报告站](https://minimax-ai.github.io/tts_tech_report/)
- [T2A HTTP](https://platform.minimax.io/docs/api-reference/speech-t2a-http) · [T2A WebSocket 指南](https://platform.minimax.io/docs/guides/speech-t2a-websocket)
- [HF MiniMax-Music3](https://huggingface.co/MiniMaxAI/MiniMax-Music3) · [GitHub MiniMax-Music3](https://github.com/MiniMax-AI/MiniMax-Music3)
- [ComfyUI · Music 3](https://docs.comfy.org/tutorials/audio/minimax/minimax-music-3)
- 视频联合声：[H3 全景](./MiniMax-H3全景与架构.md)
