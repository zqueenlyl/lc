"""离线 eval：用例 + 程序裁判（复用 agent-skills 的契约思想）

运行：
    python3 mvp.py
"""

from __future__ import annotations

from dataclasses import dataclass
import importlib.util
import sys
from pathlib import Path

# 按路径加载 agent-skills/mvp.py（先注册 sys.modules，兼容 3.9 dataclass）
_skills = Path(__file__).resolve().parents[1] / "agent-skills" / "mvp.py"
_spec = importlib.util.spec_from_file_location("agent_skills_mvp", _skills)
_mod = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
sys.modules["agent_skills_mvp"] = _mod
_spec.loader.exec_module(_mod)
handle = _mod.handle


@dataclass
class Case:
    id: str
    priority: str
    utterance: str
    context: dict
    expect_status: str
    expect_skill: str | None = None
    ask_contains: str | None = None


CASES = [
    Case("refund-missing", "P0", "帮我退款", {}, "blocked", "refund", "缺字段"),
    Case("refund-ok", "P0", "帮我退款", {"order_id": "O-88", "amount": 59}, "ok", "refund"),
    Case("release-red", "P0", "今晚发布吧", {"tests_passed": False, "changelog": "x"}, "blocked", "release"),
    Case("chitchat", "P1", "今天天气如何", {}, "no_skill"),
]


def judge(case: Case, result: dict) -> list[str]:
    errs = []
    if result.get("status") != case.expect_status:
        errs.append(f"status {result.get('status')} != {case.expect_status}")
    if case.expect_skill and result.get("skill") != case.expect_skill:
        errs.append(f"skill {result.get('skill')} != {case.expect_skill}")
    if case.ask_contains and case.ask_contains not in str(result.get("ask_human", "")):
        errs.append(f"ask_human 未包含 {case.ask_contains!r}")
    return errs


def run() -> int:
    stats = {"P0": [0, 0], "P1": [0, 0]}  # pass, total
    print("=== eval ===")
    for case in CASES:
        result = handle(case.utterance, case.context)
        errs = judge(case, result)
        stats[case.priority][1] += 1
        if not errs:
            stats[case.priority][0] += 1
            print(f"  PASS {case.priority} {case.id}")
        else:
            print(f"  FAIL {case.priority} {case.id}: {errs}")
    print("\n=== 汇总 ===")
    gate_fail = False
    for p, (ok, n) in stats.items():
        rate = ok / n if n else 1.0
        print(f"  {p} {ok}/{n} = {rate:.0%}")
        if p == "P0" and ok < n:
            gate_fail = True
    if gate_fail:
        print("门禁：P0 未全过，阻断发布")
        return 1
    print("门禁：P0 全过")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
