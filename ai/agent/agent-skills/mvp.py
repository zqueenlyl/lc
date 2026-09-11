"""Agent Skills：按需加载 SOP（无 LLM 依赖）

两份技能：
  refund   — 退款必须先查订单、再确认金额、禁止编造单号
  release  — 发布必须测试通过 + 变更记录，缺一不可

运行：
    python3 mvp.py
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Skill:
    name: str
    trigger: tuple[str, ...]
    description: str
    required_fields: tuple[str, ...]
    steps: tuple[str, ...]
    forbidden: tuple[str, ...]


SKILLS = [
    Skill(
        name="refund",
        trigger=("退款", "refund", "退钱"),
        description="客服退款：先核单再退，禁止虚构订单号。",
        required_fields=("order_id", "amount"),
        steps=("核验订单存在", "核对金额", "提交退款单", "回写工单"),
        forbidden=("编造订单号", "未核验直接退款"),
    ),
    Skill(
        name="release",
        trigger=("发布", "上线", "release"),
        description="发布检查：测试与变更记录必须齐。",
        required_fields=("tests_passed", "changelog"),
        steps=("确认测试绿", "确认 changelog", "打 tag", "通知值班"),
        forbidden=("测试失败仍发布",),
    ),
]


def route(utterance: str) -> Skill | None:
    text = utterance.lower()
    for skill in SKILLS:
        if any(t.lower() in text for t in skill.trigger):
            return skill
    return None


def execute(skill: Skill, context: dict) -> dict:
    missing = [f for f in skill.required_fields if f not in context]
    if missing:
        return {
            "status": "blocked",
            "skill": skill.name,
            "ask_human": f"缺字段 {missing}，按技能硬规则停止，不猜测。",
            "forbidden": skill.forbidden,
        }
    if skill.name == "release" and context.get("tests_passed") is not True:
        return {
            "status": "blocked",
            "skill": skill.name,
            "ask_human": "测试未通过，命中禁止事项：测试失败仍发布。",
        }
    return {
        "status": "ok",
        "skill": skill.name,
        "did": list(skill.steps),
        "used_context": {k: context[k] for k in skill.required_fields},
    }


def handle(utterance: str, context: dict) -> dict:
    skill = route(utterance)
    if skill is None:
        return {"status": "no_skill", "note": "未命中技能，走通用对话。"}
    print(f"加载技能 [{skill.name}] {skill.description}")
    print("步骤:", " → ".join(skill.steps))
    return execute(skill, context)


if __name__ == "__main__":
    cases = [
        ("帮我退款", {}),
        ("帮我退款", {"order_id": "O-88", "amount": 59}),
        ("今晚发布吧", {"tests_passed": False, "changelog": "fix login"}),
        ("今晚发布吧", {"tests_passed": True, "changelog": "fix login"}),
        ("今天天气如何", {}),
    ]
    for utter, ctx in cases:
        print(f"\n=== 用户: {utter} | ctx={ctx} ===")
        print(handle(utter, ctx))
