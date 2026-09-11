# Qwen-Omni 系列全景调研

> 调研时间：2026-09-11 ｜ 范围：阿里通义 Qwen-Omni 全模态系列（开源权重线 + 百炼 API 线 + Realtime 实时线）
> **口径约定**：`官方`=阿里云百炼文档 / 通义技术报告 / 官方模型页；`社区`=第三方报道与解读（显式标注，不当结论用）；`推断`=本文基于机制的分析。官方未披露项一律标注「未披露」，不臆造。

---

## 一、摘要（TL;DR）

1. **阿里是唯一「开源权重 + 官方实时 API」双轨并行**的玩家：豆包 SeedRealtime 未开源未开放 API，智谱 GLM-Realtime 未开源但 API 开放，只有 Qwen 同时给出 Apache-2.0 权重（30B-A3B）与生产级 Realtime 接口。
2. **技术路线是「解耦」而非「糅在一起」**：Thinker（多模态理解 + 文本推理）与 Talker（流式语音生成）是两个模块，Talker 直接消费 Thinker 的隐状态 → 这既保住了文本/视觉能力不退化，又用多码本 + 轻量因果 ConvNet 把语音首包压下来。
3. **产品线要分清三条**（最易混淆）：开源权重线（`Qwen3-Omni-30B-A3B-*`）、API 离线线（`qwen3-omni-flash`，非实时）、**API 实时线**（`*-realtime`，本文重点）。
4. **实时线走「逐档放能力」的渐进策略**：`tools` / `enable_search` / `semantic_vad` / 音频格式细粒度配置等**只在新档位生效**（2026-09 时点为 `qwen3.5-omni-*` 系列），旧档位仍可用但功能受限——选型时必须先对齐「档位 → 能力矩阵」。
5. **工程约束是硬约束**：视频侧本质是**抽帧上传**（JPG/JPEG、≤1080P、单帧 base64 ≤256KB、建议 1~2 fps），不是传视频流；VAD 关闭时模型回复期间必须停止输入（退化为半双工）。

---

## 二、系列谱系（时间线）

| 时间 | 事件 | 意义 | 来源性质 |
|------|------|------|----------|
| 2025-03-26 | **Qwen2.5-Omni**（开源 7B） | 首次提出 **Thinker–Talker** 架构；用位置嵌入融合音视频时间对齐（TMRoPE 口径） | 官方仓库（QwenLM/Qwen2.5-Omni）／社区 |
| 2025-09-15 | 快照 `qwen3-omni-flash-realtime-2025-09-15` | Realtime 线最早可查快照（官方模型页快照列表） | 官方 |
| 2025-09-22 | **Qwen3-Omni 技术报告**（arXiv:2509.17765） | Thinker–Talker **MoE**、全模态无退化 SOTA 的主张 | 官方（论文） |
| 2025-09-26 | **Qwen3-Omni 正式发布 + 开源**（30B-A3B 族） | 权重 Apache-2.0 公开，含 Instruct / Thinking / Captioner | 官方（论文/仓库）／社区 |
| 2025-12-01 | 快照 `qwen3-omni-flash-realtime-2025-12-01` | 增加音色数量等迭代；功能与主版本等同 | 官方 |
| 2025-12-11 | **Qwen3-Omni-Flash** 上线 API | 离线/半实时全模态 API（混合思考、≤150s 音视频） | 社区（官方页未标日期） |
| 2026-03-30 | **Qwen3.5-Omni** 发布 | 社区口径称 215 项任务 SOTA、256K 上下文、Plus/Flash/Light 分档 | 社区（官方 SDK 文档可见型号名） |
| 2026-09 | 官方 SDK 文档出现 `qwen3.5-omni-plus-realtime` / `qwen3.5-omni-flash-realtime` | 实时线进入 3.5 代，补齐 `tools`/`enable_search`/`semantic_vad` | 官方 |

