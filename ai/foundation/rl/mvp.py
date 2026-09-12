"""RL 最小可运行演示（纯 Python 标准库，无 numpy / torch）

三小节，对应 RL 主线的三个核心动作：

  §1 值迭代               —— "算"：已知环境模型时，把 V* 迭代到不动点（呼应环节 01 §8）
  §2 网格世界的 Q-learning —— "试"：没有模型，只靠采样学出策略（呼应环节 02 §8）
  §3 三臂老虎机 REINFORCE  —— "调概率"：不估分，直接用回报对策略求导（呼应环节 03 §10）

每条结论的推导、方法对比与面试追问见同目录 `环节01`–`环节03` 长文。

运行：
    python3 mvp.py
"""

from __future__ import annotations

import math
import random
import statistics


# ============================================================
# §1 值迭代：只有 2 个状态的 MDP（环节 01）
# ============================================================
def demo_value_iteration() -> None:
    """S = {A, B}，A = {stay, go}，γ = 0.9。

    规则（确定性）：
        A --stay--> A, +1        A --go--> B, +2
        B --stay--> B, +3        B --go--> A,  0
    手算答案：V*(A) = 29、V*(B) = 30；π* = {A: go, B: stay}
    """
    gamma = 0.9
    actions = ("stay", "go")
    trans = {
        ("A", "stay"): ("A", 1.0),
        ("A", "go"): ("B", 2.0),
        ("B", "stay"): ("B", 3.0),
        ("B", "go"): ("A", 0.0),
    }

    print("=" * 64)
    print("§1 值迭代（有模型）：把 Bellman 最优方程迭代到不动点")
    print("=" * 64)

    V = {"A": 0.0, "B": 0.0}
    for it in range(1, 41):
        V = {s: max(r + gamma * V[s2] for (s2, r) in (trans[(s, a)] for a in actions))
             for s in V}
        if it <= 3 or it == 40:
            print(f"  第 {it:>2} 轮：V(A) = {V['A']:7.4f}   V(B) = {V['B']:7.4f}")

    policy = {
        s: max(actions, key=lambda a: trans[(s, a)][1] + gamma * V[trans[(s, a)][0]])
        for s in V
    }
    print(f"  收敛后 π*(A) = {policy['A']}，π*(B) = {policy['B']}   （手算：go / stay）")
    print()


