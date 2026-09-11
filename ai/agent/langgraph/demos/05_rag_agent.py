"""05 · RAG Agent（依赖 LLM + Embedding）

演示「检索增强生成 + 循环重试」：
retrieve -> decide（质量门禁）-> generate 或 rewrite（改写后重新检索，最多 2 次）。

需要设置：export OPENAI_API_KEY="sk-..."

运行：
    python 05_rag_agent.py
"""

import os
from typing import TypedDict

from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langgraph.graph import StateGraph, START, END

# 内嵌知识库（替代真实文档，便于直接运行）
DOCS = [
    Document(page_content="LangGraph 是一个用于构建有状态、多步骤 LLM 应用的图编排框架。"),
    Document(page_content="RAG 通过从外部知识库检索相关内容来增强大语言模型的生成能力，缓解幻觉。"),
    Document(page_content="LangGraph 支持条件分支、循环、持久化和多智能体编排。"),
    Document(page_content="向量数据库用于存储文本的 embedding，并支持语义相似度检索。"),
]

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 构建向量库（全局复用）
vectorstore = Chroma.from_documents(DOCS, OpenAIEmbeddings())
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})


class State(TypedDict):
    question: str
    context: str
    attempts: int
    answer: str


def retrieve(state: State) -> dict:
    """向量检索 top-k 文档，拼接为上下文。"""
    docs = retriever.invoke(state["question"])
    return {
        "context": "\n".join(d.page_content for d in docs),
        "attempts": state.get("attempts", 0) + 1,
    }


def decide(state: State) -> str:
    """质量门禁：有上下文或已达重试上限 -> 生成；否则改写重试。"""
    if state["context"].strip() or state["attempts"] >= 2:
        return "generate"
    return "rewrite"


def rewrite(state: State) -> dict:
    """改写问题以提升召回。"""
    return {"question": state["question"] + "（请结合知识库更精确回答）"}


def generate(state: State) -> dict:
    """基于上下文生成答案。"""
    prompt = (
        "你是一名助手，仅依据以下上下文回答问题，不要编造。\n"
        f"上下文：\n{state['context']}\n\n"
        f"问题：{state['question']}"
    )
    return {"answer": llm.invoke(prompt).content}


def build_graph():
    g = StateGraph(State)
    g.add_node("retrieve", retrieve)
    g.add_node("rewrite", rewrite)
    g.add_node("generate", generate)

    g.add_edge(START, "retrieve")
    g.add_conditional_edges("retrieve", decide, {"generate": "generate", "rewrite": "rewrite"})
    g.add_edge("rewrite", "retrieve")   # 回指 -> 循环
    g.add_edge("generate", END)
    return g.compile()


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("请先设置环境变量：export OPENAI_API_KEY=...")

    app = build_graph()
    print("=== 图结构 ===")
    print(app.get_graph().draw_ascii())

    question = "LangGraph 是什么？"
    result = app.invoke({"question": question})
    print("=== 问题 ===")
    print(question)
    print("=== 检索到的上下文 ===")
    print(result["context"])
    print("=== 回答 ===")
    print(result["answer"])
