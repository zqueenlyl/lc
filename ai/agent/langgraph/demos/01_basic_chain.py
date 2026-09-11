"""01 · 线性流水线（无 LLM 依赖）

演示 LangGraph 最核心的四个抽象：State / Node / Edge / compile+invoke。

流程：retrieve -> rewrite -> generate，一条直线走到底。

运行：
    python 01_basic_chain.py
"""

from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    """图里流转的共享状态。节点只返回需要更新的字段。"""
    query: str
    docs: str
    answer: str


def retrieve(state: State) -> dict:
    """模拟检索：根据 query 拿到相关文档。"""
    return {"docs": f"检索到 3 篇与「{state['query']}」相关的文档"}


def rewrite(state: State) -> dict:
    """模拟查询改写：优化 query 表达。"""
    return {"query": f"{state['query']}（已优化）"}


def generate(state: State) -> dict:
    """模拟生成：基于文档产出答案。"""
    return {"answer": f"基于「{state['docs']}」生成最终答案"}


def build_graph():
    g = StateGraph(State)
    g.add_node("retrieve", retrieve)
    g.add_node("rewrite", rewrite)
    g.add_node("generate", generate)

    g.add_edge(START, "retrieve")
    g.add_edge("retrieve", "rewrite")
    g.add_edge("rewrite", "generate")
    g.add_edge("generate", END)
    return g.compile()


if __name__ == "__main__":
    app = build_graph()

    print("=== 图结构 ===")
    print(app.get_graph().draw_ascii())

    print("=== 执行结果 ===")
    result = app.invoke({"query": "LangGraph 是什么？"})
    for k, v in result.items():
        print(f"{k}: {v}")
