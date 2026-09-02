"""格子世界：学习转移 ≈ 世界模型，再在模型里规划（无神经网络）

运行：
    python3 mvp.py
"""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
import random


ACTIONS = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}


@dataclass(frozen=True)
class Grid:
    n: int = 5
    walls: frozenset = frozenset({(1, 1), (2, 1), (2, 2)})
    goal: tuple = (4, 4)

    def valid(self, s: tuple[int, int]) -> bool:
        r, c = s
        return 0 <= r < self.n and 0 <= c < self.n and s not in self.walls

    def step(self, s: tuple[int, int], a: str) -> tuple[int, int]:
        dr, dc = ACTIONS[a]
        nxt = (s[0] + dr, s[1] + dc)
        return nxt if self.valid(nxt) else s


class WorldModel:
    """计数估计：每个 (s,a) 记最常见的 s'。"""

    def __init__(self):
        self.counts: dict[tuple, dict[tuple, int]] = defaultdict(lambda: defaultdict(int))

    def observe(self, s, a, sp) -> None:
        self.counts[(s, a)][sp] += 1

    def predict(self, s, a, fallback):
        table = self.counts.get((s, a))
        if not table:
            return fallback(s, a)
        return max(table.items(), key=lambda kv: kv[1])[0]


def explore(env: Grid, model: WorldModel, n: int = 400, seed: int = 0) -> None:
    rng = random.Random(seed)
    s = (0, 0)
    for _ in range(n):
        a = rng.choice(list(ACTIONS))
        sp = env.step(s, a)
        model.observe(s, a, sp)
        s = (0, 0) if rng.random() < 0.05 else sp


def plan(model: WorldModel, env: Grid, start: tuple) -> list[str] | None:
    q = deque([(start, [])])
    seen = {start}
    while q:
        s, path = q.popleft()
        if s == env.goal:
            return path
        for a in ACTIONS:
            sp = model.predict(s, a, env.step)
            if sp not in seen and env.valid(sp):
                seen.add(sp)
                q.append((sp, path + [a]))
    return None


def execute(env: Grid, start: tuple, actions: list[str]) -> list[tuple]:
    s = start
    traj = [s]
    for a in actions:
        s = env.step(s, a)
        traj.append(s)
    return traj


if __name__ == "__main__":
    env = Grid()
    model = WorldModel()
    explore(env, model)
    start = (0, 0)
    path = plan(model, env, start)
    print(f"学到的 (s,a) 条数: {len(model.counts)}")
    print("模型规划路径:", path)
    traj = execute(env, start, path or [])
    print("真实执行:    ", traj)
    print("到达目标:" , traj[-1] == env.goal)
    print("说明：转移表是最朴素的世界模型；深度模型用神经网络拟合同一接口 f(s,a)→s'。")
