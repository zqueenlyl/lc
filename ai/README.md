# AI 技术手册

按**大类**整理的 AI / LLM 学习文档与可运行 MVP。每个专题一个文件夹：讲解（原理 / 功能 / 场景）+ 尽量无外部 API 依赖的 `mvp.py`。

> **本目录 = 技术手册层 + 原理层，同树**：横向、可跳读、速查 + MVP 在此；原理纵深（环节式长文、须按序读）也已并入同一棵树，散落在各专题内（`环节NN-*.md`），不再单列 `llm/`。
> 产业扫盲见 [landscape.md](./landscape.md)（2026-09 快照）；三大域学习地图见 [learning-path.md](./learning-path.md)。

## 目录结构

```
ai/
├── README.md                 # 本索引
├── landscape.md              # 产业扫盲：产品 / 公司 / 模型家族（六层坐标系）
├── learning-path.md          # 学习地图：基模 / Agent 工程化 / 后端 三大域
│
├── foundation/               # ① 基模：模型是什么 / 怎么造 / 怎么变强 / 怎么生成
│   ├── transformer/          #    骨架 + 环节01-11 原理长文 + 评测选型 + RL 对齐 + RNN
│   ├── reasoning/            #    推理模型 / test-time scaling
│   ├── moe/  peft-lora/  slm/  multimodal/
│   └── generative/           #    生成 + 多模态：README（手册）+ 00-AIGC总揽（模态矩阵 + 两大范式）
│       ├── diffusion/  video/  audio-speech/  world-models/
│
├── agent/                    # ② Agent 应用：把模型编成能自己干活的系统
│   ├── README.md             #    总图
│   ├── 环节00-总揽与环节导航.md   # 原理：一条主循环 + 10 环节
│   ├── 环节01-*.md ~ 环节10-*.md      # 原理长文（按序读）
│   ├── loop-engineering.md
│   └── langgraph/  mcp/  a2a/  agent-skills/  computer-use/  harness/  case-studies/
│
├── knowledge/                # ③ 知识与记忆：决定往上下文窗口里塞什么
│   └── rag/  vector-db/  knowledge-base/  memory/  context-engineering/
│
├── reliability/              # ④ 治理与上线：决定能不能上生产
│   └── guardrails/  sandbox/  eval/  structured-output/  model-routing/
│
└── runtime/                  # ⑤ 运行与加速：决定跑得多快 / 多省 / 本地 / 实时
    └── local-inference/  speculative-decoding/  voice-realtime/
```

## 五类怎么分（判断口诀）

| 大类 | 一句话 | 判断口诀 |
|---|---|---|
| [foundation](./foundation/) | 模型本体 | 「讲模型内部 / 权重 / 训练 / 生成范式」→ 归这 |
| [agent](./agent/) | 模型 → 系统 | 「讲循环 / 工具 / 协议 / 外壳」→ 归这 |
| [knowledge](./knowledge/) | 塞什么进窗口 | 「讲检索 / 记忆 / 裁剪」→ 归这 |
| [reliability](./reliability/) | 能不能上生产 | 「讲拦错 / 打分 / 隔离 / 降级」→ 归这 |
| [runtime](./runtime/) | 跑多快多省 | 「讲引擎 / 显存 / 延迟 / 量化 / 实时」→ 归这 |

## 怎么读

每个专题文件夹内：

| 文件 | 内容 |
|---|---|
| `README.md` | 技术讲解、功能作用、应用场景、相邻技术对比、落地建议、延伸阅读 |
| `mvp.py` | 可运行最小实现（`python mvp.py`，默认不调外部模型） |
| `环节NN-*.md` | 原理长文（仅 `transformer/`、`agent/` 有），须按序读 |

已有专题保持原文件名（`rag-types.md`、`agent-memory.md` 等），不强制改名。

---

## 全景索引

### ① foundation · 基模