> 关键观察：从 Qwen2.5-Omni（7B 开源）到 Qwen3-Omni（30B-A3B 开源）再到 Qwen3.5-Omni，**每一代都同时更新「开源权重」与「API 档位」两条腿**，而实时线（`-realtime`）独立于开源权重演进——**开源的 30B-A3B 并不是百炼实时 API 背后的那个模型**，这是选型/成本测算时最容易踩的认知坑。

---

## 三、三条产品线（先分清，再谈能力）

| 维度 | ① 开源权重线 | ② API 离线线 | ③ **API 实时线** |
|------|--------------|--------------|------------------|
| 代表型号 | `Qwen3-Omni-30B-A3B-Instruct` / `-Thinking` / `-Captioner` | `qwen3-omni-flash`、`qwen-omni-turbo` | `qwen3-omni-flash-realtime`、`qwen3.5-omni-plus/flash-realtime`、`qwen-omni-turbo-realtime` |
| 开放形式 | **Apache-2.0 权重**，自部署 | 百炼 API，请求-响应/流式 | 百炼 API，**WebSocket 长连接** |
| 输入 | 文本 / 图像 / 音频 / 视频 | 文本 + **单一**其他模态（图片/音频/视频） | 文本 + 音频流 + **视频帧流** |
| 输出 | 文本（Instruct 另有语音） | 文本 / 文本+语音 | 文本 + 语音（`output_modalities` 控制） |
| 典型用途 | 私有化、可复现评测、二次微调 | 短视频/音视频分析（≤150s） | **实时视频通话类交互** |
| 时延定位 | 取决于自部署 | 非实时 | 实时（官方未给毫秒级指标） |

**判断**：做「实时视频交互」只有 ③ 可用；做「离线音视频理解」用 ② 更便宜；做「私有化/可控/研究」才上 ①。三者能力与上下文口径并不通用。

---

## 四、型号规格对照（官方口径）

### 4.1 开源权重线（Qwen3-Omni，arXiv:2509.17765 + HF 模型卡）

| 型号 | 组件 | 输入 | 输出 | 说明 |
|------|------|------|------|------|
| `Qwen3-Omni-30B-A3B-Instruct` | Thinker + Talker | 文本/图/音/视频 | 文本 + 语音 | HF 标注总参数 **35B**（含 thinker+talker）；默认音色 `Ethan` |
| `Qwen3-Omni-30B-A3B-Thinking` | 仅 Thinker | 同上 | **仅文本** | 显式思维链，无语音输出 |
| `Qwen3-Omni-30B-A3B-Captioner` | 仅 Thinker | 音频 | 文本 | 音频细粒度描述微调版，主打低幻觉 |

- 语言覆盖（官方）：文本 **119** 种；语音理解 **19** 种；语音输出 **10** 种。
- 「30B-A3B」命名表示 MoE 稀疏（总 30B 级、激活 3B 级）；**激活参数官方模型卡未单列，勿凭命名断言精确值**。
- 音频输出采样率 24 kHz；`speaker` 内置 Ethan（男，默认）/ Chelsie（女）/ Aiden（男）。

### 4.2 API 实时线（官方模型页 + SDK 文档）

| 项目 | `qwen3-omni-flash-realtime` |
|------|------------------------------|
| 架构口径 | Thinker–Talker MoE |
| 输入模态 | Text / Image / Video / Audio |
| 输出模态 | Text / Audio |
| 上下文 | 总 65,536（最大输入 49,152 / 最大输出 16,384） |
| 语言/音色 | 文本 119 种、语音交互 20 种、音色 49 种（快照版本说明口径） |
| 快照 | `-2025-09-15`、`-2025-12-01` |
| 明确不支持 | Function Calling、结构化输出、联网搜索、前缀续写、上下文缓存、批量推理、模型调优 |

> 注：官方《Qwen-Omni》页与实时模型页在语种数量上口径略有差异（19 vs 20 种语音交互、49 音色归因于某快照），引用时以对应页面为准。

---

## 五、Realtime 线能力矩阵（选型第一张表）

