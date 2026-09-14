"""循环与图工程 MVP：执行图 + 上下文图（纯标准库，无外部 API）

场景：客服问「订单 8821 为什么被拒退？」
- 关键词检索只命中订单文档，看不到「企业客户 + 激活码不可退」这条关系。
- 上下文图沿 订单 → 客户类型 → 政策 走出原因。
- 执行图按条件边：关键词不够 → 图遍历 → 退款是高危操作，停在人审。

运行：
    python3 mvp.py
"""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Callable


# ── 1. 上下文图：属性图 + 局部遍历 + 连通分量（当社区）────────────────


@dataclass
class Node:
    id: str
    type: str
    props: dict = field(default_factory=dict)
    source: str = ""


@dataclass
class Edge:
    src: str
    rel: str
    dst: str
    source: str = ""
    confidence: float = 1.0


class ContextGraph:
    def __init__(self) -> None:
        self.nodes: dict[str, Node] = {}
        self.out: dict[str, list[Edge]] = defaultdict(list)
        self.inn: dict[str, list[Edge]] = defaultdict(list)

    def upsert(self, node: Node) -> None:
        self.nodes[node.id] = node

    def link(self, edge: Edge) -> None:
        self.out[edge.src].append(edge)
        self.inn[edge.dst].append(edge)

    def neighbors(self, nid: str) -> list[Edge]:
        return self.out.get(nid, []) + self.inn.get(nid, [])

    def bfs_subgraph(self, seeds: list[str], hops: int = 2) -> list[str]:
        seen: set[str] = set()
        q: deque[tuple[str, int]] = deque((s, 0) for s in seeds if s in self.nodes)
        order: list[str] = []
        while q:
            nid, d = q.popleft()
            if nid in seen:
                continue
            seen.add(nid)
            order.append(nid)
            if d >= hops:
                continue
            for e in self.neighbors(nid):
                nxt = e.dst if e.src == nid else e.src
                if nxt not in seen:
                    q.append((nxt, d + 1))
        return order

    def path(self, src: str, dst: str) -> list[Edge] | None:
        prev: dict[str, Edge] = {}
        q: deque[str] = deque([src])
        seen = {src}
        while q:
            cur = q.popleft()
            if cur == dst:
                chain: list[Edge] = []
                at = dst
                while at != src:
                    e = prev[at]
                    chain.append(e)
                    at = e.src if e.dst == at else e.dst
                chain.reverse()
                return chain
            for e in self.neighbors(cur):
                nxt = e.dst if e.src == cur else e.src
                if nxt not in seen:
                    seen.add(nxt)
                    prev[nxt] = e
                    q.append(nxt)
        return None

    def communities(self) -> dict[str, str]:
        """并查集：无向连通分量当社区（演示用，生产用 Leiden）。"""
        parent = {n: n for n in self.nodes}

        def find(x: str) -> str:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a: str, b: str) -> None:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[rb] = ra

        for nid, edges in self.out.items():
            for e in edges:
                union(nid, e.dst)
        return {n: find(n) for n in self.nodes}

    def community_summaries(self) -> dict[str, str]:
        comm = self.communities()
        buckets: dict[str, list[str]] = defaultdict(list)
        for nid, cid in comm.items():
            node = self.nodes[nid]
            buckets[cid].append(f"{node.type}:{nid}")
        return {cid: "、".join(members) for cid, members in buckets.items()}


def build_context_graph() -> ContextGraph:
    """规则抽取：生产里这一步通常是 LLM。这里用词典 + 共现，保证可跑、可复现。"""
    docs = {
        "ticket.md": "工单 T-19：用户企业客户A询问订单 8821 拒退，已激活。",
        "order.md": "订单 8821 金额 299，商品为专业版许可证，状态已激活，归属企业客户A。",
        "policy.md": "退款政策：7 天无理由。企业客户购买的已激活许可证不可退。个人客户未激活可退。",
    }
    g = ContextGraph()
    catalog = {
        "订单8821": ("Order", "order.md"),
        "企业客户A": ("Customer", "order.md"),
        "工单T-19": ("Ticket", "ticket.md"),
        "专业版许可证": ("Product", "order.md"),
        "退款政策": ("Policy", "policy.md"),
        "已激活许可证不可退": ("Clause", "policy.md"),
        "7天无理由": ("Clause", "policy.md"),
    }
    for nid, (typ, src) in catalog.items():
        g.upsert(Node(nid, typ, source=src))

    triples = [
        ("工单T-19", "ABOUT", "订单8821", "ticket.md"),
        ("订单8821", "OWNED_BY", "企业客户A", "order.md"),
        ("订单8821", "HAS_PRODUCT", "专业版许可证", "order.md"),
        ("企业客户A", "BOUND_BY", "退款政策", "policy.md"),
        ("退款政策", "CONTAINS", "已激活许可证不可退", "policy.md"),
        ("退款政策", "CONTAINS", "7天无理由", "policy.md"),
        ("专业版许可证", "TRIGGERED", "已激活许可证不可退", "policy.md"),
    ]
    for s, rel, d, src in triples:
        g.link(Edge(s, rel, d, source=src, confidence=0.95))
    return g


def keyword_retrieve(docs: dict[str, str], query: str, k: int = 2) -> list[str]:
    q = set(query)
    scored = []
    for name, text in docs.items():
        overlap = sum(1 for ch in set(text) if ch in q)
        scored.append((overlap, name, text))
    scored.sort(reverse=True)
    return [f"[{n}] {t}" for _, n, t in scored[:k]]


