"""JSON Schema 校验 + 修复循环（无 LLM，无 jsonschema 库）

演示：模型草稿不合法 → 错误信息回灌 → 再生成。

运行：
    python3 mvp.py
"""

from __future__ import annotations

import json
from typing import Any


SCHEMA = {
    "type": "object",
    "required": ["order_id", "amount", "reason"],
    "properties": {
        "order_id": {"type": "string", "minLength": 3},
        "amount": {"type": "number", "exclusiveMinimum": 0},
        "reason": {"type": "string", "enum": ["quality", "delay", "other"]},
    },
}


def validate(obj: Any, schema: dict = SCHEMA) -> list[str]:
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for key in schema["required"]:
        if key not in obj:
            errs.append(f"missing {key}")
    props = schema["properties"]
    if "order_id" in obj and not isinstance(obj["order_id"], str):
        errs.append("order_id must be string")
    elif "order_id" in obj and len(obj["order_id"]) < props["order_id"]["minLength"]:
        errs.append("order_id too short")
    if "amount" in obj and not isinstance(obj["amount"], (int, float)):
        errs.append("amount must be number")
    elif "amount" in obj and obj["amount"] <= props["amount"]["exclusiveMinimum"]:
        errs.append("amount must be > 0")
    if "reason" in obj and obj["reason"] not in props["reason"]["enum"]:
        errs.append(f"reason must be one of {props['reason']['enum']}")
    extra = set(obj) - set(props)
    if extra:
        errs.append(f"unknown keys {sorted(extra)}")
    return errs


# 模拟「模型」：第 1 次缺字段，第 2 次类型错，第 3 次正确
DRAFTS = [
    {"order_id": "O-1", "reason": "delay"},
    {"order_id": "O-1", "amount": "12", "reason": "delay"},
    {"order_id": "O-188", "amount": 12.5, "reason": "delay"},
]


def generate(errors: list[str], attempt: int) -> dict:
    print(f"  generate#{attempt}  看到的错误: {errors or '∅'}")
    return DRAFTS[min(attempt - 1, len(DRAFTS) - 1)]


def complete(max_attempts: int = 3) -> dict | None:
    errors: list[str] = []
    for i in range(1, max_attempts + 1):
        draft = generate(errors, i)
        errors = validate(draft)
        print(f"  draft={draft}  valid={not errors}")
        if not errors:
            return draft
    return None


if __name__ == "__main__":
    print("schema required:", SCHEMA["required"])
    result = complete()
    print("\n最终:", json.dumps(result, ensure_ascii=False) if result else "放弃")
