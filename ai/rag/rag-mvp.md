# RAG 各类技术方法与 MVP 实现

> 配套文档：[rag-types.md](./rag-types.md)（类型全景、特性/场景/优缺点、选型对比）。
> 本文针对每一种 RAG 类型，讲解其**技术方法**（核心流程、关键步骤）与**MVP 最小可行实现**（技术栈选型 + 最简代码骨架）。
> 代码统一采用 Python 生态：`LangChain` / `LlamaIndex` / `LangGraph` / `FAISS` / `Chroma` / `Neo4j` 等。

---

## 1. Naive RAG（基础 RAG）

### 技术方法

标准三段式流水线：

1. **索引（Indexing）**
   - 文档加载：读取 PDF / Markdown / 网页等异构文档。
   - 文本切块（Chunking）：按固定大小 + 滑动窗口或递归分隔符切分，chunk 过大影响精度、过小丢上下文，常见 `chunk_size=500~1000`、`overlap=50~100`。
   - 向量化：用 embedding 模型（OpenAI `text-embedding-3`、BGE、text2vec 等）把每个 chunk 映射成稠密向量。
   - 建库：写入向量数据库（FAISS / Chroma / Milvus / Pinecone）。
2. **检索（Retrieval）**
   - 把 query 用同一 embedding 模型向量化。
   - 用余弦相似度 / 内积计算与库中 chunk 的相似度。
   - 取 top-k（常见 k=4~8）最相似 chunk。
3. **生成（Generation）**
   - 将 top-k chunk + 原始 query 拼进 prompt（system 提示 + 上下文 + 问题）。
   - LLM 基于上下文生成答案，通常要求"仅依据给定上下文回答"。

### MVP 实现

**技术栈**：LangChain + Chroma（本地向量库）+ OpenAI embeddings + OpenAI LLM。

```python
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

# 1) 加载 + 切块
loader = TextLoader("docs.txt")
docs = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

# 2) 向量化 + 建索引
vs = Chroma.from_documents(chunks, OpenAIEmbeddings())

# 3) 检索 + 生成
qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-4o-mini"),
    retriever=vs.as_retriever(search_kwargs={"k": 4}),
)
print(qa.invoke("你的问题"))
```

**跑通即 MVP**：三行核心（切块 → 建库 → 问答），约 20 行代码。

---

## 2. Advanced RAG（高级 RAG）

### 技术方法

在 Naive 基础上对 **Pre-Retrieval → Retrieval → Post-Retrieval** 全链路优化：

1. **Pre-Retrieval（检索前）**
   - 查询改写：用 LLM 把口语化/模糊 query 改写成更适合检索的规范表述。
   - 查询扩展：生成多个子查询（multi-query）或同义扩展，提高召回。
   - HyDE：先让 LLM 生成"假设答案"再用假设答案检索（见第 8 节）。
   - 查询路由：按意图把 query 分发给不同检索器（如 FAQ 检索 vs 文档检索）。
2. **Retrieval（检索）**
   - 混合检索：稠密向量 + BM25 稀疏检索结合（见第 10 节）。
   - 重排序（Rerank）：用交叉编码器（如 `bge-reranker`、Cohere Rerank）对候选重排，把真正相关的排前面。
3. **Post-Retrieval（检索后）**
   - 上下文压缩：LLM 剔除 chunk 中的无关句子，压缩 token。
   - 重排/融合：多路结果融合（RRF 等）。

### MVP 实现

**技术栈**：LangChain + BM25Retriever + FAISS + CrossEncoder 重排。

```python
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.retrievers import EnsembleRetriever
from sentence_transformers import CrossEncoder

# 混合检索：BM25 + 向量
bm25 = BM25Retriever.from_documents(chunks)
bm25.k = 10
vector = FAISS.from_documents(chunks, OpenAIEmbeddings())
vector.k = 10
hybrid = EnsembleRetriever(retrievers=[bm25, vector], weights=[0.3, 0.7])

# 重排序
reranker = CrossEncoder("BAAI/bge-reranker-base")
docs = hybrid.get_relevant_documents(query)
scores = reranker.predict([(query, d.page_content) for d in docs])
top = [d for _, d in sorted(zip(scores, docs), key=lambda x: -x[0])[:4]]
```

**MVP 要点**：先加混合检索，再加重排，是性价比最高的两步优化。

---

## 3. Modular RAG（模块化 RAG）

### 技术方法

把检索流程拆成**可插拔、可编排的模块**，通过 DAG / 状态机自由组合：

- 核心模块：`Retriever`（检索器）、`Reranker`（重排）、`Memory`（记忆）、`Router`（路由）、`Generator`（生成器）、`Fusion`（融合器）。
- 编排方式：LangGraph（图状态机）、LlamaIndex `QueryPipeline`（声明式管道）。
- 动态决策：根据中间状态决定下一模块（如"检索结果差 → 触发重检索 → 否则生成"）。

