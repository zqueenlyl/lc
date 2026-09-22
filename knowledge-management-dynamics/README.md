# Knowledge Management Dynamics in a Transformative Environment

> IntechOpen 论文集（Mohiuddin / Hosseini / Gani / Ed-Dafali 编，2026-02-18）：7 章独立、全部开放获取。书名像「转型环境里的知识管理」，实际是**四章组织行为学 + 一章机器学习 + 一章发展经济学 + 一章本体入门**。本目录是**学习笔记**，与 [naval/](../naval/)、[agentic-design-patterns/](../agentic-design-patterns/) 同级；逐章详解，**不摘录正文、不入库 PDF**。

一句人话：**外部 KM 学科把 LLM 写成「查询时综合器」，本库把同一件事写成 RAG 的失败模式。** 但通读七章会发现更有意思的一点——书里推荐落地栈的那一章，用的正是另一章宣布过时的 SharePoint / Confluence。

- 书页：https://www.intechopen.com/books/1004253
- ISBN：978-1-83634-494-0（纸）/ 978-1-83634-495-7（PDF）；152 页
- 版权：各章 CC 开放获取。笔记编译结构、主张、证据边界与本库映射，不复制正文。
- 书页自报影响力（检索日 2026-09-20）：章下载约 1,342、引用 7。**不作质量证据**。

---

## 一、本手册交付标准

对齐 `lc/` 已交付的书笔记（[博弈论](../game-theory/README.md)、[Agentic Design Patterns](../agentic-design-patterns/README.md)）。这本书的特殊要求是：**每章方法与证据等级都不同，必须逐章写清，不能一句「质量参差」打包**。

| 层 | 必须有 | 本目录落点 |
|---|---|---|
| **索引** | 一句人话、七章总表、书内矛盾、跳读、红线 | 本页 + [01](./01-坐标系与七章总表.md) |
| **章** | 作者与时间、逐节走读、关键定义/表/数字、证据边界、本库对照 | [02](./02-ch1-本体与信息科学.md)–[08](./08-ch7-SME绿色知识管理.md)（一章一篇） |
| **过线** | 按章问 + 诊断四问 + 证据等级速查 + 事实禁区 | [09](./09-自测与红线.md) |

读者不翻原书能做到这四件，才算读过：

1. **讲得出每章在做什么**：方法、样本、有没有一手数据。
2. **分得清两套「知识转移」**：ML 的表征迁移（第 2 章）≠ 组织的跨部门流动（第 5 章）。
3. **画得出 query-time vs 编译**：现场综合 vs 带 `raw/` 的编译产物；本库站后者。
4. **拒得掉一组数字**：第 5 章匿名案例、第 4 章企业自报、「GPT-4 1.7T」、第 3 章把系数当百分点。

---

## 二、目录结构

```
knowledge-management-dynamics/
├── README.md                              # 本索引：七章总表 + 冲突 + 跳读
├── 01-坐标系与七章总表.md                  # 书的元信息 / 三堆分组 / 书内自相矛盾
├── 02-ch1-本体与信息科学.md                # 定性综述：哲学→OWL→SDLC
├── 03-ch2-先验知识引导的表示学习.md        # 唯一有基准表的 ML 章：FeAug / CapKP / MSR
├── 04-ch3-移动应用与小农生产力.md          # n=220 问卷 + logit：WhatsApp 才是农业知识系统
├── 05-ch4-集体智慧与知识分享实践.md        # 存储≠触达 + 两家印度企业的真实知识栈
├── 06-ch5-LLM跨域知识转移.md               # 主菜：query-time 综合 + epistemic dependency
├── 07-ch6-知识分享理论透镜.md              # 分享四态 + SCT/SET/TRA/TPB/RBV + 领导力
├── 08-ch7-SME绿色知识管理.md               # 14 家保加利亚 SME 深访：都做 KM，没人有 KM 战略
└── 09-自测与红线.md                        # 十问 + 证据等级速查 + 事实禁区 + 处境速查
```

---

## 三、七章总表

> 「本库」列指向已经写过的原理，不是「书可以不看」。书的价值是**外部学科的同期表述与真实落地栈**；本库的价值是**工程红线**。

