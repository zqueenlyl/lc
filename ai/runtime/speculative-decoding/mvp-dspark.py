"""DSpark 玩具：半自回归草稿 + 置信度调度验证（纯 Python 标准库，零依赖）

对照同目录 mvp.py（标准投机解码：草稿猜 k 个 → 目标一次校验 → 统计接受长度），
本文件把 DSpark 相对标准算法的两处改动各做成一个可跑的小实验：

  A. 顺序头（Markov，低秩转移偏置）
     并行骨干对每个位置独立给分布 → 拼起来会「多模态碰撞」（不同模式混搭）。
     顺序头只加一个依赖「前一个草稿 token」的偏置：
         p_k(v) = softmax( U_k(v) + B(x_(k-1), v) ),   B = W1 @ W2（秩 r）
     偏置是局部的 → 逐 token 概率仍然精确 → 拒绝采样与无损性不受影响。

  B. 置信度调度
     a_(r,j) = ∏_(i<=j) c_i（累积存活概率），Θ = τ · SPS(B)。
     按 a 降序全局贪心裁剪每请求的验证长度；再用一条锯齿状 SPS 曲线
     演示为什么生产上必须去掉 early-stopping。

两者都是词表上的概率表，不是神经网络：目的是把结构讲清楚，不是复现论文数字。
运行：
    python3 mvp-dspark.py
"""

from __future__ import annotations

import math


# ============================================================
# A. 顺序头：并行草稿 vs 半自回归草稿
# ============================================================

VOCAB = ["no", "of", "problem", "course"]

# 并行骨干对两个位置给出的基础 logits。
# 关键：位置 2 的输出只看 target 上下文，与位置 1 采到了什么无关
# —— 这正是「在全部可能前驱上边缘化」。
U1 = {"no": 0.0, "of": 0.0, "problem": -9.0, "course": -9.0}
U2 = {"no": -9.0, "of": -9.0, "problem": 0.0, "course": 0.0}

# target 模型的真实条件分布：no→problem、of→course，两种模式互斥。
P_T1 = {"no": 0.5, "of": 0.5, "problem": 0.0, "course": 0.0}
P_T2 = {
    "no": {"no": 0.0, "of": 0.0, "problem": 0.95, "course": 0.05},
    "of": {"no": 0.0, "of": 0.0, "problem": 0.05, "course": 0.95},
}

# 低秩转移偏置 B = W1 @ W2，秩 r = 2（论文默认 r = 256，这里缩到能一眼看完）。
# 约定：B(x_(k-1), ·) = W1[x_(k-1)] · W2 = W2 中对应 x_(k-1) 的那一行。
R = 2
W1 = {
    "no": [1.0, 0.0],
    "of": [0.0, 1.0],
}
W2 = [
    [0.0, 0.0, 1.0, -1.0],  # 前一个 token 是 no  → 抬高 problem、压低 course
    [0.0, 0.0, -1.0, 1.0],  # 前一个 token 是 of  → 抬高 course、压低 problem
]


def softmax(logits: dict[str, float]) -> dict[str, float]:
    m = max(logits.values())
    exps = {k: math.exp(v - m) for k, v in logits.items()}
    z = sum(exps.values())
    return {k: v / z for k, v in exps.items()}


def markov_bias(prev: str) -> dict[str, float]:
    """B(x_(k-1), ·)：一次嵌入查表 + 一次秩 r 的投影，复杂度与词表大小无关的常数级开销。"""
    emb = W1.get(prev, [0.0] * R)
    return {v: sum(emb[i] * W2[i][j] for i in range(R)) for j, v in enumerate(VOCAB)}


def accept_prob(p_draft: dict[str, float], p_target: dict[str, float]) -> float:
    """单步接受概率 = Σ_v min(p_d, p_t) = 1 − ½·‖p_d − p_t‖₁（Leviathan et al., 2023）。"""
    return sum(min(p_draft[v], p_target[v]) for v in VOCAB)


