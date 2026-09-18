# AI 技术手册

按**大类**整理的 AI / LLM 学习文档与可运行 MVP。每个专题一个文件夹：讲解（原理 / 功能 / 场景）+ 尽量无外部 API 依赖的 `mvp.py`。

> **本目录 = 技术手册层 + 原理层 + 案例层，同树**：横向、可跳读、速查 + MVP 在此；原理纵深（环节式长文、须按序读）也已并入同一棵树，散落在各专题内（`环节NN-*.md`），不再单列 `llm/`。
> 产业扫盲见 [landscape.md](./landscape.md)（2026-09 快照）；三大域学习地图见 [learning-path.md](./learning-path.md)；外部课程（CMU / Stanford / MIT）优先级与学习产出映射见 [courses.md](./courses.md)（快照型）；**FDE（前沿部署工程师）岗位要求与成长路径**见 [fde.md](./fde.md)（快照型）；按厂商纵向深挖见 [model-cases/](./model-cases/)（快照型，会过期）。

## 目录结构

```
ai/
├── README.md                 # 本索引
├── landscape.md              # 产业扫盲：产品 / 公司 / 模型家族（六层坐标系）
├── learning-path.md          # 学习地图：基模 / Agent 工程化 / 后端 三大域
├── courses.md                # 外部课程路线：CMU 11-768 / CS329Z / CS329A / CS146S / MIT（按优先级）
├── fde.md                    # 职业与落地视角：FDE 岗位要求 / 三支柱能力模型 / 现场五关 / 转型路径
│
├── model-cases/              # 案例层：按厂商 / 产品纵向深挖（快照型，模型 ID / 端点 / 价格会过期）
│   └── deepseek/  qwen/  glm/  doubao/  minimax/  providers/
│
├── foundation/               # ① 基模：骨架 / 训练 / 变体 / 模态（分组见 foundation/README）
│   ├── transformer/          #    骨架 + 环节01-11 + 评测/长上下文横切 + RNN
│   ├── rl/                   #    对齐：环节00-08 + 推理侧 test-time 横切 + 选型总表
│   ├── peft-lora/            #    LoRA 几何直觉：环节00-04 + mvp.py
│   ├── moe/  slm/            #    变体/档位（薄手册）
│   └── generative/           #    模态家族：00 地图 + 生成 + 理解
│       ├── diffusion/  video/  audio-speech/  world-models/
│       └── multimodal/       #    理解侧（原 foundation/multimodal）
│
├── agent/                    # ② Agent 应用：把模型编成能自己干活的系统
│   ├── README.md             #    总图
│   ├── 环节00-总揽与环节导航.md   # 原理：一条主循环 + 10 环节
│   ├── 环节01-*.md ~ 环节10-*.md      # 原理长文（按序读）
│   ├── loop-graph/  #    循环与图深讲（栈总览在 agent/README §七）
│   ├── mcp/  a2a/  agent-skills/  computer-use/  harness/
│   └── case-studies/            #    案例层：commerce-agents / pi / mini-swe-agent / trpc-agent-go / langgraph
│
├── knowledge/                # ③ 知识与记忆：决定往上下文窗口里塞什么
│   └── rag/  vector-db/  knowledge-base/  memory/  context-engineering/
│
├── reliability/              # ④ 治理与上线：决定能不能上生产
│   ├── sandbox/              #    环节系列（README + 环节00–13 + 13 notebook + 选型总表）
│   └── guardrails/  eval/  structured-output/  model-routing/
│
└── runtime/                  # ⑤ 运行与加速：决定跑得多快 / 多省 / 本地 / 实时
    └── local-inference/  speculative-decoding/  voice-realtime/
```

## 五类怎么分（判断口诀）

