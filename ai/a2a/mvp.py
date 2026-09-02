"""A2A 最小形状（无外部依赖）

客服 Agent 发现账务 Agent 的 Card，提交 Task，轮询到 completed，只拿到 Artifact，
看不到账务内部的「数据库」。

运行：
    python3 mvp.py
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4


BILLS = {
    "B-1001": {"user": "u1", "amount": 128.0, "reason": "会员自动续费"},
    "B-1002": {"user": "u1", "amount": 36.0, "reason": "流量加油包"},
}


@dataclass
class AgentCard:
    name: str
    url: str
    skills: list[dict]
    description: str = ""


@dataclass
class Task:
    id: str
    skill: str
    input: dict
    state: str = "submitted"
    artifact: Any = None
    error: str | None = None


class SpecialistAgent:
    """被委托方：对外只有 card + send/get，对内可以随便查库。"""

    def __init__(self):
        self.card = AgentCard(
            name="billing-agent",
            url="memory://billing",
            description="处理账单查询与争议解释，不开放底层 SQL。",
            skills=[
                {
                    "id": "explain_charge",
                    "name": "解释一笔扣费",
                    "input": {"bill_id": "string"},
                    "output": {"summary": "string"},
                }
            ],
        )
        self._tasks: dict[str, Task] = {}

    def send(self, skill: str, payload: dict) -> Task:
        task = Task(id=str(uuid4())[:8], skill=skill, input=payload, state="working")
        self._tasks[task.id] = task
        self._run(task)
        return task

    def get(self, task_id: str) -> Task:
        return self._tasks[task_id]

    def _run(self, task: Task) -> None:
        if task.skill != "explain_charge":
            task.state = "failed"
            task.error = f"unknown skill: {task.skill}"
            return
        bill_id = task.input.get("bill_id")
        row = BILLS.get(bill_id)
        if not row:
            task.state = "failed"
            task.error = f"bill not found: {bill_id}"
            return
        # 内部细节不出现在 artifact 里
        task.artifact = {
            "summary": f"账单 {bill_id} 扣费 {row['amount']} 元，原因：{row['reason']}。",
            "user": row["user"],
        }
        task.state = "completed"


@dataclass
class Orchestrator:
    registry: dict[str, SpecialistAgent] = field(default_factory=dict)

    def register(self, agent: SpecialistAgent) -> None:
        self.registry[agent.card.name] = agent

    def discover(self, name: str) -> AgentCard:
        return self.registry[name].card

    def delegate(self, name: str, skill: str, payload: dict) -> Task:
        return self.registry[name].send(skill, payload)


class SupportAgent:
    """委托方：只有 A2A 信封，没有 BILLS 表。"""

    def __init__(self, orch: Orchestrator):
        self.orch = orch

    def handle(self, user_text: str) -> str:
        bill_id = "B-1001" if "1001" in user_text else "B-1002"
        card = self.orch.discover("billing-agent")
        skill_ids = [s["id"] for s in card.skills]
        assert "explain_charge" in skill_ids
        task = self.orch.delegate("billing-agent", "explain_charge", {"bill_id": bill_id})
        # 生产里这里是 SSE / 轮询
        task = self.orch.registry["billing-agent"].get(task.id)
        if task.state != "completed":
            return f"委托失败: {task.error}"
        return f"[客服转述] {task.artifact['summary']}"


if __name__ == "__main__":
    orch = Orchestrator()
    orch.register(SpecialistAgent())
    support = SupportAgent(orch)

    print("=== Agent Card ===")
    card = orch.discover("billing-agent")
    print(f"{card.name} @ {card.url}")
    print(f"skills: {[s['id'] for s in card.skills]}")

    print("\n=== 用户: 为什么扣了 1001 这笔？ ===")
    print(support.handle("为什么扣了 1001 这笔？"))

    print("\n=== 隔离检查：客服侧看不到 BILLS ===")
    print("SupportAgent 属性:", [k for k in support.__dict__])
    print("账务内部表只在 SpecialistAgent 模块常量中，不在 Artifact 的 SQL 层。")
