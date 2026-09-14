"""02 · 条件分支 / 路由（无 LLM 依赖）

演示 add_conditional_edges：根据当前状态把请求分流到不同处理节点。

流程：classify（分类） -> 按 kind 路由到 handle_code / handle_sales / handle_general。

运行：
    python 02_branching_router.py
"""

from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    text: str
    kind: str
    result: str


def classify(state: State) -> dict:
    """按关键词把输入分到不同类别。"""
    text = state["text"]
    if any(w in text for w in ("代码", "bug", "报错", "python", "error")):
        kind = "code"
    elif any(w in text for w in ("价格", "购买", "下单", "多少钱")):
        kind = "sales"
    else:
        kind = "general"
    return {"kind": kind}


def handle_code(state: State) -> dict:
    return {"result": f"[技术通道] 已受理问题：{state['text']}"}


def handle_sales(state: State) -> dict:
    return {"result": f"[销售通道] 已受理问题：{state['text']}"}


def handle_general(state: State) -> dict:
    return {"result": f"[通用通道] 已受理问题：{state['text']}"}


def route(state: State) -> str:
    """路由函数：只读状态，返回下一个节点名。"""
    return state["kind"]


def build_graph():
    g = StateGraph(State)
    g.add_node("classify", classify)
    g.add_node("handle_code", handle_code)
    g.add_node("handle_sales", handle_sales)
    g.add_node("handle_general", handle_general)

    g.add_edge(START, "classify")
    g.add_conditional_edges(
        "classify",
        route,
        {
            "code": "handle_code",
            "sales": "handle_sales",
            "general": "handle_general",
        },
    )
    for node in ("handle_code", "handle_sales", "handle_general"):
        g.add_edge(node, END)
    return g.compile()


if __name__ == "__main__":
    app = build_graph()

    print("=== 图结构 ===")
    print(app.get_graph().draw_ascii())

    print("=== 路由测试 ===")
    for text in ["我的代码报错了，帮忙看下", "这个课程多少钱？", "今天天气不错"]:
        result = app.invoke({"text": text})
        print(f"输入：{text}")
        print(f"  -> {result['result']}")
