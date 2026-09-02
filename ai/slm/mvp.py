"""SLM 舰队：按任务选档 + 离线兜底（无真实模型）

档位：
  tiny     — 端侧，只能分类
  small    — 便宜云 / 强端侧，做抽取
  frontier — 贵，做开放推理

运行：
    python3 mvp.py
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Reply:
    model: str
    text: str
    cost: float


def tiny(task: str, text: str) -> Reply:
    if task == "intent":
        label = "refund" if any(k in text for k in ("退", "refund")) else "chitchat"
        return Reply("tiny", label, 0.0001)
    return Reply("tiny", "本地只能做分类，请上送或换 small。", 0.0001)


def small(task: str, text: str) -> Reply:
    if task == "extract":
        oid = "O-88" if "88" in text else "UNKNOWN"
        return Reply("small", f'{{"order_id":"{oid}"}}', 0.001)
    if task == "intent":
        return tiny(task, text)
    return Reply("small", "小模型不确定，建议 frontier。", 0.001)


def frontier(task: str, text: str) -> Reply:
    return Reply("frontier", f"深度回答：针对「{text}」给出带步骤的方案。", 0.05)


def route(task: str, offline: bool) -> str:
    if offline:
        return "tiny"
    return {"intent": "tiny", "extract": "small", "reason": "frontier"}[task]


RUNNERS = {"tiny": tiny, "small": small, "frontier": frontier}


def handle(task: str, text: str, offline: bool = False) -> Reply:
    model = route(task, offline)
    return RUNNERS[model](task, text)


if __name__ == "__main__":
    cases = [
        ("intent", "我想退款", False),
        ("extract", "订单 88 要退", False),
        ("reason", "设计一个带重试的支付对账 Agent", False),
        ("reason", "设计一个带重试的支付对账 Agent", True),
    ]
    total = 0.0
    for task, text, offline in cases:
        r = handle(task, text, offline)
        total += r.cost
        net = "离线" if offline else "在线"
        print(f"[{net}] {task:7} → {r.model:8} ${r.cost:.4f}  {r.text}")
    print(f"\n本段模拟成本合计 ${total:.4f}（全走 frontier 会是 ${0.05 * len(cases):.2f}）")
