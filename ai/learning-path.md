# 学习地图

> 位置：`ai/learning-path.md`（原题 `知识点地图`，原 `llm/知识点.md`，2026-09 并入 `ai/` 时更名）。§1 基模 / §2 Agent 的正文分别落在 [`foundation/`](./foundation/) 与 [`agent/`](./agent/)，§3 后端软件工程为跨域索引。
> 三大知识域：**基础 LLM（基模）→ Agent 工程化 → 后端软件工程**
> 学习顺序建议：③ 是地基（已有）→ ① 是认知 → ② 是落地。
> 外部课程（CMU 11-768 / Stanford CS329Z·CS329A·CS146S / MIT）按优先级排序、并映射回本库模块 → [courses.md](./courses.md)

---
## 1、基础 LLM 知识（基模）

### 1.1 Transformer 基础

> **先读总揽**：[环节00-总揽与环节导航.md](./foundation/transformer/环节00-总揽与环节导航.md) —— 宏观主流程 + 环节导航总表 + 结构全景图（附 AIGC 扩展）
> 每个环节一份详解文档（干什么 / 怎么干 / 方法对比 / 优缺点 / 面试题）：
> - 入口三站：环节 01 Tokenizer → [环节01-Tokenizer分词详解.md](./foundation/transformer/环节01-Tokenizer分词详解.md) ｜ 环节 02 Embedding → [环节02-Embedding查表详解.md](./foundation/transformer/环节02-Embedding查表详解.md) ｜ 环节 03 位置编码/RoPE（零基础一步步版）→ [环节03-位置编码详解.md](./foundation/transformer/环节03-位置编码详解.md)
> - 核心机制：环节 04 Attention（含数值手算 + 可运行代码）→ [环节04-Attention注意力详解.md](./foundation/transformer/环节04-Attention注意力详解.md) ｜ 环节 05 FFN·MoE → [环节05-FFN激活与MoE详解.md](./foundation/transformer/环节05-FFN激活与MoE详解.md) ｜ 环节 06 残差·归一化 → [环节06-残差连接与归一化详解.md](./foundation/transformer/环节06-残差连接与归一化详解.md)
> - 组装与目标：环节 07 架构与 RNN/LSTM 演进 → [环节07-Block堆叠与整体架构详解.md](./foundation/transformer/环节07-Block堆叠与整体架构详解.md) ｜ 环节 08 输出头与训练目标（与环节 04 数值走查连体）→ [环节08-输出头与训练目标详解.md](./foundation/transformer/环节08-输出头与训练目标详解.md)
> - 前史与纵深：RNN/LSTM 本体全体系（BPTT 数值手推 / LSTM·GRU / 双向·Seq2Seq / 现代类 RNN 谱系）→ [RNN知识整理.md](./foundation/transformer/RNN知识整理.md)
> - 生命周期：环节 09 训练管线 → [环节09-训练管线详解.md](./foundation/transformer/环节09-训练管线详解.md) ｜ 环节 10 推理解码与 KV Cache → [环节10-推理解码与KV缓存详解.md](./foundation/transformer/环节10-推理解码与KV缓存详解.md) ｜ 环节 11 服务化与推理引擎 → [环节11-服务化与推理引擎详解.md](./foundation/transformer/环节11-服务化与推理引擎详解.md)

- **主流程（一条流水线）**：Tokenizer（BPE/Unigram/SentencePiece）→ Embedding 查表 → 位置编码（RoPE 主流/ALiBi）→ N×(Attention → 残差+归一化 → FFN → 残差+归一化) → LM Head → 训练走 CE / 推理走采样
- **架构全貌**：Encoder-Decoder（T5/BART）vs Decoder-only（GPT 系，当前主流）；并行不偷看靠因果 Mask
- **RNN/LSTM 前史（本体纵深）**：串行 + 有损压缩 vs 注意力并行 + 无损可见；BPTT 梯度消失是分水岭；现代"类 RNN"（线性注意力 / RWKV / Mamba）借"状态复用"回归 —— 详见 [RNN知识整理.md](./foundation/transformer/RNN知识整理.md)
- **Attention 机制**：Self-Attention、QKV 投影、缩放点积、Multi-Head Attention（MHA）
  - 变体优化：MQA（多查询）、GQA（分组查询，**现在主流**）、MLA（DeepSeek 的多头潜在注意力）、FlashAttention（IO 优化）