def demo_a() -> None:
    print("=" * 70)
    print("A. 并行草稿 vs 半自回归草稿（治「多模态碰撞」）")
    print("=" * 70)
    print("场景：位置 1 在 no / of 之间二选一；位置 2 必须是配对的那个（problem / course）。")
    print("      并行骨干给位置 2 的分布与位置 1 无关 —— 它把两种模式边缘化成了 0.5 : 0.5。\n")

    par = softmax(U2)
    shown = {k: round(v, 3) for k, v in par.items() if v > 0.01}
    print(f"位置 1 分布（两者相同）        = {{'no': 0.5, 'of': 0.5}}  接受率 1.000")
    print(f"位置 2 并行草稿 p_d            = {shown}")
    print("  ↑ 采出来约一半是 no course / of problem 这类跨模式组合。\n")

    tot_par = tot_mar = 0.0
    for prev in ("no", "of"):
        bias = markov_bias(prev)
        mar = softmax({v: U2[v] + bias[v] for v in VOCAB})
        a_par = accept_prob(par, P_T2[prev])
        a_mar = accept_prob(mar, P_T2[prev])
        tot_par += 0.5 * a_par
        tot_mar += 0.5 * a_mar
        print(f"前一 token = {prev!r}")
        print("  B(x_(k-1), ·) = W1[x_(k-1)]·W2 =", {k: round(bias[k], 2) for k in VOCAB})
        print(f"  并行      p_d            = {({k: round(par[k], 3) for k in VOCAB})}  接受率 {a_par:.3f}")
        print(f"  加顺序头  softmax(U+B)   = {({k: round(mar[k], 3) for k in VOCAB})}  接受率 {a_mar:.3f}")

    print(f"\n位置 2 的期望单步接受率：并行 {tot_par:.3f} → 半自回归 {tot_mar:.3f}"
          f"（+{(tot_mar / tot_par - 1) * 100:.0f}%）")
    print("注意偏置只给到 ±1.0，softmax 之后是「倾斜」而不是「锁死」——")
    print("它便宜（一次查表），而且没有破坏逐位置归一化，所以依旧能算出精确的逐 token 概率。")
    print("反过来，CRF 那种全局归一化 / CTC 那种对齐路径边缘化，都会让概率算不准 → 无法做拒绝采样。\n")
    assert tot_mar > tot_par, "顺序头应当提高接受率"


# ============================================================
# B. 置信度调度：验证多长才划算
# ============================================================

# 引擎步速曲线 SPS(B)：batch 大小 B（含全部待验证 token）下每秒能跑几步。
# 真实曲线由引擎初始化时剖分得到，本质是锯齿状阶梯（不是平滑单峰）；
# 下面的档位是示意数字，只为演示结构。
SPS_LIGHT = [(12, 900), (18, 820), (24, 560), (30, 700), (48, 420), (96, 260)]
SPS_HEAVY = [(3, 620), (6, 520), (9, 400), (15, 300), (24, 220), (48, 140)]


def sps(b: int, table: list[tuple[int, float]]) -> float:
    for cap, v in table:
        if b <= cap:
            return v
    return table[-1][1]


def survival(conf: list[float]) -> list[float]:
    """累积存活概率 a_j = ∏_(i<=j) c_i（链式法则）。"""
    out, acc = [], 1.0
    for c in conf:
        acc *= c
        out.append(acc)
    return out


def schedule(conf: dict[str, list[float]],
             table: list[tuple[int, float]],
             early_stop: bool) -> tuple[float, dict[str, int], int, float]:
    """硬件感知前缀调度（论文 Algorithm 1 的简化版）。

    返回 (Θ_best, 每请求选定的前缀长度 ℓ_r*, 该点的 batch 大小 B, 该点的期望接受数 τ)。
    early_stop=True  → 论文线上前的版本：Θ 不再增长就 break（保非预测性）
    early_stop=False → 生产改法：扫完整个候选池（靠异步调度当因果屏障）
    """
    cands: list[tuple[str, int, float]] = []
    for r, c in conf.items():
        a = survival(c)
        assert all(a[i] >= a[i + 1] for i in range(len(a) - 1)), "a_(r,j) 必须单调非增"
        cands += [(r, j + 1, a[j]) for j in range(len(a))]
    cands.sort(key=lambda t: -t[2])  # 全局按存活概率降序 —— 单调性保证块内前缀依赖

    lens = {r: 0 for r in conf}
    b = len(conf)          # 每个请求至少有一个 anchor token
    tau = float(len(conf))
    best = (tau * sps(b, table), dict(lens), b, tau)

    for r, j, a in cands:
        lens[r] = j
        b += 1
        tau += a
        theta = tau * sps(b, table)
        if theta > best[0]:
            best = (theta, dict(lens), b, tau)
        elif early_stop:
            break          # 只用「已处理的前缀」决策，保证 non-anticipating
    return best


def full_verify(conf: dict[str, list[float]],
                table: list[tuple[int, float]]) -> tuple[float, int, float]:
    """固定长度验证（= 全部 γ 位都验）：调度器要打败的基线。"""
    b = sum(1 + len(c) for c in conf.values())
    tau = sum(1 + sum(survival(c)) for c in conf.values())
    return tau * sps(b, table), b, tau