### MVP 实现

**技术栈**：LangGraph（节点 = 模块，边 = 编排）。

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class State(TypedDict):
    query: str
    docs: list
    answer: str

def retrieve(s): 
    s["docs"] = hybrid.get_relevant_documents(s["query"]); return s
def rerank(s):
    s["docs"] = top_k_after_rerank(s["query"], s["docs"]); return s
def generate(s):
    s["answer"] = llm(gen_prompt(s["query"], s["docs"])); return s

g = StateGraph(State)
g.add_node("retrieve", retrieve)
g.add_node("rerank", rerank)
g.add_node("generate", generate)
g.add_edge("retrieve", "rerank")
g.add_edge("rerank", "generate")
g.add_edge("generate", END)
g.set_entry_point("retrieve")
app = g.compile()
print(app.invoke({"query": "问题"}))
```

**MVP 要点**：模块接口统一（入参 State、出参 State），新增/替换模块只需改图定义。

---

## 4. Graph RAG（图谱 RAG，微软 2024）

### 技术方法

用知识图谱承载实体-关系，支持"局部检索 + 全局理解"：

1. **构建图谱**
   - LLM 从文档抽取实体（人物/组织/概念）与关系（三元组 `<head, relation, tail>`）。
   - 写入图数据库（Neo4j），实体为节点、关系为边，可带属性。
2. **索引（社区摘要）**
   - 用社区检测算法（Leiden / Louvain）把图划分成社区。
   - LLM 对每个社区生成**逐层摘要**（底层→高层），形成层次化全局知识。
3. **检索**
   - 局部检索：定位实体邻居子图，回答"具体实体"相关问题。
   - 全局检索：按 query 匹配社区摘要，回答"这个数据集整体讲了什么"这类总结性问题。
4. **生成**：合并局部 + 全局证据，生成答案。

### MVP 实现

**技术栈**：微软官方 `graphrag` 库（零代码跑通）或 LangChain `Neo4jGraph`。

**方案 A：官方 graphrag（最快 MVP）**

```bash
pip install graphrag
python -m graphrag.index --init --root ./ragtest   # 生成配置
# 放入输入文本后执行索引
python -m graphrag.index --root ./ragtest
python -m graphrag.query --root ./ragtest --method global --query "数据集主要讲了什么"
```

**方案 B：LangChain + Neo4j（更可控）**

```python
from langchain_neo4j import Neo4jGraph
from langchain_openai import ChatOpenAI
from langchain.chains import GraphCypherQAChain

graph = Neo4jGraph(url="bolt://localhost:7687", username="neo4j", password="password")
chain = GraphCypherQAChain.from_llm(
    ChatOpenAI(model="gpt-4o"),
    graph=graph,
    verbose=True,
)
chain.invoke({"query": "与 X 相关的实体有哪些？"})
```

**MVP 要点**：优先用官方 `graphrag` 先跑通；需要融入现有图库时再走 Neo4j + Cypher。

---

## 5. Agentic RAG（智能体 RAG）

### 技术方法

引入 Agent 在 **规划-行动-观察-反思** 循环中自主编排检索：

1. **规划**：把复杂 query 拆解为子任务。
2. **工具选择**：在向量搜索、Web 搜索、数据库查询、API 调用之间动态选择。
3. **执行**：调用工具并观察结果。
4. **反思**：判断结果是否充分，不充分则换工具 / 重检索 / 改写 query。
- 常用范式：ReAct（Thought-Action-Observation）、Function Calling、LangGraph 状态机。

### MVP 实现

**技术栈**：LangGraph + ReAct Agent + 检索工具 + Web 搜索工具。

```python
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool

@tool
def vector_search(q: str) -> str:
    """在内部知识库检索"""
    return "\n".join(d.page_content for d in hybrid.get_relevant_documents(q))

@tool
def web_search(q: str) -> str:
    """联网搜索公开信息"""
    from langchain_community.tools import TavilySearchResults
    return TavilySearchResults(max_results=3).invoke(q)