| 大类 | 一句话 | 判断口诀 |
|---|---|---|
| [foundation](./foundation/) | 模型本体 | 「讲模型内部 / 权重 / 训练 / 生成范式」→ 归这 |
| [agent](./agent/) | 模型 → 系统 | 「讲循环 / 图编排 / 工具 / 协议 / 外壳」→ 归这 |
| [knowledge](./knowledge/) | 塞什么进窗口 | 「讲检索 / 记忆 / 裁剪」→ 归这 |
| [reliability](./reliability/) | 能不能上生产 | 「讲拦错 / 打分 / 隔离 / 降级」→ 归这 |
| [runtime](./runtime/) | 跑多快多省 | 「讲引擎 / 显存 / 延迟 / 量化 / 实时」→ 归这 |

> **案例层 [model-cases/](./model-cases/) 不在这五类里**：五类按**技术维度**分，案例层按**厂商维度**分（纵向深挖单个模型 / 产品），与 [landscape.md](./landscape.md)、[learning-path.md](./learning-path.md) 同属横向入口。

## 怎么读

每个专题文件夹内：

| 文件 | 内容 |
|---|---|
| `README.md` | 技术讲解、功能作用、应用场景、相邻技术对比、落地建议、延伸阅读 |
| `mvp.py` | 可运行最小实现（`python mvp.py`，默认不调外部模型） |
| `环节NN-*.md` | 原理长文（`transformer/`、`agent/`、`rl/`、`peft-lora/` 有），须按序读 |

已有专题保持原文件名（`rag-types.md`、`agent-memory.md` 等），不强制改名。

---

## 全景索引

### ① foundation · 基模

分组与挂靠规则见 [foundation/README](./foundation/README.md)。

**骨架**

| 主题 | 一句话 | 入口 |
|---|---|---|
| **Transformer（手册）** | 自注意力骨架；RNN/LSTM 为何被取代 | [transformer/](./foundation/transformer/) |
| **Transformer 全链路（原理）** | 一条主线 + 两个生命周期，11 环节 | [总揽](./foundation/transformer/环节00-总揽与环节导航.md) |
| **评测与选型 / 长上下文 / RNN** | 横切 + 前史 | [选型](./foundation/transformer/模型评测与选型方法详解.md) · [长上下文](./foundation/transformer/长上下文工程详解.md) · [RNN](./foundation/transformer/RNN知识整理.md) |

**训练**

| 主题 | 一句话 | 入口 |
|---|---|---|
| **强化学习与模型对齐** | SFT 之后为什么要 RL：RLHF → DPO → GRPO → RLVR | [总揽](./foundation/rl/环节00-总揽与环节导航.md) |
| **推理模型 / test-time scaling** | 第三条缩放律：推理时多花算力换准确率 | [横切](./foundation/rl/推理侧搜索与test-time-scaling.md) |
| **PEFT / LoRA** | 只训少量参数；几何直觉见环节课 | [手册](./foundation/peft-lora/) · [环节00](./foundation/peft-lora/环节00-总揽与环节导航.md) |

**变体 / 档位**

| 主题 | 一句话 | 入口 |
|---|---|---|
| **MoE** | 稀疏专家：总参大、激活小 | [moe/](./foundation/moe/) |
| **SLM** | 小模型与端侧 | [slm/](./foundation/slm/) |

**模态**（生成 + 理解，同一张地图）

| 主题 | 一句话 | 入口 |
|---|---|---|
| **Generative（手册）** | 生成侧入口：扩散 / 视频 / 语音 / 世界模型 | [generative/](./foundation/generative/) |
| **AIGC 总揽** | 模态矩阵 + 两大生成范式 + 公共底座 | [00](./foundation/generative/00-AIGC总揽与多模态地图.md) |
| **Diffusion / Video / Audio / World** | 各模态生成 | [diffusion](./foundation/generative/diffusion/) · [video](./foundation/generative/video/) · [audio](./foundation/generative/audio-speech/) · [world-models](./foundation/generative/world-models/) |
| **Multimodal（理解）** | CLIP → VLM → 统一模型 | [手册](./foundation/generative/multimodal/) · [详解](./foundation/generative/multimodal/多模态理解与统一模型详解.md) |