以下为**官方 SDK 文档**给出的「能力 → 档位」生效关系，是本系列最实用的一张表：

| 能力 / 参数 | `qwen3.5-omni-*`-realtime | `qwen3-omni-flash-realtime` | `qwen-omni-turbo-realtime` |
|-------------|:---:|:---:|:---:|
| 音频格式细粒度配置 `input_audio_config` / `output_audio_config` | ✅ | ❌（只能用 legacy `*_format`） | ❌ |
| `semantic_vad`（语义 VAD，过滤无意义语音/背景音） | ✅ | ❌ | ❌ |
| `tools`（Function Calling） | ✅ | ❌ | ❌ |
| `enable_search`（联网搜索，与 `tools` **互斥**） | ✅ | ❌ | ❌ |
| `idle_timeout_ms`（静默超时主动引导，仅 server_vad） | ✅ | ❌ | ❌ |
| `smooth_output`（口语化/书面化） | ❌ | ✅ | ❌ |
| 生成参数可调（temperature/top_p/…） | ✅ | ✅ | ❌ |
| 默认音色 | `Tina` | `Cherry` | `Chelsie` |

**读法**：`qwen3-omni-flash-realtime` 只能「纯聊天 + 视频理解」；要**工具调用/联网/语义打断**，必须上 `qwen3.5-omni-*-realtime`。这与「老型号便宜就先用老的」的直觉冲突——功能缺失不是调参能补的。

---

## 六、计费与容量（官方）

**计费方式**：按 Token 计费（不是按时长），音/图/视**分项单价**。

`qwen3-omni-flash-realtime` 华北2（北京）原价：

| 计费项 | 元 / 百万 tokens |
|--------|------------------|
| 输入 · 文本 | 2.2 |
| 输入 · 音频 | 18.9 |
| 输入 · 图片/视频 | 3.9 |
| 输出 · 文本（输入仅文本） | 8.3 |
| 输出 · 文本（输入含图/音/视） | 15.2 |
| 输出 · **文本 + 音频**（文本不计费） | 75.1 |

- 限流：北京 / 新加坡均 **RPM 60、TPM 100,000**。
- 换算规则（官方）：音频 token ≈ `音频时长(秒) × 12.5`；图片每 `32×32` 像素 ≈ 1 token（单图最少 4、默认上限 1280）。
- **成本含义**：语音输出单价（75.1）是文本输入的 34 倍，**长回复是成本主要来源**；视频帧按 3.9 计费看似便宜，但 2 fps × 720P 的 token 量会持续累积。

---

## 七、与同业横向对比（2026-09 口径）

| 维度 | **Qwen-Omni（阿里）** | **SeedRealtime（字节）** | **GLM-Realtime（智谱）** | OpenAI Realtime | Gemini Live |
|------|------------------------|---------------------------|---------------------------|-----------------|-------------|
| 首发 | 2025-09（实时快照 09-15） | 2026-08 | 2025-01 | 2024-10 | 2025 |
| 开源权重 | ✅ Apache-2.0（30B-A3B） | ❌ | ❌ | ❌ | ❌ |
| 实时 API | ✅ 百炼（WebSocket） | ❌（仅产品内） | ✅（WebSocket） | ✅ | ✅ |
| 模态 | 文本/图/**视频帧**/音频 → 文本+音频 | 原生音视频全双工 | 视频+音频+文本 → **仅音频** | 音频为主 + 图/文 | 音频+视频+文本 |
| 轮次判断 | **服务端 VAD（声学/语义）** | 模型内生建模（宣称不依赖外部 VAD） | 服务端/客户端 VAD 可选 | 服务端 VAD | 模型内时间上下文 |
| 上下文 | 65,536（实时档） | 未披露 | 音频 8K / 视频 32K | — | — |
| 计费口径 | 按 Token，音/视分项 | 未开放 | **按分钟**（音频/视频分计） | 按 token + 音频分钟 | — |
| 透明度 | 论文 + 权重 + API 文档 | 仅博客/产品 | 仅 API 文档 | API 文档 | API 文档 |

