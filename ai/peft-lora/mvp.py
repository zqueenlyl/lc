"""LoRA 热插拔（纯 Python 矩阵，无 torch）

W 是底座；每个领域只存 A、B。同一输入，换 LoRA 就换风格。

运行：
    python3 mvp.py
"""

from __future__ import annotations

from dataclasses import dataclass


Mat = list[list[float]]


def matmul(a: Mat, b: Mat) -> Mat:
    n, k, m = len(a), len(b), len(b[0])
    out = [[0.0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            out[i][j] = sum(a[i][t] * b[t][j] for t in range(k))
    return out


def add(a: Mat, b: Mat) -> Mat:
    return [[x + y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def scale(a: Mat, g: float) -> Mat:
    return [[x * g for x in row] for row in a]


def vecmul(w: Mat, x: list[float]) -> list[float]:
    return [sum(row[i] * x[i] for i in range(len(x))) for row in w]


def fmt(mat: Mat) -> str:
    return "  " + "\n  ".join("[" + ", ".join(f"{v:5.1f}" for v in row) + "]" for row in mat)


@dataclass
class LoRA:
    name: str
    a: Mat  # r × k
    b: Mat  # d × r
    gamma: float = 1.0

    def delta(self) -> Mat:
        return scale(matmul(self.b, self.a), self.gamma)


class BaseModel:
    def __init__(self, w: Mat):
        self.w = w

    def forward(self, x: list[float], lora: LoRA | None = None) -> list[float]:
        weight = self.w if lora is None else add(self.w, lora.delta())
        return vecmul(weight, x)


if __name__ == "__main__":
    w: Mat = [
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
    ]
    formal = LoRA("formal", a=[[2.0, 0.0, 0.0]], b=[[1.0], [0.0], [0.0]])
    pirate = LoRA("pirate", a=[[0.0, 0.0, 2.0]], b=[[0.0], [0.0], [1.0]])

    model = BaseModel(w)
    x = [1.0, 1.0, 1.0]

    print("W (底座, 一份):\n" + fmt(w))
    print("\nformal ΔW = B A:\n" + fmt(formal.delta()))
    print("pirate ΔW = B A:\n" + fmt(pirate.delta()))

    print("\n=== 同一 x，热插拔 ===")
    for adapter in (None, formal, pirate):
        name = adapter.name if adapter else "base"
        y = model.forward(x, adapter)
        print(f"  {name:7} y={['%.1f' % v for v in y]}")

    print("\n存储：底座 9 个数 + 每个 LoRA 3+3 个数，而不是 3 份完整 W。")
