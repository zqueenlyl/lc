# 系统设计教材（三份）

> 位置：`courses.md`（学习库根，与 `ai/`、`naval/` 同级）。
> 分工：[ai/courses.md](./ai/courses.md) 排学期课（CMU / Stanford / MIT）；本页排三份可自学的系统设计材料。后端大纲在 [learning-path.md §3](./ai/learning-path.md)。
> 快照 **2026-09-24**。图和正文留在上游，本页只做「先看哪段、看它图什么、看完往本库哪块对照」。

一句人话：**小册子给提问顺序，ByteByteGo 给传统系统图解，AI System Design Guide 给生产 AI 系统的章节地图。** 本库已经写过的原理不重读，只补缺口。

## 0. 总表

| # | 材料 | 体量 | 解决什么 | 怎么用 |
|---|---|---|---|---|
| **1** | [Machine Learning Systems Design](https://github.com/chiphuyen/machine-learning-systems-design)（Chip Huyen，2019 小册子） | 四步流程 + 12 则案例 + 27 道开放题 | 面试和立项时按什么顺序问：目标、数据、模型、上线 | 先通读流程，再抽 3 道练习用同一张清单答完 |
| **2** | [System Design 101](https://github.com/ByteByteGoHq/system-design-101)（ByteByteGo） | 15 个栏目的图解索引 | 传统系统设计的词汇和取舍，对照 §3 查漏 | 只读「必读」五行；AI 栏目不在这里学 |
| **3** | [AI System Design Guide](https://github.com/ombharatiya/ai-system-design-guide)（Om Bharatiya） | 00–19 章 + 评测长文 + 20 则案例 | 生产 RAG / Agent / 评测 / 多租户的设计地图 | 本库已有的章跳过，只读面试框架、评测和案例缺口 |

**和已有材料的关系**

- 2022 年 O'Reilly《Designing Machine Learning Systems》的目录与工具笔记在 [chiphuyen/dmls-book](https://github.com/chiphuyen/dmls-book)。本页按上面第一个链接，整理 **2019 小册子**。
- 系统课教材（Harvard CS249r / MLSysBook、CMU 10-414）已经在 [ai/courses.md §8.1](./ai/courses.md#s8-1)。那两门讲系统实现与算力账；本页这两份讲设计提问与图解。
- ByteByteGo 许可证为 **CC BY-NC-ND 4.0**。只链回原文，不复述图、不改写文章入库。
- AI System Design Guide 为 **MIT**。模型名、价格、协议版本以它自己的更新日期为准，和本库笔记冲突时回官方核，不把上游快照抄进来。

---

## 1. Machine Learning Systems Design（2019 小册子）

在线阅读：[目录](https://huyenchip.com/machine-learning-systems-design/toc.html)。仓库用 magicbook 从 `content/` 生成 HTML / PDF。

| 章 | 源文件 | 要带走的东西 |
|---|---|---|
| 研究 vs 生产 | [research-vs-production.md](https://github.com/chiphuyen/machine-learning-systems-design/blob/master/content/research-vs-production.md) | 生产看延迟、吞吐、可维护；研究看离线指标。算力预算决定模型能不能上 |
| 设计四步 | [design-a-machine-learning-system.md](https://github.com/chiphuyen/machine-learning-systems-design/blob/master/content/design-a-machine-learning-system.md) | 下面这张提问清单 |
| 案例 | [case-studies.md](https://github.com/chiphuyen/machine-learning-systems-design/blob/master/content/case-studies.md) | 12 则 2017–2019 工程博客。优先 Booking.com 六条教训：模型分 ≠ 业务分、延迟要进目标、用随机对照看业务影响 |
| 练习 | [exercises.md](https://github.com/chiphuyen/machine-learning-systems-design/blob/master/content/exercises.md) | 27 道故意写模糊的开放题。社区答案在 [answers/](https://github.com/chiphuyen/machine-learning-systems-design/tree/master/answers) |

### 1.1 四步提问清单

答题时按这个顺序收窄，不要先报模型名。

**立项**

1. 目标：优化的业务量是什么，成功长什么样。
2. 用户路径：人在哪一步看到预测、能否忽略它。
3. 性能约束：时延、精度 / 召回谁更贵、错的代价。
4. 评测：训练期指标，以及上线后用什么用户行为当代理指标。
5. 个性化粒度：全局一个模型、一群人一个、还是每人一个。
6. 项目约束：上线窗口、标注预算、能不能收集新数据。

**数据**

- 现有数据有多少、标没标、标注贵不贵。
- 用户反馈怎么收回来、能不能当下一轮标签。
- 样本放哪、一条样本进不进内存、用什么结构。
- 原始输入怎么变成模型吃的表示；要不要特征工程。
- 隐私：能否回传服务器、怎么匿名。
- 偏见：数据会不会把现有偏差再放大。

**建模**

- 选型：任务形态（分类 / 排序 / 生成 / 匹配）先于架构名。
- 训练：调试时分开看假设、实现、eval/train 模式、超参、数据本身脏不脏。
- 扩展：加数据是续训还是重训；改结构通常要重来。

**上线**

- 上线前用什么实验证明满足约束；预测要不要带置信度、低置信度是否不展示。
- 推理放端上还是服务器：延迟、隐私、更新频率、机型碎片。
- 复杂模型做消融：拿掉一块，指标掉多少。
- 可解释：拒贷、风控这类决策要能说出原因。
- 误用与偏差：上线后模型会被怎么用偏。
- 假设是否还成立：可预测性、IID、平滑、决策边界形状。分布一变，这些会先坏。

### 1.2 27 道练习怎么抽

题目故意含糊，第一步是追问范围。按题型抽，不必按编号刷完。

| 题型 | 题面方向（转述） | 答题时多盯 |
|---|---|---|
| 检索与排序 | 相关搜索、以图搜图、相似问题去重、房源地理检索、回答排序 | 召回 / 精排拆开；延迟预算；新文档怎么进索引 |
| 推荐与冷启动 | 关注推荐、趋势标签、缺货替代、阅读难度递进 | 新用户没有行为时用什么先验；探索与利用 |
| 分类与检测 | 盗刷、语种、唤醒词、简单图形、分布外样本、一词多义 | 类不平衡；误报代价；训练集里根本没有的类 |
| 匹配与决策 | 拼车、房价后的投资决策、弃剧预测、缩短结账 | 预测之后还有一个决策；优化结账时间不一定是再训一个模型 |
| 数据与对话 | 学校名真假、生日缺失、昵称归一、订房对话、文档问答 | 标签从哪来；对话状态谁持有；答案必须能指回原文 |

**读完往本库写哪儿**

| 小册子里的点 | 本库 |
|---|---|
| 评测、上线指标、业务对照实验 | [reliability/eval/](./ai/reliability/eval/) |
| 端上 / 服务端推理、延迟 | [runtime/](./ai/runtime/) · [环节11 服务化](./ai/foundation/transformer/环节11-服务化与推理引擎详解.md) |
| 检索、排序、问答 | [knowledge/rag/](./ai/knowledge/rag/) |
| 传统系统那一半（存储、缓存、队列） | 本页 §2，对照 [learning-path §3](./ai/learning-path.md) |

案例年份停在 2019。LLM 服务、Agent harness、评测 4-tuple 以 [ai/courses.md](./ai/courses.md) 的 11-768 / CS329Z 为准，不从这本小册子补。

---

## 2. System Design 101（ByteByteGo）

仓库正文就是 [README 目录](https://github.com/ByteByteGoHq/system-design-101/blob/main/README.md)，每条链到 bytebytego.com 的一页图解。本地对照物是 [learning-path §3](./ai/learning-path.md)（计算机基础 → 并发 → 接口 → 存储 → 队列 → 分布式 → 架构 → 治理 → 交付 → 安全 → 云原生）。

| 栏目 | 读法 | 对照 |
|---|---|---|
| [Cloud & Distributed Systems](https://bytebytego.com/guides/cloud-distributed-systems) | **必读** | §3.6 分布式、§3.11 云原生。优先：取舍、幂等、重试、故障检测、高可用、唯一 ID、事件溯源 |
| [Database and Storage](https://bytebytego.com/guides/database-and-storage) | **必读** | §3.4–3.5。优先：隔离级别、锁、B-Tree / LSM、分片、一致哈希、CAP、Kafka 投递语义、CDC |
| [Caching & Performance](https://bytebytego.com/guides/caching-performance) | **必读** | §3.4 Redis。优先：策略、淘汰、击穿、大 key、Redis 持久化、延迟数量级 |
| [Software Architecture](https://bytebytego.com/guides/software-architecture) | **必读** | §3.7。优先：编排 vs 编舞、微服务边界、DDD 词汇、架构模式、系统取舍 |
| [How it Works?](https://bytebytego.com/guides/how-it-works) | **练手** | 设计题：聊天、文档、地图、通知、直播、支付、实验平台。用 §1 的提问顺序口头过一遍，不抄图 |
| [API and Web Development](https://bytebytego.com/guides/api-web-development) | 对照 | §3.1 网络、§3.3 接口。优先：REST / gRPC / GraphQL、网关 vs 负载均衡、分页、HTTP/2·3、轮询 vs Webhook vs SSE |
| [Security](https://bytebytego.com/guides/security) | 对照 | §3.10。优先：会话 / JWT / OAuth、密码存储、SSO。Agent 沙箱与凭据走 [reliability/sandbox/](./ai/reliability/sandbox/)，不在这套图里 |
| [DevOps and CI/CD](https://bytebytego.com/guides/devops-cicd) | 对照 | §3.8–3.9。优先：部署策略、日志 / 指标 / 追踪、Kubernetes 服务类型 |
| [Real World Case Studies](https://bytebytego.com/guides/real-world-case-studies) | 选读 | 架构演进直觉：Discord 消息、Airbnb、Netflix、Figma 的 Postgres。当故事读，不当教科书 |
| [Payment and Fintech](https://bytebytego.com/guides/payment-and-fintech) | 按需 | 本库没有支付专题。要做时从支付系统、对账、避免重复扣款三页进入 |
| [Technical Interviews](https://bytebytego.com/guides/technical-interviews) | 方法 | 和 §1 练习一起用：先问清范围，再画数据流，最后讲取舍 |
| [Software Development](https://bytebytego.com/guides/software-development) | 查漏 | §3.2。并发 vs 并行、GC、阻塞队列。其余语言史、范式图跳过 |
| [Computer Fundamentals](https://bytebytego.com/guides/computer-fundamentals) | 查漏 | §3.1。DNS、TCP/UDP、进程 vs 线程、死锁 |
| [AI and Machine Learning](https://bytebytego.com/guides/ai-machine-learning) | 不作主线 | 模型与 Agent 在 [ai/](./ai/README.md)。这里只有时间线和一页图 |
| [DevTools & Productivity](https://bytebytego.com/guides/devtools-productivity) | 跳过 | Git、Linux 命令图。需要时再翻 |

**读完往本库写哪儿：** 仍写回 [learning-path §3](./ai/learning-path.md) 里标了「待写」的专题（例如 CAP / BASE），每次只补一个概念的「为什么」，不把图解目录搬进来。

---

## 3. AI System Design Guide

仓库：[ombharatiya/ai-system-design-guide](https://github.com/ombharatiya/ai-system-design-guide)。上游自述是持续更新的生产参考（README 写到 2026-08 的模型与协议），MIT。入口按目的跳，见仓库 README 的 Quick Navigation。

生命周期五段：基础 → 构建 → 运行 → 治理 → 应用。本库已有原理的章节只当目录用。

| 章 | 读法 | 本库 |
|---|---|---|
| [00 面试](https://github.com/ombharatiya/ai-system-design-guide/tree/main/00-interview-prep) | **必读** | 128 题 + 答题框架 + 白板练习。和 §1 的四步清单一起用：先收窄范围，再画数据流 |
| [14 评测与可观测](https://github.com/ombharatiya/ai-system-design-guide/tree/main/14-evaluation-and-observability) | **必读** | [reliability/eval/](./ai/reliability/eval/)。另两篇长文：[Phoenix + Langfuse](https://github.com/ombharatiya/ai-system-design-guide/blob/main/ai_evals_comprehensive_study_guide.md)、[LangWatch + Langfuse](https://github.com/ombharatiya/ai-system-design-guide/blob/main/ai_evals_complete_guide_langwatch_langfuse.md)。榜单解读看基准污染与 harness 方差 |
| [06 检索](https://github.com/ombharatiya/ai-system-design-guide/tree/main/06-retrieval-systems) | 补缺口 | [knowledge/rag/](./ai/knowledge/rag/)。已有 RAG 基础则只补 Contextual Retrieval、ColBERT、Agentic RAG、数据工程（去重 / PII / 去污染） |
| [12 安全与访问](https://github.com/ombharatiya/ai-system-design-guide/tree/main/12-security-and-access) | 补缺口 | 多租户隔离。传统鉴权在 §2 Security；Agent 凭据在 [reliability/sandbox/](./ai/reliability/sandbox/) |
| [11 基础设施](https://github.com/ombharatiya/ai-system-design-guide/tree/main/11-infrastructure-and-mlops) | 补缺口 | 网关与模型路由 → [reliability/model-routing/](./ai/reliability/model-routing/)；Token 成本单列一页，本库按专题散落 |
| [16 案例](https://github.com/ombharatiya/ai-system-design-guide/tree/main/16-case-studies) | 选读 | 优先四则：多租户 SaaS、评测门禁 CI、按租户 LoRA、基于 trace 的蒸馏。其余和本库案例重复的跳过 |
| [07 Agent](https://github.com/ombharatiya/ai-system-design-guide/tree/main/07-agentic-systems) | 对照 | [agent/](./ai/agent/README.md)、[loop-graph/](./ai/agent/loop-graph/)、[mcp/](./ai/agent/mcp/)。只补 durable execution 与 loop 预算 |
| [13 可靠与安全](https://github.com/ombharatiya/ai-system-design-guide/tree/main/13-reliability-and-safety) | 对照 | [guardrails/](./ai/reliability/guardrails/)。治理与合规（EU AI Act / NIST）本库薄，需要时再读 |
| [17 计算机使用](https://github.com/ombharatiya/ai-system-design-guide/tree/main/17-tool-use-and-computer-agents) | 对照 | [computer-use/](./ai/agent/computer-use/) |
| [18 语音](https://github.com/ombharatiya/ai-system-design-guide/tree/main/18-voice-and-audio-agents) | 对照 | [voice-realtime/](./ai/runtime/voice-realtime/) |
| [08 记忆](https://github.com/ombharatiya/ai-system-design-guide/tree/main/08-memory-and-state) | 对照 | [knowledge/memory/](./ai/knowledge/memory/) |
| [09 框架](https://github.com/ombharatiya/ai-system-design-guide/tree/main/09-frameworks-and-tools) | 对照 | [langgraph/](./ai/agent/case-studies/langgraph/)。框架版本漂移那一页值得留 |
| [01 基础](https://github.com/ombharatiya/ai-system-design-guide/tree/main/01-foundations) · [03 训练](https://github.com/ombharatiya/ai-system-design-guide/tree/main/03-training-and-adaptation) · [04 推理](https://github.com/ombharatiya/ai-system-design-guide/tree/main/04-inference-optimization) | 跳过当主线 | [foundation/](./ai/foundation/README.md)、[runtime/](./ai/runtime/README.md) 更深 |
| [02 模型版图](https://github.com/ombharatiya/ai-system-design-guide/tree/main/02-model-landscape) | 快照 | [landscape.md](./ai/landscape.md)、[厂商总览](./ai/model-cases/providers/各大厂商代表模型总览.md)。价格与型号会过期 |
| [05 提示](https://github.com/ombharatiya/ai-system-design-guide/tree/main/05-prompting-and-context) · [10 文档](https://github.com/ombharatiya/ai-system-design-guide/tree/main/10-document-processing) · [15 模式](https://github.com/ombharatiya/ai-system-design-guide/tree/main/15-ai-design-patterns) · [19 多模态生成](https://github.com/ombharatiya/ai-system-design-guide/tree/main/19-multimodal-generation) | 查漏 | 提示与上下文 → [context-engineering/](./ai/knowledge/context-engineering/)；模式名 → [agentic-design-patterns/](./agentic-design-patterns/README.md)；生成 → [generative/](./ai/foundation/generative/README.md) |

上游还挂了 [COURSES.md](https://github.com/ombharatiya/ai-system-design-guide/blob/main/COURSES.md)、[TRANSITION_GUIDE.md](https://github.com/ombharatiya/ai-system-design-guide/blob/main/TRANSITION_GUIDE.md)、[RESEARCH-RADAR.md](https://github.com/ombharatiya/ai-system-design-guide/blob/main/RESEARCH-RADAR.md)。学期课仍以本库 [ai/courses.md](./ai/courses.md) 为准；转岗路径本库有 [fde.md](./ai/fde.md)。

---

## 4. 学习顺序（现有三份）

三轮。本库已有的 Transformer / 训练 / 推理 / Agent 环节不插入这三轮。若换主材料，按 [§5](#s5)，这一节只排现在这三份。

**第一轮 · 提问骨架（小册子，短）**

1. [研究 vs 生产](https://github.com/chiphuyen/machine-learning-systems-design/blob/master/content/research-vs-production.md)
2. [四步清单](https://github.com/chiphuyen/machine-learning-systems-design/blob/master/content/design-a-machine-learning-system.md)（立项 → 数据 → 建模 → 上线）
3. Booking.com 六条：模型分和业务分分开、延迟写进目标、用随机对照看影响
4. 用同一张清单口头答 3 题：检索排序、盗刷或分布外、房价投资或缩短结账。先追问范围再答

**第二轮 · 生产 AI 缺口（Guide，主课）**

5. [00 面试框架](https://github.com/ombharatiya/ai-system-design-guide/tree/main/00-interview-prep)：用第一轮的清单收窄，再用这里的框架把图画完
6. [14 评测](https://github.com/ombharatiya/ai-system-design-guide/tree/main/14-evaluation-and-observability) + [Phoenix / Langfuse 长文](https://github.com/ombharatiya/ai-system-design-guide/blob/main/ai_evals_comprehensive_study_guide.md)，对照 [reliability/eval/](./ai/reliability/eval/)
7. 检索只补三页：Contextual Retrieval、ColBERT、数据工程（去重 / PII / 去污染）
8. 案例四则：多租户 SaaS、评测门禁 CI、按租户 LoRA、基于 trace 的蒸馏
9. 若还要往下：durable execution、loop 预算、网关与 Token 成本

**第三轮 · 传统系统（ByteByteGo，碰到再翻）**

10. 一道设计题卡在存储、缓存或分片时，才开这四栏：分布式取舍、数据库与分片、缓存失效、架构边界
11. 再挑一道 How it Works（聊天或通知），仍用第一轮的清单口头过

停在这里。Guide 的基础 / 训练 / 推理 / 模型版图，以及 ByteByteGo 的 API、安全、DevOps、AI 栏目，都不进顺序。学期课仍按 [ai/courses.md §0](./ai/courses.md#s0)，不和这三轮混排。

---

<a id="s5"></a>

## 5. 更好的材料（2026-09-24）

现在这三份里，只有 Guide 值得留作目录。小册子和 System Design 101 都有更完整的替代。

### 5.1 传统系统设计（替换第 2 份）

System Design 101 是图解目录，没有作业，也没有把一个设计从需求讲到失败模式。有经验的人按这个顺序：

| 顺位 | 材料 | 为什么更好 | 怎么用 |
|---|---|---|---|
| 1 | [HelloInterview · System Design in a Hurry](https://www.hellointerview.com/learn/system-design/in-a-hurry/introduction) | 按面试真实问法组织：需求、估算、数据模型、接口、深潜、取舍。免费，比 101 的散图能串成一次答题 | 先通读框架，再做 2 道（限流或聊天、feed 或通知） |
| 2 | [DDIA 第 2 版](https://dataintensive.net/)（Kleppmann、Riccomini） | 讲存储、复制、分片、事务、一致性为什么会坏。101 和 Alex Xu 的案例都停在这一层前面 | 只读：存储与检索、复制、分区、事务、一致性与共识。中文架构对照仍是《凤凰架构》，已在 [learning-path §3.7](./ai/learning-path.md) |
| 3 | Alex Xu《System Design Interview》卷 1–2 | 同一作者的完整案例，比 GitHub 图多了估算和取舍。付费站 [ByteByteGo](https://bytebytego.com/) 是这套书的加长版，不是另一门课 | 卷 1 当案例；卷 2 挑和手上系统像的题。不两卷通读 |
| 4 | [MIT 6.5840](https://pdos.csail.mit.edu/6.5840/index.html)（原 6.824） | 唯一要动手的：Raft、复制 KV、分片。材料全公开 | 只在要把「共识」写出来时做 Lab。不作为面试主线 |

101 降为第三轮的图鉴：DDIA 或 HelloInterview 里某个词不熟，再点开对应那一页。

### 5.2 机器学习 / AI 系统（替换第 1 份，第 3 份降为目录）

2019 小册子是作者自己标过的初稿。Guide 覆盖面大，但是百科，不是一门有作业的课。

| 顺位 | 材料 | 为什么更好 | 怎么用 |
|---|---|---|---|
| 1 | Chip Huyen《[AI Engineering](https://github.com/chiphuyen/aie-book)》（O'Reilly，2025） | 地基模型应用：提示与上下文、RAG、Agent、评测、推理成本。和本库 `ai/` 同题，比 2019 小册子新一整个范式 | 主课。评测章对着 [reliability/eval/](./ai/reliability/eval/) 读 |
| 2 | Chip Huyen《Designing Machine Learning Systems》（O'Reilly，2022），目录在 [dmls-book](https://github.com/chiphuyen/dmls-book) | 传统 ML：数据、特征、再训练、监控。AIE 故意写得浅的部分在这里 | 只补 AIE 指回 DMLS 的章，不从头读 |
| 3 | [CMU 17-445/645 Machine Learning in Production](https://mlip-cmu.github.io/s2026/)（当季仓库 [f2026](https://github.com/mlip-cmu/f2026)） | 把模型放进要运维的软件：需求、架构、测试、监控、事故。有往年公开材料，比 Guide 有课程结构 | 跟当季或刷最近一轮公开讲义。Agent 作业仍以 [ai/courses.md](./ai/courses.md) 的 11-768 / CS329Z 为准 |
| 4 | 现有 Guide | 多租户、评测门禁、按租户 LoRA、trace 蒸馏这些案例，两本书不展开 | 保持 §4 第二轮的第 8 步，其余章当目录 |

算力与推理引擎（vLLM、Roofline）不在这四份里。那条线已经在 [ai/courses.md](./ai/courses.md) 的 MLSysBook、MIT 6.5940、Berkeley Scalable AI。

### 5.3 换成这两条之后的顺序

1. HelloInterview 框架 + 2 道口头设计。
2. 《AI Engineering》通读，评测章对照本库。
3. DDIA 五章（存储、复制、分区、事务、一致性），用来回答第 1 步里说不清的取舍。
4. CMU 17-445 挑「需求 / 测试 / 监控」相关讲次。
5. Guide 只留四则案例；Alex Xu 只留和手上系统像的题；6.5840 的 Raft 以后再说。
