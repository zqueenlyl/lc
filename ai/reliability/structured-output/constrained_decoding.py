"""约束解码最小实现：从正则到每一步的 token mask（纯标准库，零依赖）

回答一个问题：约束解码在解码循环的每一步到底做了什么，
凭什么能把「语法合法率」抬到 ~100%？

四个演示：
  Part 1  粒度错位：约束建在「字符」上，模型吐的是「token」——一个 token 可跨多个状态
  Part 2  闭包判定：为每个状态算出「哪些 token 整条字符路径都走得通」，这就是 mask
  Part 3  mask 生效位置：softmax 之前把非法 token 的 logits 置 -inf，概率恰好为 0
  Part 4  两个经典坑：屏蔽 EOS 会合法地一直写；某状态允许集合为空时必须报错

运行：
    python3 constrained_decoding.py

对应长文：[约束解码原理.md](./约束解码原理.md)
  —— §二 五步流程、§三.1 粒度错位与闭包、§三.2 mask 开销、§6.5 屏蔽 EOS 的两个坑。
"""

from __future__ import annotations

import math

EOS = "</s>"
DIGITS = set("0123456789")
DEAD = -1


class DigitDFA:
    """数字串的字符级 DFA —— 约束解码里「文法」的本体。

    exact=True  → 恰好 n 位数字，即正则 [0-9]{n}
    exact=False → 至少 n 位数字、无上限，即正则 [0-9]{n,}

    状态 = 已吃掉的数字个数；吃到非法字符或超出上限即进入 DEAD。
    """

    def __init__(self, n: int, exact: bool = True):
        self.n = n
        self.exact = exact

    def step(self, state: int, ch: str) -> int:
        """吃一个字符，返回新状态；走不通返回 DEAD。"""
        if state == DEAD:
            return DEAD
        if ch not in DIGITS:
            return DEAD
        nxt = state + 1
        if self.exact and nxt > self.n:
            return DEAD
        return nxt

    def accepts(self, state: int) -> bool:
        """当前状态是否「可以到此为止」。"""
        if state == DEAD:
            return False
        return state == self.n if self.exact else state >= self.n


def run_token(dfa: DigitDFA, state: int, token: str) -> int:
    """让整个 token 从 state 出发走一遍，返回落点状态；中途死掉返回 DEAD。

    这就是「闭包」的最小形式：只有 token 的**整条字符路径**都走得通，它才算合法。
    """
    for ch in token:
        state = dfa.step(state, ch)
        if state == DEAD:
            return DEAD
    return state


def allowed_tokens(
    dfa: DigitDFA, vocab: list[str], state: int, eos_allowed: bool | None = None
) -> dict[str, int]:
    """当前状态的合法 token → 落点状态。空 dict 表示「无路可走」。

    EOS 不走字符自动机，由引擎单独处理：默认「接受态才放行」（见 Part 4）。
    """
    if eos_allowed is None:
        eos_allowed = dfa.accepts(state)
    allowed: dict[str, int] = {}
    for tok in vocab:
        if tok == EOS:
            if eos_allowed:
                allowed[tok] = state
            continue
        nxt = run_token(dfa, state, tok)
        if nxt != DEAD:
            allowed[tok] = nxt
    return allowed


def softmax(logits: dict[str, float]) -> dict[str, float]:
    mx = max(logits.values())
    exps = {k: math.exp(v - mx) for k, v in logits.items()}
    z = sum(exps.values())
    return {k: v / z for k, v in exps.items()}


def apply_mask(
    logits: dict[str, float], allowed: dict[str, int]
) -> dict[str, float]:
    """约束解码的落点：非法 token 的 logits 直接置 -inf（位置在 softmax 之前）。"""
    return {k: (v if k in allowed else float("-inf")) for k, v in logits.items()}


def greedy(masked: dict[str, float], order: list[str]) -> str | None:
    """从 mask 后的 logits 里贪心取最高分；全为 -inf 时返回 None。"""
    best: str | None = None
    best_v = float("-inf")
    for tok in order:
        v = masked.get(tok, float("-inf"))
        if v > best_v:
            best, best_v = tok, v
    return None if best_v == float("-inf") else best


# ---------------------------------------------------------------------------
# 一个 tiny 词表。注意里面故意放了「跨多字符」的 token（123 / 12 / 99 / 456）
# 和干扰项（abc / x / 9a）—— 它们正是 Part 1 要展示的粒度错位来源。
# ---------------------------------------------------------------------------
VOCAB = ["abc", "x", "9a", "1", "12", "123", "456", "99", EOS]

# 模拟模型的原始倾向：越靠前越「想说」，与格式是否合法无关。
PREFERENCE = ["abc", "x", "9a", "123", "12", "99", "456", "1", EOS]


def raw_logits() -> dict[str, float]:
    """按 PREFERENCE 造一组 logits：最想吐的 5.0，依次递减 0.5。"""
    return {tok: 5.0 - 0.5 * i for i, tok in enumerate(PREFERENCE)}


def part1() -> None:
    print("=" * 70)
    print("Part 1 · 粒度错位：约束建在「字符」上，模型吐的是「token」")
    print("=" * 70)
    dfa = DigitDFA(3)  # 文法 = [0-9]{3}
    print("文法 = [0-9]{3}   →   状态 0 / 1 / 2 是过程态，状态 3 可结束")
    print(f"词表 = {VOCAB}")
    print()
    for tok in ["1", "12", "123", "9a", "abc"]:
        end = run_token(dfa, 0, tok)
        if end == DEAD:
            print(f"  {tok!r:>8}  →  DEAD（整条字符路径走不通 → 非法）")
        else:
            print(
                f"  {tok!r:>8}  →  state {end}"
                f"（一步吃掉 {len(tok)} 个字符、跨 {len(tok)} 个状态）"
            )
    print(f"  {EOS!r:>8}  →  不走字符自动机，由引擎单独放行 / 屏蔽（见 Part 4）")
    print()
    print("  → 所以不能「每步只看下一个字符」：token '12' 一步就从 state 0 到了 state 2。")
    print("  → 判定必须是「这个 token 的整条字符路径都走得通」——这就是闭包。")