- **位置编码**：绝对（Sinusoidal/可学习）、相对、RoPE（旋转位置编码，主流）、ALiBi（短训长外推）
- **其他组件**：FFN / SwiGLU 激活（MoE 在此替换）、LayerNorm / RMSNorm（Pre-LN）、残差连接
- **关键认知**：Attention 的 \(O(n^2)\) 复杂度 → 长上下文成本、KV Cache 的由来（GQA/MLA 为省它而生）

### 1.2 主流模型（DeepSeek、混元等）

- **DeepSeek**：V3（MoE 基座）、R1（推理模型，GRPO 强化学习）、V3.2 / R1 蒸馏版、V4 / V4-Flash / V4.1-Flash
  - 关键技术：MLA 注意力、DeepSeekMoE（细粒度专家 + 共享专家）、无辅助损失负载均衡；长上下文两代换代 **DSA**（V3.2）→ **CSA + HCA 序列轴压缩**（V4）
  - 注：V4-Flash 官方以 **DeepSeek Harness 极简模式**作为测试框架（模型与 Agent 框架协同演进，见 2.8 / 2.10）
  - **案例纵深**（[model-cases/deepseek/](./model-cases/deepseek/)）：谱系时间线 + 三代注意力架构 + 长上下文经济学 → [DeepSeek技术路线与架构演进.md](./model-cases/deepseek/DeepSeek技术路线与架构演进.md)；三套协议入口 + 思考模式 + 硬盘缓存 + 峰谷定价 → [DeepSeek API接入与成本优化.md](./model-cases/deepseek/DeepSeek%20API接入与成本优化.md)
  - 训练报告精读 **待写**（`DeepSeek-V3训练报告详解.md`：14.8T token / FP8 / DualPipe / $5.6M 总账；`DeepSeek-R1训练报告详解.md`：GRPO 四阶段 / 蒸馏，已刊 Nature）——原 `../deepseek/` 目录已不存在
- **混元（腾讯）**：Turbo / T1 推理模型，多模态与长文能力
- **其他必知**：GPT 系列、Claude 系列、Gemini、Qwen（阿里，开源生态强）、Llama（Meta）
- **关注维度**：上下文长度、推理/非推理模型差异、开源 vs 闭源、许可证商用限制、评测榜单（MMLU / GPQA / SWE-bench / Aider）
- **厂商代表模型与接口速查**（2026-09 快照）：各厂商当前模型 ID / 上下文 / 协议族 / API 端点 → [providers/各大厂商代表模型总览.md](./model-cases/providers/各大厂商代表模型总览.md)；同一功能在不同厂商的字段差异与"假兼容"陷阱 → [providers/模型服务API协议对比.md](./model-cases/providers/模型服务API协议对比.md)；产业层扫盲（公司 / 产品 / 榜单）见 [ai/landscape.md](landscape.md)

### 1.3 训练

- **三阶段范式**：Pre-training（预训练）→ SFT（监督微调）→ 对齐（RLHF / DPO / GRPO）—— 对齐专题（RL 基础 / PPO→DPO→GRPO→RLVR 谱系 / 选型表 / R1 四阶段 / 奖励黑客）见 [强化学习与模型对齐专题](./foundation/rl/环节00-总揽与环节导航.md)
- **预训练**：数据清洗配比、Scaling Law（参数/数据/算力的关系）、涌现能力 —— 详解见 [环节09-训练管线详解.md](./foundation/transformer/环节09-训练管线详解.md)
- **微调**：全参微调 vs PEFT（LoRA / QLoRA / P-Tuning），何时该微调、何时不该（优先 RAG/Prompt）—— 同上
- **分布式训练**：数据并行 / 张量并行 / 流水线并行、ZeRO（1/2/3）、Megatron-LM、显存优化（重计算、混合精度）

### 1.4 推理

- **采样参数**：`temperature`（分布拉平/拉陡，T→0 趋近贪心）、`top-p`（核采样截断候选集）、`top-k`
  - 实践：二者只调其一；结构化/代码场景 T=0；创意场景 0.9+；需固定 seed 才能完全复现
