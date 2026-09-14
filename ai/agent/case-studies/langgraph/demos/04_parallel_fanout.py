"""04 · 并行 fan-out / fan-in（无 LLM 依赖）

演示 Send API：把一个节点「扇出」成多个并行分支，各自处理后再汇总。
这是 LangGraph 官方推荐的 fan-out 写法：
  - fan-out：在 START 上用 add_conditional_edges 返回 list[Send]
  - fan-in：靠 `Annotated[list, add]` reducer 自动汇总并行结果

运行：
    python 04_parallel_fanout.py
"""

from typing import TypedDict, Annotated
from operator import add

from langgraph.graph import StateGraph, START, END
from langgraph.types import Send


class State(TypedDict):
    subjects: list[str]
    results: Annotated[list, add]  # add reducer：并发结果自动汇总


def fan_out(state: State) -> list[Send]:
    """为每个 subject 生成一个 Send，指向同一个 worker 节点。"""
    return [Send("worker", {"subject": s}) for s in state["subjects"]]


def worker(state: dict) -> dict:
    """每个并行分支独立执行；这里用假任务模拟耗时处理。"""
    subject = state["subject"]
    return {"results": [f"已处理主题「{subject}」"]}


def build_graph():
    g = StateGraph(State)
    g.add_node("worker", worker)

    # 关键：START 上用条件边返回 list[Send] 实现扇出
    g.add_conditional_edges(START, fan_out)
    # 每个 worker 结束即到 END，靠 add reducer 自动 fan-in
    g.add_edge("worker", END)
    return g.compile()


if __name__ == "__main__":
    app = build_graph()

    print("=== 图结构 ===")
    print(app.get_graph().draw_ascii())

    result = app.invoke({"subjects": ["向量检索", "图谱推理", "多智能体"]})
    print("=== 并行结果（已自动汇总）===")
    for r in result["results"]:
        print(f"  - {r}")
    print(f"共 {len(result['results'])} 条结果")
