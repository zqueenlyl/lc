"""玩具 MoE：4 专家，每个 token 只激活 top-2（无深度学习框架）

专家 = 不同的「词风格变换」。路由器给每个专家打分，取最高 2 个做加权。

运行：
    python3 mvp.py
"""

from __future__ import annotations

from dataclasses import dataclass


def softmax(xs: list[float]) -> list[float]:
    m = max(xs)
    exps = [pow(2.718281828, x - m) for x in xs]
    s = sum(exps)
    return [e / s for e in exps]


@dataclass
class Expert:
    name: str
    tag: str

    def forward(self, token: str) -> str:
        return f"{token}[{self.tag}]"


class Router:
    """演示用：用 token 字符和专家名的重叠当 logit，保证可复现、可打印。"""

    def __init__(self, experts: list[Expert], top_k: int = 2):
        self.experts = experts
        self.top_k = top_k

    def route(self, token: str) -> list[tuple[Expert, float]]:
        logits = [float(sum(1 for ch in token if ch in e.name)) + 0.1 * i for i, e in enumerate(self.experts)]
        weights = softmax(logits)
        ranked = sorted(zip(self.experts, weights), key=lambda x: x[1], reverse=True)
        picked = ranked[: self.top_k]
        # 在被选集合上重新归一，模拟常见实现
        z = sum(w for _, w in picked)
        return [(e, w / z) for e, w in picked]


class MoE:
    def __init__(self, experts: list[Expert], top_k: int = 2):
        self.router = Router(experts, top_k)
        self.n_experts = len(experts)
        self.top_k = top_k

    def forward(self, tokens: list[str]) -> list[str]:
        outs = []
        for tok in tokens:
            picked = self.router.route(tok)
            parts = [f"{w:.2f}*{e.forward(tok)}" for e, w in picked]
            outs.append(" + ".join(parts))
            names = ",".join(e.name for e, _ in picked)
            print(f"  token={tok!r:8} → experts [{names}]  (激活 {self.top_k}/{self.n_experts})")
        return outs


if __name__ == "__main__":
    experts = [
        Expert("code", "py"),
        Expert("legal", "law"),
        Expert("chat", "talk"),
        Expert("math", "num"),
    ]
    moe = MoE(experts, top_k=2)
    tokens = ["sum", "contract", "hello", "def"]
    print("=== 稀疏前向 ===")
    moe.forward(tokens)
    dense_ops = len(tokens) * moe.n_experts
    sparse_ops = len(tokens) * moe.top_k
    print(f"\n相对稠密 FFN：{sparse_ops}/{dense_ops} = {sparse_ops / dense_ops:.0%} 专家计算")
    print("真实模型里专家是巨型 FFN，路由是小线性层；负载均衡是训练必做的功课。")