- **推理流程**：Prefill（并行算 prompt）→ Decode（逐 token 自回归），两阶段瓶颈不同
- **核心优化**：
  - **KV Cache**：缓存注意力键值，避免重复计算（显存大户）
  - **PagedAttention / vLLM**：显存分页管理，大幅提升吞吐
  - **Continuous Batching**：请求级动态批处理
  - **量化**：FP8 / INT8 / INT4、GPTQ / AWQ / GGUF（本地部署常用）
  - **投机解码 / 前缀缓存**：降延迟与成本
- **推理引擎**：vLLM、SGLang、TensorRT-LLM、Ollama（本地）、LMDeploy —— 原理详解见 [环节11-服务化与推理引擎详解.md](./foundation/transformer/环节11-服务化与推理引擎详解.md)；本地实操（llama.cpp / Ollama / LM Studio / MLX 安装·参数·API·实测）见 [本地推理运行时操作手册](runtime/local-inference/README.md)

### 1.5 部署

- **服务化**：OpenAI 兼容 API（事实标准）、vLLM / TGI 起服务
- **性能指标**：首 token 延迟（TTFT）、每 token 延迟（TPOT）、吞吐（tokens/s/QPS）
- **流式输出**：SSE / WebSocket，前端打字机效果
- **成本与容量**：GPU 选型（A100/H800/4090）、显存估算（参数量 × 精度 + KV Cache）、按 Token 计费的成本模型
- **网关层**：模型路由、多Key 轮询、限流、降级、缓存

### 1.6 多模态

- **视觉**：ViT、CLIP（图文对齐，机制详解见 [多模态理解与统一模型详解.md](./foundation/multimodal/多模态理解与统一模型详解.md)）、视觉理解（OCR/图表/截图问答）
- **语音**：ASR（语音识别，Whisper 系）、TTS（语音合成）、端到端语音对话
- **生成**：文生图（Diffusion / DiT）、文生视频
- **AIGC 全谱系与工程化**：文/图/音/视频/3D/代码生成范式（自回归 vs 扩散）、审核/版权/评测 —— 库入口 [00-AIGC总揽与多模态地图.md](./foundation/generative/00-AIGC总揽与多模态地图.md)：图像扩散 [图像扩散模型详解.md](./foundation/generative/diffusion/图像扩散模型详解.md) ｜ 视频 [视频生成详解.md](./foundation/generative/video/视频生成详解.md) ｜ 音频语音 [音频与语音详解.md](./foundation/generative/audio-speech/音频与语音详解.md) ｜ 多模态统一 [多模态理解与统一模型详解.md](./foundation/multimodal/多模态理解与统一模型详解.md)
- **实时多模态交互（案例研究库）**：级联 vs 端到端、全双工与打断机制、抽帧上传 / VAD / 上下文工程 —— 案例 [model-cases/](./model-cases/README.md)：豆包 SeedRealtime ｜ 阿里 [Qwen-Omni](./model-cases/qwen/Qwen-Omni系列全景调研.md) ｜ 智谱 [GLM-Realtime](./model-cases/glm/GLM-Realtime技术文档.md)
- **工程关注**：多模态 RAG（图片/表格的解析与检索）、Token 消耗、跨模态对齐方案

### 1.7 MoE（Mixture of Experts，混合专家）

- **原理**：把 FFN 拆成多个"专家"，Router（门控网络）每次只激活 Top-K 个 → **参数量大、激活参数少**
- **优势**：同等推理成本下模型容量更大；训练更快
- **代价与挑战**：显存占用高（所有专家都要驻留）、负载均衡（防止专家坍缩）、训练不稳定、路由抖动
- **代表**：Switch Transformer、Mixtral、**DeepSeekMoE**（细粒度专家 + 共享专家隔离）、Qwen3-MoE
- **面试点**：MoE 是"用显存换算力/容量"的取舍

---

## 2、基础 Agent 知识（工程化）

> 核心心法：**Agent 应用 = 传统后端 + 一个生成式组件；LLM 是外部不可靠服务，重试/超时/限流/降级/缓存全部照搬。**

