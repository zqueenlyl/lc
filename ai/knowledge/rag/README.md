# RAG · 检索增强生成

> 一句话：**生成前先「检索」——把与问题相关的外部片段拼进上下文，再让模型作答**。一次解决幻觉、知识陈旧、私域数据不可见三件事，是 LLM 落地企业知识场景的默认形态。
>
> 技术谱系：Naive → Advanced → Modular → Graph → Agentic（外加 Self-RAG / CRAG / HyDE / RAPTOR / 混合检索 / 多跳等变体）。

本目录聚焦 **RAG 本体**：类型全景与选型 → [rag-types.md](./rag-types.md)；每类的「技术方法 + MVP 骨架」→ [rag-mvp.md](./rag-mvp.md)。
完整工程链路（解析 / 切分 / 召回 / 评测 / 常见坑）见 [agent 环节 06-检索增强RAG详解](../../agent/环节06-检索增强RAG详解.md)；存储底座见 [../vector-db/](../vector-db/)。

---

## 一、技术讲解

RAG 的动机：模型参数里只有「训练时见过、且记得住」的知识，改不动也记不全。RAG 不动模型，只在推理时**现场查阅**：

```
离线：文档 → 解析/清洗 → 切分 chunk → Embedding → 写入向量库
在线：query →（可选改写）→ 检索 top-k →（可选重排/压缩）→ 拼接 prompt → LLM 生成
```

链路两头都要优化，缺一头就白搭：

| 环节 | 要解决的问题 | 主要手段 |
|---|---|---|
| **召回** | 找得到（recall） | 混合检索（BM25 + 向量 + RRF）、Rerank 精排、Query 改写 / HyDE / 多查询 |
| **利用** | 用得好（faithfulness） | 上下文压缩、去噪、引用溯源、按 token 预算裁剪（见 [../context-engineering/](../context-engineering/)） |

关键约束：**query 与文档必须用同一个 embedding 模型**，否则不在同一语义空间；换模型 = 全量重算向量。

---

## 二、功能作用

- **降幻觉**：答案有出处，可溯源到命中块。
- **知识可更新**：改文档即改知识，不必重训模型。
- **私域可用**：企业内网数据不进训练集也能被问到。
- **成本可控**：相比继续预训练 / 微调，RAG 是改知识最便宜的一条路。

---

## 三、应用场景

| 场景 | 典型形态 |
|---|---|
| 企业知识问答 / 客服 | Naive → Advanced（混合检索 + 重排）起步 |
| 法规 / 合同 / 医疗等强溯源 | 加引用、加 CRAG 兜底、加人审 |
| 跨实体关系、全局总结 | Graph RAG（知识图谱 + 社区摘要） |
| 复杂开放任务、多工具 | Agentic RAG（检索作为 Agent 的一个工具） |
| 冷启动、无标注语料 | HyDE（先造假设答案再检索） |

---

## 四、两条演进线（速查）

**主线范式**（详见 [rag-types.md](./rag-types.md)）：

| 范式 | 一句话 |
|---|---|
| Naive RAG | 索引 → 检索 → 生成 三段式基线 |
| Advanced RAG | 每个环节单独优化（改写 / 混合检索 / Rerank / 压缩） |
| Modular RAG | 模块可插拔、可编排 |
| Graph RAG | 知识图谱 + 社区摘要，攻多跳与全局问题 |
| Agentic RAG | 检索降级为 Agent 的工具，自主决定查不查、查几轮 |

**重要变体**：Self-RAG（自我反思忠实度）、CRAG（检索质量差则纠错/联网）、HyDE、RAPTOR、混合检索、多跳 RAG。

> 落地通常是组合拳：如「混合检索 + 重排 + CRAG 纠错」，或「Graph 做全局理解 + 向量做细节召回」。

---

## 五、怎么读本目录

| 文档 | 讲什么 | 什么时候读 |
|---|---|---|
| [rag-types.md](./rag-types.md) | 5 大范式 + 6 类变体：特性 / 场景 / 优缺点 + 选型对比与建议 | 先读，建全景 |
| [rag-mvp.md](./rag-mvp.md) | 11 类 RAG 逐一的「技术方法 + MVP 最小实现」（LangChain / LlamaIndex / LangGraph / FAISS / Chroma / Neo4j） | 要落地时按类查 |

---

## 六、与相邻技术

| 技术 | 关系 |
|---|---|
| [../vector-db/](../vector-db/) | RAG 的语义召回层；ANN 索引、过滤、混合检索都在这里 |
| [../knowledge-base/](../knowledge-base/) | 更上层视角：知识库按存储 / 检索 / 形态 / 建模 / 维护五维分类 |
| [../context-engineering/](../context-engineering/) | 检索结果如何按 token 预算裁剪、排序、拼进窗口 |
| [../memory/](../memory/) | 长期记忆的召回与 RAG 同构（向量检索 + 写过滤） |
| [agent 环节 06](../../agent/环节06-检索增强RAG详解.md) | 工程链路纵深：切分策略、评测、失败模式 |

---

## 七、落地建议

1. **先跑通再优化**：Naive RAG 打通链路，再按「召回 → 重排 → 压缩」顺序加料。
2. **Rerank 是性价比之王**：双塔粗排 + 交叉编码器精排，通常比换生成模型收益大。
3. **必做混合检索**：纯向量漏专有名词、编号、代码，加一路 BM25 + RRF 融合。
4. **检索与生成分开评**：recall@k / MRR 评召回，忠实度 / 相关性评生成（见 [eval](../../reliability/eval/)）。
5. **切分按语义不按字数**：Parent-Child（小块检索、大块返回）常比调 chunk_size 有效。

---

## 八、延伸阅读

- 原论文：RAG（Lewis et al. 2020）、Self-RAG、CRAG、HyDE、RAPTOR、GraphRAG（微软 2024）
- 相邻专题：[../vector-db/](../vector-db/)、[../knowledge-base/](../knowledge-base/)、[../context-engineering/](../context-engineering/)
- 上级索引：[../README.md](../README.md) ｜ 总索引 [../../README.md](../../README.md)
