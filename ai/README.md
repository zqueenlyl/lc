# AI 热点技术手册

按主题分类整理的 AI / LLM 学习文档与可运行 MVP。每种技术一个文件夹：讲解（原理 / 功能 / 场景）+ 尽量无外部 API 依赖的 `mvp.py`。

收集范围覆盖 **Foundation（模型与训练）**、**协议与编排**、**工程落地**、**推理与生成**，不限于某一层。

产业扫盲（产品 / 公司 / 模型家族 / 常用网站，按层看而不是背版本号）见 [landscape.md](./landscape.md)（2026-09 快照）。

## 目录结构

```
ai/
├── README.md                 # 本索引
├── landscape.md              # 产品 / 技术 / 公司一览（扫盲）
├── loop-engineering.md       # 循环工程（已有）
│
├── rag/                      # RAG 检索增强（已有）
├── 知识库/                   # 知识库形态（已有）
├── memory/                   # Agent 记忆（已有）
├── langgraph/                # 图编排框架（已有）
│
├── mcp/                      # Model Context Protocol
├── a2a/                      # Agent-to-Agent 协议
├── computer-use/             # 电脑/浏览器操控
├── agent-skills/             # Agent Skills 技能包
├── harness/                  # 编码 Agent 运行时外壳
│
├── reasoning/                # 推理模型 / Test-time Scaling
├── moe/                      # Mixture of Experts
├── multimodal/               # 多模态
├── slm/                      # 小模型 / 端侧
├── peft-lora/                # 参数高效微调
│
├── context-engineering/      # 上下文工程
├── structured-output/        # 结构化输出 / Function Calling
├── guardrails/               # 护栏与安全
├── eval/                     # 评测与可观测
├── model-routing/            # 多模型路由
│
├── voice-realtime/           # 实时语音
├── world-models/             # 世界模型
├── speculative-decoding/     # 投机解码
└── diffusion/                # 扩散生成
```

## 怎么读

每个专题文件夹内：

| 文件 | 内容 |
|---|---|
| `README.md` | 技术讲解、功能作用、应用场景、相邻技术对比、落地建议、延伸阅读 |
| `mvp.py` | 可运行最小实现（`python mvp.py`，默认不调外部模型） |

已有专题保持原文件名（`rag-types.md`、`agent-memory.md` 等），不强制改名。

## 全景索引

### 市场扫盲

| 主题 | 一句话 | 入口 |
|---|---|---|
| **产品 / 技术 / 公司一览** | 六层坐标系 + 模型家族 + 应用产品 + 芯片云 + 常用网站，2026-09 快照 | [landscape.md](./landscape.md) |

### 已有专题

| 主题 | 一句话 | 入口 |
|---|---|---|
| **循环工程** | 从提示工程到「规划-执行-验证」闭环 | [loop-engineering.md](./loop-engineering.md) |
| **RAG** | 检索增强生成：Naive → Agentic 全谱系 | [rag/](./rag/) |
| **知识库** | 知识库类型五维整理 | [知识库/](./知识库/) |
| **Memory** | Agent 工作 / 短期 / 长期记忆 | [memory/](./memory/) |
| **LangGraph** | 图编排 + 8 个 demo | [langgraph/](./langgraph/) |

### 协议与智能体（2025–2026 标准层）

| 主题 | 一句话 | 入口 |
|---|---|---|
| **MCP** | Agent ↔ 工具 / 数据源的 USB-C | [mcp/](./mcp/) |
| **A2A** | Agent ↔ Agent 的对等委托协议 | [a2a/](./a2a/) |
| **Computer Use** | 看屏幕、点鼠标、操作浏览器/桌面 | [computer-use/](./computer-use/) |
| **Agent Skills** | 把领域流程打成可发现、可复用技能包 | [agent-skills/](./agent-skills/) |
| **Harness** | 编码 Agent 的循环外壳：工具 / 插件 / 子 Agent | [harness/](./harness/) |

### Foundation（模型、训练、能力）

| 主题 | 一句话 | 入口 |
|---|---|---|
| **Reasoning** | 推理模型 + 测试时算力缩放（第三条缩放律） | [reasoning/](./reasoning/) |
| **MoE** | 稀疏专家混合：总参大、激活小 | [moe/](./moe/) |
| **Multimodal** | 文本 / 图 / 音 / 视频原生一体 | [multimodal/](./multimodal/) |
| **SLM** | 小模型与端侧：便宜、快、可私有化 | [slm/](./slm/) |
| **PEFT / LoRA** | 只训少量参数就能适配领域 | [peft-lora/](./peft-lora/) |

### 工程落地（把模型变成系统）

| 主题 | 一句话 | 入口 |
|---|---|---|
| **Context Engineering** | 在合适时机把合适信息放进窗口 | [context-engineering/](./context-engineering/) |
| **Structured Output** | JSON Schema / Function Calling，让输出可机器消费 | [structured-output/](./structured-output/) |
| **Guardrails** | 输入过滤、工具门禁、输出校验、人审 | [guardrails/](./guardrails/) |
| **Eval** | 自定义评测 + Trace；LLM 是考试，Agent 是上机 | [eval/](./eval/) |
| **Model Routing** | 按任务/成本/失败自动选模型 | [model-routing/](./model-routing/) |

### 产出与推理加速

| 主题 | 一句话 | 入口 |
|---|---|---|
| **Voice / Realtime** | 双向音视频流，延迟预算 &lt; 500ms | [voice-realtime/](./voice-realtime/) |
| **World Models** | 预测「世界如何演化」，而不只是下一个 token | [world-models/](./world-models/) |
| **Speculative Decoding** | 小模型草稿 + 大模型一次校验，加速解码 | [speculative-decoding/](./speculative-decoding/) |
| **Diffusion** | 扩散模型：图像 / 视频 / 音频生成主路径 | [diffusion/](./diffusion/) |

## 技术栈怎么叠

```
应用：Computer Use / Voice / RAG / Skills / Harness
编排：LangGraph · 循环工程 · Memory · Context Engineering
协议：MCP（工具） · A2A（Agent 互操作）
治理：Guardrails · Eval · Model Routing
模型：Reasoning · Multimodal · SLM · MoE · PEFT
加速：Speculative Decoding · 量化
生成：Diffusion · World Models
```

MCP 连工具，A2A 连 Agent，二者互补而不是二选一。RAG / Memory / Context Engineering 解决「塞什么进窗口」，Guardrails / Eval 解决「能不能上线」。

## 跑 MVP

多数专题是纯标准库：

```bash
cd ai/<专题>
python3 mvp.py
```

LangGraph 相关 demo 见 [langgraph/demos/requirements.txt](./langgraph/demos/requirements.txt)。
