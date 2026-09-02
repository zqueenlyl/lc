"""评测对照：学校考试（LLM）vs 上机考试（Agent = 模型 × Harness）

1) llm_exam   — prompt vs 参考答案
2) skill_gate — 复用 agent-skills 契约（轻量 Agent）
3) lab_exam   — 受控仓库 + 工具轨迹 + 验收测试

运行：
    python3 mvp.py
"""

from __future__ import annotations

from dataclasses import dataclass, field
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


# --- 1. 学校考试：试卷 + 参考答案 + 阅卷 ---

@dataclass
class ExamItem:
    id: str
    prompt: str
    reference: str


LLM_PAPER = [
    ExamItem("capitals", "法国首都？", "巴黎"),
    ExamItem("arith", "2+2", "4"),
]


def llm_answer(prompt: str) -> str:
    """假装模型答卷；真实系统在这里调 API。"""
    canned = {"法国首都？": "巴黎", "2+2": "4"}
    return canned.get(prompt, "")


def grade_exam(item: ExamItem, answer: str) -> bool:
    return answer.strip() == item.reference.strip()


# --- 2. 技能门禁（原有） ---

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


# --- 3. 上机考试：环境 + Harness + 产物 + 轨迹 ---

BUGGY = "def tax(n):\n    return n * 3 // 100\n"


@dataclass
class LabEnv:
    files: dict[str, str]
    trajectory: list[str] = field(default_factory=list)

    def edit(self, path: str, old: str, new: str) -> str:
        src = self.files[path]
        if old not in src:
            msg = "edit_miss"
        else:
            self.files[path] = src.replace(old, new, 1)
            msg = "edit_ok"
        self.trajectory.append(f"edit:{path}:{msg}")
        return msg

    def accept(self) -> bool:
        ns: dict = {}
        exec(self.files["shop.py"], ns)  # noqa: S102 — 受控夹具
        try:
            return ns["tax"](100) == 13
        except Exception:
            return False


def lab_solve(env: LabEnv) -> None:
    """规则策略扮演「模型 × 最小 Harness」。"""
    env.edit("shop.py", "n * 3 // 100", "n * 13 // 100")


def lab_judge(env: LabEnv) -> list[str]:
    errs = []
    if not any(t.startswith("edit:") for t in env.trajectory):
        errs.append("轨迹里没有工具操作")
    if not env.accept():
        errs.append("验收测试未通过")
    return errs


def run() -> int:
    print("=== 学校考试（LLM：试卷 / 参考答案）===")
    exam_fail = False
    for item in LLM_PAPER:
        ans = llm_answer(item.prompt)
        ok = grade_exam(item, ans)
        print(f"  {'PASS' if ok else 'FAIL'} {item.id}: {item.prompt!r} -> {ans!r}")
        exam_fail = exam_fail or not ok

    print("\n=== 技能门禁（轻量 Agent 契约）===")
    stats = {"P0": [0, 0], "P1": [0, 0]}
    for case in CASES:
        result = handle(case.utterance, case.context)
        errs = judge(case, result)
        stats[case.priority][1] += 1
        if not errs:
            stats[case.priority][0] += 1
            print(f"  PASS {case.priority} {case.id}")
        else:
            print(f"  FAIL {case.priority} {case.id}: {errs}")

    print("\n=== 上机考试（Task+Env × Model×Harness × 轨迹+验收）===")
    env = LabEnv(files={"shop.py": BUGGY})
    lab_solve(env)
    lab_errs = lab_judge(env)
    if lab_errs:
        print(f"  FAIL lab-tax: {lab_errs}  trajectory={env.trajectory}")
    else:
        print(f"  PASS lab-tax  trajectory={env.trajectory}")

    print("\n=== 汇总 ===")
    gate_fail = exam_fail or bool(lab_errs)
    for p, (ok, n) in stats.items():
        rate = ok / n if n else 1.0
        print(f"  {p} {ok}/{n} = {rate:.0%}")
        if p == "P0" and ok < n:
            gate_fail = True
    if gate_fail:
        print("门禁：未全过，阻断发布")
        return 1
    print("门禁：学校考试 + P0 + 上机验收全过")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