### ② agent · Agent 应用

| 主题 | 一句话 | 入口 |
|---|---|---|
| **Agent（总图）** | 有目标、调工具、看反馈再试；聊天/工作流/Agent 三分 | [agent/](./agent/) |
| **Agent 全链路（原理）** | 一条主循环 + 支撑面 / 横切的宏观总揽与环节导航 | [总揽](./agent/环节00-总揽与环节导航.md) |
| **循环与图** | 五层栈总览（agent/README §七）+ Loop / Graph 深讲 | [agent/README](./agent/README.md) · [loop-graph/](./agent/loop-graph/) |
| **LangGraph** | 图编排 + 8 个 demo（案例层） | [langgraph/](./agent/case-studies/langgraph/) |
| **MCP** | Agent ↔ 工具 / 数据源的 USB-C | [mcp/](./agent/mcp/) ｜ [版本演进](./agent/mcp/版本演进.md) |
| **A2A** | Agent ↔ Agent 的对等委托协议 | [a2a/](./agent/a2a/) |
| **Computer Use** | 看屏幕、点鼠标、操作浏览器/桌面 | [computer-use/](./agent/computer-use/) |
| **Agent Skills** | 把领域流程打成可发现、可复用技能包 | [agent-skills/](./agent/agent-skills/) |
| **Harness** | 编码 Agent 的循环外壳：工具 / 插件 / 子 Agent | [harness/](./agent/harness/) |

**原理长文（环节 01–10，按序读）**：决策与推理范式 → 提示与上下文 → 记忆与状态 → 工具调用 → MCP → RAG → 编排与循环 → 多 Agent 协作 → 评测与可观测 → 生产级工程化，全部在 [agent/](./agent/)；关卡地图见 [环节00-总揽与环节导航](./agent/环节00-总揽与环节导航.md)。另有 [langgraph/01–04](./agent/case-studies/langgraph/) 为**框架实操教程**（自带 4 篇教程 + 8 个 demo，编号独立于环节系列）。

**开源 Agent 项目 / 框架案例**（把理论拼成生产，目录见 [case-studies/](./agent/case-studies/)）：

| 项目 / 框架 | 一句话 | 入口 |
|---|---|---|
| **commerce-agents** | Anthropic 电商 Agent 范本：门禁 + 围栏 + 人审，安全靠代码强制 | [commerce-agents](./agent/case-studies/commerce-agents.md) |
| **pi** | 极简编码 harness：最小核（4 工具）+ 外部沙箱 | [pi](./agent/case-studies/pi.md) |
| **mini-swe-agent** | 约 100 行的编码 Agent：只有 bash、线性历史、无状态执行（SWE-bench Bash Only 榜外壳） | [mini-swe-agent](./agent/case-studies/mini-swe-agent.md) |
| **trpc-agent-go** | 腾讯 Go 生产级 Agent 框架：GraphAgent + 自我进化 + 可观测 | [trpc-agent-go](./agent/case-studies/trpc-agent-go.md) |
| **LangGraph** | 图状态机编排框架：State / Node / Edge + checkpoint / interrupt，4 篇教程 + 8 个 demo | [langgraph](./agent/case-studies/langgraph/) |

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
| **Sandbox** | 沙箱隔离执行：内核原语 / 隔离强度 / 文件系统 / 网络出口 / 凭证 / 逃逸加固 / 可观测验收 / 数据通道 / 平台化 / 跨平台机制 / 开销实测（环节 01–13） | [sandbox/](./reliability/sandbox/) |
| **Eval** | 自定义评测 + Trace；LLM 是考试，Agent 是上机 | [eval/](./reliability/eval/) |
| **Model Routing** | 按任务/成本/失败自动选模型 | [model-routing/](./reliability/model-routing/) |

### ⑤ runtime · 运行与加速

