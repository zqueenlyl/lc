"""上下文预算编译器（按 token 近似 = 字符数/2）

槽位：system / skill / memory / rag / dialog
溢出策略：dialog 摘要、rag 丢分低的块，system 不砍。

运行：
    python3 mvp.py
"""

from __future__ import annotations

from dataclasses import dataclass, field


def toks(s: str) -> int:
    return max(1, len(s) // 2)


@dataclass
class Chunk:
    slot: str
    text: str
    score: float = 1.0
    sticky: bool = False


@dataclass
class Window:
    budget: int
    parts: list[Chunk] = field(default_factory=list)

    def used(self) -> int:
        return sum(toks(p.text) for p in self.parts)

    def render(self) -> str:
        return "\n---\n".join(f"[{p.slot}] {p.text}" for p in self.parts)


def compress(chunks: list[Chunk], budget: int) -> list[Chunk]:
    # 先放 sticky，再按 score 贪心
    sticky = [c for c in chunks if c.sticky]
    flexible = sorted((c for c in chunks if not c.sticky), key=lambda c: c.score, reverse=True)
    out = list(sticky)
    used = sum(toks(c.text) for c in out)
    for c in flexible:
        t = toks(c.text)
        if used + t <= budget:
            out.append(c)
            used += t
        elif c.slot == "dialog":
            brief = Chunk("dialog", "摘要：" + c.text[:40] + "…", c.score)
            if used + toks(brief.text) <= budget:
                out.append(brief)
                used += toks(brief.text)
    return out


def compile_window(sources: list[Chunk], budget: int) -> Window:
    return Window(budget, compress(sources, budget))


if __name__ == "__main__":
    sources = [
        Chunk("system", "你是客服。禁止承诺未审核退款。" + "（红线）" * 4, sticky=True),
        Chunk("skill", "退款SOP：核单→核金额→提交。缺字段就问人。", 0.9),
        Chunk("memory", "用户是企业客户，偏好简短答复。", 0.7),
        Chunk("rag", "退款政策：7 天无理由，已激活码除外。", 0.95),
        Chunk("rag", "去年双十一活动文案……" + "啊" * 80, 0.2),
        Chunk("dialog", "用户长篇抱怨物流和发票，中间夹杂家庭琐事。" + "啦" * 60, 0.5),
    ]
    raw = sum(toks(c.text) for c in sources)
    print(f"原始合计 ≈ {raw} tokens")
    for b in (80, 160, 400):
        w = compile_window(sources, b)
        print(f"\n=== budget={b}  used={w.used()} ===")
        for p in w.parts:
            print(f"  {p.slot:7} {toks(p.text):3}t  {p.text[:48]}")