def part2() -> None:
    print()
    print("=" * 70)
    print("Part 2 · 闭包：为每个状态预先算出 mask（这一步允许哪些 token）")
    print("=" * 70)
    dfa = DigitDFA(3)
    for state in [0, 1, 2, 3]:
        allowed = allowed_tokens(dfa, VOCAB, state)
        items = "、".join(f"{t}→{s}" for t, s in allowed.items())
        print(f"  state {state}（已吃 {state} 位）：{items or '（空集，引擎须报错）'}")
    print()
    print("  同一个 token '12'：")
    print(f"    state 0 合法（落点 state {run_token(dfa, 0, '12')}）")
    print(f"    state 2 非法（会超出 3 位，落点 DEAD = {run_token(dfa, 2, '12')}）")
    print("  → 合法性只取决于「当前状态」，与语义无关。")
    print("  → state 3 已满 3 位：数字 token 全部非法，只剩 EOS 可走。")


def part2b() -> None:
    print()
    print("=" * 70)
    print("Part 2b · 分词歧义：多条 token 路径到达同一状态 → 取并集")
    print("=" * 70)
    dfa = DigitDFA(3)
    for path in [["12"], ["1", "2"], ["9", "9"]]:
        state = 0
        for tok in path:
            state = run_token(dfa, state, tok)
        print(f"  切分 {(' + '.join(path)):<12} → 落点 state {state}")
    print()
    print("  '12' 一步与 '1'+'2' 两步是同一段字符的两种切法，落点相同")
    print("  → 多条路径汇到同一状态，取并集即可，结果不受切分影响。")
    print("  （DFA 下多重路径只会汇流；换 JSON 这类可嵌套文法要用下推自动机 PDA，")
    print("    才需要同时维护多条栈 —— 见 约束解码原理.md §三.1 与 §四。）")


def part3() -> None:
    print()
    print("=" * 70)
    print("Part 3 · mask 生效位置：softmax 之前，非法概率恰好为 0")
    print("=" * 70)
    dfa = DigitDFA(3)
    logits = raw_logits()
    allowed = allowed_tokens(dfa, VOCAB, 0)
    before = softmax(logits)
    masked = apply_mask(logits, allowed)
    after = softmax(masked)

    print(f"  站在 state 0，模型很想吐 'abc'（原始 logits {logits['abc']:.1f}，全词表最高）")
    print()
    print("  token      原始logits  mask后logits   原始概率   mask后概率")
    for tok in PREFERENCE:
        m = masked[tok]
        mtxt = "    -inf" if m == float("-inf") else f"{m:8.1f}"
        print(
            f"  {tok:<10} {logits[tok]:>9.1f}  {mtxt:>12}"
            f"   {before[tok]:>8.4f}   {after[tok]:>9.4f}"
        )
    print()
    print(f"  'abc' 的采样概率：{before['abc']:.4f} → {after['abc']:.4f}")
    print("  → 不是「变小」，是**恰好为 0**。约束不放宽模型的偏好，")
    print("    只是把非法项从候选集里删掉 —— 它连犯错的机会都没有。")
    print()
    print("  顺序提醒：mask 必须在 softmax 之前、且在 top-k / top-p 之前；")
    print("  否则截断可能先把合法 token 切掉、或把非法 token 留在候选集里。")
    print("  （数学上 -inf / T 仍是 -inf，mask 与 temperature 可交换；但顺序错了就是 bug。）")


def part4() -> None:
    print()
    print("=" * 70)
    print("Part 4 · 两个经典坑")
    print("=" * 70)

    print()
    print("  4a) 文法 [0-9]+（不限长）且把 EOS 也 mask 掉")
    dfa = DigitDFA(1, exact=False)
    state, out = 0, []
    for step in range(1, 9):
        allowed = allowed_tokens(dfa, VOCAB, state, eos_allowed=False)
        tok = greedy(apply_mask(raw_logits(), allowed), PREFERENCE)
        if tok is None:
            print(f"      第 {step} 步：已无合法 token")
            break
        out.append(tok)
        state = allowed[tok]
        print(f"      第 {step} 步：{len(allowed)} 个合法 token → 选中 {tok!r} → state {state}")
    print(f"      已输出 {len(out)} 步：{''.join(out)}")
    print("      → 每一步都合法、全程语法正确，但**永不停止**，只能靠 max_tokens 截断。")
    print("      → 所以 schema 要在结构上「可终结」：限长、限项，别让模型合法地话痨。")

    print()
    print("  4b) 文法 [0-9]{3} 的接受态，同样把 EOS 屏蔽掉")
    dfa = DigitDFA(3)
    allowed = allowed_tokens(dfa, VOCAB, 3, eos_allowed=False)
    print(f"      state 3 的合法 token 集合 = {allowed}")
    if not allowed:
        print("      → 空集！mask 后 logits 全为 -inf，softmax 无定义。")
        print("      → 引擎此时必须**报错或明确退化**，绝不能静默产出一个非法 token。")


def main() -> None:
    print()
    print("约束解码最小实现 · 解码循环每一步都在做的事：把非法 token 从候选里删掉")
    part1()
    part2()
    part2b()
    part3()
    part4()
    print()
    print("=" * 70)
    print("一句话：约束解码不改模型、不改权重、不改 prompt，")
    print("只在 softmax 之前加一个 mask —— 变的只是「这一步允许它说哪些词」。")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
