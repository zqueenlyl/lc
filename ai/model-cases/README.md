# 模型案例研究（Model Cases）

本目录是 [`ai/`](../README.md) 的**案例层**（按**厂商维度**，区别于 `foundation/` 等五类技术专题）：沉淀对当前前沿模型的**案例化深度研究**，聚焦单个模型 / 产品做纵向深挖（架构、能力、边界、落地、演进）。

## 目录约定

- 每个模型或产品系列一个子目录，命名用 `kebab-case`（如 `doubao/`）。
- 每个目录内维护：全景调研、单模型技术文档、专题分析、评测/对比笔记、参考来源。
- 优先基于官方博客/论文/技术报告，第三方解读需显式标注「推断」与「未披露」。
- **内容为带日期的检索快照**（模型 ID / 端点 / 字段 / 价格），迭代极快——上线前以 `GET /v1/models` 或官方模型页校准；产业扫盲（不记版本号）见 [../landscape.md](../landscape.md)。

## 案例索引

| 目录 | 状态 | 说明 |
|------|------|------|
| [`doubao/`](./doubao/) | ✅ 已研究 | 字节跳动**豆包 / Seed** 体系视频交互技术栈（豆包 = 产品品牌，Seed = 技术品牌） |
| [`qwen/`](./qwen/) | ✅ 已研究 | 阿里通义 Qwen-Omni 系列（开源权重 + 百炼 Realtime API） |
| [`glm/`](./glm/) | ✅ 已研究 | 智谱 GLM-Realtime 实时音视频通话模型 |
| [`deepseek/`](./deepseek/) | ✅ 已研究 | DeepSeek 模型谱系与架构演进 + API 三协议接入与成本优化 |
| [`providers/`](./providers/) | ✅ 已研究 | **横切层**：各大厂商代表模型 + 模型服务 API 协议对比 |

### 厂商与协议（providers/）

内容清单：

- 《各大厂商代表模型总览.md》—— 海外 / 国内 / 开源权重 / 聚合分发四组的**代表模型、上下文、模态、协议族、端点**速查；工程选型维度；未核实清单
- 《模型服务API协议对比.md》—— **三代协议演进**（Completions → Chat Completions → Responses/Interactions）、逐家协议速查表、十类字段差异、**"假兼容"陷阱清单**、多厂商接入架构、Chat Completions → Responses 迁移清单

关键事实边界：模型 ID 均为 **2026-09-11 检索快照**，迭代极快，上线请以 `GET /v1/models` 或官方模型页校准。与 [`landscape.md`](../landscape.md) 有明确分工——**landscape 是产业扫盲层（不记版本号），本目录是工程可操作层（模型 ID / 端点 / 字段）**，两层互链不重复。MiniMax、火山方舟官方文档为 JS 单页应用，正文未能抓取，相关细节在文中标注为「未核实」。

### 豆包 / Seed（doubao/）

**品牌口径**：豆包（Doubao）是**产品品牌**（面向用户的 App / 服务），Seed 是字节的**技术品牌**（模型系列）。本目录覆盖的主体实为 **Seed 系列**（Seedance / Seedream / SeedEdit / SeedRealtime），目录名沿用产品品牌。

内容清单：

- 《豆包视频交互技术深度调研报告.md》—— 视频交互全景（Seedance / SeedEdit / SeedRealtime / Seedream / 豆包 3.0 / 世界模型）
- 《实时多模态交互技术深度分析.md》—— 专题深化：级联 vs 端到端、全双工机制
- 《SeedRealtime 技术文档.md》—— 原生音视频全双工大模型单点深挖

关键事实边界：官方未披露参数量、量化精度、具体延迟毫秒数；SeedRealtime 公开 API 未发布、未开源。

### 阿里通义（qwen/）

内容清单：

- 《Qwen-Omni系列全景调研.md》—— 系列谱系、**三条产品线**（开源权重 / API 离线 / API 实时）、Realtime 档位能力矩阵、计费与限流、与同业横向对比
- 《Qwen3-Omni技术文档.md》—— 开源权重版单点深挖：Thinker–Talker MoE、多码本 + 因果 ConvNet 替代扩散、显存与部署约束（vLLM 分支/仅 thinker serve）
- 《Qwen-Omni实时接入与工程实践.md》—— 百炼 Realtime 接入：会话参数、VAD 与打断、音视频硬约束、按帧 token 的成本估算、坑清单

