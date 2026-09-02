"""09 · Agent 记忆：三层记忆架构（无 LLM 依赖）

演示「工作记忆 + 短期记忆 + 长期记忆」三层记忆：
  1. 工作记忆（Working Memory）= LangGraph State，存放本次任务中间状态
  2. 短期记忆（Short-term）  = 会话内滑动窗口，只保留最近 N 条
  3. 长期记忆（Long-term）   = 跨会话的用户级记忆库（写入 / 召回 / 覆盖更新）

运行：
    python 09_agent_memory.py
"""

from typing import Optional, TypedDict, Annotated

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages


# ---------------------------------------------------------------------------
# 长期记忆库：跨会话持久，按 user_id 隔离
# 真实场景用向量库 + embedding 做语义检索，这里用「字符重叠度」近似，避免外部依赖
# ---------------------------------------------------------------------------
class LongTermMemory:
    def __init__(self):
        self._facts = {}  # user_id -> [fact, ...]

    def save(self, user_id: str, fact: str) -> None:
        """写入一条事实；已存在则跳过（去重/覆盖）。"""
        facts = self._facts.setdefault(user_id, [])
        if fact not in facts:
            facts.append(fact)

    def recall(self, user_id: str, query: str, k: int = 3) -> list:
        """按语义相似度召回 top-k 条长期记忆。"""
        facts = self._facts.get(user_id, [])
        if not facts:
            return []
        return sorted(facts, key=lambda f: self._similarity(query, f), reverse=True)[:k]

    @staticmethod
    def _similarity(a: str, b: str) -> float:
        """字符重叠度近似语义相似度（演示用，生产用 embedding）。"""
        sa, sb = set(a), set(b)
        if not sa or not sb:
            return 0.0
        return len(sa & sb) / len(sa | sb)

    def all_facts(self, user_id: str) -> list:
        return self._facts.get(user_id, [])


# 全局单例，模拟「跨会话持久化」的存储后端
ltm = LongTermMemory()

# 事实抽取规则：模拟 LLM「反思抽取」，把身份/偏好类信息提炼为长期记忆
FACT_MARKERS = {
    "我叫": "称呼",
    "我是": "身份",
    "我喜欢": "偏好",
    "我偏好": "偏好",
    "我讨厌": "负面偏好",
}


def extract_fact(text: str) -> Optional[str]:
    for marker, label in FACT_MARKERS.items():
        if marker in text:
            return f"{label}：{text}"
    return None


# ---------------------------------------------------------------------------
# State：工作记忆的载体
#   messages —— 会话历史（短期记忆的原料）
#   recalled —— 本轮召回的长期记忆
#   working  —— 本次任务的中间结果
# ---------------------------------------------------------------------------
class State(TypedDict):
    messages: Annotated[list, add_messages]
    user_id: str
    recalled: list
    working: dict


SHORT_TERM_WINDOW = 4  # 短期记忆滑动窗口大小


def recall_node(state: State) -> dict:
    """召回长期记忆 + 截取短期记忆，写入工作记忆。"""
    messages = state["messages"]
    query = messages[-1].content if messages else ""

    recalled = ltm.recall(state["user_id"], query, k=3)
    recent = messages[-SHORT_TERM_WINDOW:]

    return {
        "recalled": recalled,
        "working": {
            "query": query,
            "recent": [m.content for m in recent],
        },
    }


def respond_node(state: State) -> dict:
    """组装三层记忆上下文并「回复」，同时反思抽取事实写入长期记忆。"""
    recalled = state.get("recalled", [])
    working = state.get("working", {})
    recent = working.get("recent", [])

    # 1) 反思：把本轮用户消息里的身份/偏好抽取为长期记忆
    for m in state["messages"]:
        if getattr(m, "type", "") == "human":
            fact = extract_fact(m.content)
            if fact:
                ltm.save(state["user_id"], fact)

    # 2) 组装上下文（此处模拟 LLM，真实场景拼进 prompt 交给模型）
    answer = (
        f"回复（结合 {len(recalled)} 条长期记忆、"
        f"{len(recent)} 条短期记忆、"
        f"工作记忆 query='{working.get('query', '')}'）"
    )
    return {"messages": [("assistant", answer)]}


def build_graph():
    g = StateGraph(State)
    g.add_node("recall", recall_node)
    g.add_node("respond", respond_node)
    g.add_edge(START, "recall")
    g.add_edge("recall", "respond")
    g.add_edge("respond", END)
    return g.compile(checkpointer=MemorySaver())


if __name__ == "__main__":
    app = build_graph()

    # ------------------------------------------------------------------
    # 场景 1：Alice 首次会话 —— 建立长期记忆
    # ------------------------------------------------------------------
    print("=" * 62)
    print("场景 1：Alice 首次会话（写入长期记忆）")
    print("=" * 62)
    cfg1 = {"configurable": {"thread_id": "alice-s1"}}
    for text in ["你好，我叫 Alice", "我是后端工程师", "我喜欢简短的回答"]:
        app.invoke({"messages": [("user", text)], "user_id": "alice"}, cfg1)

    s1 = app.get_state(cfg1).values
    print("\n① 完整会话历史（checkpointer 持久化的全部消息）：")
    for m in s1["messages"]:
        print(f"   [{m.type}] {m.content}")

    print(f"\n② 短期记忆（滑动窗口，只保留最近 {SHORT_TERM_WINDOW} 条）：")
    for c in s1["working"]["recent"]:
        print(f"   - {c}")

    print("\n③ Alice 的长期记忆库（跨会话持久）：")
    for f in ltm.all_facts("alice"):
        print(f"   - {f}")

    # ------------------------------------------------------------------
    # 场景 2：Alice 第二次会话 —— 跨会话召回长期记忆
    # ------------------------------------------------------------------
    print()
    print("=" * 62)
    print("场景 2：Alice 第二次会话（跨会话召回长期记忆）")
    print("=" * 62)
    cfg2 = {"configurable": {"thread_id": "alice-s2"}}  # 新 thread，短期记忆归零
    app.invoke({"messages": [("user", "推荐一个后端框架")], "user_id": "alice"}, cfg2)

    s2 = app.get_state(cfg2).values
    print("\n① 召回的长期记忆（新会话短期记忆为空，但长期记忆仍在）：")
    for f in s2["recalled"]:
        print(f"   - {f}")

    print("\n② 工作记忆：")
    for k, v in s2["working"].items():
        print(f"   {k} = {v}")

    # ------------------------------------------------------------------
    # 场景 3：用户隔离 —— Bob 的长期记忆与 Alice 互不干扰
    # ------------------------------------------------------------------
    print()
    print("=" * 62)
    print("场景 3：Bob 的长期记忆与 Alice 隔离")
    print("=" * 62)
    cfg3 = {"configurable": {"thread_id": "bob-s1"}}
    app.invoke({"messages": [("user", "我叫 Bob")], "user_id": "bob"}, cfg3)
    app.invoke({"messages": [("user", "我是前端工程师")], "user_id": "bob"}, cfg3)

    print("\n① Bob 的长期记忆：")
    for f in ltm.all_facts("bob"):
        print(f"   - {f}")

    print("\n② Alice 的长期记忆（不受 Bob 影响）：")
    for f in ltm.all_facts("alice"):
        print(f"   - {f}")
