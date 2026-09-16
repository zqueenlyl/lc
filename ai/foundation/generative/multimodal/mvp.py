"""多模态消息与跨模态引用（无视觉模型）

会话里混排文本、图像元数据、音频转写。回答必须引用 source_id，
模拟「请看第二张图红色列」这类产品形态。

运行：
    python3 mvp.py
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Part:
    kind: str  # text | image | audio
    text: str
    source_id: str = ""
    extra: dict | None = None


@dataclass
class Message:
    role: str
    parts: list[Part]


def flatten_index(messages: list[Message]) -> dict[str, Part]:
    idx = {}
    for msg in messages:
        for p in msg.parts:
            if p.source_id:
                idx[p.source_id] = p
    return idx


def answer(question: str, messages: list[Message]) -> str:
    idx = flatten_index(messages)
    q = question.lower()
    # 引用解析：图2 / img2 / 录音
    if "图2" in question or "img2" in q:
        part = idx.get("img2")
        assert part and part.extra
        col = part.extra.get("red_column", "?")
        return f"根据 {part.source_id}（{part.text}）：红色列表示「{col}」。"
    if "录音" in question or "audio" in q:
        part = idx.get("aud1")
        return f"根据 {part.source_id}：{part.text}"
    texts = [p.text for m in messages for p in m.parts if p.kind == "text"]
    return "仅文本上下文：" + " / ".join(texts)


if __name__ == "__main__":
    thread = [
        Message(
            "user",
            [
                Part("text", "对比这两张表和一段会议录音。"),
                Part("image", "Q1 收入表", "img1", {"red_column": "同比"}),
                Part("image", "Q2 收入表", "img2", {"red_column": "毛利率"}),
                Part("audio", "老板强调毛利率优先于收入规模。", "aud1"),
            ],
        )
    ]
    print("=== 会话模态 ===")
    for p in thread[0].parts:
        print(f"  {p.kind:5} {p.source_id or '-':5} {p.text}")

    for q in ("图2 红色列是什么？", "录音里老板怎么说？", "总结一下"):
        print(f"\nQ: {q}")
        print("A:", answer(q, thread))