agent = create_react_agent(
    llm, tools=[vector_search, web_search]
)
print(agent.invoke({"messages": [("user", "比较内部文档与外部最新信息回答……")]}))
```

**MVP 要点**：把每个检索源封装成 `@tool`，Agent 自动决定调用顺序与次数。

---

## 6. Self-RAG（自我反思 RAG）

### 技术方法

让模型用**反思 token** 自我控制检索与生成：

- `Retrieve`：是否需要检索（判断 query 是否依赖外部知识）。
- `IsREL`：检索到的段落是否与 query 相关。
- `IsSUP`：段落是否支持当前生成内容（防止幻觉）。
- `IsUSE`：生成的答案是否有用。
- 训练：在语料上标注 reflection tokens 并微调；推理时模型一边生成内容一边输出反思 token 做自适应。
- 批判性修正：反思为"不支持/无用"时，触发重新检索或改写。

### MVP 实现

**技术栈**：HuggingFace 预训练 Self-RAG 模型（`selfrag/selfrag_llama2_7b`）或 LangGraph 模拟反思流程。

```python
# 方案 A：直接用 Self-RAG 模型（需 GPU）
from transformers import AutoTokenizer, AutoModelForCausalLM
tok = AutoTokenizer.from_pretrained("selfrag/selfrag_llama2_7b")
model = AutoModelForCausalLM.from_pretrained("selfrag/selfrag_llama2_7b")
# 生成时模型自动输出 [Retrieval]/[Relevant]/[Supported] 等 token
```

**方案 B：LangGraph 模拟反思（无需微调）**

```python
def should_retrieve(s): return "retrieve" if s["need_retrieve"] else "generate"
def check_relevance(s): 
    s["relevant"] = llm_judge("检索结果是否与问题相关？", s["docs"])
    return "generate" if s["relevant"] else "rewrite"
def rewrite(s):
    s["query"] = llm("改写问题以提升检索质量", s["query"]); return retrieve(s)
```

**MVP 要点**：无 GPU 时用方案 B 用「LLM 打分 + 状态机」低成本复刻反思逻辑。

---

## 7. CRAG（Corrective RAG，纠错 RAG）

### 技术方法

在检索后、生成前加一道**质量评估 + 纠错**关卡：

1. **Retrieval Evaluator**：把检索结果评分为三档——
   - `Correct`（正确）：直接用检索结果生成。
   - `Ambiguous`（模糊）：分解 query / 补充检索。
   - `Incorrect`（错误）：丢弃，改用 Web 搜索兜底。
2. **纠错**：对错误/模糊结果触发外部搜索（如 Tavily）或查询重写。
3. **生成**：基于纠错后的证据生成。

### MVP 实现

**技术栈**：LangGraph + LLM 评估器 + Tavily 兜底。

```python
def evaluate(s):
    verdict = llm("判断检索结果质量：correct / ambiguous / incorrect", s["docs"])
    s["verdict"] = verdict
    return {"correct": "generate", "ambiguous": "rewrite", "incorrect": "web"}[verdict]

def web_fallback(s):
    s["docs"] = tavily_search(s["query"]); return "generate"

def rewrite(s):
    s["query"] = llm("分解或改写问题", s["query"])
    s["docs"] = hybrid.get_relevant_documents(s["query"]); return "generate"
```

**MVP 要点**：核心就是「评估器 + 三分类路由」，对检索质量不稳定的场景收益最明显。

---

## 8. HyDE（Hypothetical Document Embeddings）

### 技术方法

解决 query 与 document 语义空间不一致问题：

1. **生成假设答案**：让 LLM 先针对 query 生成一段"假设文档/答案"（即便不准确也没关系）。
2. **向量检索**：用这段假设文档（而非原始 query）做 embedding 并检索。
3. **生成**：用检索到的真实文档 + 原始 query 生成最终答案。
- 原理：假设文档与真实文档同处"文档语义空间"，比简短 query 更能命中。

### MVP 实现

**技术栈**：LangChain（内置 `HypotheticalDocumentEmbedder`）+ Chroma。

```python
from langchain.chains import HypotheticalDocumentEmbedder, LLMChain
from langchain.prompts import PromptTemplate

hyde_prompt = PromptTemplate.from_template("请针对问题写一段相关段落：{question}")
llm_chain = LLMChain(llm=llm, prompt=hyde_prompt)

embeddings = HypotheticalDocumentEmbedder(
    llm_chain=llm_chain,
    base_embeddings=OpenAIEmbeddings(),
)
vs = Chroma.from_documents(chunks, embeddings)
retriever = vs.as_retriever(k=4)
```

**MVP 要点**：改动最小——只替换 embedding 这一层，零样本召回即可提升。

---

## 9. RAPTOR

### 技术方法

构建**分层树形摘要**，支持跨块多粒度检索：

1. **分块**：文档切块并 embedding。
2. **聚类**：对 chunk 向量做降维（UMAP）+ 聚类（GMM）。
3. **摘要**：LLM 对每个簇生成摘要节点。
4. **迭代**：把摘要节点作为下一层输入，重复聚类+摘要，直到根节点，形成树。
5. **检索**：
   - 自顶向下（树遍历）：逐层比较 query 与节点，向下走最相关分支。
   - 折叠树（collapsed tree）：把所有层节点拍平成一层做相似度检索。
6. **生成**：基于命中的多层节点生成。

### MVP 实现

**技术栈**：LlamaIndex（内置 RAPTOR 实现）。

```python
from llama_index.packs.raptor import RaptorPack
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