> **先读总揽**：[环节00-总揽与环节导航.md](./agent/环节00-总揽与环节导航.md) —— 一条主循环 + 支撑面/横切的宏观总揽、环节导航总表与结构全景图
> 每环节一份详解（干什么 / 怎么干 / 方法对比 / 工程红线 / 面试题）：
> - 决策循环：环节 01 决策范式 → [环节01-决策与推理范式详解.md](./agent/环节01-决策与推理范式详解.md) ｜ 环节 02 提示上下文 → [环节02-提示与上下文工程详解.md](./agent/环节02-提示与上下文工程详解.md) ｜ 环节 03 记忆状态 → [环节03-记忆与状态详解.md](./agent/环节03-记忆与状态详解.md)
> - 手脚与知识：环节 04 工具调用 → [环节04-工具调用详解.md](./agent/环节04-工具调用详解.md) ｜ 环节 05 MCP → [环节05-工具接入协议MCP详解.md](./agent/环节05-工具接入协议MCP详解.md) ｜ 环节 06 RAG → [环节06-检索增强RAG详解.md](./agent/环节06-检索增强RAG详解.md)
> - 编排与团队：环节 07 编排循环 → [环节07-编排与循环控制详解.md](./agent/环节07-编排与循环控制详解.md) ｜ 环节 08 多Agent协作 → [环节08-多Agent协作详解.md](./agent/环节08-多Agent协作详解.md)
> - 工程门槛（横切）：环节 09 评测可观测 → [环节09-评测与可观测详解.md](./agent/环节09-评测与可观测详解.md) ｜ 环节 10 生产工程化 → [环节10-生产级工程化详解.md](./agent/环节10-生产级工程化详解.md)

### 2.1 Agent 决策范式

- **ReAct（Reasoning + Acting）**：
  - 循环：`Thought（思考）→ Action（行动/调工具）→ Observation（观察结果）` ↺ 直到 `Final Answer`
  - 对比：纯推理（CoT，只想不做 → 幻觉）vs 纯行动（Act-only，只做不想 → 盲目）
  - 工程三要点：**终止条件**（Final Answer 或最大步数，防死循环）、**上下文膨胀**（观察累积撑爆窗口 → 需摘要/截断）、**失败反馈**（工具报错当 Observation 回填，让模型换策略）
- **其他范式**：Plan-and-Execute（先规划再执行）、Reflexion（反思重试）、Tree-of-Thought（多路径搜索）
  - 推理范式全家桶详解（CoT / Self-Consistency / ToT / GoT / Reflexion / ReAct，含成本权衡与工程选型）见 [环节01-决策与推理范式详解.md](./agent/环节01-决策与推理范式详解.md)

### 2.2 提示工程（Prompt）

- System Prompt 设计、Few-shot、CoT、指令分层与结构化（思维链原理与变体详解见 [环节01-决策与推理范式详解.md](./agent/环节01-决策与推理范式详解.md)）
- 结构化输出：JSON Mode、Schema 约束、`tool_choice` 强制
- Prompt 注入与越狱防护（安全基线）

### 2.3 工具调用（Function Calling / Tool Use）

- **机制**：模型输出结构化调用请求（函数名 + 参数），应用侧执行后回填结果
- **协议细节**：`tools` 声明（JSON Schema）、`tool_choice`（auto/required/指定函数）、`arguments` 为 JSON 字符串、必须回填 `role:"tool"` 消息（按 `tool_call_id` 对应）、流式时 arguments 需累积拼接
- **提取结构化数据**：把 Schema 当工具参数 + `tool_choice` 强制调用 → 从 `arguments` 拿数据（比让模型裸写 JSON 稳一个量级）

### 2.4 结构化输出与强校验

- 三层闭环：**引导**（JSON Mode / Function Calling）→ **校验**（Pydantic / Zod / JSON Schema）→ **修复**（错误回填重试，2-3 次）→ **兜底**（默认值 / 规则引擎 / 报错）
- **正确率评测**：无约束解码下跨模型 JSON 正确率、语法合法 vs 内容正确、约束解码的边界 → [结构化输出正确率评测](reliability/structured-output/正确率评测.md)
- 校验维度：必填、类型、枚举、范围、格式（正则）、嵌套、业务规则（`@field_validator`）
- 常见坑：markdown 代码块包裹、字段命名漂移、多余字段（`extra="forbid"`）、数字被输出成字符串（严格模式）