| # | 章 | 一句话 | 方法 / 有无一手数据 | 本库对照 | 笔记 |
|---|---|---|---|---|---|
| 1 | Integrating Ontology in IS and AI | 从 Harvey 1663 讲到 OWL，末尾接一张「本体贡献于 SDLC 各阶段」的图 | 定性综述；无实验 | [ontology](../ai/knowledge/ontology/) | [02](./02-ch1-本体与信息科学.md) |
| 2 | Cross-Level Unbiased Prior Knowledge-Guided DRL | 先验知识按引入时机分三层，各给一法：FeAug / CapKP / MSR | Perspective + 基准表；**有数据** | [transformer](../ai/foundation/transformer/) · [多模态](../ai/foundation/generative/multimodal/) · [loop-graph](../ai/agent/loop-graph/) | [03](./03-ch2-先验知识引导的表示学习.md) |
| 3 | Mobile Applications × 东开普小农 | 70% 在用，WhatsApp 占 54%；卡在钱、信号、素养 | 问卷 n=220 + logit；**有数据**（2019） | 无（方法可借） | [04](./04-ch3-移动应用与小农生产力.md) |
| 4 | Unlocking Collective Wisdom | 存下来 ≠ 送到人手上；附两家印度企业知识栈 | 综述 + 案例叙事 | [knowledge-base](../ai/knowledge/knowledge-base/) · [context-engineering](../ai/knowledge/context-engineering/) | [05](./05-ch4-集体智慧与知识分享实践.md) |
| 5 | Cross-Domain Knowledge Transfer in Large Models | LLM 当查询时综合器与「主动主体」；提出 epistemic dependency | 概念框架 + 匿名案例；**无受控实验** | [rag](../ai/knowledge/rag/) · [memory](../ai/knowledge/memory/) · [guardrails](../ai/reliability/guardrails/) | [06](./06-ch5-LLM跨域知识转移.md) |
| 6 | Knowledge Sharing: Theoretical Lenses | 显性/隐性、捐出/收集、分享四态、五种透镜 | 理论综述；无数据 | 本库无 SECI 页 | [07](./07-ch6-知识分享理论透镜.md) |
| 7 | Environmental Challenges in SMEs through KM | 14 家 SME 都做 KM，但无人有 KM 战略；绿色多由资金与形象驱动 | 深访 n=14；**有数据** | 无（观察可借） | [08](./08-ch7-SME绿色知识管理.md) |

