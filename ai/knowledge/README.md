# knowledge · 知识与记忆

> **定位**：决定**往上下文窗口里塞什么**。
> **口诀**：「讲检索 / 记忆 / 裁剪」→ 归这。

上级索引：[../README.md](../README.md) ｜ 学习地图：[../learning-path.md](../learning-path.md)

## 专题

| 专题 | 一句话 | 入口 |
|---|---|---|
| **RAG** | 检索增强生成：Naive → Advanced → Agentic 全谱系 | [rag/](./rag/) |
| **向量数据库** | Milvus / Qdrant / pgvector：ANN 索引 + 语义检索底座 | [vector-db/](./vector-db/) |
| **知识库** | 知识库类型五维整理 | [knowledge-base/](./knowledge-base/) |
| **Memory** | Agent 工作 / 短期 / 长期记忆 | [memory/](./memory/) |
| **Context Engineering** | 在合适时机把合适信息放进窗口 | [context-engineering/](./context-engineering/) |

## 四件事的分工

| 环节 | 干什么 | 对应专题 |
|---|---|---|
| **取** | 从外部知识里捞出相关片段 | RAG / 向量库 / 知识库 |
| **存** | 跨会话保留用户画像与沉淀事实 | Memory |
| **装配** | 按 token 预算把上面两者裁剪、排序、拼进窗口 | Context Engineering |
| **可见性** | 只有进了窗口的模型才看得见；长期记忆是「有求才现」 | 见 [../agent/环节03-记忆与状态详解.md](../agent/环节03-记忆与状态详解.md) |

## 原理纵深（按序）

- 提示与上下文工程 → [../agent/环节02-提示与上下文工程详解.md](../agent/环节02-提示与上下文工程详解.md)
- 记忆与状态 → [../agent/环节03-记忆与状态详解.md](../agent/环节03-记忆与状态详解.md)
- 检索增强 RAG → [../agent/环节06-检索增强RAG详解.md](../agent/环节06-检索增强RAG详解.md)

## 相邻大类

- 输出拦不拦得住、量不量得出 → [../reliability/](../reliability/)
- 这些东西由谁在循环里调度 → [../agent/](../agent/)