# ============================================================
# §2 网格世界：值迭代 vs Q-learning（环节 02）
# ============================================================
def demo_gridworld_q_learning() -> None:
    """4×3 网格世界：起点 (0,0)；转移到目标 (3,2) → +1；转移到陷阱 (3,1) → −1。

    其他转移奖励 0；撞墙留在原地；γ = 0.9。
    Q-learning：α = 0.4，ε = 0.1，20000 回合。
    """
    W, H, GOAL, PIT = 4, 3, (3, 2), (3, 1)
    TERM = {GOAL, PIT}
    GAMMA, ALPHA, EPS, EPISODES = 0.9, 0.4, 0.1, 20000
    ACTS = ((0, 1), (0, -1), (-1, 0), (1, 0))          # 上 下 左 右
    STATES = [(x, y) for x in range(W) for y in range(H)]

    def step(s, a):
        ns = (s[0] + a[0], s[1] + a[1])
        if not (0 <= ns[0] < W and 0 <= ns[1] < H):
            ns = s                                     # 撞墙：留在原地
        if ns == GOAL:
            return ns, 1.0, True                       # 转移到目标 → +1
        if ns == PIT:
            return ns, -1.0, True                      # 转移到陷阱 → −1
        return ns, 0.0, False

    def show(V, title):
        print(title)
        for y in range(H - 1, -1, -1):
            row = []
            for x in range(W):
                if (x, y) == GOAL:
                    row.append("      G")
                elif (x, y) == PIT:
                    row.append("      P")
                else:
                    row.append(f"{V[(x, y)]:7.3f}")
            print("  ".join(row))
        print()

    # —— 真值：值迭代（有模型） ——
    V = {s: 0.0 for s in STATES}
    for _ in range(500):
        V = {s: (0.0 if s in TERM else
                 max(r + (0.0 if d else GAMMA * V[ns])
                     for (ns, r, d) in (step(s, a) for a in ACTS)))
             for s in STATES}

    print("=" * 64)
    print("§2 网格世界：有模型的值迭代 vs 无模型的 Q-learning")
    print("=" * 64)
    show(V, "① 真值（值迭代，有模型）")

    def q_learn(random_start, seed=0):
        random.seed(seed)
        Q = {(s, a): 0.0 for s in STATES for a in ACTS}
        visit = dict.fromkeys(STATES, 0)
        for _ in range(EPISODES):
            s = random.choice(STATES) if random_start else (0, 0)
            while s not in TERM:
                visit[s] += 1
                a = (random.choice(ACTS) if random.random() < EPS
                     else max(ACTS, key=lambda a: Q[(s, a)]))
                ns, r, done = step(s, a)
                target = r + (0.0 if done else GAMMA * max(Q[(ns, a2)] for a2 in ACTS))
                Q[(s, a)] += ALPHA * (target - Q[(s, a)])
                s = ns
        Vq = {s: (0.0 if s in TERM else max(Q[(s, a)] for a in ACTS)) for s in STATES}
        return Vq, visit

    Vq, visit = q_learn(random_start=False)
    show(Vq, "② Q-learning（固定起点 (0,0)，20000 回合）")
    gap = max(abs(Vq[s] - V[s]) for s in STATES if s not in TERM)
    leaked = [s for s in STATES if s not in TERM and visit[s] == 0]
    print(f"  访问 0 次的状态：{leaked}，最大偏差：{gap:.3f}")
    print("  访问次数：", {s: visit[s] for s in STATES if s not in TERM})
    print("  → 算法没错：这个状态从固定起点出发根本访问不到（没访问 = 没学到）。")
    print()

    Vq2, _ = q_learn(random_start=True)
    gap2 = max(abs(Vq2[s] - V[s]) for s in STATES if s not in TERM)
    show(Vq2, "③ 只把起点改成随机（其余参数不动）")
    print(f"  最大偏差 {gap2:.3f}（与真值逐格一致）")
    print()


# ============================================================
# §3 三臂老虎机 REINFORCE（环节 03）
# ============================================================
def demo_reinforce() -> None:
    """真实成功率 p = [0.2, 0.5, 0.8]（智能体不知道）；softmax 策略参数化。

    θ ← θ + α·A·∇logπ，α = 0.1，3000 回合，5 个随机种子取平均。
    """
    P = [0.2, 0.5, 0.8]
    ALPHA, EPISODES = 0.1, 3000

    def softmax(th):
        m = max(th)
        e = [math.exp(t - m) for t in th]
        s = sum(e)
        return [x / s for x in e]

    def run(use_baseline, seed):
        random.seed(seed)
        th, b = [0.0, 0.0, 0.0], 0.0
        for _ in range(EPISODES):
            pi = softmax(th)
            r, acc, a = random.random(), 0.0, 0
            for a, p in enumerate(pi):                 # 按 π 采样一个臂
                acc += p
                if r <= acc:
                    break
            R = 1.0 if random.random() < P[a] else 0.0
            adv = R - (b if use_baseline else 0.0)     # ← 基线在这里
            grad = [(1.0 if i == a else 0.0) - pi[i] for i in range(3)]   # ∇logπ = onehot − π
            for i in range(3):
                th[i] += ALPHA * adv * grad[i]         # θ ← θ + α·A·∇logπ
            b += 0.05 * (R - b)                        # 基线用运行均值估计
        return softmax(th)

    print("=" * 64)
    print("§3 三臂老虎机 REINFORCE：直接对策略调概率（全程不知道 p）")
    print("=" * 64)
    for use_baseline in (False, True):
        runs = [run(use_baseline, seed) for seed in range(5)]
        avg = [statistics.fmean(p[i] for p in runs) for i in range(3)]
        tag = "有基线" if use_baseline else "无基线"
        print(f"  {tag}：收敛 π = [{avg[0]:.3f}  {avg[1]:.3f}  {avg[2]:.3f}]"
              f"    （最优臂真实成功率 p = 0.8）")
    print("  → 两者都收敛到「几乎总是选臂 3」：基线不改最优解，只降方差。")
    print()


if __name__ == "__main__":
    demo_value_iteration()
    demo_gridworld_q_learning()
    demo_reinforce()