def demo_b() -> None:
    print("=" * 70)
    print("B. 置信度调度：验证多长才划算（治「无差别验证」）")
    print("=" * 70)

    conf = {
        "A-数学": [0.95, 0.93, 0.90, 0.86, 0.80, 0.72, 0.60],
        "B-闲聊": [0.90, 0.70, 0.45, 0.25, 0.12, 0.06, 0.03],
        "C-代码": [0.92, 0.88, 0.80, 0.70, 0.58, 0.45, 0.32],
    }

    print("置信度头输出 c_k（第 k 位在前 k−1 位全被接受的条件下通过验证的概率）：\n")
    print(f"{'请求':<8}" + "".join(f"{'c' + str(j + 1):>8}" for j in range(7)))
    for r, c in conf.items():
        print(f"{r:<8}" + "".join(f"{v:>8.2f}" for v in c))
    print("\n累积存活概率 a_(r,j) = ∏ c_i（单调非增 → 扩一位的边际增益恰为 a_(r,j)）：\n")
    print(f"{'请求':<8}" + "".join(f"{'a' + str(j + 1):>8}" for j in range(7)))
    for r, c in conf.items():
        print(f"{r:<8}" + "".join(f"{v:>8.3f}" for v in survival(c)))

    print("\n" + "-" * 70)
    print("轻载（SPS 曲线高、但 B>12 掉档，且 B>18 回弹 —— 锯齿）")
    print("-" * 70)
    g_theta, g_lens, g_b, g_tau = schedule(conf, SPS_LIGHT, early_stop=True)
    f_theta, f_lens, f_b, f_tau = schedule(conf, SPS_LIGHT, early_stop=False)
    base_theta, base_b, base_tau = full_verify(conf, SPS_LIGHT)

    print(f"{'策略':<24}{'ℓ(A,B,C)':<14}{'B':>4}{'τ':>9}{'Θ=tok/s':>11}")
    print(f"{'① 早停（Algorithm 1）':<22}"
          f"{str(tuple(g_lens.values())):<14}{g_b:>4}{g_tau:>9.3f}{g_theta:>11.0f}")
    print(f"{'② 去早停（生产改法）':<22}"
          f"{str(tuple(f_lens.values())):<14}{f_b:>4}{f_tau:>9.3f}{f_theta:>11.0f}")
    print(f"{'③ 固定长度验证（全验 7 位）':<20}"
          f"{str((7, 7, 7)):<14}{base_b:>4}{base_tau:>9.3f}{base_theta:>11.0f}")

    print(f"\n  ② / ① = {f_theta / g_theta - 1:+.1%} —— 锯齿把早停困在 B={g_b} 的局部极大，")
    print(f"           错过了 B={f_b} 处 SPS 回弹带来的 {f_theta - g_theta:.0f} tok/s。")
    print(f"  ② / ③ = {f_theta / base_theta - 1:+.1%} —— 这才是调度器相对「全验」的净收益。")

    print("\n" + "-" * 70)
    print("重载（同一条曲线整体下移：并发升高时 B 落在更低的档位）")
    print("-" * 70)
    h_theta, h_lens, h_b, h_tau = schedule(conf, SPS_HEAVY, early_stop=False)
    hb_theta, hb_b, hb_tau = full_verify(conf, SPS_HEAVY)
    print(f"{'策略':<24}{'ℓ(A,B,C)':<14}{'B':>4}{'τ':>9}{'Θ=tok/s':>11}")
    print(f"{'① 去早停 · 重载':<22}{str(tuple(h_lens.values())):<14}{h_b:>4}{h_tau:>9.3f}{h_theta:>11.0f}")
    print(f"{'② 固定长度验证 · 重载':<20}{str((7, 7, 7)):<14}{hb_b:>4}{hb_tau:>9.3f}{hb_theta:>11.0f}")
    print(f"\n  同样三个请求：轻载选 {tuple(f_lens.values())}（共 {f_b} token 待验），"
          f"重载自动缩到 {tuple(h_lens.values())}（共 {h_b} token）。")
    print("  低置信度的尾 token 在被消耗关键 batch 容量之前就被剪掉了。")

    assert f_theta >= g_theta, "全局搜索不可能比早停差"
    assert all(v <= 7 for v in list(g_lens.values()) + list(f_lens.values()) + list(h_lens.values()))
    assert sum(h_lens.values()) < sum(f_lens.values()), "重载下验证预算应当收缩"
    print()


if __name__ == "__main__":
    demo_a()
    demo_b()
