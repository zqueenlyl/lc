# MiniMax 全景与产品线

> 调研时间：2026-09-18 ｜ 范围：MiniMax 官方三条模态线（文本 M 系 / 视频 H 系 / 音频 Speech + Music3），组织 [`MiniMaxAI`](https://huggingface.co/MiniMaxAI)
> 口径：官方博客、HF 模型卡、已发表论文。凡未在官方页核对的标「未核实」或「第三方」。
> 不要和 [`fal/`](../fal/fal全景与生态.md) 混——fal 是另一家推理平台。

---

## 一、摘要（TL;DR）

MiniMax 按**任务族**拆线，不是「一个 Omni 包打天下」。官网导航也是 LLM / VIDEO / SPEECH & MUSIC 三栏。

| 线 | 旗舰（开源权重） | 干什么 | 论文 / 报告 |
|----|------------------|--------|-------------|
| **文本 · M 系** | [`MiniMax-M3`](https://huggingface.co/MiniMaxAI/MiniMax-M3)（约 428B / 激活 ~23B，1M 窗） | 对话、Agent、代码、图/视频**理解**（输入） | **有**：[MSA](https://arxiv.org/abs/2606.13392)、[MaxProof](https://arxiv.org/abs/2606.13473) |
| **视频 · H 系** | [`MiniMax-H3`](https://huggingface.co/MiniMaxAI/MiniMax-H3)（33B Base） | 文/图/参考 → **音视频联合生成** | **无独立 Tech Report**（博客预告「soon」，2026-09-18 仍未见） |
| **音频 · 语音** | 线上 `speech-2.8-*` 等；研究侧 MiniMax-Speech | TTS / 克隆 / 流式合成 | **有**：[MiniMax-Speech](https://arxiv.org/abs/2505.07916)（2025-05） |
| **音频 · 音乐** | [`MiniMax-Music3`](https://huggingface.co/MiniMaxAI/MiniMax-Music3) | 歌词 + 描述 → 最长约 5 分钟整曲 | 模型卡级架构说明；未见独立 arXiv |

**核心判断**：三条线的 tokenizer、协议、许可证、开源范围都不同。拿 M3 的 Chat Completions 去调 H3、拿 Speech 的 `t2a_v2` 去当 Music3、拿 H3 片里的立体声去对比 Music3 成曲，都是配错产品。H3 博客写过下一版 H 系计划吸收 M 系能力——那是路线图，**不是**现网已经合成一个模型。

纵深：文本 → [M3 篇](./MiniMax-M3全景与架构.md)；视频 → [H3 全景](./MiniMax-H3全景与架构.md) / [部署](./MiniMax-H3本地部署与API接入.md)；音频 → [Speech 与 Music3](./MiniMax音频线Speech与Music3.md)。接口速查仍见 [providers · MiniMax](../providers/各大厂商代表模型总览.md#36-minimax)。

---

## 二、三线对照（不要混规格）

```
┌──────────── M 系 对话 / Agent ────────────┐
│  文本 + 图/视频理解 → 文本（可 think）      │
│  协议：chatcompletion_v2 / OpenAI 兼容     │
└────────────────────────────────────────────┘

┌──────────── H 系 海螺视频 ────────────────┐
│  文/图/视频/音频条件 → 768p 或 2K 片+立体声 │
│  协议：video-generation-v2-* 异步任务      │
└────────────────────────────────────────────┘

┌──────────── 音频 两套 ────────────────────┐
│  Speech：文本 → 说话人声波（TTS API 为主）  │
│  Music3：歌词+caption → 整曲 WAV（开源）   │
│  协议：/v1/t2a_v2  vs  /v1/audio/speech    │
└────────────────────────────────────────────┘
```

| 维度 | M3 | H3 | Speech（线上） | Music3 |
|------|----|----|----------------|--------|
| 模态方向 | 理解为主（图/视频进、文本出） | **生成**音视频 | **生成**语音 | **生成**音乐 |
| 开源 | 完整 MoE 权重 | 只开 H3-Base；IR / 2K 仍托管 | 研究论文 + 部分演示；旗舰在 API | 开源权重 |
| 规模口径 | ~428B / 激活 ~23B | 33B 稠密（~13B AdaLN 可卸载） | 未披露线上参数量 | 架构：8B Global + 0.6B Local + 2.4B Flow Matching；HF 控件另标 2B（见音频篇） |
| 上下文 / 时长 | 1M token | 成片 4–15 s | 单次文本 &lt; 1 万字（API） | 最长约 5 min；9000 声学帧上限 |
| 本地推理栈 | SGLang / vLLM / Transformers | SGLang Diffusion / vLLM / Modular / ComfyUI | 以平台 API 为主 | SGLang-Omni / diffusers / ComfyUI |
| 许可证 | MiniMax Community License（以仓库原文为准，**不要直接套 H3 领土条款**） | **H3** Community License（排除美/欧/英/韩） | API ToS | 仓库 LICENSE |

国内 / 国际 API 域名仍要拆：`api.minimaxi.com` vs `api.minimax.io`。按量 Key 与 Token Plan 不可混。

---

## 三、时间线（产品线级）

| 日期 | 线 | 事件 | 来源 |
|------|----|------|------|
| 2025-05 | 语音 | MiniMax-Speech 技术报告：可学习 speaker encoder + Flow-VAE | [arXiv:2505.07916](https://arxiv.org/abs/2505.07916) |
| 更早–2026-03 | 文本 | M2 → M2.1 / M2.5 → **M2.7**（自称参与自身进化） | M2.7 博客 2026-03-18 |
| 2026-06-01 前后 | 文本 | **M3** 发布；MSA 论文 2026-06-11；MaxProof 博客 2026-06-09 | 官方博客 / arXiv |
| 2026-07-31 | 视频 | **H3** 发布；Tech Report 标后续 | [H3 博客](https://www.minimax.io/blog/minimax-h3) |
| 2026-08-02 | 视频 | H3-Base Community License / 开源 | HF LICENSE |
| 2026-08 中旬 | 音乐 | Music3 权重与 Demo（HF 组织页 Updated Aug 14） | [Music3](https://huggingface.co/MiniMaxAI/MiniMax-Music3) |
| 线上 TTS | 语音 | API 档位滚动到 `speech-2.8-hd/turbo`（仍保留 2.6 / 02 / 01） | [T2A HTTP](https://platform.minimax.io/docs/api-reference/speech-t2a-http) |

相邻、本页不展开：VTP（视觉 tokenizer / 特征提取）、M3-MXFP8 量化仓、NVIDIA NVFP4 社区量化。

---

## 四、选型怎么问

1. **要写代码 / 长会话 / 看图看视频再回答** → M3，不要 H3。
2. **要出带同期声的片子** → H3；本地只有 768p Base。
3. **要配音、克隆音色、Agent 开口** → Speech API（`speech-2.8-*`）；论文里的 MiniMax-Speech 是研究底座，不等于线上同名档。
4. **要一首完整歌** → Music3；不要用 H3 的联合音画去「唱五分钟」。
5. **论文从哪找**：M 系与 Speech 有；H3 目前只有博客 + 模型卡。

---

## 五、参考来源

- 组织：[huggingface.co/MiniMaxAI](https://huggingface.co/MiniMaxAI)
- M3 博客：[Frontier Coding, 1M Context…](https://www.minimax.io/blog/minimax-m3)
- H3 博客：[Breaking the Boundaries…](https://www.minimax.io/blog/minimax-h3)
- Speech 报告页：[minimax-ai.github.io/tts_tech_report](https://minimax-ai.github.io/tts_tech_report/)
- 本目录：[M3](./MiniMax-M3全景与架构.md) · [H3](./MiniMax-H3全景与架构.md) · [音频](./MiniMax音频线Speech与Music3.md)