| 主题 | 一句话 | 入口 |
|---|---|---|
| **Transformer（手册）** | 自注意力骨架；RNN/LSTM 为何被取代；因果 vs 双向 | [transformer/](./foundation/transformer/) |
| **Transformer 全链路（原理）** | 一条主线 + 两个生命周期，11 环节关卡地图 | [总揽](./foundation/transformer/环节00-总揽与环节导航.md) |
| **模型评测与选型（原理）** | 训练产出后「怎么验」、部署前「怎么选」 | [详解](./foundation/transformer/模型评测与选型方法详解.md) |
| **强化学习与模型对齐（原理）** | SFT 之后为什么要 RL：RLHF → DPO → GRPO → RLVR | [详解](./foundation/transformer/强化学习与模型对齐详解.md) |
| **RNN** | Attention 之前的历史：串行、长距离难题 | [RNN知识整理](./foundation/transformer/RNN知识整理.md) |
| **Reasoning** | 推理模型 + 测试时算力缩放（第三条缩放律） | [reasoning/](./foundation/reasoning/) |
| **MoE** | 稀疏专家混合：总参大、激活小 | [moe/](./foundation/moe/) |
| **Multimodal（手册）** | 文本 / 图 / 音 / 视频原生一体 | [multimodal/](./foundation/multimodal/) |
| **多模态理解与统一模型（原理）** | CLIP 对齐 → VLM 三代接入 → 统一模型 | [详解](./foundation/multimodal/多模态理解与统一模型详解.md) |
| **SLM** | 小模型与端侧：便宜、快、可私有化 | [slm/](./foundation/slm/) |
| **PEFT / LoRA** | 只训少量参数就能适配领域 | [peft-lora/](./foundation/peft-lora/) |
| **Generative（手册）** | 生成侧入口：扩散 / 视频 / 语音 / 世界模型 | [generative/](./foundation/generative/) |
| **AIGC 总揽** | 模态矩阵 + 两大生成范式 + 公共底座 | [总揽](./foundation/generative/00-AIGC总揽与多模态地图.md) |
| **Diffusion** | 扩散模型：图像 / 视频 / 音频生成主路径 | [diffusion/](./foundation/generative/diffusion/) ｜ [图像扩散模型详解](./foundation/generative/diffusion/图像扩散模型详解.md) |
| **视频生成（原理）** | 视频 = 图 + 时间：时空 patch / 3D VAE / DiT | [视频生成详解](./foundation/generative/video/视频生成详解.md) |
| **音频与语音（原理）** | ASR / TTS 三代演化 / 端到端语音对话 | [音频与语音详解](./foundation/generative/audio-speech/音频与语音详解.md) |
| **World Models** | 预测「世界如何演化」，而不只是下一个 token | [world-models/](./foundation/generative/world-models/) |

### ② agent · Agent 应用

| 主题 | 一句话 | 入口 |
|---|---|---|
| **Agent（总图）** | 有目标、调工具、看反馈再试；聊天/工作流/Agent 三分 | [agent/](./agent/) |
| **Agent 全链路（原理）** | 一条主循环 + 支撑面 / 横切的宏观总揽与环节导航 | [总揽](./agent/环节00-总揽与环节导航.md) |
| **循环工程** | 从提示工程到「规划-执行-验证」闭环 | [loop-engineering.md](./agent/loop-engineering.md) |
| **LangGraph** | 图编排 + 8 个 demo | [langgraph/](./agent/langgraph/) |
| **MCP** | Agent ↔ 工具 / 数据源的 USB-C | [mcp/](./agent/mcp/) ｜ [版本演进](./agent/mcp/版本演进.md) |
| **A2A** | Agent ↔ Agent 的对等委托协议 | [a2a/](./agent/a2a/) |
| **Computer Use** | 看屏幕、点鼠标、操作浏览器/桌面 | [computer-use/](./agent/computer-use/) |
| **Agent Skills** | 把领域流程打成可发现、可复用技能包 | [agent-skills/](./agent/agent-skills/) |
| **Harness** | 编码 Agent 的循环外壳：工具 / 插件 / 子 Agent | [harness/](./agent/harness/) |

**原理长文（环节 01–10，按序读）**：决策与推理范式 → 提示与上下文 → 记忆与状态 → 工具调用 → MCP → RAG → 编排与循环 → 多 Agent 协作 → 评测与可观测 → 生产级工程化，全部在 [agent/](./agent/)；关卡地图见 [环节00-总揽与环节导航](./agent/环节00-总揽与环节导航.md)。另有 [langgraph/01–04](./agent/langgraph/) 为**框架实操教程**（自带 4 篇教程 + 8 个 demo，编号独立于环节系列）。

