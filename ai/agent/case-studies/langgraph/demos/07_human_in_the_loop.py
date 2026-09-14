"""07 · 人机协同 / interrupt（无 LLM 依赖）

演示用 interrupt 在关键节点「暂停」，等待人类审批后再继续。

流程：submit -> approve（interrupt 挂起）-> 按审批结果 publish / reject。

运行：
    python 07_human_in_the_loop.py
"""

from typing import TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command, interrupt


class State(TypedDict):
    request: str
    approved: bool
    result: str


def submit(state: State) -> dict:
    return {"result": f"已提交请求：{state['request']}"}


def approve(state: State) -> dict:
    """在这里挂起，等待人类输入 yes/no。"""
    decision = interrupt({"question": f"是否批准执行「{state['request']}」？（yes/no）"})
    return {"approved": decision == "yes"}


def route(state: State) -> str:
    return "publish" if state["approved"] else "reject"


def publish(state: State) -> dict:
    return {"result": f"已执行：{state['request']}"}


def reject(state: State) -> dict:
    return {"result": f"已拒绝：{state['request']}"}


def build_graph():
    g = StateGraph(State)
    g.add_node("submit", submit)
    g.add_node("approve", approve)
    g.add_node("publish", publish)
    g.add_node("reject", reject)

    g.add_edge(START, "submit")
    g.add_edge("submit", "approve")
    g.add_conditional_edges("approve", route, {"publish": "publish", "reject": "reject"})
    g.add_edge("publish", END)
    g.add_edge("reject", END)

    # interrupt 需要 checkpointer 才能恢复
    return g.compile(checkpointer=MemorySaver())


if __name__ == "__main__":
    app = build_graph()
    config = {"configurable": {"thread_id": "approval-1"}}

    # 第一次执行：会在 approve 节点挂起
    print("=== 第一次 invoke（将挂起等待审批）===")
    state = app.invoke({"request": "删除生产数据库"}, config)
    print("当前状态：", state)
    print("下一步（挂起点）：", app.get_state(config).next)

    # 模拟人类决策：拒绝
    print("\n=== 人工决策：拒绝 -> 恢复执行 ===")
    final = app.invoke(Command(resume="no"), config)
    print("最终结果：", final["result"])
