# 上下文图（Context Graph）

> 跨会话、跨 Agent，系统**知道什么**（客户 / 合同 / 政策）。图层总览：[graph-engineering.md](./graph-engineering.md)。走路怎么编排 → [execution-graph.md](./execution-graph.md)。窗口里怎么裁 → [上下文工程](./context-engineering.md)（本目录栈内口径）· [knowledge/CE](../../knowledge/context-engineering/)（预算手册）。不是本篇。

---

## 一、从文档到可查询的图

GraphRAG 只是上下文图的一条**检索**用法。完整管线：

```
语料 / 业务库
   │  抽取（实体、关系、属性；LLM 或规则）
   ▼
实体对齐（同一客户多个源 ID → 一个稳定 ID）
   │
   ▼
写入图（默认属性图；要强约束推理再上 RDF/OWL）
   │
   ├─ 社区检测 + 分层摘要     → 全局问题
   ├─ 邻居 / 路径 / PageRank  → 多跳问题
   └─ 仍保留向量 / BM25       → 细节原文
   │
   ▼
增量维护（新文档、时效、冲突、权限）→ 再检索
```

| 检索路 | 做法 | 擅长 |
|---|---|---|
| **局部** | 锚到实体，扩 k 跳或最短路径 | 具体实体、因果链 |
| **全局** | 社区摘要 / 主题层 | 「全库总结」 |
| **混合** | 图路径当骨架 + 原文块当证据 | 既要关系又要引用 |

向量回答「这段话像不像问题」；图回答「这件事连着什么、沿哪条路径」。召回之后仍要按 token 预算裁进窗口，见 [Context Engineering](../../knowledge/context-engineering/)。

---

## 二、必须显式设计的契约

框架能持久化 ≠ 领域契约：

| 问题 | 不设计就会发生 |
|---|---|
| 稳定身份 | CRM / 工单 / 账单三个「张三」对不上 |
| 类型化关系 | 只有「相关」没有 `OWNS` / `SUPERSEDES`，多跳走乱 |
| 时效 | 改了合同状态，说不清决策当时哪一版为真 |
| 来源（provenance） | 分不清「模型猜测」和「政策原文」 |
| 并发写入 | 两个 Agent 同时改同一客户，后写覆盖先写 |
| 权限 | 客服 Agent 读到账务字段 |
| 框架可迁移 | Schema 绑死在某一家 Checkpointer / Store 上 |

本体不必上 OWL。**带类型的应用 Schema + 稳定 ID** 对有界领域通常够用。形式化 Ontology 见 [知识库 · 表示层](../../knowledge/knowledge-base/)。

---

## 三、GraphRAG 家族（检索侧速查）

| 路线 | 机制 | 代价 / 坑 |
|---|---|---|
| **Microsoft GraphRAG**（2024） | LLM 抽三元组 → Leiden 社区 → 分层摘要；局部 + 全局 | 构图 LLM 量大，全量重建贵 |
| **LightRAG** | 实体层 + 关系层双级索引 | 全局总结弱于社区摘要 |
| **LazyGraphRAG** | 贵的社区摘要推迟到真正问到 | 适合先索引、后按需总结 |
| **HippoRAG** | 海马式索引 + Personalized PageRank | 多跳强，工程栈相对小众 |
| **LlamaIndex PropertyGraph** | 属性图索引，可接 Neo4j 等 | 和现有 LlamaIndex 栈好拼 |
| **Graphiti / Zep** | **时序**知识图谱记忆 | 偏记忆，不是离线文档 GraphRAG |
| **Cognee** | 图式长期记忆 | 同上 |
| **Agentic GraphRAG**（2025–26） | 检索做成多轮 think → 查子图 → 再想 | 延迟费用上升；先有图再 Agent 化 |

**选型**：先 Naive + Hybrid + Rerank 跑通（[RAG](../../knowledge/rag/)）→ 有跨实体 / 全局总结的失败案例再上 GraphRAG → 要跨系统共享可变事实，再做本节契约。**别一上来就全库抽实体。** 检索谱系位置见 [环节 06](../环节06-检索增强RAG详解.md)。

---

## 四、存储与查询

| 层 | 常见选择 |
|---|---|
| 图数据库 | Neo4j、FalkorDB、Memgraph、NebulaGraph、Amazon Neptune |
| 查询语言 | Cypher / openCypher；Gremlin、SPARQL（RDF 线） |
| 混合 | 图存关系 + 向量存原文块 + BM25 存符号；用稳定 ID 对齐 |
| Agent 怎么碰 | 工具：`search_nodes` / `traverse` / `run_cypher`（只读起步）；[MCP](../mcp/) 接到图库 |

生产默认**属性图**。RDF/SPARQL 留给已有语义网资产或强约束推理。