**开源 Agent 项目案例**（把理论拼成生产，目录见 [case-studies/](./agent/case-studies/)）：

| 项目 | 一句话 | 入口 |
|---|---|---|
| **commerce-agents** | Anthropic 电商 Agent 范本：门禁 + 围栏 + 人审，安全靠代码强制 | [commerce-agents](./agent/case-studies/commerce-agents.md) |
| **pi** | 极简编码 harness：最小核（4 工具）+ 外部沙箱 | [pi](./agent/case-studies/pi.md) |
| **trpc-agent-go** | 腾讯 Go 生产级 Agent 框架：GraphAgent + 自我进化 + 可观测 | [trpc-agent-go](./agent/case-studies/trpc-agent-go.md) |

### ③ knowledge · 知识与记忆

| 主题 | 一句话 | 入口 |
|---|---|---|
| **RAG** | 检索增强生成：Naive → Agentic 全谱系 | [rag/](./knowledge/rag/) |
| **向量数据库** | Milvus/Qdrant/pgvector 等：ANN 索引 + 语义检索底座 | [vector-db/](./knowledge/vector-db/) |
| **知识库** | 知识库类型五维整理 | [knowledge-base/](./knowledge/knowledge-base/) |
| **Memory** | Agent 工作 / 短期 / 长期记忆 | [memory/](./knowledge/memory/) |
| **Context Engineering** | 在合适时机把合适信息放进窗口 | [context-engineering/](./knowledge/context-engineering/) |

### ④ reliability · 治理与上线

| 主题 | 一句话 | 入口 |
|---|---|---|
| **Structured Output** | JSON Schema / Function Calling，让输出可机器消费 | [structured-output/](./reliability/structured-output/) ｜ [正确率评测](./reliability/structured-output/正确率评测.md) |
| **Guardrails** | 输入过滤、工具门禁、输出校验、人审 | [guardrails/](./reliability/guardrails/) |
| **Sandbox** | 沙箱隔离执行：不可信代码/命令关进受控环境跑 | [sandbox/](./reliability/sandbox/) |
| **Eval** | 自定义评测 + Trace；LLM 是考试，Agent 是上机 | [eval/](./reliability/eval/) |
| **Model Routing** | 按任务/成本/失败自动选模型 | [model-routing/](./reliability/model-routing/) |

### ⑤ runtime · 运行与加速

| 主题 | 一句话 | 入口 |
|---|---|---|
| **本地推理运行时** | llama.cpp / Ollama / LM Studio / MLX：安装、参数、本地 API、实测（原理见环节11） | [local-inference/](./runtime/local-inference/) |
| **Speculative Decoding** | 小模型草稿 + 大模型一次校验，加速解码 | [speculative-decoding/](./runtime/speculative-decoding/) |
| **Voice / Realtime** | 双向音视频流，延迟预算 &lt; 500ms | [voice-realtime/](./runtime/voice-realtime/) |

---

## 技术栈怎么叠

```
应用：Computer Use / Voice / Skills / Harness / 案例
编排：LangGraph · 循环工程 · Memory · Context Engineering
协议：MCP（工具） · A2A（Agent 互操作）
治理：Guardrails · Eval · Model Routing · Structured Output
知识：RAG · 向量库 · 知识库
模型：Transformer · Reasoning · Multimodal · SLM · MoE · PEFT
生成：Diffusion · Video · Audio/Speech · World Models
加速：Speculative Decoding · 量化
本地运行：llama.cpp · Ollama · LM Studio · MLX
```

MCP 连工具，A2A 连 Agent，二者互补而不是二选一。Agent 总图见 [agent/](./agent/)。RAG / Memory / Context Engineering 解决「塞什么进窗口」，Guardrails / Eval 解决「能不能上线」。

## 跑 MVP

多数专题是纯标准库：

```bash
cd ai/<大类>/<专题>
python3 mvp.py
```

LangGraph 相关 demo 见 [langgraph/demos/requirements.txt](./agent/langgraph/demos/requirements.txt)。