| 主题 | 一句话 | 入口 |
|---|---|---|
| **本地推理运行时** | llama.cpp / Ollama / LM Studio / MLX：安装、参数、本地 API、实测 + 操作向 notebook 01–04（原理见环节11） | [local-inference/](./runtime/local-inference/) ｜ [总揽](./runtime/local-inference/环节00-总揽与环节导航.md) |
| **Speculative Decoding** | 小模型草稿 + 大模型一次校验，加速解码 | [speculative-decoding/](./runtime/speculative-decoding/) |
| **Voice / Realtime** | 双向音视频流，延迟预算 &lt; 500ms | [voice-realtime/](./runtime/voice-realtime/) |

### ⑥ model-cases · 模型案例（按厂商纵向深挖）

> 内容为**带日期的检索快照**（模型 ID / 上下文 / 端点 / 字段 / 价格），迭代极快——**上线前务必以 `GET /v1/models` 或官方模型页校准**。分工：产业扫盲层看 [landscape.md](./landscape.md)（不记版本号），工程可操作层看这里。

| 主题 | 一句话 | 入口 |
|---|---|---|
| **DeepSeek** | 模型谱系 + 三代注意力架构（MLA → DSA → CSA/HCA）+ 三协议接入与成本优化 + V4.1-Flash KV 压缩 | [deepseek/](./model-cases/deepseek/) |
| **Qwen-Omni** | 三条产品线（开源权重 / API 离线 / API 实时）+ 实时接入工程实践 | [qwen/](./model-cases/qwen/) |
| **GLM-Realtime** | 实时音视频通话：WebSocket 事件协议 / VAD / 成本估算 | [glm/](./model-cases/glm/) |
| **豆包 / Seed** | 视频交互体系（Seedance / SeedEdit / Seedream / SeedRealtime） | [doubao/](./model-cases/doubao/) |
| **MiniMax** | 三线：文本 M3（MSA/1M）· 视频 H3（768p Base）· 音频 Speech+Music3 | [minimax/](./model-cases/minimax/) |
| **fal** | 生成媒体推理平台；H3 人像写实 LoRA（非 MiniMax 官方模块） | [fal/](./model-cases/fal/) |
| **providers（横切）** | 各厂商代表模型总览 + 服务 API 协议对比与「假兼容」陷阱 | [providers/](./model-cases/providers/) |

---

## 技术栈怎么叠

```
应用：Computer Use / Voice / Skills / Harness / 案例
编排：LangGraph · 循环与图工程 · Memory · Context Engineering
协议：MCP（工具） · A2A（Agent 互操作）
治理：Guardrails · Eval · Model Routing · Structured Output
知识：RAG · 向量库 · 知识库 · 上下文图（GraphRAG）
模型：Transformer · RL（含推理侧） · SLM · MoE · PEFT
生成 / 理解：Diffusion · Video · Audio/Speech · World Models · Multimodal
加速：Speculative Decoding · 量化
本地运行：llama.cpp · Ollama · LM Studio · MLX
案例纵深：DeepSeek / Qwen-Omni / GLM-Realtime / 豆包·Seed / MiniMax（M3·H3·音频） / fal（model-cases/）
```

MCP 连工具，A2A 连 Agent，二者互补而不是二选一。Agent 总图见 [agent/](./agent/)。RAG / Memory / Context Engineering 解决「塞什么进窗口」，[循环与图](./agent/loop-graph/)（[栈总览](./agent/README.md#七按栈升级从提示到图)）管验证闭环、执行图接线和领域事实契约，Guardrails / Eval 解决「能不能上线」，[model-cases/](./model-cases/) 解决「某个具体模型到底怎么用」。

## 跑 MVP

多数专题是纯标准库：

```bash
cd ai/<大类>/<专题>
python3 mvp.py
```

LangGraph 相关 demo 见 [langgraph/demos/requirements.txt](./agent/case-studies/langgraph/demos/requirements.txt)。
