"""08 · 持久化与记忆（无 LLM 依赖）

演示 checkpointer + thread_id：
  1. 同一 thread_id 的多次调用共享历史（多轮记忆）
  2. 不同 thread_id 之间会话隔离
  3. get_state / get_state_history 回溯状态

运行：
    python 08_checkpointer_memory.py
"""

from typing import TypedDict, Annotated

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list, add_messages]


def reply(state: State) -> dict:
    """记住用户最后一句，并回复。"""
    last = state["messages"][-1].content
    return {"messages": [("ai", f"我记住了：{last}")]}


def build_graph():
    g = StateGraph(State)
    g.add_node("reply", reply)
    g.add_edge(START, "reply")
    g.add_edge("reply", END)
    return g.compile(checkpointer=MemorySaver())


if __name__ == "__main__":
    app = build_graph()

    alice = {"configurable": {"thread_id": "alice"}}
    bob = {"configurable": {"thread_id": "bob"}}

    # 同一会话连续对话，共享记忆
    app.invoke({"messages": [("user", "我叫 Alice")]}, alice)
    app.invoke({"messages": [("user", "我喜欢写代码")]}, alice)

    # 另一个会话完全隔离
    app.invoke({"messages": [("user", "我叫 Bob")]}, bob)

    print("=== Alice 会话的完整记忆（含历史）===")
    for m in app.get_state(alice).values["messages"]:
        print(f"  [{m.type}] {m.content}")

    print("\n=== Bob 会话的完整记忆（互不干扰）===")
    for m in app.get_state(bob).values["messages"]:
        print(f"  [{m.type}] {m.content}")

    print("\n=== Alice 会话的历史快照数 ===")
    print(len(list(app.get_state_history(alice))))
