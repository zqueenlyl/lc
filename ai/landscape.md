# AI 产品、技术与公司一览（扫盲）

> 快照：**2026-09**。模型名大约十周换一代，**看「层」和「家族」**，不要背具体版本号。
> 本文是市场地图，不是排行榜；公开榜单测的是「模型 + 评测脚手架」，落到你的任务上要自己评。

---

## 0. 先建立坐标系

把 AI 产业想成六层叠起来。日常听到的「ChatGPT / Claude / 豆包 / Cursor / NVIDIA」其实不在同一层：

```
应用层     ChatGPT · 豆包 · Cursor · Midjourney · 可灵 · Perplexity
编排层     Agent 循环 · RAG · Memory · MCP / A2A · LangGraph
模型层     GPT · Claude · Gemini · Qwen · DeepSeek · Llama
平台层     云 API · Hugging Face · 向量库 · 推理服务
框架层     PyTorch · vLLM · llama.cpp · LangChain
算力层     NVIDIA GPU · Google TPU · 昇腾 · 海光
```

**怎么用这张图**

| 你在做的事 | 该看哪一层 |
|---|---|
| 「用哪个聊天产品」 | 应用层 |
| 「写代码用 Cursor 还是 Copilot」 | 应用层（编程 Agent） |
| 「API 调哪家模型」 | 模型层 + 平台层 |
| 「私有化部署 / 数据不出域」 | 开权重模型 + 算力 + 推理框架 |
| 「做企业知识问答」 | 编排层（RAG / Memory）+ 向量库 |
| 「卡脖子 / 成本」 | 算力层 + Flash 级小模型 |
| 「现在谁强 / 谁便宜 / 编程 Agent 跑多久」 | [常用网站](#6-常用网站) |

一句话：**模型是发动机，产品是车，编排是驾驶系统，芯片是油。** 选发动机前先问自己开的是什么车。

---

## 1. 技术扫盲（名词对照）

本仓库各专题就是编排层 / 模型层的细拆。这里只给「市面上在卖什么」的对应关系。

| 技术 | 一句话 | 市面代表 | 本仓库 |
|---|---|---|---|
| **Transformer** | 自注意力序列骨架，取代 RNN | 几乎所有 LLM / ViT | [transformer/](./transformer/) |
| **LLM** | 大语言模型，下一个 token 预测 | GPT / Claude / Qwen | [transformer/](./transformer/) |
| **Reasoning / 推理模型** | 先想再答，测试时多花算力 | o 系列思路、R1 蒸馏、各家 Thinking 档 | [reasoning/](./reasoning/) |
| **MoE** | 总参很大、每次只激活一小撮专家 | Mixtral、Qwen-MoE、DeepSeek、Llama 4 | [moe/](./moe/) |
| **Multimodal** | 文图音视频原生一体 | Gemini、GPT、豆包、Gemma | [multimodal/](./multimodal/) |
| **Diffusion** | 图像 / 视频生成主路径 | Flux、Midjourney、可灵、Seedance、Veo | [diffusion/](./diffusion/) |
| **RAG** | 先检索再生成，给模型外挂知识 | 几乎所有企业知识问答 | [rag/](./rag/) |
| **Agent** | 规划 → 调工具 → 验证的循环 | Claude Code、Cursor Agent、千问办公 | [agent/](./agent/) |
| **Harness** | 套在模型外的编码循环外壳 | Claude Code、Codex、Kimi Code、Pi | [harness/](./harness/) |
| **MCP** | Agent 连工具的 USB-C | Cursor / Claude / ChatGPT 都能插 | [mcp/](./mcp/) |
| **A2A** | Agent 互相对话委托 | 跨系统多智能体 | [a2a/](./a2a/) |
| **Computer Use** | 看屏幕、点鼠标、开浏览器 | Claude Computer Use、各家浏览器 Agent | [computer-use/](./computer-use/) |
| **Function Calling** | 模型按 schema 调工具、吐 JSON | 所有主流 API | [structured-output/](./structured-output/) |
| **PEFT / LoRA** | 只训少量参数做领域适配 | 开源微调标配 | [peft-lora/](./peft-lora/) |
| **SLM / 端侧** | 小模型跑在手机 / 笔记本 | Gemma、Phi、Apple 端侧、MiMo | [slm/](./slm/) |
| **投机解码** | 小模型打草稿、大模型一次校验 | vLLM / SGLang 常见加速 | [speculative-decoding/](./speculative-decoding/) |
| **World Models** | 预测世界怎么演化，不只预测字 | JEPA、机器人 / 仿真方向 | [world-models/](./world-models/) |
| **Agent Skills** | 按需加载的 SOP / 程序记忆 | Cursor / Claude SKILL.md | [agent-skills/](./agent-skills/) |
| **Context Engineering** | 窗口里塞什么、砍什么、如何缓存 | 长上下文 + 前缀缓存产品 | [context-engineering/](./context-engineering/) |
| **Memory** | 工作 / 短期 / 长期记忆 | Mem0、Zep、各框架 Checkpointer | [memory/](./memory/) |
| **Guardrails** | 输入筛、工具门禁、输出校验、人审 | 云 Moderations、自建策略平面 | [guardrails/](./guardrails/) |
| **Eval / Trace** | 学校考试评模型；上机考试评模型×Harness | LangSmith、Langfuse、SWE-bench、AA Coding Agents | [eval/](./eval/) |
| **Model Routing** | 按难度/模态/故障选模型 | AI Gateway、LiteLLM、OpenRouter | [model-routing/](./model-routing/) |
| **Voice / Realtime** | 双向音视频流，中途护栏 | Realtime / Live API、电话 Agent | [voice-realtime/](./voice-realtime/) |

2026 年工程侧的共识：

1. **没有单一最强模型**，生产系统是路由（难任务走前沿，日常走 Flash / 本地）。
2. **开权重的重心在东边**：DeepSeek / Qwen / Kimi / GLM / MiniMax 把价格地板压得很低；西方开源锚点从 Llama 前沿后撤。
3. **Agent 把 Token 账单放大**：一次对话变几十次工具调用，Flash / 缓存 / 路由比「旗舰榜单」更重要。
4. **模型可用性是政策变量**：出口管制、备案、评测延期会让某档模型暂时下线——生产系统要有备胎。

---

## 2. 公司一览：谁在造模型

先分四类，避免把「实验室 / 大厂 / 云 / 芯片」混成一张表。

### 2.1 闭源前沿实验室（Frontier）

比的是最难任务的上限，卖 API + 自家应用。版本号极快，**记家族**。

| 公司 | 总部 | 家族 | 当前代际（约 2026 中后期） | 卖点 | 产品入口 |
|---|---|---|---|---|---|
| **OpenAI** | 旧金山 | GPT | GPT-5.x（Sol / Terra / Luna 等分档） | 产品面最广、节奏最快、生态默认起点 | ChatGPT、API、Codex |
| **Anthropic** | 旧金山 | Claude | Opus / Sonnet / Haiku；其上还有受限更高档 | 编程与长 Agent 链、文笔、安全叙事 | Claude.ai、Claude Code、Bedrock / Vertex |
| **Google DeepMind** | 伦敦 / 山景城 | Gemini | Pro 偏旗舰、Flash 偏性价比；另有 Gemma 开源线 | 超长多模态上下文、搜索/Workspace 集成 | Gemini App、AI Studio、Vertex |
| **xAI** | 奥斯汀 | Grok | Grok 4.x | 前沿里偏便宜、工具调用、X 实时信息 | grok.com、X、API |
| **Meta Superintelligence** | 门洛帕克 | Muse | Muse Spark（2026 起闭源旗舰） | 元宇宙 / 社交表面的原生多模态 | Meta 自家产品 + 有限 API |

**怎么记**

- 日常对话 / 插件生态 → OpenAI 仍是最大公约数。
- 写代码、长任务、要稳 → Claude 经常是默认。
- 视频 / 超长文档 / Google 全家桶 → Gemini。
- 量大、要压单次成本、能接受风格更「野」 → Grok 值得进路由表。

### 2.2 开权重（Open Weights）——可下载参数自己跑

「开权重」≠ 开源：通常只公开参数，训练数据和完整训练代码不公开。许可证要看法务（MIT / Apache 友好，Llama 社区许可有用户规模等限制）。

| 公司 | 家族 | 许可倾向 | 为什么重要 |
|---|---|---|---|
| **DeepSeek（深度求索）** | DeepSeek V4 Pro / Flash | MIT | 推理与性价比锚点；R1 让「推理蒸馏」成为主流手法 |
| **阿里巴巴** | Qwen（通义千问）开源档 | 多为 Apache 2.0 | 尺寸最全、多语言、HF 下载量最大之一；**Max 档是 API 闭源** |
| **月之暗面 Moonshot** | Kimi K2 / K3 | 改版 MIT | Agent 编程、长工具循环、超长上下文 |
| **智谱 Zhipu / Z.ai** | GLM | MIT | 长程编程、企业私有化 |
| **MiniMax** | M 系列 | 开权重 | 低成本吞吐 + 原生多模态；视频线 Hailuo |
| **Mistral AI** | Large / Small / Ministral | Apache 2.0 | 欧洲数据驻留、多语言、真能自托管 |
| **Google** | Gemma | 较友好 | 西方实验室里最干净的本地选项之一 |
| **Meta** | Llama 3.3 / 4 | 社区许可 | 生态与工具链最深，但 2026 前沿转向闭源 Muse |
| **OpenAI** | gpt-oss | 开权重 | 想要「OpenAI 味道」但自己跑 |
| **NVIDIA** | Nemotron | 开权重 | 在自家 GPU 上抠吞吐 |
| **IBM** | Granite | Apache 2.0 | 小模型、受监管行业 |

### 2.3 中国大厂：模型 + 场景 + 云

大厂卖的是「模型 + 流量 + 云 + 办公/社交/电商」捆绑，不只是榜单分数。

| 公司 | 模型品牌 | 2026 粗印象 | 场景抓手 |
|---|---|---|---|
| **字节跳动** | 豆包 / Seed | C 端用户与 Token 调用量最大档；视频生成 Seedance | 抖音 / 豆包 App / 火山引擎 |
| **阿里巴巴** | 通义千问 Qwen | 开源生态最完整；Qwen-Max 冲综合与 Agent | 云 + 钉钉/千问办公 + 电商 |
| **腾讯** | 混元 Hunyuan | 社交/办公/游戏内嵌；算力曾公开喊紧 | 微信 / 腾讯云 / 元宝 |
| **百度** | 文心 ERNIE | 搜索与政务/企业项目 | 文心一言、百度云 |
| **华为** | 盘古 / openPangu | 绑昇腾，央企私有化叙事 | 鸿蒙、昇腾、华为云 |
| **小米** | MiMo | 端侧 + 人车家 | 手机 / 车机 |
| **美团** | LongCat | 全国产万卡训练叙事 | 到店 / 配送等内部场景 |
| **快手** | 可灵 Kling + 快意 | 视频生成全球一线 | 短视频、可灵 App |
| **科大讯飞** | 星火 Spark | 语音、教育、医疗；国产算力多模态 | 语音交互垂直 |
| **京东** | JoyAI | 零售供应链 | 京东云 / 内部业务 |
| **商汤** | 日日新 SenseNova | 视觉与行业大模型 | 城市视觉、行业方案 |

### 2.4 中国独立实验室（技术向）

没有大厂场景，靠模型质量和开源说话。

| 公司 | 产品 | 一句话 |
|---|---|---|
| **DeepSeek** | 对话 + API + 开源权重 | 2025 R1 震惊行业；2026 比拼 Flash 效率与推理 |
| **月之暗面** | Kimi | 长文档起家，转向 Agent / 编程 |
| **智谱** | 清言 / GLM API / 私有化 | 高校基因，企业部署盘大 |
| **MiniMax** | 海螺 / 语音 / 视频 | 多模态生成公司里产品最全之一 |
| **零一万物 01.AI** | Yi | 早期开源玩家，份额已被前几家挤压 |
| **百川 / 阶跃星辰** 等 | 各有对话与多模态线 | 第二梯队，跟节奏即可 |

### 2.5 云巨头与企业向模型（不一定最强，但是交付入口）

| 公司 | 自有模型 | 真正的生意 |
|---|---|---|
| **Microsoft** | MAI 家族（端侧 + Copilot） | Azure OpenAI、GitHub Copilot、Office / Windows |
| **Amazon** | Nova | **Bedrock**：一家控制台里卖 18+ 家开权重和闭源模型 |
| **Oracle** | — | 给训练集群卖算力和云 |
| **Salesforce / SAP** | 各自 Einstein / Joule 等 | 业务 SaaS 里嵌 AI；SAP 还押注表格基础模型 |
| **Cohere** | Command 等 | 企业检索、Embedding、多语言，生成模型不是主战场 |

---

## 3. 模型家族一张表

读列不读行：**Weights** 决定架构（调用依赖 vs 文件归你），「擅长」一季一变。

| 家族 | 厂商 | 权重 | 2026 大致定位 |
|---|---|---|---|
| GPT-5.x | OpenAI | 闭源；另有 gpt-oss | 产品面 / 编程 Agent / 迭代最快 |
| Claude | Anthropic | 闭源 | 编程、长 Agent、写作 |
| Gemini | Google | 闭源 + Gemma 开源 | 长多模态、Flash 性价比 |
| Grok | xAI | 现行闭源 | 前沿里偏便宜、工具与实时 |
| Muse | Meta | 闭源 | Meta 表面多模态旗舰 |
| Llama | Meta | 开权重 | 生态深，前沿已不是它 |
| DeepSeek | DeepSeek | 开权重 | 价格地板、推理 |
| Qwen | 阿里 | 开源档开权重；Max 闭源 | 家族最全、中文与多语言 |
| Kimi | 月之暗面 | 开权重 | Agent 编程、超长上下文 |
| GLM | 智谱 | 开权重 | 开源里的长程编程 |
| MiniMax M | MiniMax | 开权重 | 便宜吞吐 + 图视频理解 |
| 豆包 / Seed | 字节 | 以 API / 应用为主 | 中文 C 端与调用量 |
| 混元 | 腾讯 | 混合 | 腾讯生态内嵌 |
| 文心 | 百度 | 闭源为主 | 搜索 / 政务企业 |
| Mistral | Mistral | 开权重 | 欧洲驻留、自托管 |
| Gemma | Google | 开权重 | 本地 / 端侧 |
| Nova | Amazon | 闭源 | 呆在 AWS 里最省事 |
| MAI | Microsoft | 闭源 + 端侧 | Windows / Copilot |
| Nemotron | NVIDIA | 开权重 | 自有 GPU 吞吐 |
| Granite | IBM | 开权重 | 受监管小模型 |

**分档口诀（各家名字不同，结构一样）**

```
旗舰 / Opus / Max / Pro / Sol     → 难推理、难编程、贵
均衡 / Sonnet / Terra              → 日常默认
Flash / Haiku / Mini / Nano / Lite → Agent 高频、路由底层
```

---

## 4. 产品一览：用户真正打开的那些

### 4.1 通用对话 / 助手

| 产品 | 公司 | 一句话 |
|---|---|---|
| **ChatGPT** | OpenAI | 全球默认助手，GPTs / 语音 / 深度研究都在这 |
| **Claude** | Anthropic | 长文、分析、编程向对话 |
| **Gemini** | Google | 搜 + 邮箱文档 + 多模态 |
| **Grok** | xAI | 绑 X，限制更少 |
| **豆包** | 字节 | 国内 C 端盘子最大档 |
| **通义千问** | 阿里 | 对话 + 办公 Agent + 开源同源 |
| **Kimi** | 月之暗面 | 长文档 / Agent |
| **文心一言** | 百度 | 搜索基因 |
| **腾讯元宝** | 腾讯 | 微信生态入口 |
| **DeepSeek** | DeepSeek | 推理向、开发者口碑 |
| **智谱清言** | 智谱 | 对话 + 企业入口 |

### 4.2 编程 Agent / IDE（2026 主战场）

编程工具已经从「补全下一行」变成「自己读仓库、跑测试、开 PR」。

| 产品 | 形态 | 谁在用、为什么 |
|---|---|---|
| **Cursor** | AI 原生产 IDE | 编辑器里改多文件、可选多家模型；付费开发者很多 |
| **Claude Code** | 终端优先 Agent | 大重构、长任务、子 Agent；Anthropic 自家旗舰场景 |
| **GitHub Copilot** | IDE 插件 + Agent 模式 | 企业采购默认、GitHub issue→PR |
| **OpenAI Codex** | 云端沙箱任务 | 后台并行干活、和 ChatGPT 账号一体 |
| **Gemini CLI / Antigravity** | 终端 / Agent | Google 线，免费额度友好 |
| **通义灵码 / 千问编程** | IDE + Agent | 国内云与阿里生态 |
| **Trae / 豆包编程** 等 | 字节线 | 跟 C 端豆包同一套模型 |
| **Cline / Continue / Aider / OpenCode** | 开源插件或 CLI | 可自带模型、可本地 |

选型极简：日常在编辑器里写 → Cursor 或 Copilot；要啃大重构 → Claude Code；公司已经 all-in GitHub → Copilot；要私有模型 → 开源插件 + vLLM。

产品（你打开的窗口）和 **Harness**（循环怎么转：默认工具、插件、子 Agent）不是一层。六款外壳对照见 [harness/](./harness/)：DeepSeek / Claude Code / Codex / Kimi Code / Pi / OpenClaw。Tool 个数不代表强弱。

### 4.3 搜索、研究、知识

| 产品 | 公司 | 差异 |
|---|---|---|
| **Perplexity** | Perplexity | 带引用的回答，研究向 |
| **ChatGPT Search / Deep Research** | OpenAI | 助手里直接搜和长研究 |
| **Gemini + Google 搜索** | Google | 索引最大 |
| **元宝 / 搜狗等** | 腾讯等 | 国内搜索入口 |
| **Notion AI / 飞书 / 钉钉 / 企微智能** | 各办公套件 | 知识在工作区里，不在公网 |

企业知识问答很少「只调一个模型」，标准形态是 **RAG**：文档 → 切片 → 向量库 → 检索 → LLM。详见 [rag/](./rag/) 与 [知识库/](./知识库/)。

### 4.4 图像生成

| 产品 / 模型 | 公司 | 备注 |
|---|---|---|
| **Midjourney** | Midjourney | 审美与社区，偏闭源产品 |
| **Flux** | Black Forest Labs | 开源 / API 图像质量标杆之一 |
| **GPT 图像 / DALL·E 线** | OpenAI | 聊天里直接画 |
| **Imagen / Gemini 画图** | Google | 搜和 Workspace 里用 |
| **即梦 / Dreamina** | 字节 | 国内设计向 |
| **通义万相** | 阿里 | 云上图像 |
| **Stable Diffusion 系** | Stability 及社区 | 本地可玩性最高，生态碎片化 |
| **Ideogram** | Ideogram | 文字渲染较好 |

### 4.5 视频生成

2026 年视频是「按镜头选模型」，没有全能冠军。OpenAI **Sora 消费级产品已收**，API 也在退场窗口，新项目不要绑它。

| 产品 / 模型 | 公司 | 大致擅长 |
|---|---|---|
| **Seedance** | 字节 | 商业/产品一致性、多参考图 |
| **可灵 Kling** | 快手 | 人物运动、性价比、国内最出圈的视频产品之一 |
| **Veo** | Google | 物理真实感、口型/对白 |
| **Runway** | Runway | 控制与后期工作流，不只是一条生成 |
| **Hailuo / 海螺** | MiniMax | 迭代快、有开权重尝试 |
| **Wan 万相视频** | 阿里 | API 管线 |
| **Pika** | Pika | 短视频、首尾帧 |
| **Grok Imagine Video** | xAI | 偏便宜、快 |

### 4.6 语音与实时

| 产品 / 模型 | 公司 | 用途 |
|---|---|---|
| **ElevenLabs** | ElevenLabs | TTS / 声音克隆 / 语音 Agent 产品标杆 |
| **OpenAI Realtime / GPT 语音** | OpenAI | 双向语音对话 |
| **Gemini Live / Flash TTS** | Google | 实时多模态语音 |
| **Nova Sonic** | Amazon | AWS 里的语音交互 |
| **Voxtral** | Mistral | 开源向语音 |
| **Whisper 及衍生** | OpenAI + 社区 | 转写体量最大 |
| **讯飞开放平台** | 科大讯飞 | 中文语音、教育医疗 |
| **豆包语音 / MiniMax 语音** | 字节 / MiniMax | 国内 C 端音色 |

实时对话的硬约束是延迟（常要 &lt; 500ms），见 [voice-realtime/](./voice-realtime/)。

### 4.7 垂直与「AI+」

不穷举。记住：**垂直产品 = 通用模型 + 领域数据 + 工作流**，护城河很少是「自研了一个 GPT」。

| 方向 | 例子 |
|---|---|
| 办公套件 | Microsoft Copilot、Google Workspace、钉钉 / 飞书智能 |
| 客服 / 工单 | 各云厂商智能客服、Intercom 等 |
| 法律 / 医疗 / 教育 | Harvey 类、讯飞医疗教育、各类合规助手 |
| 机器人 / 具身 | Gemini Robotics、Figure、国内具身初创 |
| 表格 / 预测 | TabPFN 类表格基础模型（和聊天模型不是一类东西） |
| 安全 | 各家 Flash Cyber / 受限高能力档，给政府和可信伙伴 |

---

## 5. 基础设施：芯片、云、工具链

### 5.1 芯片（真正的上游）

| 玩家 | 角色 |
|---|---|
| **NVIDIA** | 训练 / 推理 GPU 事实标准；CUDA 生态锁人 |
| **AMD** | Instinct 抢份额，软件栈仍是短板 |
| **Google TPU** | 自用 + GCP，Gemini 训练主力之一 |
| **AWS Trainium / Inferentia** | 亚马逊自研，绑 Bedrock 成本 |
| **华为昇腾** | 国产训练推理主路径，盘古 / 部分开源模型在适配 |
| **海光 / 昆仑芯 / 寒武纪** | 国产第二梯队，政策驱动采购 |
| **Apple Silicon** | 统一内存让 Mac 本地推理很香（MLX） |

2026 云巨头资本开支是千亿美元级，大部分砸在电、数据中心和 GPU 上。模型公司收入相对这笔 capex 仍然很小——**算力才是当前最大的生意**。

### 5.2 云与模型分发

| 平台 | 你在买什么 |
|---|---|
| OpenAI API / Anthropic API / Google AI Studio | 第一方，功能最新 |
| **Azure OpenAI** | 企业合同、数据承诺、和微软账号 |
| **AWS Bedrock** | 一个 API 后面很多家模型，企业默认目录 |
| **Vertex AI** | Gemini + 开源托管 |
| **阿里云百炼 / 火山方舟 / 腾讯云** | 国内模型 + 备案 + 发票 |
| **SiliconFlow / Fireworks / Together / Groq** | 第三方推理，开源模型更便宜或更快 |
| **Hugging Face** | 权重分发、Spaces、推理端点；开源世界的 GitHub |

### 5.3 开源枢纽与本地运行

| 工具 | 干什么 |
|---|---|
| **Hugging Face Hub** | 下模型、看卡片和许可 |
| **Ollama** | 本地模型「包管理器」，入门首选 |
| **LM Studio** | 带 GUI 的本地聊天 |
| **llama.cpp / GGUF** | CPU/消费级 GPU 量化运行的底座 |
| **MLX** | Apple 芯片推理 |
| **vLLM / SGLang** | 服务端高吞吐（连续 batch、PagedAttention） |
| **WebLLM** | 浏览器 WebGPU 跑小模型 |

内存粗算：4-bit 下约「参数量(B) × 0.5 GB」+ KV cache。8GB 内存玩 3B–4B；16–24GB 是笔记本甜区；大 MoE（千亿总参）仍然要多卡。

### 5.4 数据、检索、观测

| 类别 | 代表 |
|---|---|
| 向量库 | Pinecone、Milvus、Qdrant、Weaviate、Chroma、pgvector |
| 数据平台 | Databricks、Snowflake |
| 标注 / 评测数据 | Scale AI、国内众包与合成数据厂 |
| Agent 观测 | LangSmith、Langfuse、Arize、各云 Trace |
| 护栏 | 云厂商内容安全 + 开源 Guardrails，见 [guardrails/](./guardrails/) |

### 5.5 开发框架与协议

| 层 | 代表 | 别把它当成模型 |
|---|---|---|
| 训练 | PyTorch（绝对主流）、JAX | 造模型用 |
| 编排 | LangGraph、LangChain、LlamaIndex、语义内核 | 把模型编成系统 |
| 协议 | **MCP**（工具）、**A2A**（Agent 互操作） | 2025–2026 标准层 |
| Agent 技能包 | Cursor Skills、Claude Skills 等 | 见 [agent-skills/](./agent-skills/) |

---

## 6. 常用网站

公开榜测的是「模型 + 对方的脚手架」，**当地图用，不当验收**。先独立横评定坐标，再看真实用量和价格，最后用自己的任务集。

### 6.1 独立横评（Artificial Analysis 这一类）

同时看智力、速度、单价、延迟，比单看 Arena 分数有用。同一模型换家推理商，价格和 tok/s 能差好几倍。

| 网站 | 看什么 | 链接 |
|---|---|---|
| **Artificial Analysis** | 智力指数、速度、单任务成本、延迟；同一模型比不同 API 商 | [artificialanalysis.ai](https://artificialanalysis.ai/) |
| AA · Coding Agents | 编程 Agent 的通过率 / 成本 / **执行时间**（你给的这种页） | [coding-agents=execution-time](https://artificialanalysis.ai/?coding-agents=execution-time) |
| AA · 图 / 视频 / 语音 | Image / Video / Speech Arena，生成模型别只看 LLM 榜 | 站点顶栏 *Speech, Image, Video* |
| AA · Inference | 同一权重，Groq / Fireworks / 硅基流动 / 官方 API 谁更快更便宜 | 顶栏 *Inference* |
| **LMArena（原 LMSYS Chatbot Arena）** | 人类盲测 Elo，对话体感金标准；偏聊天，不直接等于干活能力 | [lmarena.ai](https://lmarena.ai/) |
| **Epoch AI** | 算力、训练成本、能力趋势，看产业而不是看下周第一名 | [epoch.ai](https://epoch.ai/) |
| **Stanford HELM** | 学术向、多场景、透明度高，更新比商业站慢 | [crfm.stanford.edu/helm](https://crfm.stanford.edu/helm/) |
| **LLM Stats / BenchLM** | 把多家榜和价格摊成一张大表，适合扫一眼 | [llm-stats.com](https://llm-stats.com/) · [benchlm.ai](https://benchlm.ai/) |

Artificial Analysis 首页还能进 **Search Index**（比搜索 API）和 **Optima**（用你自己的题做自定义榜）。智力指数会换组成（当前常见构件：GPQA Diamond、Humanity's Last Exam、Terminal-Bench、SciCode、GDPval 等），**指数涨不代表你的业务涨**。

### 6.2 专项评测（编程 / Agent / 中文）

| 网站 | 测的是 | 链接 |
|---|---|---|
| **SWE-bench** | 真实 GitHub issue → 改仓过测试；看 **% Resolved**。默认常看 Verified；要比模型锁外壳看 **Bash Only** | [swebench.com](https://www.swebench.com/) |
| **Terminal-Bench** | 在终端里把活干完（装依赖、跑脚本），AA Coding Agent 的组成之一 | [tbench.ai](https://www.tbench.ai/) |
| **LiveCodeBench** | 持续收新竞赛题，抗污染，看「会不会写新题」 | [livecodebench.github.io](https://livecodebench.github.io/) |
| **Aider Polyglot** | 多语言代码编辑质量，偏「结对改文件」 | [aider.chat/docs/leaderboards](https://aider.chat/docs/leaderboards/) |
| **OpenCompass** | 国内开源评测套件 + 公开榜，中文和多模态覆盖好 | [rank.opencompass.org.cn](https://rank.opencompass.org.cn/) |
| **SuperCLUE** | 中文综合能力横评，看国内对话体感 | [superclueai.com](https://www.superclueai.com/) |

写代码不要只看 HumanEval。有区分度的公开上机榜是 [SWE-bench](https://www.swebench.com/)（Full / Verified / Lite / Bash Only / 多语言 / 多模态）、Terminal-Bench、LiveCodeBench。SWE-bench Pro / Live 是后续变体，和官网这几张表不要混成一行。再往上是你自己的仓库 + CI。子集怎么读见 [eval 专题](./eval/)。

### 6.3 真实用量、价格、一键试用 API

榜单说「谁强」，这类站说「谁在被调用、多少钱」。

| 网站 | 看什么 | 链接 |
|---|---|---|
| **OpenRouter** | 一个 key 调很多家模型；[Rankings](https://openrouter.ai/rankings) 是真实 Token 用量，不是质量 | [openrouter.ai](https://openrouter.ai/) |
| **硅基流动 SiliconFlow** | 国内常用的开源模型推理，DeepSeek / Qwen / Kimi / GLM 上新快 | [siliconflow.cn](https://siliconflow.cn/) / [siliconflow.com](https://siliconflow.com/) |
| **Together / Fireworks / Groq** | 海外第三方推理：便宜或极快（Groq 吃延迟） | 各官网 |
| **fal.ai** | 图像 / 视频 / 语音 API 聚合，生成模型调试常用 | [fal.ai](https://fal.ai/) |
| 官方控制台 | 功能最新、账单最清楚 | [OpenAI](https://platform.openai.com/) · [Anthropic](https://console.anthropic.com/) · [Google AI Studio](https://aistudio.google.com/) |
| 国内云 MaaS | 备案、发票、内网 | 阿里云百炼 · 火山方舟 · 腾讯云 · 百度千帆 |

OpenRouter 用量榜前排经常是 Flash / 免费档（DeepSeek Flash、GLM Flash、Luna…），说明 **Agent 时代劳动力是便宜模型**，不要把它读成「最强模型排行」。

### 6.4 模型仓库、本地跑、工具目录

| 网站 | 干什么 | 链接 |
|---|---|---|
| **Hugging Face** | 开源世界的 GitHub：权重、数据集、Spaces、论文日更 | [huggingface.co](https://huggingface.co/) |
| HF · Daily Papers | 每天在传的论文，比自己刷 arXiv 省 | [huggingface.co/papers](https://huggingface.co/papers) |
| HF · Open LLM Leaderboard | **只含开权重**，和 GPT/Claude 不在一张表 | Spaces 里搜 Open LLM Leaderboard |
| **ModelScope 魔搭** | 国内镜像 + 国产模型，下 Qwen / GLM 更顺 | [modelscope.cn](https://www.modelscope.cn/) |
| **Ollama Library** | 本地一键跑，笔记本入门 | [ollama.com/library](https://ollama.com/library) |
| **Civitai** | 图像 LoRA / Checkpoint 社区（偏 SD / Flux） | [civitai.com](https://civitai.com/) |
| **MCP 目录** | 现成工具插头 | [modelcontextprotocol.io](https://modelcontextprotocol.io/) · [smithery.ai](https://smithery.ai/) |

### 6.5 论文、新闻、动手笔记

| 网站 | 定位 | 链接 |
|---|---|---|
| **arXiv** | 预印本源头，`cs.LG` / `cs.CL` / `cs.AI` | [arxiv.org](https://arxiv.org/) |
| **Papers with Code** | 论文 ↔ 代码 ↔ 旧榜，找实现用 | [paperswithcode.com](https://paperswithcode.com/) |
| **The Batch** | Andrew Ng 周报，产业扫盲密度高 | [deeplearning.ai/the-batch](https://www.deeplearning.ai/the-batch/) |
| **Latent Space** | 播客 + 新闻，偏工程和 Agent | [latent.space](https://www.latent.space/) |
| **Simon Willison** | 个人实测笔记，工具和模型发布当天就能看到人怎么用 | [simonwillison.net](https://simonwillison.net/) |
| **Interconnects** | 训练 / 后训练 / 开源模型解读（Nathan Lambert） | [interconnects.ai](https://www.interconnects.ai/) |
| **机器之心 / 量子位** | 中文产业新闻，发布会和融资跟得快 | [jiqizhixin.com](https://www.jiqizhixin.com/) · [qbitai.com](https://www.qbitai.com/) |
| **r/LocalLLaMA** | 本地部署、显卡、量化，水分大但信号快 | [reddit.com/r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/) |

实验室一手来源（发布当天看）：[OpenAI](https://openai.com/news/) · [Anthropic](https://www.anthropic.com/news) · [Google DeepMind](https://deepmind.google/discover/blog/) · [通义](https://qwenlm.github.io/) · [DeepSeek](https://www.deepseek.com/) Hugging Face 卡片。

### 6.6 国内合规与备案

对企业比 Arena 更硬的约束：

- 生成式 AI 服务备案、算法备案：看网信办公示，上线 C 端产品前先确认。
- 各云控制台的「已备案模型」列表，往往比新闻稿可靠。
- 开权重下载到自有机房，和「调杭州 / 硅谷的 API」，是两种合规画像。

### 6.7 每周最小书签（够用）

```
行情     https://artificialanalysis.ai/
编程 Agent https://artificialanalysis.ai/?coding-agents=execution-time
体感     https://lmarena.ai/
谁在被用  https://openrouter.ai/rankings
下模型    https://huggingface.co/  +  https://www.modelscope.cn/
论文     https://huggingface.co/papers
```

其余按需：写代码再打开 SWE-bench / Terminal-Bench；做图视频用 AA 的 Image & Video + fal.ai；要发票走国内云。

---

## 7. 怎么选：给工程同学的最短路径

```
只是聊天、写邮件、翻译
  → 豆包 / ChatGPT / Gemini，别自建

写代码
  → Cursor 或 Copilot 日常；大重构加 Claude Code
  → 模型：Claude / GPT 旗舰；国内用 Qwen / Kimi / GLM / DeepSeek 做备胎

企业知识库问答
  → RAG + 任意均衡模型，检索质量 > 旗舰榜单
  → 数据敏感：开权重 + 私有化（Qwen / GLM / DeepSeek）

要自己跑、数据不出网
  → 开权重 + vLLM/Ollama；许可选 Apache/MIT

Agent 要大规模调工具
  → 默认 Flash / Haiku / Mini，难题再升级；务必做路由

图像
  → Midjourney / Flux / 即梦，按审美和是否要 API

视频
  → 可灵 / Seedance / Veo / Runway，按镜头类型拆，不要绑 Sora

中国大陆合规、发票、备案
  → 阿里 / 字节火山 / 腾讯云 / 百度，不要只看 Arena 分数
```

**三条反直觉**

1. 把模型名写死在代码里会过期。做成配置 + 路由，见 [model-routing/](./model-routing/)。
2. Embedding / 重排对 RAG 的影响，常常大于换生成模型。
3. 「开源模型」若走国外托管 API，和「权重下载到自己机房」是两种合规画像。

---

## 8. 术语表（扫盲）

| 词 | 意思 |
|---|---|
| **Token** | 模型计费/计算的小块文本，不是「一个字」 |
| **上下文窗口** | 一次能塞进去的 Token 上限；宣传值和有效值常不一致 |
| **权重 / Weights** | 训练好的参数文件；开权重 = 能下载自己跑 |
| **闭源 / API-only** | 只能调 HTTP，参数不给你 |
| **预训练 Pretrain** | 在海量数据上学会语言和世界知识 |
| **微调 Fine-tune / SFT** | 用指令数据改行为 |
| **对齐 / RLHF / RL** | 让模型更听话、更能完成任务；推理模型大量靠强化学习 |
| **幻觉** | 说得像真的但不是真的 |
| **MaaS** | Model as a Service，按 Token 卖模型 |
| **Agent** | 能调用工具、多步完成目标的系统，不只是聊天 |
| **Harness** | 编码 Agent 的运行时：工具、权限、插件、子循环 |
| **MCP** | 工具与数据源的标准插头 |
| **RAG** | 检索增强生成 |
| **Embedding** | 把文本变成向量，供检索 |
| **量化 Quantization** | 用更少 bit 存参数，换显存和速度，略损质量 |
| **蒸馏 Distillation** | 大模型教小模型，DeepSeek R1 让这事出圈 |
| **Flash 模型** | 各家的高效档，Agent 时代的默认劳动力 |
| **Arena / SWE-bench** | 人类盲测 Elo / 真实修 issue；常见榜，当地图不当验收 |

---

## 9. 和本仓库的对应

读完地图之后，按层往下钻：

| 你想搞懂 | 去 |
|---|---|
| Agent 怎么转起来 | [agent/](./agent/)、[loop-engineering.md](./loop-engineering.md)、[langgraph/](./langgraph/)、[harness/](./harness/) |
| 知识怎么塞进模型 | [rag/](./rag/)、[知识库/](./知识库/)、[memory/](./memory/) |
| 工具和多 Agent | [mcp/](./mcp/)、[a2a/](./a2a/)、[agent-skills/](./agent-skills/) |
| 模型骨架（RNN → 注意力 → Transformer） | [transformer/](./transformer/) |
| 模型内部在升级什么 | [reasoning/](./reasoning/)、[moe/](./moe/)、[multimodal/](./multimodal/) |
| 怎么上线别炸 | [guardrails/](./guardrails/)、[eval/](./eval/)、[model-routing/](./model-routing/) |

专题总索引见 [README.md](./README.md)。

---

## 10. 延伸阅读（会过期，当入口）

- 网站总表见 [§6 常用网站](#6-常用网站)，最小书签从 Artificial Analysis 和 Hugging Face Papers 起。
- 国内调用与备案：各云 MaaS 控制台、网信办生成式 AI 备案列表。
- 编程 Agent：直接试用 Cursor / Claude Code / Copilot，比看评测快。
- 本页不追踪具体分数；需要验收时用**自己的任务集**，不要用公开榜单代替 [eval/](./eval/)。