公开章链接：[Ch1](https://www.intechopen.com/chapters/1200731) · [Ch2](https://www.intechopen.com/chapters/1208486) · [Ch3](https://www.intechopen.com/chapters/1208553) · [Ch4](https://www.intechopen.com/chapters/1209447) · [Ch5](https://www.intechopen.com/chapters/1209560) · [Ch6](https://www.intechopen.com/chapters/1212924) · [Ch7](https://www.intechopen.com/chapters/1215292)

---

## 四、学习路线

```
只想知道「为什么要记这本书」（30 分钟）
  本页冲突节 → 01 §四 书内矛盾 → 06（Ch5）

要对外讲「Wiki 不是 SharePoint」（半天）
  01 → 06 → 05（看真实落地栈）→ 09 红线 → 回 [rag](../ai/knowledge/rag/)

补组织 KM 词汇（不改本库定义）
  07（四态 + 透镜）→ 05（实践）→ 若要 SECI 回 Nonaka 1995

只对技术章有兴趣
  03（Ch2：对比学习 / KG 提示 / 因果后门调整）——与 KM 主线无关，独立可读

方法论借用
  04（扩散理论 + TPB + logit 怎么设计问卷）· 08（小样本深访怎么写结果）
```

**按需求跳读**：

| 你的问题 | 读这些 |
|---|---|
| 有人说「LLM 打破知识孤岛，wiki 过时了」 | 本页冲突 → [06](./06-ch5-LLM跨域知识转移.md) → [05](./05-ch4-集体智慧与知识分享实践.md) |
| 有人把 Ontology 从亚里士多德讲到 OWL | [02](./02-ch1-本体与信息科学.md) → [ontology](../ai/knowledge/ontology/) |
| 要 SECI / 隐性知识 / 囤积 这套词 | [07](./07-ch6-知识分享理论透镜.md)，定义源另找 |
| 评估「企业知识中台 / 第二大脑」方案 | [06 §七](./06-ch5-LLM跨域知识转移.md) + [09 诊断四问](./09-自测与红线.md) |
| 想看对比学习 / CLIP 提示 / 因果去混淆 | [03](./03-ch2-先验知识引导的表示学习.md) |
| 内部知识产品为什么没人用 | [04](./04-ch3-移动应用与小农生产力.md)（工具在已打开的 App 里）+ [08](./08-ch7-SME绿色知识管理.md)（顺习惯而非立战略） |

---

## 五、和本库的显式冲突

第 5 章把早期 wiki / SharePoint / Confluence 写成「传统仓库」：擅长显性知识，卡在隐性知识与部门墙；主张用 LLM **实时跨域综合**，并称模型能「生成新知识」。

本库结论相反，写在 [知识库类型整理 §五](../ai/knowledge/knowledge-base/知识库类型整理.md) 与 [rag](../ai/knowledge/rag/)：

| | 第 5 章（query-time KM） | 本库（编译型 Wiki / 受控检索） |
|---|---|---|
| **知识何时成形** | 提问的那一刻，由模型现场综合 | Ingest 时编译进页面；Query 是阅读已编译物 |
| **wiki 的位置** | 过时仓库，和 SharePoint 同类 | 唯一写作层；`raw/` 才是事实真相层 |
| **矛盾怎么处理** | 未讨论 | 显式标注来源与冲突 |
| **失败之后** | 没有源层可修 | 保留源才修得回来 |
| **「新知识」** | 发现跨域模式即创造 | 模型不编造事实；跨域类比只是假说 |
| **引用** | 不是验收项 | 答不在命中块里 = 失败 |

不要悄悄改本库立场。对外一句话划界：**他们说的 wiki 是文档柜；本库说的 Wiki 是带 `raw/` 的编译产物。**

**补一记更硬的反驳**（通读全书才有）：同书第 4 章的 IT 安全公司案例，知识栈是 SharePoint 中央库 + Confluence 威胁情报 + Slack/Teams + Jira/Asana + LMS；药企案例是 PKMS 仓库 + AI 搜索 + 实践社区。**实践章在建仓库，理论章在宣布仓库死亡。** 详见 [01 §四](./01-坐标系与七章总表.md)。

---

## 六、怎么用这本书（以及这份笔记）

1. **按章取用，不按书取用。** 七章方法与证据等级差别极大，速查见 [09 §三](./09-自测与红线.md)。
2. **带走三样**：① query-time 综合的阵营标签；② *epistemic dependency*（判断外包的认知依赖，无操作化，当检查项）；③ 第 4 / 7 章的真实落地栈与「无 KM 战略」观察。
3. **第 5 章的治理清单可以直接用**：联邦学习、零信任、对抗式去偏、SHAP/LIME 可解释、定期审计、干系人参与——这是全章质量最高的一节。
4. **SECI / 本体定义要一手**。第 6 章只证明本库缺 SECI 页；第 1 章不能覆盖 Gruber 与 Palantir。更好的 SECI 后继（**本库未读**，仅检索命中）：GRAI（Emerald *VINE* 2026）、arXiv `2603.21866`。
5. **数字一律待验证**。禁区清单在 [09 §四](./09-自测与红线.md)。

一手读开放获取章页；本笔记负责把每章收成可检索的骨架，并指回 `ai/knowledge` 已经写过的红线。

---

## 七、与本仓其它专题

- 知识五维 / LLM Wiki → [ai/knowledge](../ai/knowledge/) · [knowledge-base](../ai/knowledge/knowledge-base/)
- RAG 失败模式 → [rag](../ai/knowledge/rag/) · [环节 06](../ai/agent/环节06-检索增强RAG详解.md)
- OWL vs 运营本体 → [ontology](../ai/knowledge/ontology/)
- 对比学习 / CLIP / 图谱提示的邻居 → [foundation](../ai/foundation/) · [loop-graph](../ai/agent/loop-graph/)
- 治理与人审 → [guardrails](../ai/reliability/guardrails/) · [agentic-design-patterns Ch13](../agentic-design-patterns/03-可靠与对齐.md)
- 同级书 / 专题笔记 → [naval](../naval/) · [game-theory](../game-theory/) · [agentic-design-patterns](../agentic-design-patterns/)