### 2.5 上下文与记忆机制

- **工作记忆**：当前任务状态、中间结果、步骤栈（LangGraph 的 `State`）→ 每次推理都注入，易失
- **会话记忆**：本次对话完整历史（消息列表、工具调用记录）→ 全程在上下文，会话级
- **长期记忆**：用户画像、稳定事实、沉淀知识 → 存向量库/DB，默认**不可见**，靠检索召回才注入上下文
- **可见性规律**：可见 = 是否在上下文窗口内；长期记忆是"有求才现"，关键是召回准确度与固化（consolidation）策略

### 2.6 RAG（检索增强生成）

- **基础流水线**：解析 → 清洗 → 切分（chunking）→ Embedding → 检索 → 拼接 → 生成
- **检索质量优化**：
  - **Hybrid Search**：BM25（关键词精确匹配）+ 向量（语义）融合，RRF 排序融合最鲁棒
  - **BM25 要点**：IDF × 词频饱和 × 文档长度归一化；`k1`（~1.2 词频饱和）、`b`（~0.75 长度归一化）；中文需分词（ik/jieba）
  - **Rerank 精排**：双塔粗排 + 交叉编码器精排（收益/成本比最高的优化）
  - **查询侧**：Query Rewriting、HyDE（假设文档嵌入）、RAG-Fusion（多查询 + RRF）
- **主要变种**：
  | 变种 | 机制 | 解决什么 |
  |------|------|---------|
  | Naive RAG | 单次检索拼上下文 | 基线 |
  | Advanced RAG | 每环节单独优化（改写/混合检索/Rerank/压缩）| 召回与相关性 |
  | Parent-Child | 小块检索、返回父大块 | 精准 vs 上下文完整 |
  | Self-RAG | 自我反思：要不要检索、结果是否支持 | 无关检索拉低质量 |
  | CRAG | 纠错：置信度低则换检索器/联网 | 知识库覆盖不足 |
  | Adaptive RAG | 按复杂度路由（不检索/单跳/多跳）| 成本与延迟 |
  | GraphRAG | 知识图谱 + 社区摘要 | 跨实体关系、全局性问题 |
  | Agentic RAG | 检索作为 Agent 工具，自主编排 | 复杂场景（终极形态）|
- **演进脉络**：Naive → Advanced/Modular → Agentic

### 2.7 MCP（Model Context Protocol）

- **定位**：开放协议，标准化 "应用（Host）↔ 外部工具/数据源（Server）" 的接入（类比 JDBC / USB-C）
  - 与 Function Calling 的关系：**不是竞争，是叠加**。FC 管"模型怎么请求调用"（模型能力），MCP 管"应用怎么发现并连接一堆工具"（系统协议）；MCP 提供的工具最终仍以 FC 格式喂给模型
- **传输**：stdio（本地子进程） / HTTP+SSE / Streamable HTTP
- **版本口径（重要）**：最新稳定版 **2026-07-28** 已**无状态化**——删除 `initialize` 握手与 `Mcp-Session-Id`，新增 `server/discover`，反向交互改 **MRTR**。以下为经典模型（≤2025-11-25）口径；**各版变更特性见 [MCP 版本演进与变更特性](agent/mcp/版本演进.md)**
- **协议分层**：JSON-RPC 2.0 消息 + 生命周期（initialize / notifications/initialized，**2026-07 起已删**）+ 三大能力（tools / resources / prompts，各版未变）
- **接口清单**（经典版 → 2026-07 变化）：
  - 生命周期：`initialize`（版本协商 + 能力声明）、`notifications/initialized` → 改为**每请求 `_meta`** + `server/discover`
  - Tools：`tools/list`、`tools/call`、`notifications/tools/list_changed` → 变化通知统一走 `subscriptions/listen`
  - Resources：`resources/list`、`resources/templates/list`、`resources/read`、`notifications/resources/updated`；`resources/subscribe` → 改 `subscriptions/listen`
  - Prompts：`prompts/list`、`prompts/get`、`notifications/prompts/list_changed`
  - 通用：`ping`、`logging/setLevel`（**已删**）、`completion/complete`、`sampling/createMessage`（服务端反向调模型 → 改 **MRTR**，且整体**弃用**）
