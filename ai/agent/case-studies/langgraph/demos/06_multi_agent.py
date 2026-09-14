"""06 · 多智能体（Supervisor 模式，依赖 LLM）

演示由一个「监督者」在多个专职 Agent 之间路由：
  supervisor -> research（研究员）/ coder（工程师） -> 回到 supervisor -> 直到 FINISH。

需要设置：export OPENAI_API_KEY="sk-..."

运行：
    python 06_multi_agent.py
"""

import os
from typing import TypedDict, Annotated

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


class State(TypedDict):
    messages: Annotated[list, add_messages]
    next: str


def supervisor(state: State) -> dict:
    """监督者：根据对话决定下一步交给谁。"""
    prompt = (
        "你是任务统筹者。根据用户最新问题，决定下一步交给谁。\n"
        "可选：research（需要调研/分析）、coder（需要写代码/技术方案）、FINISH（已完成可结束）。\n"
        f"用户问题：{state['messages'][-1].content}\n"
        "只回复 research / coder / FINISH。"
    )
    decision = llm.invoke(prompt).content.strip().lower()
    return {"next": decision}


def researcher(state: State) -> dict:
    """研究员：产出调研/分析结论。"""
    prompt = f"你是一名研究员，针对问题给出简洁的分析结论：{state['messages'][-1].content}"
    result = llm.invoke(prompt).content
    return {"messages": [("ai", f"[研究员] {result}")]}


def coder(state: State) -> dict:
    """工程师：产出代码/技术方案。"""
    prompt = f"你是一名工程师，针对问题给出简洁的技术方案：{state['messages'][-1].content}"
    result = llm.invoke(prompt).content
    return {"messages": [("ai", f"[工程师] {result}")]}


def route(state: State) -> str:
    return "finish" if state["next"] == "finish" else state["next"]


def build_graph():
    g = StateGraph(State)
    g.add_node("supervisor", supervisor)
    g.add_node("research", researcher)
    g.add_node("coder", coder)

    g.add_edge(START, "supervisor")
    g.add_conditional_edges(
        "supervisor",
        route,
        {"research": "research", "coder": "coder", "finish": END},
    )
    # 子 Agent 完成后回到监督者，由其决定下一步
    g.add_edge("research", "supervisor")
    g.add_edge("coder", "supervisor")
    return g.compile()


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("请先设置环境变量：export OPENAI_API_KEY=...")

    app = build_graph()
    print("=== 图结构 ===")
    print(app.get_graph().draw_ascii())

    result = app.invoke(
        {"messages": [("user", "调研一下 LangGraph 的优势，并给出一个 Hello World 示例代码")]},
        config={"recursion_limit": 20},
    )
    print("=== 协作过程 ===")
    for m in result["messages"]:
        print(f"{m.type}: {m.content}\n")
