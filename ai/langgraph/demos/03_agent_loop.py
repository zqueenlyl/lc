"""03 · ReAct Agent 循环（依赖 LLM）

演示 Agent 的本质：一个「调 LLM -> 执行工具 -> 回到 LLM」的循环图。
这里同时给出两种写法：
  1. 用 create_react_agent 一行构建（推荐）
  2. 手写 agent <-> tools 循环（理解内部原理）

需要设置：export OPENAI_API_KEY="sk-..."

运行：
    python 03_agent_loop.py
"""

import os

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI


@tool
def multiply(a: int, b: int) -> int:
    """两个整数相乘。"""
    return a * b


@tool
def add(a: int, b: int) -> int:
    """两个整数相加。"""
    return a + b


def demo_prebuilt():
    """方式一：官方 create_react_agent。"""
    from langgraph.prebuilt import create_react_agent

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    agent = create_react_agent(llm, tools=[multiply, add])

    print("=== create_react_agent 图结构 ===")
    print(agent.get_graph().draw_ascii())

    result = agent.invoke(
        {"messages": [("user", "先算 3 乘以 4，再把结果加 10，最终是多少？")]}
    )
    print("=== 最终回答 ===")
    print(result["messages"][-1].content)


def demo_handwritten():
    """方式二：手写 agent <-> tools 循环，揭示内部原理。"""
    from typing import TypedDict, Annotated

    from langgraph.graph import StateGraph, START, END
    from langgraph.graph.message import add_messages
    from langgraph.prebuilt import ToolNode

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0).bind_tools([multiply, add])

    class State(TypedDict):
        messages: Annotated[list, add_messages]

    def call_model(state: State):
        return {"messages": [llm.invoke(state["messages"])]}

    def should_continue(state: State):
        last = state["messages"][-1]
        # 有工具调用 -> 执行工具；否则 -> 结束
        return "tools" if getattr(last, "tool_calls", None) else END

    g = StateGraph(State)
    g.add_node("agent", call_model)
    g.add_node("tools", ToolNode([multiply, add]))
    g.add_edge(START, "agent")
    g.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    g.add_edge("tools", "agent")
    app = g.compile()

    print("\n=== 手写 ReAct 图结构 ===")
    print(app.get_graph().draw_ascii())

    result = app.invoke({"messages": [("user", "7 乘以 8 等于多少？")]})
    print("=== 最终回答 ===")
    print(result["messages"][-1].content)


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("请先设置环境变量：export OPENAI_API_KEY=...")

    demo_prebuilt()
    demo_handwritten()