- **错误码**：-32700 解析错误 / -32601 方法未找到 / -32602 无效参数 / -32603 内部错误 / -32002 资源未找到（**2026-07 起改为 -32602**）
- **关键约束**：initialize 之前不能发其他请求（**2026-07 起无握手**，改为每请求 `_meta` 校验版本，不符返回 `UnsupportedProtocolVersionError`）；capabilities 声明驱动客户端行为；日志必须走 stderr（stdio 传输下不能污染协议流）

### 2.8 Agent 框架与编排

- **LangChain**（生态老大哥，宜当"概念字典"，勿当生产依赖）：
  - 核心模块：Models（模型封装）、Prompts、Chains（线性链）、Agents（早期 ReAct 风格）、Memory、Retrieval、Callbacks
  - 价值：**概念启蒙 + 快速原型**——把 RAG、Agent、Memory、Tool 抽象成标准模块，生态最大、模板最全，学概念首选手册
  - 争议：抽象过厚、1.x 后 API 收敛但历史包袱重、黑盒难调优、版本升级破坏多 → 生产环境口碑分化，不少团队用半年后迁回自研薄封装或裸调模型 SDK（2026 年此类案例仍高频）
- **LangGraph**（推荐，生产级；LangChain 团队出品，但定位完全不同）：
  - 核心概念：**State**（可序列化全局状态，节点共享）、**Node**（执行单元）、**Edge / conditional_edges**（有向边 + 条件路由）、**Checkpointer**（检查点持久化 → 断点续跑/恢复）、**interrupt**（暂停等人工输入，Human-in-the-loop）、**并行分支与循环**（图天然表达循环，告别链式）
  - 定位：**Agent = 状态机编程**——编排从"线性链"升级为"有向图"，循环/分支/并行/中断全部显式可控
  - 为什么生产级：每步状态可见可测、checkpoint 断点续跑、图可序列化版本化、配 LangSmith 全链路 trace；LangGraph Platform 提供部署托管与可视化调试
  - 现状：正在从实验工具进化为**企业级 Agent 编排的事实标准之一**（采用率远高于 LangChain 本体）
- **对比速查**：
  | 维度 | LangChain | LangGraph |
  |------|-----------|-----------|
  | 编排模型 | 线性 Chain | 有向图（循环/分支/并行） |
  | 状态管理 | 隐式（调用链传参） | 显式 State 图 |
  | 生产特性 | 弱 | Checkpointer / 中断 / 人机协同 |
  | 适用场景 | 原型、概念学习、简单链 | 生产级复杂多步 Agent |
  | 采用现状 | 生态大、生产口碑分化 | 企业级 Agent 编排事实标准之一 |
- 其他：LlamaIndex（RAG 数据侧）、AutoGen / CrewAI（多 Agent 协作）、OpenAI Agents SDK / Anthropic Claude Code（官方轻量路线）、自研状态机（大厂主流）
- 认知：**Agent = 状态机编程**；多 Agent 编排模式：主管-下属、流水线、辩论竞争
- **`Model + Harness = Agent`**（DeepSeek Harness 提出的架构公式）：
  - Harness = **模型驾驭层**：环绕模型的一整套控制与编排工具链（上下文管理、工具调用与权限、记忆、规划循环、可观测、人机协同）
  - 核心洞察：**模型能力 ≠ Agent 能力**，同一模型配不同 Harness 效果差异巨大——Harness 才是 Agent 能力的放大器与稳定器
  - 工程启示：做 Agent 应用时，模型选型只解决"聪不聪明"，Harness 设计决定"能不能稳定干活"；这也是自研 Agent 框架 vs 直接用模型的分水岭

### 2.9 生产级工程化（落地门槛）

