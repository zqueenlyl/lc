"""一维玩具扩散：加噪再去噪（无深度学习）

真实 DDPM 用网络预测 ε；这里 ε 已知（演示公式），看 x_t 如何走回 x_0。

运行：
    python3 mvp.py
"""

from __future__ import annotations

import math
import random


def l2(a: list[float], b: list[float]) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def add(a: list[float], b: list[float]) -> list[float]:
    return [x + y for x, y in zip(a, b)]


def scale(a: list[float], s: float) -> list[float]:
    return [x * s for x in a]


def q_sample(x0: list[float], t: int, t_max: int, rng: random.Random) -> tuple[list[float], list[float]]:
    """xt = sqrt(alpha) x0 + sqrt(1-alpha) ε，alpha 随 t 线性减小。"""
    alpha = 1.0 - 0.9 * (t / t_max)
    eps = [rng.gauss(0, 1) for _ in x0]
    xt = add(scale(x0, math.sqrt(alpha)), scale(eps, math.sqrt(1 - alpha)))
    return xt, eps


def denoise_step(xt: list[float], eps_pred: list[float], t: int, t_max: int) -> list[float]:
    """已知 ε 时的一步还原（示意，非正式采样器）。"""
    alpha = 1.0 - 0.9 * (t / t_max)
    x0_hat = scale(add(xt, scale(eps_pred, -math.sqrt(1 - alpha))), 1 / math.sqrt(alpha))
    return x0_hat


if __name__ == "__main__":
    x0 = [0.0, 1.0, 2.0, 3.0, 2.0, 1.0, 0.0, -1.0]
    t_max = 10
    rng = random.Random(42)
    print("x0:", ["%.2f" % v for v in x0])
    print("\n=== 只加噪（越往后越不像）===")
    for t in (1, 5, 10):
        xt, _ = q_sample(x0, t, t_max, random.Random(t))
        print(f" t={t:2}  L2={l2(xt, x0):.2f}  xt={['%.2f' % v for v in xt]}")

    print("\n=== 用真实 ε 一步还原（理想教师）===")
    for t in (1, 5, 10):
        xt, eps = q_sample(x0, t, t_max, random.Random(t))
        hat = denoise_step(xt, eps, t, t_max)
        print(f" t={t:2}  还原 L2={l2(hat, x0):.3f}")

    print("\n网络的工作：看不见 ε，要从 xt 和 t 预测它。预测越准，还原越接近 x0。")
