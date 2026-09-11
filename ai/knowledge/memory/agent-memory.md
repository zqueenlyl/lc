# Agent 记忆技术全景整理

> 传统 LLM 是**无状态**的：每次调用都从零开始，既不记得上一轮说了什么，也不记得用户是谁、之前做过什么。要让 Agent 真正像人一样连续工作、跨会话协作，必须给它装上一套「记忆系统」。
>
> 本文从**为什么需要记忆**出发，梳理记忆的分类、核心能力、经典实现方案、开源框架与选型建议，并给出一个可落地的 LangGraph 示例。

---

## 一、为什么 Agent 需要记忆

LLM 的「失忆」体现在三个层面，记忆系统要逐一解决：

| 问题 | 表现 | 记忆要解决的 |
|---|---|---|
| **上下文窗口有限** | 对话一长就溢出，只能截断，丢失早期信息 | 压缩 / 摘要 / 检索而非全量塞入 |
| **跨会话无状态** | 换一个 `thread_id` 就「失忆」，用户身份、历史偏好全丢 | 长期记忆持久化 + 按身份隔离 |
| **信息过载** | 全部历史都塞进 prompt，噪音大、成本高、还干扰推理 | 只召回「相关」的记忆 |

一句话：**记忆 = 在合适的时间，把合适的信息，以合适的成本，放进上下文。**

---

## 二、记忆的本质：分类与层次

### 2.1 按时间尺度分层（最常用）

| 层级 | 别名 | 存什么 | 生命周期 | 典型实现 |
|---|---|---|---|---|
| **工作记忆** | Working Memory | 当前任务的中间状态、工具结果、变量 | 单次任务内 | State 里的 `messages`、变量 |
| **短期记忆** | Short-term / 会话记忆 | 本次会话的对话历史 | 单次会话 | Buffer、滑动窗口、摘要 |
| **长期记忆** | Long-term / 情景+语义 | 跨会话的用户偏好、事实、经验 | 持久 | 向量库、图库、Mem0/Zep |

### 2.2 按内容类型分层（认知科学类比）

- **情景记忆（Episodic）**：具体发生过的事——"上次用户问过 XX，我给了 YY 答案"。
- **语义记忆（Semantic）**：抽象出来的事实与偏好——"用户喜欢简短回答"、"用户是后端工程师"。
- **程序记忆（Procedural）**：怎么做事——工具调用经验、成功的流程路径。

> 工程落地时，最实用的是 **时间尺度分层**（工作 / 短期 / 长期），内容类型分层用于指导「长期记忆该存什么」。

---

## 三、记忆系统的四大核心能力

任何记忆方案，本质都是这四件事的组合：

1. **写入（Encode/Write）**：从交互中抽取值得记的信息。可以是即时写（存原文），也可以是事后反思写（LLM 提取摘要/事实）。
2. **存储（Store）**：以什么形式存（原文 / 摘要 / 向量 / 图 / 结构化字段），存到哪里（内存 / 向量库 / 图库 / 关系库）。
3. **检索（Retrieve）**：按需召回相关记忆。是记忆系统**最关键的环节**——召不回等于没记。
4. **更新/遗忘（Update/Forget）**：记忆会过时、会冲突，需要覆盖、压缩、淘汰。

---

## 四、经典实现方案（按技术演进）

### 1. 全量上下文（Naive Context）

把整段历史直接拼进 prompt。

- **实现**：无特殊处理，把 `messages` 全部发给模型。
- **优点**：零成本、零丢失。
- **缺点**：窗口一满就爆，必须截断；长历史成本高、噪音大。
- **适用**：极短会话、原型验证。

### 2. 缓冲记忆（Conversation Buffer）

只保留最近 N 条消息的滑动窗口。

```python
# LangChain 风格（示意）
from langchain.memory import ConversationBufferWindowMemory
memory = ConversationBufferWindowMemory(k=10)  # 只保留最近 10 轮
```

