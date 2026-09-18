# TypeSafe 全景与 System One

> 检索时点：**2026-09-18** ｜ 范围：TypeSafe AI 的模型类 **System One**、旗舰 **Jev 1.13**
> **口径约定**：`官方`= [typesafe.ai](https://typesafe.ai) 博客 / [docs.typesafe.ai](https://docs.typesafe.ai) / OpenRouter 模型页；`社区`= 第三方解读（显式标注）；`未披露`= 官方未给数字或实现细节。
> ⚠️ **不是聊天模型。** Jev 不写字、不写代码、不解释推理过程。把它塞进 `/v1/chat/completions` 是接错协议。接入见 [《Jev 接入与工程实践》](./Jev接入与工程实践.md)。
> ⚠️ **也不是 Scala 那个 Typesafe**（Akka / Lightbend）。这家是 2026 年公开的决策模型实验室。
> 配套 notebook：[Jev原语与置信度门闩演示.ipynb](./Jev原语与置信度门闩演示.ipynb)（按 [OpenRouter Jev Latest](https://openrouter.ai/~typesafe/jev-latest) Quick Start 写；无 key 用同构 fixture）。

---

## 一、摘要（TL;DR）

1. **TypeSafe 卖的是「给软件用的快判断」，不是对话。** 官方把自己的模型类叫 **System One**：吃一段 `state`（字符串 / JSON / 数组），对你预先定义的问题做并行求值，吐出带校准概率的类型化答案。旗舰叫 **Jev**，现网版本 `jev-1.13.0`。
2. **三个原语覆盖全部问题形状。** `noul`（是/否概率）· `choice`（从你给的选项里挑一个，最多 255）· `score`（落在你写的有序量表上，2～10 档）。应用代码拥有工作流：阈值、加权、升级到人 / 推理模型，都写在仓库里，不写在散文提示里。
3. **和 LLM 的结构化输出不是同一条路。** LLM 仍在逐 token 生成字符串，再被 schema / 工具协议约束；Jev **放弃字符串生成**，官方称并行采样、类型错误在数学上不可能。语义判断仍会错——「不幻觉」只保证**不越出你定义的答案空间**，不保证判断正确。
4. **现网规格（官方 Models 页）**：输入 **$0.042 / MTok**，输出免费；端到端宣称 **70～500ms**；请求总预算 **64k** token，其中 `state` + 最长那条问题 **32k**。只吃文本。权重不开源，不能 LoRA。

**核心判断**：选型时 Jev 和 GPT / Claude / DeepSeek **不在同一列**。后者是发动机（生成、推理、工具循环）；Jev 是代码里的模糊 if——路由、打分、校验、护栏。该生成时仍用 LLM；该分支时再问 Jev。

---

## 二、身份与命名

| 项 | 口径 | 来源 |
|----|------|------|
| 公司 | TypeSafe AI，[typesafe.ai](https://typesafe.ai) | 官方 |
| 创始人 | Diogo Almeida（官方自述曾在 OpenAI 做指令跟随，参与 ChatGPT 背后的方法） | 官方博客 |
| 公开 | 博客 **2026-09-15**；OpenRouter 上架 **2026-09-18** | 官方 / OpenRouter |
| 模型类 | **System One**（Kahneman《思考，快与慢》的 System 1：快、直觉式判断） | 官方 |
| 旗舰 | **Jev**，纪念 Jevons 悖论：效率提升会放大用量，而不是省用量 | 官方 |
| 现网 ID | `jev-1.13.0`；别名 `jev-latest` / `jev-preview` 当前都指向它 | 官方 Models |
| 开放形式 | 仅 API（early access / 候补名单）；**未见权重、未见论文** | 官方 |
| 渠道 | 原生 `api.typesafe.ai`；OpenRouter Decisions API；Cloudflare Workers AI；Vercel AI Gateway | 官方 / 渠道页 |

「System One」强调的是**快、窄、可组合**，不是「比 System 2 笨」。官方明确：他们相信这类模型可以比「用 LLM 硬挤结构化答案」更可靠，理由写在校准与类型约束上，细节 `未披露`。

---

## 三、现网规格快照（Jev 1.13）

| 项 | 数字 | 人话 | 来源 |
|----|------|------|------|
| 版本化 ID | `jev-1.13.0` | 调阈值请钉这个，别钉别名 | 官方 |
| 别名 | `jev-latest`（SDK 默认）、`jev-preview` | 现都指向 1.13.0；有预览构建时 preview 会先行 | 官方 |
| 输入价 | **$0.042 / MTok**（=$42 / BTok） | 只收输入 | 官方 + OpenRouter |
| 输出价 | **$0** | 官方口径「too cheap to meter」 | 官方 |
| 延迟 | **70～500ms** 端到端 | 官方自测多从美西笔记本打到现网服务 | 官方博客 |
| 限流 | 250,000 tok/s · 1,200 RPM | **动态调整**，超限 `429`；过载 `529` | 官方 |
| 上下文 | 整请求 **64k**；`state` + 最长问题 **32k** | OpenRouter 模型页只标 **32k**（见接入篇） | 官方 / OpenRouter |
| 输入 | 文本：string / JSON object / text array | 图 / 音 / 视频要先转成文字再塞 `state` | 官方 |
| 输出 | 结构化决策，不是 token 流 | `noul` / `choice`+分布 / `score`+legend | 官方 |
| 语言 | 英语最好；含 CJK 的其它语言「能处理但较差」 | 非英语工作负载先用自己的数据测，盯 `confidence` | 官方 |
| 微调 | **不提供**客户数据 LoRA / fine-tune | 领域适配靠 `state` + `instructions` / `criteria` | 官方 |
| 数据 | 不拿客户请求训练；企业可谈 ZDR | 见 Legal / DPA | 官方 |

参数量、层数、是否 Transformer、并行采样器实现、RLCD 损失形式、训练数据构成：**全部未披露**。

---

## 四、System One 和 LLM 差在哪

官方对照（博客 2026-09-15），这里只保留工程上用得上的列：

| 维度 | 现有 LLM | System One / Jev |
|------|---------|------------------|
| 优化目标 | RLHF / RLVR：人偏好的写稿，或可程序验证的答案 | **RLCD**：在 System One 任务上给出认知上诚实的概率 |
| 输入重心 | 顺序消息 | **程序状态**（记录、票据、政策、短名单） |
| 输出 | 字符串（再解析 / 再校验） | 预先定义的类型化值 + 校准概率 |
| 采样 | 自回归，一个 token 接下一个 | **并行**：一次查询给出所有答案 |
| 置信 | 即便被要求报置信，也常过自信、不稳定 | 每条答案带概率；Choice / Score 另有 `confidence` |
| 典型用法 | 聊天、Copilot、需要人盯的 Agent、可验证搜索 | 工作流里的模糊 if、大规模 map-reduce、实时 UX、给 LLM 做校验 |

官方宣传的量级（**厂商自述，不是第三方复现**）：

- 同等 System One 智力下，比前沿 LLM **快 40×～200×**；主页还有 **193.6× 更快 / 444.6× 更便宜** 的工作流评测数字，官方自己说这是偏高一侧。
- 对照模型：侧写 demo 用 **GPT-5.6 Terra**；工作流评测用 **GPT-6 Astra 与 Fable 5.1 的平均**当参考概率。LLM 侧走的是 TypeSafe 自己的「System One wrapper」（强迫 LLM 吐兼容格式），不是各家裸 chat。
- 「0% 类型错误」：**不是实测**。官方说 schema 匹配是保证的，所以可以画 0%；LLM 的类型错误数字来自 OpenRouter，复杂请求可能被路由到更好的模型，有偏。

**不要把「不能幻觉」读成「判断永远对」。** 类型安全 ≠ 语义正确。答案一定落在你给的选项里；选错选项、概率校准漂移、字面理解指令，官方 jaggedness 页都承认。

---

## 五、三个原语

一次请求 = 一份 `state` + 一张 `questions` 表。每个问题独立、并行、看到同一份 state。问题的 **key 不进模型**，完整判断写在 `instructions` 里。

| 类型 | 问的是 | 你必须给 | 回来的东西 | 适合 |
|------|--------|----------|------------|------|
| **Noul** | 这句话是真的吗？ | `instructions`；可选 `criteria.true` / `false` | `noul` ∈ [0, 1]。**没有单独的 confidence** | 退款意愿、是否紧急、是否越狱 |
| **Choice** | 这些选项里哪一个？ | `criteria` 映射，最多 **255** 项 | `choice` + 全分布 `probabilities` + `confidence` | 路由部门、文档类型、技能名 |
| **Score** | 落在量表哪一档？ | 有序 `criteria` 数组，**2～10** 档 | `score`（可落在两档之间）+ `legend` + `probabilities` + `confidence` | 愤怒程度、严重度、风险 |

选用口诀：

- 答案是无序闭集 → Choice（列表可能盖不全就加 `other` / `none`）。
- 答案是有序光谱，且每一档能用情景描述 → Score。档位写情景（「有变通办法的故障」），不要写程度词（「中等严重」）。
- 答案是干净的是否，**概率本身就是信号** → Noul。Noul = 0.5 表示「是/否各一半」，**不是**「中等程度」。测技能高低请用 Score。

`score` 是档位编号的**概率加权均值**。同一分数可以来自完全不同的分布（全压在 1，或 0 与 2 各一半）——所以要同时读 `probabilities` 和 `confidence`。官方警告：**不要用相邻两档插值去还原一个精确数字**，1.13 的数值校准弱。

`confidence`（仅 Choice / Score）是从分布形状算出的 0～1 统计量：越尖越高。官方给的是便捷默认，你也可以自己用 `probabilities` 算别的。Noul 没有这个字段，靠近 0.5 本身就是不确定。

---

## 六、该用 / 不该用

**该用（官方 + 食谱方向）**

- 工单 / 线索 / 表单的路由、分级、紧急度
- 把复杂判断拆成原子分，在代码里加权（composite scoring）
- 一次请求里扇出十几条问题（speculative fan-out）；官方 cookbook：13 问打进一枪，相对 13 次独立调用约 **12.2× 便宜、10.0× 快**（另一处写 11.5× / 9.6×，以 cookbook 页为准）
- RAG 段落过滤、引用核对、LLM 输入/输出护栏
- 高基数重排、层级分类、技能选择（先 Choice 再对短名单 Noul）
- 实时 UX：官方 Doom demo 量级约 10 QPS、约 $7/小时（结构化游戏状态，**不是看画面**）

**不该用（官方 jaggedness，适用于 `jev-1.13`，审阅 2026-09-17）**

| # | 失败模式 | 改法 |
|---|---------|------|
| 1 | 字面阅读：否定、范围词按字面吃 | 把边界写进 `instructions` / `criteria` |
| 2 | 计数、算术、hex/RGB 远近 | 算术放代码；语义判断再问模型 |
| 3 | 日期先后、窗口、季度 | 拆成 Choice 抽月/日/年，比较在代码里 |
| 4 | 双重否定、多跳间接 | 减跳数；用反引号路径点名字段 |
| 5 | 大 state 里塞无关内容 | 先过滤；Jev 有 context rot |
| 6 | 对抗性 / 注入式 state | 准则写死；上线前测边角 |
| 7 | `instructions` 与 `criteria` 打架 | 两者当同一句话的两半 |
| 8 | 以为 Noul 与 Choice yes/no 算术恒等 | 不要把 Noul 阈值搬到 Choice；不要要求 `P + ¬P = 1` |
| 9 | 用 Choice 链「生成」文本 | 用生成模型；抽取先正则/LLM 出候选，再让 Jev 选 |

System Two（多层间接、长推理、要写稿）交给推理模型。Jev 负责「内行看一眼能拍板」的那种判断。

---

## 七、和本仓库其它层怎么接

| 层 | 关系 | 不要混成 |
|----|------|----------|
| [Structured Output](../../reliability/structured-output/) | LLM 仍生成 token，再用 schema / 约束解码卡住形状 | Jev **不是** Outlines / `response_format` 的另一种写法 |
| [Model Routing](../../reliability/model-routing/) | Jev 很适合当前置分类器：难/易、要不要人、走哪条 LLM | 不要把 Jev 当旗舰生成模型的平替 |
| [Guardrails](../../reliability/guardrails/) | 官方 cookbook 就是用 Noul+Score 筛越狱与危害度，阈值在你代码里 | L2 工具门禁仍必须是确定性策略，别让 Jev 自评「能不能转账」 |
| [Agent](../../agent/) | 技能选择、意图分流、引用核对可以挂在循环外缘 | Jev 不产 tool call 字符串；function calling 食谱是「闭集参数 → Choice」 |
| [landscape.md](../../landscape.md) | 产业扫盲只记「有一类不是 LLM 的决策模型」 | 版本号与端点以本目录为准 |

---

## 八、未披露 / 未核实

| 项 | 状态 |
|----|------|
| 参数量、是否 Transformer、并行采样器细节 | 未披露 |
| RLCD 公式、奖励、训练数据 | 未披露（官方 FAQ 有「训练数据从哪来」折叠项，页面抓取未展开） |
| 工作流评测的可复现 harness / 是否过拟合自家工作流 | 官方承认评测由能力团队撰写，可能有偏 |
| 「不能幻觉」对语义错误的覆盖 | 官方只保证类型/schema；语义错误见 jaggedness |
| 中文 / CJK 的定量差距 | 只说「较差」，无数字 |
| 候补名单放量节奏、稳定限流承诺 | 限流「在 GPU 到位前会变」 |
| OpenRouter `/api/v1` Chat Completions 能否打 Jev | 模型页走 **Decisions API**；厂商聚合页 FAQ 仍写 OpenAI 兼容——**以模型页为准**，见接入篇 |

---

## 九、参考来源

**官方**

- [Introducing System One Models & Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev)（Diogo Almeida，2026-09-15）
- [System One](https://docs.typesafe.ai/concepts/system-one) · [Introduction](https://docs.typesafe.ai/introduction) · [Models](https://docs.typesafe.ai/models) · [Primitives](https://docs.typesafe.ai/primitives)
- [Choice](https://docs.typesafe.ai/primitives/choice) · [Score](https://docs.typesafe.ai/primitives/score) · [Noul](https://docs.typesafe.ai/primitives/noul) · [Confidence](https://docs.typesafe.ai/confidence)
- [Jev 1.13 jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13)（审阅 2026-09-17）
- [How to build with TypeSafe](https://docs.typesafe.ai/concepts/how-to-build-with-system-one) · [API reference](https://docs.typesafe.ai/api)

**渠道**

- [OpenRouter · TypeSafe: Jev Latest](https://openrouter.ai/~typesafe/jev-latest) · [Jev 1.13](https://openrouter.ai/typesafe/jev-1.13) · [Typesafe 厂商页](https://openrouter.ai/typesafe)
- [Cloudflare AI · typesafe/jev](https://developers.cloudflare.com/ai/models/typesafe/jev/)

**社区（线索，不当结论）**

- [A deep dive into Jev, TypeSafe's System One model](https://flaviocopes.com/jev/)（Flavio Copes；含 Vercel AI Gateway `typesafe-ai/jev`、AI SDK `experimental_evaluate`）

接入、协议、坑清单：[《Jev 接入与工程实践》](./Jev接入与工程实践.md)

配套 notebook：[Jev原语与置信度门闩演示.ipynb](./Jev原语与置信度门闩演示.ipynb)