关键事实边界：实时档位能力**分档解锁**（`tools` / `enable_search` / `semantic_vad` / 音频格式细配仅 `qwen3.5-omni-*`-realtime 可用）；视频侧本质是**抽帧上传**（JPG、≤1080P、base64 ≤256KB、建议 1~2 fps）；**开源权重模型 ≠ 百炼线上实时模型**，规格/能力/成本不可混用；实时版参数量、量化、真实延迟均未披露。

### 智谱（glm/）

内容清单：

- 《GLM-Realtime技术文档.md》—— 定位与发布背景、模型档位（9B Flash / 32B Air）、能力清单、「2 分钟记忆」三重口径辨析、未披露清单
- 《音视频通话接入与工程实践.md》—— WebSocket 事件协议、VAD 两模式（server / client）与调参、音视频工程约束、按分钟成本估算、坑清单

关键事实边界：仅提供 API（**未见权重开源**、无论文、无延迟毫秒指标）；输出**只有音频**；`tools` 目前**只支持语音通话**；`usage` 字段暂返回 0，计费不可自核；视频帧率由客户端决定（官方无规定）。

### DeepSeek（deepseek/）

内容清单：

- 《DeepSeek技术路线与架构演进.md》—— 官方版本时间线、模型 ID 沿革、**三代注意力架构**（MLA → DSA → CSA + HCA）、V4 双规格与训练课程、长上下文经济学、未披露边界
- 《DeepSeek API接入与成本优化.md》—— 三套协议入口（Chat Completions / Responses / Anthropic）对照、思考模式三档、硬盘缓存机制、峰谷定价、降本优先级与成本算例、13 条工程坑

关键事实边界：DeepSeek 是**唯一同时提供三套协议入口**的平台；**最强档 `deepseek-v4-pro` 不支持图像理解**（只有 `deepseek-flash` 支持）；Anthropic 侧**未识别的模型名会静默降级**为 flash，日志模型名 ≠ 真实模型；Responses API **完全无状态**（不支持 `previous_response_id` / `store`）。V4 的架构细节（CSA/HCA、mHC、Muon、FP4 QAT）来自**第三方对技术报告的解读**，官方 API 文档未披露；训练资源、数据构成、Serving 栈均**未披露**。

### 三家横向速查（实时音视频交互赛道）

| 维度 | 豆包 SeedRealtime | 阿里 Qwen-Omni Realtime | 智谱 GLM-Realtime |
|------|-------------------|--------------------------|-------------------|
| 首发 | 2026-08 | 2025-09（最早快照） | **2025-01** |
| 开放形式 | 仅产品（无 API、未开源） | **API + 开源权重（Apache-2.0）** | 仅 API |
| 视频输入 | 原生音视频全双工流 | 抽帧上传（JPG，1~2 fps） | 抽帧上传（JPG，帧率自定） |
| 输出 | 语音 + 文本 | 文本 + 语音 | **仅音频** |
| 轮次/打断 | 模型内生建模（宣称不依赖外部 VAD） | 服务端 VAD（声学/语义）+ 打断 | server / client VAD 可选 |
| 工具调用 | 支持（产品内） | 支持（仅 3.5 档位） | 支持（仅语音通话） |
| 上下文 | 未披露 | 65,536 | 音频 8K / 视频 32K |
| 计费 | 未开放 | 按 token（音/视分项） | 按分钟（音/视分计） |
| 透明度 | 博客 + 产品 | **论文 + 权重 + API 文档** | 仅 API 文档 |

## 待研究案例（候选）

- 字节跳动 Seedance / Seedream / SeedEdit（视频生成与编辑，单点深挖）
- OpenAI Realtime / Google Gemini Live（实时多模态，补齐海外对照）
- 其它 2026 年新发布的多模态与视频交互模型
