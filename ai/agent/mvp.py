"""ReAct Agent 最小循环（无 LLM）

目标：给订单退款。策略层用规则模拟模型：
  Thought → Action(lookup / refund / finish) → Observation → …

缺单号则停，不编造。演示「观察进状态、验证才结束」。

运行：
    python3 mvp.py
"""

from __future__ import annotations

from dataclasses import dataclass, field


ORDERS = {"O-88": {"amount": 59, "user": "ada"}}


@dataclass
class ToolResult:
    ok: bool
    data: str


def lookup_order(order_id: str) -> ToolResult:
    row = ORDERS.get(order_id)
    if not row:
        return ToolResult(False, f"not_found:{order_id}")
    return ToolResult(True, f"amount={row['amount']} user={row['user']}")


def refund(order_id: str, amount: int) -> ToolResult:
    row = ORDERS.get(order_id)
    if not row:
        return ToolResult(False, "order_missing")
    if amount != row["amount"]:
        return ToolResult(False, f"amount_mismatch expect={row['amount']}")
    return ToolResult(True, f"refunded {amount} for {order_id}")


TOOLS = {"lookup_order": lookup_order, "refund": refund}


@dataclass
class Step:
    thought: str
    action: str
    args: dict
    observation: str


@dataclass
class ReactAgent:
    goal: str
    order_id: str | None = None
    max_steps: int = 6
    known_amount: int | None = None
    refunded: bool = False
    log: list[Step] = field(default_factory=list)

    def think_and_act(self) -> tuple[str, str, dict]:
        if not self.order_id:
            return ("没有订单号，不能编造。", "finish", {"reason": "missing_order_id"})
        if self.refunded:
            return ("退款已完成。", "finish", {"reason": "done"})
        if self.known_amount is None:
            return (
                f"先查订单 {self.order_id} 的金额。",
                "lookup_order",
                {"order_id": self.order_id},
            )
        return (
            f"金额已知为 {self.known_amount}，执行退款。",
            "refund",
            {"order_id": self.order_id, "amount": self.known_amount},
        )

    def observe(self, action: str, args: dict) -> str:
        if action == "finish":
            return args.get("reason", "stop")
        fn = TOOLS[action]
        result = fn(**args)
        if action == "lookup_order" and result.ok:
            # 从观察里解析金额，禁止模型「猜」
            self.known_amount = int(result.data.split("amount=")[1].split()[0])
        if action == "refund" and result.ok:
            self.refunded = True
        return ("ok " if result.ok else "err ") + result.data

    def run(self) -> str:
        print(f"GOAL {self.goal!r}  order_id={self.order_id!r}\n")
        for i in range(1, self.max_steps + 1):
            thought, action, args = self.think_and_act()
            obs = self.observe(action, args)
            self.log.append(Step(thought, action, args, obs))
            print(f"--- step {i} ---")
            print(f"Thought     {thought}")
            print(f"Action      {action} {args}")
            print(f"Observation {obs}\n")
            if action == "finish":
                return obs
        return "max_steps"


def main() -> None:
    print("=== 有单号：应 lookup → refund → finish ===")
    ok = ReactAgent(goal="给用户退款", order_id="O-88")
    print("RESULT", ok.run(), "refunded=", ok.refunded)

    print("\n=== 无单号：应直接 finish，不调用 refund ===")
    blocked = ReactAgent(goal="给用户退款", order_id=None)
    print("RESULT", blocked.run(), "refunded=", blocked.refunded)
    assert not blocked.refunded
    assert all(s.action != "refund" for s in blocked.log)


if __name__ == "__main__":
    main()