- **评估（Eval）**：离线数据集 + 指标（忠实度、相关性、召回率）、在线质量回归 → Agent 上线最大门槛（详解见 [环节09-评测与可观测详解.md](./agent/环节09-评测与可观测详解.md)）
- **可观测性**：Langfuse / LangSmith，trace + token 成本 + 延迟 + 质量分
- **可靠性**：重试、幂等、断点续跑（checkpoint）、降级（无 LLM 时走规则引擎）
- **成本工程**：模型分级路由、语义缓存、Token 压缩、批处理
- **安全**：Prompt 注入防护、工具权限最小化、敏感数据脱敏、审计日志
- **交互体验**：SSE / WebSocket 流式、前端打字机、长任务的进度反馈
- **上线流程**：灰度、A/B、回滚、效果看板

### 2.10 Agent 产品与工具生态

| 工具 | 定位 |
|------|------|
| CodeBuddy | AI 编程助手（IDE 内代码生成、工程理解、多文件改写）|
| Cursor | AI 原生代码编辑器（Agent 模式、代码库索引）|
| Codex | OpenAI 的编程 Agent（云端异步任务、代码修改与验证）|
| **DeepSeek Harness** | DeepSeek 首款 Agent 产品（2026-08 发布，桌面端智能体编程，对标 Claude Code / Codex）；提出 `Model + Harness = Agent`，Harness 即"模型驾驭层"（上下文、工具、记忆、规划、可观测的编排控制层）|
| WorkBuddy | 办公协作类 AI 助手（工作流/知识/协作场景）|
| Pi | 对话式个人助手（情感化、陪伴向交互）|
| trpc-go-agent | 基于 tRPC-Go 生态的 Go 语言 Agent 开发框架 |

> 关注点：这些产品背后是同一套技术栈（工具调用 + 上下文工程 + 记忆 + 人机协同），拆解它们的交互设计与工程实现，是最好的反向学习材料。
> Code Agent 这类编程智能体的完整拆解（验证器闭环 / code retrieval / 安全 / 评估）见 `CodeAgent详解.md`（待写）

---

## 3、基础后端开发知识（传统软件工程）

> 9 年经验区：**不补基础，重在体系化与原理级掌握**（面试与架构决策都考"为什么"）。

### 3.1 计算机基础

- **网络**：HTTP/1.1 / 2 / 3、HTTPS/TLS、TCP（握手、拥塞控制、TIME_WAIT）、DNS、WebSocket
- **操作系统**：进程/线程/协程、I/O 多路复用（epoll）、零拷贝、内存管理、上下文切换成本
- **数据结构与算法**：哈希表、跳表、B+ 树、堆、图算法；常见复杂度分析与高频题

### 3.2 语言与并发

- **主语言**（Go / Java / Python / C++）：内存模型、GC 机制、性能剖析（pprof / jstack）
- **并发模型**：锁（互斥/读写/自旋）、CAS、AQS、线程池参数依据
  - Go：GMP 调度、Channel、Context、内存逃逸
  - Java：JMM、锁升级、并发容器、JVM 调优
- **异步编程**：回调 / Future / async-await、事件循环、背压

### 3.3 接口与通信

- **协议**：RESTful 设计、gRPC（protobuf、流式）、GraphQL（了解）
- **序列化**：JSON / Protobuf / MsgPack，兼容性与性能取舍
- **网关**：路由、鉴权、限流、灰度、协议转换；API 版本管理

### 3.4 数据存储

- **关系型（MySQL/PostgreSQL）**：
  - 索引：B+ 树原理、最左前缀、覆盖索引、索引失效场景
  - 事务：ACID、隔离级别、MVCC、锁（行锁/间隙锁/next-key）、死锁
  - 性能：慢查询、执行计划、分库分表、读写分离、连接池
- **缓存（Redis）**：数据结构与使用场景、持久化（RDB/AOF）、过期与淘汰、分布式锁
  - 三大问题与方案：穿透（布隆过滤器/空值缓存）、击穿（互斥重建）、雪崩（随机 TTL/多级缓存）
  - **缓存一致性**：Cache-Aside、延迟双删、订阅 binlog 更新
- **搜索引擎（ES）**：倒排索引、分词（中文 ik）、BM25 评分、写入与查询优化
- **其他**：MongoDB（文档）、对象存储、时序数据库

### 3.5 消息队列