- **优点**：实现简单、控制上下文长度。
- **缺点**：窗口外信息彻底丢失，无长期记忆。
- **适用**：对「最近上下文」敏感的客服、闲聊。

### 3. 摘要记忆（Conversation Summary）

用 LLM 把历史**压缩成摘要**，新对话只携带摘要。

```python
from langchain.memory import ConversationSummaryMemory
memory = ConversationSummaryMemory(llm=llm, max_token_limit=2000)
```

- **优点**：突破窗口限制，能概括长历史；成本可控。
- **缺点**：摘要会**丢失细节**；错误会随摘要累积。
- **适用**：长会话、需要「印象式」上下文而非精确历史。

### 4. 向量检索记忆（RAG 式记忆）

把历史交互写入向量库，对话时**按语义相似度召回**相关片段——即「给自己的记忆做 RAG」。

```
写入：交互记录 → 分块 → embedding → 向量库
召回：当前 query → embedding → 相似度检索 top-k → 拼进 prompt
```

- **优点**：可海量存储、按需召回、成本与相关性平衡。
- **缺点**：只召回「语义相似」的，可能漏掉「时间上最近」或「全局重要」的记忆。
- **适用**：长期记忆的主体方案，几乎所有生产 Agent 都会用。

### 5. 图 / 结构化记忆

用知识图谱或结构化实体存储关系（"用户 A —属于— 团队 B —偏好— 产品 C"）。

- **优点**：关系推理强、可解释、能多跳关联。
- **缺点**：构建成本高（要抽取实体关系）、维护复杂。
- **代表**：Zep 的 Graph Memory、Cognee、Graphiti。

### 6. 混合记忆（Hybrid，生产推荐）

实际落地几乎都是**组合拳**：

- **工作记忆** = 当前 State；
- **短期记忆** = 滑动窗口 + 摘要；
- **长期记忆** = 向量检索 + 结构化字段 + （可选）图。

---

## 五、长期记忆开源框架

### 1. Mem0

- **定位**：记忆层（Memory Layer），专注「提取 + 检索」用户级记忆。
- **特点**：自动从对话中**抽取可复用的事实/偏好**（`add()` 时 LLM 提取），支持向量存储；提供 `search()` 语义召回。
- **适用**：个性化助手、用户画像、跨会话记忆。

### 2. Letta（原 MemGPT）

- **定位**：Agent 框架 + 操作系统式记忆管理。
- **特点**：源自 MemGPT 论文——把「主上下文」当作 RAM，「外部存储」当作磁盘，用**分页（paging）**机制按需换入换出记忆；支持自编辑记忆块。
- **适用**：需要精细控制上下文、超长任务记忆的场景。

### 3. Zep

- **定位**：为 AI Agent 构建的长期记忆服务（可自托管开源）。
- **特点**：同时支持**时序记忆（Temporal）+ 向量记忆 + 图记忆**；自动摘要、实体抽取、时间衰减检索。
- **适用**：生产级、多租户、需要时间维度和关系推理的记忆。

### 4. LangGraph Checkpointer

- **定位**：LangGraph 内置的**状态持久化**，是会话记忆的基础设施。
- **特点**：把每次节点执行的 State 快照存下来，按 `thread_id` 隔离，支持**断点恢复、时间旅行（回溯到任意历史 State）**；后端可换（内存 / SQLite / Postgres）。
- **适用**：LangGraph 应用的标准会话记忆底座。

### 5. LangChain Memory 类

- **定位**：早期记忆抽象（`ConversationBufferMemory` / `SummaryMemory` 等）。
- **特点**：简单易用，但偏「链式」设计，现代 Agent（LangGraph）更多直接管理 State。
- **适用**：快速原型、简单链式应用。

### 6. 其他

- **LlamaIndex ChatMemoryBuffer**：LlamaIndex 生态的会话记忆。
- **Cognee**：知识图谱记忆，强调图式长期记忆。
- **Graphiti**：Zep 出品的时序知识图谱记忆，擅长实体关系随时间的演变。

---

## 六、关键技术细节

