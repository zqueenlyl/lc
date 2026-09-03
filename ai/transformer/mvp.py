"""缩放点积注意力 vs RNN 隐状态接力（纯 Python，无 numpy/torch）

句子：猫 吃 了 鱼 它
- 双向注意力：每个词都能看所有词
- 因果注意力：只能看自己和左边（LLM 解码）
- RNN：历史乘 0.5 往下传，早期词被冲淡；句尾「它」仍可用注意力回指「猫」

运行：
    python3 mvp.py
"""

from __future__ import annotations

import math

Mat = list[list[float]]
Vec = list[float]


def matmul(a: Mat, b: Mat) -> Mat:
    n, k, m = len(a), len(b), len(b[0])
    out = [[0.0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            out[i][j] = sum(a[i][t] * b[t][j] for t in range(k))
    return out


def transpose(a: Mat) -> Mat:
    return [list(col) for col in zip(*a)]


def softmax_row(row: Vec) -> Vec:
    m = max(row)
    exps = [math.exp(x - m) for x in row]
    s = sum(exps)
    return [e / s for e in exps]


def fmt_mat(mat: Mat, names: list[str] | None = None) -> str:
    lines = []
    if names:
        header = "        " + "  ".join(f"{n:>4}" for n in names)
        lines.append(header)
    for i, row in enumerate(mat):
        prefix = f"{names[i]:>6}  " if names else "  "
        lines.append(prefix + "  ".join(f"{v:4.2f}" for v in row))
    return "\n".join(lines)


def scaled_dot_product_attention(
    q: Mat,
    k: Mat,
    v: Mat,
    causal: bool = False,
) -> tuple[Mat, Mat]:
    d_k = len(k[0])
    scores = matmul(q, transpose(k))
    scale = math.sqrt(d_k)
    scores = [[s / scale for s in row] for row in scores]
    if causal:
        n = len(scores)
        for i in range(n):
            for j in range(i + 1, n):
                scores[i][j] = -1e9
    weights = [softmax_row(row) for row in scores]
    return weights, matmul(weights, v)


def rnn_carry(xs: Mat, decay: float = 0.5) -> tuple[list[Vec], list[float]]:
    """h_t = decay * h_{t-1} + x_t。返回各步隐状态，以及 x_0 在每一步的残留系数。"""
    hs: list[Vec] = []
    coeff_x0: list[float] = []
    h = [0.0] * len(xs[0])
    c0 = 0.0
    for t, x in enumerate(xs):
        h = [decay * h_i + x_i for h_i, x_i in zip(h, x)]
        c0 = decay * c0 + (1.0 if t == 0 else 0.0)
        hs.append(h)
        coeff_x0.append(c0)
    return hs, coeff_x0


if __name__ == "__main__":
    tokens = ["猫", "吃", "了", "鱼", "它"]
    # 手工 Q/K：吃 查施事+受事；它 像代词一样回指施事
    q: Mat = [
        [2.0, 0.0, 0.0],  # 猫：查施事
        [2.0, 0.0, 2.0],  # 吃：同时查施事和受事
        [0.0, 2.0, 0.0],  # 了：查助词
        [0.0, 0.0, 2.0],  # 鱼：查受事
        [2.0, 0.0, 0.0],  # 它：回指施事
    ]
    k: Mat = [
        [3.0, 0.0, 0.0],  # 猫 ≈ 施事
        [0.4, 0.4, 0.4],  # 吃
        [0.0, 3.0, 0.0],  # 了
        [0.0, 0.0, 3.0],  # 鱼 ≈ 受事
        [0.5, 0.2, 0.2],  # 它
    ]
    v: Mat = [
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.5, 0.0],
        [0.0, 0.0, 1.0],
        [0.2, 0.0, 0.0],
    ]

    print("句子:", " ".join(tokens))
    print("行 = Query（谁在看），列 = Key（被看谁）\n")

    w_bi, _ = scaled_dot_product_attention(q, k, v, causal=False)
    print("=== 双向 self-attention（BERT 类，能看未来）===")
    print(fmt_mat(w_bi, tokens))
    print("观察：吃 → 猫 / 鱼 的权重明显高于「了」。\n")

    w_ca, _ = scaled_dot_product_attention(q, k, v, causal=True)
    print("=== 因果 self-attention（GPT 类，只能看左边）===")
    print(fmt_mat(w_ca, tokens))
    print("观察：下三角；吃 还看不见后面的 鱼。生成「鱼」时，才由最后一个位置去看前文。\n")

    _, coeff = rnn_carry(v, decay=0.5)
    print("=== RNN 接力：每个新步把旧隐状态 ×0.5 ===")
    for t, (tok, c) in enumerate(zip(tokens, coeff)):
        print(f"  走到「{tok}」时，第一个词「猫」的残留系数 = {c:.3f}")
    attn_to_cat = [row[0] for row in w_ca]
    print("\n因果注意力里，各位置直接分给「猫」的权重:")
    for tok, a in zip(tokens, attn_to_cat):
        print(f"  {tok} → 猫 {a:.2f}")
    print("\n走到句尾「它」时：RNN 里「猫」只剩指数衰减后的系数；")
    print("注意力仍可一步点名「猫」（代词回指），不必经过中间的「吃了鱼」。")
    print("真实模型里 Q/K/V 是学出来的线性层，多头再拆成多组这种矩阵。")