**差异化判断**：

- **阿里的独特价值在「可复现」**：有技术报告 + 开源权重，能自建基线、做消融、跑私有数据——另两家只能黑盒调 API。
- **字节的独特价值在「全双工叙事」**：宣称节奏内生建模、不依赖外部 VAD；但 API 未开放，工程上无法用。
- **智谱的独特价值在「便宜 + 落地早」**：2025-01 就开放音视频通话 API，按分钟计费对原型验证友好，但输出只有音频、能力边界更窄。

---

## 八、判断与展望

1. **「开源权重 + 实时 API」双轨是阿里的结构性优势**，但也带来认知成本：**开源模型 ≠ API 实时模型**，两套规格、两套成本、两套能力边界。
2. **Thinker–Talker 解耦是「保能力」的最优解**：把语音生成从主干里拆出去，避免「为了会说话把文本/视觉能力训退化」——这与字节「一个模型统一建模」是两种哲学，短期阿里的路线更容易做到全模态无退化，长期谁在全双工自然度上更优仍待评测。
3. **实时线的能力是「分档解锁」的**：`tools` / `enable_search` / `semantic_vad` 目前绑定 `qwen3.5-omni-*`，说明阿里在把 Realtime 从「能聊天」推向「能办事」，选型时要按档位而非按系列选。
4. **工程上的硬天花板不是模型而是输入形态**：视频靠抽帧（1~2 fps、JPG、≤256KB/帧），本质上仍是「低频视觉采样 + 高频语音」的混合流；真正的「连续视频流原生建模」目前只有字节在讲。
5. **未披露项**（选型前必须自测）：实时版参数量与量化精度、真实端到端/首包延迟毫秒数、视频帧率与并发上限、长会话的上下文管理策略。

---

## 九、参考来源

**官方**
- [Qwen3-Omni Technical Report（arXiv:2509.17765，2025-09-22）](https://arxiv.org/abs/2509.17765)
- [Qwen3-Omni-30B-A3B-Instruct 模型卡（Hugging Face）](https://huggingface.co/Qwen/Qwen3-Omni-30B-A3B-Instruct)
- [QwenLM/Qwen3-Omni（GitHub）](https://github.com/QwenLM/Qwen3-Omni)
- [Qwen-Omni 模型说明（阿里云百炼）](https://help.aliyun.com/zh/model-studio/qwen-omni)
- [qwen3-omni-flash-realtime 模型信息（阿里云百炼）](https://help.aliyun.com/zh/model-studio/qwen3-omni-flash-realtime)
- [Python SDK 调用 Qwen-Omni 实时模型接口与参数（阿里云百炼）](https://help.aliyun.com/zh/model-studio/omni-realtime-python-sdk)
- [QwenLM/Qwen2.5-Omni（GitHub，前代架构）](https://github.com/QwenLM/Qwen2.5-Omni)

**社区（仅作线索，不作结论）**
- [阿里 Qwen3-Omni-Flash 发布：实时全模态交互，API 定价 1 元起（掘金）](https://juejin.cn/post/7582207260199977014)
- [Qwen3.5-Omni 功能介绍（阿里云开发者社区投稿，含推广，数据需以官方为准）](https://developer.aliyun.com/article/1749213)

---

## 相关笔记

- [Qwen3-Omni 技术文档.md](./Qwen3-Omni技术文档.md) —— 架构单点深挖
- [Qwen-Omni 实时接入与工程实践.md](./Qwen-Omni实时接入与工程实践.md) —— WebSocket 接入、VAD、打断、成本
- [豆包视频交互技术深度调研报告](../doubao/豆包视频交互技术深度调研报告.md) ｜ [实时多模态交互技术深度分析](../doubao/实时多模态交互技术深度分析.md)
- [GLM-Realtime 技术文档](../glm/GLM-Realtime技术文档.md)

---

*调研完 · 2026-09-11*
