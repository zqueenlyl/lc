"""Computer Use 最小循环（无真实键鼠、无视觉模型）

字符网格桌面：
  [搜索框] [提交]
  结果: ...

策略层用规则模拟多模态模型：根据画面文本决定 click / type / done。

运行：
    python3 mvp.py
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Desktop:
    query: str = ""
    focused: str = "search"
    result: str = ""
    submitted: bool = False

    def screenshot(self) -> str:
        box = self.query if self.query else "(empty)"
        focus = "*" if self.focused == "search" else " "
        btn = "*" if self.focused == "submit" else " "
        return (
            f"+--------------------------+\n"
            f"| [{focus}] search: {box:<12} |\n"
            f"| [{btn}] [提交]              |\n"
            f"| result: {self.result:<16} |\n"
            f"+--------------------------+"
        )

    def click(self, target: str) -> None:
        if target not in {"search", "submit"}:
            raise ValueError(target)
        self.focused = target
        if target == "submit":
            self.submitted = True
            self.result = f"hits for '{self.query}'" if self.query else "empty query"

    def type_text(self, text: str) -> None:
        if self.focused != "search":
            return
        self.query += text

    def key(self, name: str) -> None:
        if name == "enter":
            self.click("submit")


@dataclass
class Action:
    name: str
    arg: str = ""


@dataclass
class ComputerAgent:
    desktop: Desktop
    goal: str
    max_steps: int = 8
    log: list[str] = field(default_factory=list)

    def perceive(self) -> str:
        return self.desktop.screenshot()

    def decide(self, frame: str) -> Action:
        """真实系统把截图交给多模态模型；这里用可解释规则。"""
        if self.goal.lower() in self.desktop.result.lower() or (
            self.desktop.submitted and self.desktop.query
        ):
            return Action("done")
        if not self.desktop.query:
            if "search:" in frame and "[*]" not in frame.split("search:")[0][-4:]:
                return Action("click", "search")
            return Action("type", self.goal)
        if not self.desktop.submitted:
            return Action("click", "submit")
        return Action("done")

    def act(self, action: Action) -> None:
        if action.name == "click":
            self.desktop.click(action.arg)
        elif action.name == "type":
            self.desktop.type_text(action.arg)
        elif action.name == "key":
            self.desktop.key(action.arg)
        elif action.name == "done":
            return
        else:
            raise ValueError(action)

    def run(self) -> bool:
        for step in range(1, self.max_steps + 1):
            frame = self.perceive()
            action = self.decide(frame)
            self.log.append(f"step {step}: {action.name} {action.arg}".rstrip())
            print(f"\n--- {self.log[-1]} ---\n{frame}")
            if action.name == "done":
                return self.goal.lower() in self.desktop.result.lower() or bool(
                    self.desktop.submitted and self.desktop.query
                )
            self.act(action)
        return False


if __name__ == "__main__":
    desk = Desktop()
    agent = ComputerAgent(desk, goal="langgraph")
    ok = agent.run()
    print("\n=== 完成 ===" if ok else "\n=== 失败：步数用尽 ===")
    print("动作轨迹:", " → ".join(agent.log))
    print("最终结果:", desk.result)