def graph_local_answer(g: ContextGraph, seed: str) -> str:
    order = g.bfs_subgraph([seed], hops=3)
    lines = ["局部子图（3 跳）："]
    for nid in order:
        n = g.nodes[nid]
        lines.append(f"  - {n.type} {nid}  (source={n.source})")
    path = g.path("订单8821", "已激活许可证不可退")
    lines.append("因果路径：")
    if path:
        cursor = "订单8821"
        bits = [cursor]
        for e in path:
            nxt = e.dst if e.src == cursor else e.src
            bits.append(f"-[{e.rel}]-> {nxt}")
            cursor = nxt
        lines.append("  " + " ".join(bits))
    else:
        lines.append("  （未找到路径）")
    return "\n".join(lines)


# ── 2. 执行图：节点 + 条件边 + 人审中断 ────────────────────────────────


@dataclass
class ExecState:
    query: str
    keyword_hits: list[str] = field(default_factory=list)
    graph_view: str = ""
    enough: bool = False
    answer: str = ""
    interrupt: str = ""
    log: list[str] = field(default_factory=list)

    def note(self, msg: str) -> None:
        self.log.append(msg)


class ExecutionGraph:
    def __init__(self) -> None:
        self.nodes: dict[str, Callable[[ExecState], str]] = {}
        self.cond: dict[str, Callable[[ExecState], str]] = {}

    def add(self, name: str, fn: Callable[[ExecState], str]) -> None:
        self.nodes[name] = fn

    def route(self, name: str, fn: Callable[[ExecState], str]) -> None:
        self.cond[name] = fn

    def run(self, start: str, state: ExecState, limit: int = 12) -> ExecState:
        cur = start
        for _ in range(limit):
            if cur in ("END", "HITL"):
                return state
            nxt = self.nodes[cur](state)
            if cur in self.cond:
                nxt = self.cond[cur](state)
            state.note(f"{cur} → {nxt}")
            cur = nxt
        state.note("step_limit")
        return state


def make_execution_graph(g: ContextGraph, docs: dict[str, str]) -> ExecutionGraph:
    eg = ExecutionGraph()

    def plan(s: ExecState) -> str:
        s.note("plan: 先关键词，不够再走图")
        return "keyword"

    def keyword(s: ExecState) -> str:
        s.keyword_hits = keyword_retrieve(docs, s.query)
        # 关键词命中里没有「不可退」条款 → 判定不够
        blob = "".join(s.keyword_hits)
        s.enough = "不可退" in blob
        s.note(f"keyword enough={s.enough}")
        return "graph"  # 实际走向由 cond 决定

    def graph_node(s: ExecState) -> str:
        s.graph_view = graph_local_answer(g, "订单8821")
        s.enough = "已激活许可证不可退" in s.graph_view
        s.note(f"graph enough={s.enough}")
        return "decide"

    def decide(s: ExecState) -> str:
        if not s.enough:
            s.answer = "证据不足，拒绝编造。"
            return "END"
        s.answer = (
            "拒退原因：订单 8821 属企业客户A，商品已激活，"
            "命中条款「已激活许可证不可退」（路径见上下文图）。"
        )
        return "refund_gate"

    def refund_gate(s: ExecState) -> str:
        s.interrupt = "HITL: 退款是写操作，等人确认后才能调 refund 工具"
        return "HITL"

    eg.add("plan", plan)
    eg.add("keyword", keyword)
    eg.add("graph", graph_node)
    eg.add("decide", decide)
    eg.add("refund_gate", refund_gate)
    eg.route("keyword", lambda s: "decide" if s.enough else "graph")
    return eg


# ── 3. 跑一遍对照 ────────────────────────────────────────────────────


DOCS = {
    "ticket.md": "工单 T-19：用户企业客户A询问订单 8821 拒退，已激活。",
    "order.md": "订单 8821 金额 299，商品为专业版许可证，状态已激活，归属企业客户A。",
    "policy.md": "退款政策：7 天无理由。企业客户购买的已激活许可证不可退。个人客户未激活可退。",
}


if __name__ == "__main__":
    g = build_context_graph()
    query = "订单 8821 为什么被拒退？"

    print("=== 上下文图：节点 / 边 ===")
    print(f"  {len(g.nodes)} nodes, {sum(len(v) for v in g.out.values())} edges")
    for e in (edge for edges in g.out.values() for edge in edges):
        print(f"  {e.src} -[{e.rel}]-> {e.dst}")

    print("\n=== 全局：连通分量摘要（演示社区） ===")
    for cid, summary in g.community_summaries().items():
        print(f"  community {cid}: {summary}")

    print("\n=== 关键词检索（会漏条款） ===")
    for hit in keyword_retrieve(DOCS, query):
        print(f"  {hit}")

    print("\n=== 图局部检索（能走出原因） ===")
    print(graph_local_answer(g, "订单8821"))

    print("\n=== 执行图：plan → keyword → graph → decide → HITL ===")
    eg = make_execution_graph(g, DOCS)
    st = ExecState(query=query)
    eg.run("plan", st)
    for line in st.log:
        print(f"  {line}")
    print(f"  answer: {st.answer}")
    print(f"  interrupt: {st.interrupt}")
    print("\n要点：checkpoint 能记下这条 run；条款本身住在上下文图，不在 State 里。")