- **模型**：发布订阅 vs 队列、分区与消费组（Kafka）、消费位点
- **可靠性三连**：不丢（确认机制/刷盘）、不重（幂等消费）、有序（分区内有序/全局有序代价）
- **治理**：堆积处理、死信队列、重试与退避、延时消息、事务消息

### 3.6 分布式与高并发

- **理论基础**：CAP/BASE（详解见 `CAP与BASE.md`，待写）、一致性模型、FLP、拜占庭（了解）
- **共识**：Raft（选主/日志复制/安全性）、Paxos（思想）、ZAB
- **高并发手段**：限流（令牌桶/滑动窗口/分布式限流）、熔断、降级、隔离（舱壁）、削峰填谷
- **幂等设计**：幂等键、状态机、去重表 / 唯一索引
- **分布式事务**：2PC / TCC / 本地消息表 / Saga / 最大努力通知，按一致性要求选型
- **其他**：分布式 ID（雪花/号段）、分布式锁（Redis vs etcd/ZK）、一致性哈希、数据分片与迁移

### 3.7 架构设计

- **演进**：单体 → 模块化单体 → 微服务（何时该拆、何时不该拆）
- **DDD**：限界上下文、聚合根、领域事件、事件风暴（用于划定服务边界）
- **架构模式**：
  - **CQRS**（命令查询职责分离）：读写模型/存储分离，源自单一职责原则；常与事件溯源搭配但**独立**；适合读多写少、复杂查询视图，简单 CRUD 别用
  - **事件驱动 / 事件溯源 / Saga**：以事件为真相源、状态重建、流程编排
- **参考书**：DDIA《设计数据密集型应用》、《凤凰架构》、《微服务架构设计模式》

### 3.8 服务治理与运维

- **治理组件**：注册发现（Nacos/Consul/etcd）、配置中心、负载均衡、健康检查、优雅上下线
- **可观测性三件套**：Metrics（Prometheus + Grafana）、Logs（结构化日志）、Traces（OpenTelemetry + Jaeger/Tempo），三者通过 trace_id 打通
- **稳定性工程**：SLO/SLI、容量规划、全链路压测、混沌工程、故障演练、变更管理与回滚预案

### 3.9 工程化与交付

- **容器与编排**：Docker（镜像分层/多阶段构建）、K8s（Pod/Deployment/StatefulSet/HPA/Operator）、Helm
- **CI/CD**：流水线、测试门禁、制品管理、GitOps
- **IaC**：Terraform 管理云资源
- **测试策略**：测试金字塔、契约测试、混沌注入、覆盖率的正确用法

### 3.10 安全

- 常见攻击与防御：SQL 注入、XSS、CSRF、SSRF、越权（水平/垂直）
- 认证授权：Session / JWT / OAuth2 / OIDC、RBAC/ABAC、密钥与证书管理
- 数据安全：加密（传输/存储）、脱敏、审计日志、合规（个人信息保护）

### 3.11 云原生与平台（延展）

- Service Mesh（Istio 流量管理/可观测）、Serverless/FaaS、边缘计算
- 云中间件选型与成本优化（托管 MySQL/Redis/Kafka/对象存储）
- 平台工程：内部开发者平台、自助化基础设施

---

## 附：三条主线如何串起来

```
后端工程（③）                     LLM 基模（①）                Agent 工程（②）
─────────────────              ─────────────────          ─────────────────
服务拆分/状态机设计 ──映射──▶    推理/采样/上下文 ──支撑──▶   ReAct 循环 / 状态机
重试/限流/降级/幂等 ──照搬──▶    API 调用/流式输出 ──支撑──▶  工具调用可靠性
缓存/索引/检索(ES/BM25) ──复用──▶ Embedding/向量库 ──支撑──▶  RAG 检索链路
监控/链路追踪/灰度 ──照搬──▶    Token 成本/延迟 ──支撑──▶   可观测 / Eval / 成本工程
MQ/任务队列          ──复用──▶    长上下文/记忆       ──支撑──▶  记忆分层 / 断点续跑
```

**一句话**：后端功底决定 Agent 能不能上生产，LLM 认知决定你知不知道它在犯什么错，Agent 工程决定两者能否组合成可靠产品。