pack = RaptorPack(
    documents=docs,
    llm=OpenAI(model="gpt-4o-mini"),
    embed_model=OpenAIEmbedding(),
)
index = pack.run()
print(index.as_query_engine().query("需要跨章节归纳的问题"))
```

**MVP 要点**：LlamaIndex 已封装，重点是理解"聚类→摘要→分层"的结构；自建时用 `sklearn` 聚类 + LLM 摘要即可。

---

## 10. 混合检索（Hybrid Retrieval）

### 技术方法

稠密 + 稀疏双路召回，再融合：

- **稠密检索**：向量 embedding + 余弦相似度，擅长语义相近。
- **稀疏检索**：BM25（词频-逆文档频率）关键词匹配，擅长专有名词、代码、精确字段。
- **融合排序（RRF）**：`score = Σ 1/(k + rank_i)`，对多路结果的排名做倒数加权融合，无需分数归一化。
- 也可用加权求和：`score = α·dense_norm + (1-α)·sparse_norm`。

### MVP 实现

**技术栈**：LangChain `EnsembleRetriever`（内置 RRF）。

```python
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import FAISS

bm25 = BM25Retriever.from_documents(chunks); bm25.k = 10
dense = FAISS.from_documents(chunks, OpenAIEmbeddings()).as_retriever(search_kwargs={"k": 10})

hybrid = EnsembleRetriever(retrievers=[bm25, dense], weights=[0.3, 0.7])  # 默认 RRF
docs = hybrid.get_relevant_documents(query)
```

**MVP 要点**：一行 `EnsembleRetriever` 即完成混合检索 + RRF 融合。

---

## 11. 多跳 RAG（Multi-hop RAG）

### 技术方法

对需要多步推理的问题做**迭代检索**：

1. **问题分解**：把复杂 query 拆成多个子问题（可用 LLM）。
2. **逐跳检索**：第一跳检索 → 得到中间事实 → 拼进下一跳 query → 再检索。
3. **证据累积**：跨跳保存已找到的证据链。
4. **终止**：达到最大跳数（如 3 跳）或证据充分即停止。
5. **生成**：基于完整证据链给出最终答案。

### MVP 实现

**技术栈**：LangGraph 循环（带跳数上限）。

```python
from langgraph.graph import StateGraph, END

class HopState(TypedDict):
    query: str
    hops: list
    evidence: list

def hop(s):
    docs = hybrid.get_relevant_documents(s["query"])
    s["evidence"].extend(docs)
    s["hops"].append(s["query"])
    return s

def should_continue(s):
    return "generate" if len(s["hops"]) >= 3 else "reformulate"

def reformulate(s):
    partial = "\n".join(d.page_content for d in s["evidence"])
    s["query"] = llm("基于已有信息，下一步还需检索什么？已有：", partial)
    return "hop"

g = StateGraph(HopState)
g.add_node("hop", hop)
g.add_node("generate", generate)
g.add_conditional_edges("hop", should_continue, {"generate": "generate", "reformulate": "reformulate"})
g.add_edge("reformulate", "hop")
g.add_edge("generate", END)
g.set_entry_point("hop")
app = g.compile()
```

**MVP 要点**：用「跳数上限 + LLM 重写 query」即可实现可终止的多跳循环。

---

## 附：MVP 选型速查

| 类型 | 最小技术栈 | 核心改动点 | MVP 代码量 |
|---|---|---|---|
| Naive RAG | LangChain + Chroma | 切块→建库→问答 | ~20 行 |
| Advanced RAG | + BM25 + CrossEncoder | 混合检索 + 重排 | ~30 行 |
| Modular RAG | LangGraph | 模块抽象为图节点 | ~40 行 |
| Graph RAG | graphrag / Neo4j | 实体抽取 + 社区摘要 | 官方库 0 代码 |
| Agentic RAG | LangGraph + 工具 | 检索源封装为 @tool | ~30 行 |
| Self-RAG | HF self-rag 模型 / LangGraph | 反思 token / LLM 打分 | ~30 行 |
| CRAG | LangGraph + Tavily | 评估器 + 三分类路由 | ~40 行 |
| HyDE | LangChain | 替换 embedding 层 | ~15 行 |
| RAPTOR | LlamaIndex RaptorPack | 聚类 + 分层摘要 | ~15 行 |
| 混合检索 | EnsembleRetriever | RRF 融合 | ~10 行 |
| 多跳 RAG | LangGraph 循环 | 迭代重写 query | ~40 行 |
