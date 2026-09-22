# Ontology · 本体（学术 OWL vs 运营层）

> **定位**：知识库五维里的「④ 表示与建模」展开。OWL / RDF 是语义网那一套；Palantir Foundry Ontology 是**组织数字孪生**那一套——同一词、不同工程目标。
>
> 快照：**2026-09-18**。官方文档口径见 [Palantir Ontology Overview](https://www.palantir.com/docs/foundry/ontology/overview/) 与 [Core concepts](https://www.palantir.com/docs/foundry/ontology/core-concepts/)；首页 [palantir.com](https://www.palantir.com/)。未在文档出现的数字 / 内部实现不写。

上级：[../README.md](../README.md) ｜ 五维总表：[../knowledge-base/](../knowledge-base/) ｜ 跨实体事实轴：[../../agent/loop-graph/context-graph.md](../../agent/loop-graph/context-graph.md)

---

## 一、先分清两条「Ontology」

「Ontology」在工程里至少指两件不相交的事。混用会把 Protégé 推理器当成企业写回层，或把 Palantir Action 当成 OWL 公理。

| | **学术 / 语义网本体** | **运营本体（Palantir 用法）** |
|---|---|---|
| **经典定义** | 领域「共享概念化的显式规范」（Gruber 1993） | 「对世界的一种分类」；在 Foundry 里是**组织的数字孪生** |
| **回答的问题** | 这个领域里合法的类、关系、公理是什么？能否推理出蕴含？ | 这家组织里真实存在的对象、关系、**允许发生的变更**是什么？人和 LLM 怎么在治理下改它？ |
| **核心构件** | Class / Property / Individual；TBox + ABox；公理 | **Object type / Object / Property / Link type / Action type**；另有 Function、Interface、Role |
| **语言 / 栈** | RDF、RDFS、OWL、SPARQL、SWRL、SKOS；Protégé | Foundry Ontology Manager；对象由数据集 / 虚拟表 / 模型**回填** |
| **「写」意味着什么** | 改公理或断言；reasoner 重算一致性 | **Action**：一次事务改对象、属性、链接，可带校验、副作用、回写源系统 |
| **和 LLM 的关系** | LLM 帮人建 OWL；OWL 反过来约束生成 / KGQA | Ontology 是 LLM **唯一被授权碰到的企业语义面**：查对象集、调 Function、提交已批准的 Action |
| **成功标准** | 逻辑一致、可互操作、可复用 | 决策可规模化：同一对象在 Explorer / Quiver / Workshop / AIP 里看到同一真相 |

选型口诀：

- 要跨机构共享概念、做形式化推理、发标准词表 → **OWL 线**。
- 要把 CRM / ERP / 工单 / 传感器对齐成「同一个客户 / 同一台设备」，并让人与 Agent **在权限内改状态** → **运营本体线**（Palantir 是工业界把这套说清楚并产品化的参照）。
- 有界领域只需要稳定 ID + 类型化关系、暂不需要动作治理 → 应用 Schema / 属性图即可，见 [上下文图](../../agent/loop-graph/context-graph.md)。不必一上来 OWL，也不必一上来买 Foundry。

---

## 二、学术本体（OWL / RDF）在本目录的位置

五维正文仍以 OWL 为主：[知识库类型整理 §四](../knowledge-base/知识库类型整理.md)。要点不重复展开：

- Taxonomy ⊂ Ontology：只有 is-a 是分类法；加上属性、实例、不相交 / 等价等才是本体。
- Ontology ≈ KG 的 **TBox**；实例是 **ABox**。
- 优点：语义精确、可推理、可共享。缺点：构建贵、大规模推理慢、难表达模糊常识。
- LLM 时代双重角色：帮人更快建本体；本体当白名单约束 LLM。个人 Wiki 侧见 `my-kb/wiki/concepts/ontology.md`。

---

## 三、Palantir Ontology：组织操作系统的语义 + 动能

官方原句（Overview）：Ontology 是组织的 **operational layer**，架在已接入平台的数字资产（datasets、virtual tables、models）之上，把它们接到现实对应物——工厂、设备、产品，或订单、交易这类概念。在许多场景里它就是组织的 **digital twin**，同时包含：

- **语义（semantic）**：objects、properties、links
- **动能（kinetic）**：actions、functions、**dynamic security**

目标不是「更漂亮的数据目录」，而是 **规模化更好的决策**：同一套对象定义驱动 Object Views、Object Explorer、Quiver、Workshop，以及 AIP 上的 Logic / Agent。

### 3.1 构件（Core concepts）

官方把 Ontology 构件和数据集结构做了一张平行表——这是理解它「不像 OWL」的最快方式：

| 数据集直觉 | Ontology |
|---|---|
| Dataset | **Object type**（一类实体或事件的 schema） |
| Row | **Object**（一个实例 = 一个真实世界实体 / 事件） |
| Column | **Property** |
| Cell | **Property value** |
| Join | **Link type**（两类对象之间一种关系的 schema） |

补充术语：

| 术语 | 含义 |
|---|---|
| **Object set** | 多个 object 的集合（一组真实实体 / 事件） |
| **Shared property** | 跨 object type 复用的属性，元数据集中管理 |
| **Link** | link type 的一条实例；文档写明 **bidirectional**，两侧各有 display / API name，可独立遍历（例：`flight.assignedAircraft.get()` ↔ `aircraft.flights.all()`） |
| **Action type** | 一次可提交的变更集合（改对象 / 属性 / 链接）+ 提交时的副作用；带参数、校验、提交条件 |
| **Function** | 代码级业务逻辑：吃 object / object set，读属性，可被 Action 与应用复用 |
| **Interface** | 描述 object type 的形状与能力 → **多态**（共享形状的类型用同一套交互） |
| **Roles** | Ontology 权限模型；可授到整棵本体或单个资源 |
| **Object View** | 某个 object 的中枢：自身字段、链接对象、指标、相关分析与应用 |

对象不是抽象 UML。官方反复强调：要把 backing datasource 挂到 object type（多对多时挂到 link type 自己），Ontology 才接到组织的真实数据。

### 3.2 Action：本体可写，才叫运营层

[Action types](https://www.palantir.com/docs/foundry/action-types/overview/)：用户通过 **apply action** 改对象。一条 action 是**单次事务**，按用户定义的逻辑改一个或多个对象的属性（以及链接）。

例：`Assign Employee` 改 `Employee.role`，参数表单标准化输入，规则可自动建 `Employee ↔ Manager` 链接，副作用可通知相关人。校验可限制「只有授权员工能提交」。

提交后：

- 变更进入 Ontology，**所有消费该对象的应用立刻看到同一版**
- 同一套 action 逻辑与校验跨应用复用 → 一致写入
- 含用户编辑的最新对象数据进入该 object type 的 **writeback dataset**

这是和 OWL 最大的产品差异：**动能是一等公民**。学术本体默认「描述世界」；Palantir Ontology 默认「在治理下改世界，并回写」。

### 3.3 和 AIP / LLM 怎么接

Palantir 把 AIP（Artificial Intelligence Platform）架在 Ontology 上：LLM 不直接扫湖仓表，而是：

1. 在授权范围内检索 / 遍历 **object set**（可叠加对象上的向量，做语义近邻）
2. 把 **Function** 当工具（读属性、聚合、调用已有逻辑）
3. 只提交 Ontology 里已配置、已鉴权的 **Action**（写回有校验与审计）

公开博客口径（[Building with Palantir AIP: Semantic Search](https://blog.palantir.com/building-with-palantir-aip-semantic-search-dc3adf40f6a6)）：Ontology = data + logic + action，是运营的实时决策图；作为 semantic system，它是 LLM **安全接触企业**的底座。Workshop 应用里用户动作仍经 Ontology 中介，设计上要写回源系统，并把决策留下学习闭环。

工程翻译：这是「工具 = 领域动作」而不是「工具 = 任意 SQL」。和 [上下文图必须显式设计的契约](../../agent/loop-graph/context-graph.md)（稳定身份、类型化关系、时效、provenance、权限）同构，只是 Palantir 把 **Action + Role** 做成了产品原语。

### 3.4 产品坐标（避免和 Gotham 混）

[palantir.com](https://www.palantir.com/) 产品线（名称级，不做内部架构推断）：

| 产品 | 常见定位 |
|---|---|
| **Foundry** | 商业 / 工业数据与运营平台；Ontology 文档挂在 Foundry docs 下 |
| **Gotham** | 政府 / 国防侧平台（与 Foundry 分产品，不要把 Ontology 文档默认成 Gotham API） |
| **AIP** | 在 Ontology 上的 AI 应用层（Logic、Agent、Copilot 类工作流） |
| **Apollo** | 持续交付 / 多环境部署 |

本页只深挖 **Foundry Ontology**。Gotham 是否共用同一套对象模型：**待官方对照页再写，不在此合并**。

---

## 四、和本手册其它专题怎么拼

```
湖仓 / 业务库 / 模型
        │  映射（backing datasource）
        ▼
运营本体：object · property · link · action · function · role
        │
        ├─ 人：Object Explorer / Quiver / Workshop / Object View
        ├─ LLM：AIP Logic / Agent（只碰授权对象 + 已登记工具）
        └─ 检索：对象集过滤 +（可选）对象向量近邻 + 仍可外挂 BM25/RAG 原文
```

| 需求 | 不要只用 | 应对 |
|---|---|---|
| 「这段话像不像问题」 | 运营本体 | [向量库](../vector-db/) + [RAG](../rag/) |
| 「这个客户连着哪些合同、哪次变更合法」 | 纯向量 | 运营本体或 [上下文图](../../agent/loop-graph/context-graph.md) |
| 「跨医院共享 SNOMED 推理」 | Foundry 对象模型 | OWL + 领域标准词表 |
| 「Agent 改工单状态还要过权」 | 让模型直接 UPDATE | Action type + Role（或自研等价：状态机 + 鉴权 + 写回） |

落地建议（自研、不绑定厂商）：

1. **对象类型表**先于向量索引：先锁「有哪些业务对象、稳定 ID 从哪来」。
2. **链接类型具名且可逆**：禁止只有「相关」；两侧 API 名分开（Palantir link 的双向遍历就是这个纪律）。
3. **变更必须是动作，不是字段 PATCH**：每个可写用例一个 action（参数、校验、副作用、审计）。
4. **LLM 只暴露动作与只读查询**，不暴露任意 SQL / 任意 SPARQL。
5. **权限挂在对象与动作上**，不要只挂在应用菜单。

---

## 五、证据边界

- 构件定义与数据集对照表：Foundry 官方 [Core concepts](https://www.palantir.com/docs/foundry/ontology/core-concepts/)。
- 语义 / 动能 / digital twin：官方 [Ontology overview](https://www.palantir.com/docs/foundry/ontology/overview/)。
- Action 事务、writeback dataset：官方 [Action types overview](https://www.palantir.com/docs/foundry/action-types/overview/)。
- Link 双向、多关系并存：官方 [Link types overview](https://www.palantir.com/docs/foundry/object-link-types/link-types-overview/)。
- AIP 与语义检索叙事：Palantir 工程博客（产品演示口径，**不是**评测论文）。
- **未写**：客户数量、AIP 模型供应商、Gotham 内部 schema、与 OWL 的官方形式化对应（文档未做 OWL 等价声明——Palantir Ontology **不是** OWL 发行版）。

---

## 延伸

- 五维分类里的 OWL 节：[../knowledge-base/知识库类型整理.md](../knowledge-base/知识库类型整理.md) §四
- 个人 Wiki 概念页：`my-kb/wiki/concepts/ontology.md`、`operational-ontology.md`
- 外部教材反例（哲学 Ontology 与 OWL 混写，不覆盖本页定义）：[../../../knowledge-management-dynamics/02-ch1-本体与信息科学.md](../../../knowledge-management-dynamics/02-ch1-本体与信息科学.md)
- 官方：[Ontology overview](https://www.palantir.com/docs/foundry/ontology/overview/) · [palantir.com](https://www.palantir.com/)