### 6.1 写入策略

| 策略 | 做法 | 优劣 |
|---|---|---|
| **即时写入** | 每条交互直接存原文 | 简单、无损，但噪音大、占空间 |
| **事后反思提取** | 任务结束后用 LLM 抽取事实/偏好/经验 | 精简、去噪，但多一次 LLM 调用 |
| **异步写入** | 后台异步做提取与入库 | 不阻塞主流程，但有时延 |

> 生产常用「**即时存原文 + 异步抽语义**」：原文兜底可回溯，语义记忆用于高效检索。

### 6.2 召回策略

- **语义相似度召回**：当前 query 与记忆做 embedding 相似度，取 top-k。
- **时间衰减**：越近的记忆权重越高（Zep 的时序记忆）。
- **重要性加权**：给记忆打分（用户强调 / 频繁提及），高权重优先召回。
- **RAG + Rerank**：先向量粗召回，再重排序精筛。
- **多路召回 + 融合**：语义 + 时间 + 结构化字段多路并取。

### 6.3 遗忘与压缩

- **LLM 摘要压缩**：把长历史压成摘要（会丢细节）。
- **淘汰（Eviction）**：按时间 / 重要性 / 访问频率淘汰旧记忆。
- **覆盖（Upsert）**：同一事实更新为最新值，避免冲突（Mem0 的 update）。
- **反思整合**：定期把多条记忆合并成更高层的洞察（reflection）。

### 6.4 记忆隔离与作用域

- **会话级（thread）**：一个 `thread_id` 一份短期记忆。
- **用户级（user）**：跨会话的用户偏好、身份、长期事实。
- **全局级（global）**：产品知识、公共经验。
- **团队/Agent 级**：多智能体共享的记忆（共享 State 或共享存储）。

> 作用域没设计好，是记忆系统最常见的坑：该隔离的没隔离（A 用户看到 B 用户记忆）、该共享的没共享（多 Agent 各自失忆）。

---

## 七、存储后端

| 存储 | 载体 | 适合记忆类型 |
|---|---|---|
| 进程内存 | `dict` / MemorySaver | 演示、单进程短期 |
| 关系库 | SQLite / Postgres | Checkpointer 快照、结构化事实 |
| 向量库 | FAISS / Chroma / pgvector / Milvus | 语义长期记忆 |
| 图库 | Neo4j / 图内存 | 实体关系记忆 |
| KV/缓存 | Redis | 热记忆、高频访问 |

---

## 八、选型对比

| 方案/框架 | 短期记忆 | 长期记忆 | 关系/图 | 提取自动化 | 实现成本 | 典型场景 |
|---|---|---|---|---|---|---|
| 全量上下文 | ✅ | ❌ | ❌ | ❌ | 极低 | 短会话原型 |
| Buffer 滑动窗口 | ✅ | ❌ | ❌ | ❌ | 低 | 客服、闲聊 |
| Summary 摘要 | ✅ | ⚠️ | ❌ | ⚠️ | 低 | 长会话概括 |
| 向量检索记忆 | ✅ | ✅ | ❌ | ⚠️ | 中 | 长期记忆主体 |
| Mem0 | ⚠️ | ✅ | ❌ | ✅（自动提取） | 中 | 个性化助手 |
| Letta | ✅ | ✅ | ⚠️ | ✅ | 中高 | 超长任务精细控制 |
| Zep | ✅ | ✅ | ✅ | ✅（摘要+实体） | 中高 | 生产级多租户 |
| LangGraph Checkpointer | ✅（状态） | ⚠️ | ❌ | ❌ | 低 | LangGraph 会话底座 |
| LangChain Memory | ✅ | ⚠️ | ❌ | ⚠️ | 低 | 快速原型 |

---

## 九、选型建议

