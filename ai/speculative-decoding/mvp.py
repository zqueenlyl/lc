"""投机解码玩具：词表上的概率校验（无神经网络）

目标分布 P，草稿 Q。草稿一次提出 k 个 token，目标从左到右接受。

运行：
    python3 mvp.py
"""

from __future__ import annotations

from dataclasses import dataclass
import random


VOCAB = ["我", "爱", "吃", "苹果", "香蕉", "和", "。"]

# 目标：更偏好「我爱吃苹果。」
P = {
    "": {"我": 0.9, "爱": 0.05, "吃": 0.05},
    "我": {"爱": 0.85, "吃": 0.1, "。": 0.05},
    "我爱": {"吃": 0.8, "苹果": 0.1, "。": 0.1},
    "我爱吃": {"苹果": 0.7, "香蕉": 0.2, "。": 0.1},
    "我爱吃苹果": {"。": 0.9, "和": 0.1},
}

# 草稿：接近但会在「苹果/香蕉」处分歧
Q = {
    "": {"我": 0.8, "爱": 0.1, "吃": 0.1},
    "我": {"爱": 0.8, "吃": 0.15, "。": 0.05},
    "我爱": {"吃": 0.75, "。": 0.25},
    "我爱吃": {"香蕉": 0.6, "苹果": 0.3, "。": 0.1},
    "我爱吃苹果": {"。": 0.85, "和": 0.15},
}


def argmax(dist: dict[str, float]) -> str:
    return max(dist, key=dist.get)


def dist_for(table: dict, prefix: str) -> dict[str, float]:
    if prefix in table:
        return table[prefix]
    return {w: 1.0 / len(VOCAB) for w in VOCAB}


@dataclass
class Stats:
    target_fwds: int = 0
    draft_fwds: int = 0
    accepted: int = 0


def decode_speculative(k: int = 3, greedy: bool = True) -> tuple[str, Stats]:
    rng = random.Random(0)
    prefix = ""
    stats = Stats()
    while not prefix.endswith("。"):
        # 草稿连续猜 k 个
        draft_tokens = []
        tmp = prefix
        for _ in range(k):
            stats.draft_fwds += 1
            qd = dist_for(Q, tmp)
            tok = argmax(qd) if greedy else rng.choices(list(qd), list(qd.values()))[0]
            draft_tokens.append(tok)
            tmp += tok
            if tok == "。":
                break
        # 目标一次「并行」校验这 k 个位置（计 1 次前向）
        stats.target_fwds += 1
        accepted_here = 0
        cur = prefix
        for tok in draft_tokens:
            pd = dist_for(P, cur)
            target_tok = argmax(pd) if greedy else tok  # greedy MVP：必须等于目标 argmax
            if tok == target_tok:
                cur += tok
                accepted_here += 1
                if tok == "。":
                    break
            else:
                # 分歧：用目标 token 补一个
                cur += target_tok
                break
        else:
            # 全部接受时，再让目标补 1 个（标准算法变体之一）
            if not cur.endswith("。"):
                stats.target_fwds += 1
                cur += argmax(dist_for(P, cur))
        stats.accepted += accepted_here
        prefix = cur
    return prefix, stats


def decode_naive() -> tuple[str, int]:
    prefix = ""
    fwds = 0
    while not prefix.endswith("。"):
        fwds += 1
        prefix += argmax(dist_for(P, prefix))
    return prefix, fwds


if __name__ == "__main__":
    naive, n_fwd = decode_naive()
    spec, st = decode_speculative(k=3)
    print("朴素目标: ", naive, f"  目标前向 {n_fwd}")
    print("投机解码: ", spec, f"  目标前向 {st.target_fwds}  草稿前向 {st.draft_fwds}  接受 {st.accepted}")
    print(f"加速比（只比目标前向）: {n_fwd / st.target_fwds:.2f}x")
    print("文本应与朴素一致（greedy）。")
    assert naive == spec
