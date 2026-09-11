"""Test-time scaling 最小演示（无 LLM）

任务：在约束下找出唯一整数 n。
策略：串行提出假设 → 可执行 verifier → 失败则换假设（并行采样的穷人版）。
对比：budget=1 vs budget=4 的成功率。

运行：
    python3 mvp.py
"""

from __future__ import annotations

from dataclasses import dataclass


CONSTRAINTS = (
    lambda n: n % 2 == 1,
    lambda n: n > 20,
    lambda n: n < 40,
    lambda n: n % 7 == 3,
)


def verify(n: int) -> tuple[bool, str]:
    for i, pred in enumerate(CONSTRAINTS, 1):
        if not pred(n):
            return False, f"违反约束 {i}"
    return True, "ok"


# 故意把正确答案放在靠后的位置，模拟「需要多想几次」
GUESSES = [11, 21, 27, 35, 31, 17, 24]


@dataclass
class Trace:
    guess: int
    ok: bool
    reason: str


def solve(budget: int) -> tuple[int | None, list[Trace]]:
    traces = []
    for guess in GUESSES[:budget]:
        ok, reason = verify(guess)
        traces.append(Trace(guess, ok, reason))
        if ok:
            return guess, traces
    return None, traces


def report(budget: int) -> None:
    ans, traces = solve(budget)
    print(f"\n=== budget={budget}（最多想 {budget} 次）===")
    for t in traces:
        mark = "✓" if t.ok else "✗"
        print(f"  think: 试 n={t.guess} → {mark} {t.reason}")
    print("  最终:", ans if ans is not None else "放弃（预算用尽）")


if __name__ == "__main__":
    print("目标：奇数、20<n<40、n≡3 (mod 7)  →  31")
    report(1)
    report(2)
    report(5)
    print("\n观察：同一套校验器，多给几次尝试就能从失败走到成功。")
    print("真实推理模型把「换一种解法」学进了生成过程，校验器可以是代码/单测/规则。")