1. **快速原型 / 简单链** → LangChain Memory 或全量上下文，先跑通。
2. **基于 LangGraph 的 Agent** → 用 **Checkpointer** 做会话底座 + **向量检索**做长期记忆。
3. **强个性化、需自动抽取用户画像** → **Mem0**。
4. **生产级、需时间维度 + 关系推理 + 多租户** → **Zep**。
5. **超长任务、要精细控制上下文分页** → **Letta**。
6. **重实体关系、知识图谱式记忆** → **Cognee / Graphiti / Zep Graph**。

> 组合是常态：例如「LangGraph Checkpointer（状态） + 向量库（语义长期） + Mem0/Zep（用户画像）」三层混合，覆盖工作/短期/长期记忆。

---

## 十、实战示例：LangGraph 三层记忆

一个最小可运行的三层记忆骨架：工作记忆用 State，短期记忆用滑动窗口，长期记忆用向量检索（示意，未接真实向量库）。

```python
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

# ---- 1) 工作记忆：State 即工作记忆 ----
class State(TypedDict):
    messages: Annotated[list, add_messages]   # 会话历史（短期记忆载体）
    # 长期记忆召回结果，拼入本轮上下文
    recalled: Annotated[list, lambda a, b: b or a]

# ---- 2) 短期记忆：滑动窗口（只取最近 N 条）----
WINDOW = 10

def build_prompt(messages, recalled):
    recent = messages[-WINDOW:]              # 滑动窗口
    history = "\n".join(f"{m.type}: {m.content}" for m in recent)
    context = "\n".join(recalled) or "（无）"
    return (
        f"【长期记忆】\n{context}\n\n"
        f"【近期对话】\n{history}\n\n"
        f"请基于以上信息回答问题。"
    )

# ---- 3) 长期记忆：向量检索（示意）----
class LongTermMemory:
    def __init__(self):
        self.store = []  # 实际应替换为向量库
    def save(self, text):          # 写入
        self.store.append(text)
    def recall(self, query, k=3):  # 召回（实际按 embedding 相似度）
        return [s for s in self.store if query in s][:k]

ltm = LongTermMemory()

def agent_node(state: State):
    # 召回长期记忆
    query = state["messages"][-1].content if state["messages"] else ""
    recalled = ltm.recall(query)
    prompt = build_prompt(state["messages"], recalled)
    # 此处省略真实 LLM 调用，返回占位回复
    return {"recalled": recalled,
            "messages": [("assistant", f"(基于 {len(recalled)} 条长期记忆回答)")]}

g = StateGraph(State)
g.add_node("agent", agent_node)
g.add_edge(START, "agent")
g.add_edge("agent", END)

app = g.compile(checkpointer=MemorySaver())  # checkpointer = 会话记忆持久化

# 按 thread_id 隔离会话记忆
config = {"configurable": {"thread_id": "user-001"}}
app.invoke({"messages": [("user", "我是后端工程师，喜欢简短回答")]}, config)
app.invoke({"messages": [("user", "推荐一个框架")]}, config)
```

要点：

- `checkpointer=MemorySaver()` 让每次 `invoke` 的状态按 `thread_id` 持久化，实现**跨调用会话记忆**。
- 滑动窗口保证**短期记忆**不被无限增长撑爆。
- `LongTermMemory` 是**长期记忆**的插槽，落地时替换为向量库 + `add()`/`search()`。

---

## 十一、小结

| 维度 | 结论 |
|---|---|
| 记忆本质 | 把「合适的信息」在「合适的时机」放进上下文 |
| 分层 | 工作记忆 / 短期记忆 / 长期记忆 |
| 四大能力 | 写入、存储、检索、更新/遗忘 |
| 短期记忆方案 | Buffer / 滑动窗口 / 摘要 |
| 长期记忆方案 | 向量检索（主体）+ 图 / 结构化 |
| 代表框架 | Mem0、Letta、Zep、LangGraph Checkpointer |
| 落地要点 | 检索比写入更重要；作用域隔离要设计好；生产用混合方案 |

> 相关文档：[RAG 类型全景](../rag/rag-types.md)、[LangGraph 持久化与记忆](../../agent/langgraph/03-持久化-流式-人机协同.md)
