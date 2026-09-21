# 环节 06 · AdaLN 条件注入（H3 的「可卸 13B」）

> 全链路第六站。对照 Transformer [环节 06 残差与归一化](../../../../foundation/transformer/环节06-残差连接与归一化详解.md)：那边的 LN/RMS 是 **与输入无关的** 稳定器。DiT 把尺度和偏置变成 **时间步的函数**，叫 Adaptive LayerNorm / AdaLN。H3 再按 **模态标签** 分三套。
> 所属总揽：[环节00](./环节00-总揽与环节导航.md)。上一站 [环节05](./环节05-MM-RoPE详解.md) → 下一站 [环节07](./环节07-Omni-Block堆叠详解.md)。
> 配套 Notebook：[环节06-AdaLN演示.ipynb](./环节06-AdaLN演示.ipynb)——13B 参数账；同一 `t` 为何推理可缓存。

---

## 1. 干什么

扩散时间 \(t\) 告诉网络「现在有多噪」。模态标签告诉网络「这行是画面、字还是声」。H3 不把这两件事做成交叉注意力旁路（当然文本也在序列里自注意力），而是：

```
e_t = TimeEmbed(t)           # 256 → 5376 → 2688
(γ,β,g)_attn, (γ,β,g)_mlp = SiLU(e_t) → Linear → 切成 6 段 × 3 模态
```

开源 `adaln_out_features = 18 × 5376`，其中 `18 = 6 × 3`。每层一个 `adaln_proj`。

官方：**约 13B 参数住在 AdaLN 相关分支**。推理调制可预计算，**纯推理可不加载这 13B**。完整权重仍放出以便微调。

## 2. 公式（一块里的前半）

\[
\begin{aligned}
h &= \mathrm{RMSNorm}(x)\odot(1+\gamma_{m,\text{attn}})+\beta_{m,\text{attn}} \\
h &= \mathrm{Attn}(h) \\
x &\leftarrow x + g_{m,\text{attn}}\odot h
\end{aligned}
\]

MLP 半边同样再来一套 \(\gamma,\beta,g\)。\(m\in\{\text{video},\text{text},\text{audio}\}\)。**QKV 矩阵不分家**——分家的只是进 Attn 之前的仿射。

门控 \(g\) 是 DiT 常见写法：残差不是裸加，而是「这一层更新允许多大步」，步长随 \(t\) 和模态变。

## 3. 参数账（必须自己算一遍）

```
每层：2688 × (6 × 5376 × 3) + bias ≈ 2.60×10⁸
× 50 层 ≈ 1.301×10¹⁰   → 13.01B
```

和官方「约 13B」对齐。这就是「架构简单但 AdaLN 很肥」：条件通路按 hidden 全宽展开，层数一乘就过十亿。

对比：若用 cross-attn 把 4K 文本接到 6 万视频 token，KV 是序列长度问题；AdaLN 是 **每层 2.6 亿固定参数**，与序列长度无关。H3 选择「肥条件、瘦模态分支」。

## 4. 为什么推理可以卸

对固定的一批 unique \(t\)（调度器那几十个点），`e_t` 和 50 层 × 3 模态的 \(\gamma\beta g\) **不依赖视频内容**。可以：

1. 事先算好表格；或
2. 部署时根本不 load `adaln_proj` 权重，用缓存张量。

微调不行：loss 对 \(\gamma\beta g\) 有梯度，LoRA 通常也不打在这 13B 上（fal 人像 LoRA 打的是共享 `qkv_proj`）。

## 5. 和 LLM 的 Cond 怎么比

| LLM | H3 AdaLN |
|-----|----------|
| 条件主要是 prompt token 自己进 Attn | 文本 token 也在序列里 **另外** 用 AdaLN 把 \(t\) 灌进每一层 |
| 没有扩散时间 | \(t\) 是第一公民 |
| 卸载不了「条件参数」 | 调制与内容解耦，可卸 |

模态专用参数官方口径：只在 **输入/输出层 + AdaLN**。这是丢掉 Hailuo-02 过巧结构之后的显式选择。

## 6. 工程要点

1. AdaLN 投影在 FSDP 上保持 fp32。社区微调把它们改 bf16 会静默坏数值。
2. `combined_index = inverse_indices * 3 + tag`：timestep 索引和 tag 接错，画面会套上音频的 scale。
3. 视频/音频 **两套** \(t\)（shift 不同），AdaLN 的 unique timesteps 要按行对齐，不能共用一个标量 \(t\)。

## 7. 面试追问

- **33B 推理为什么说可以更轻？** 卸 13B AdaLN，内容主干约 20B 量级仍在。
- **AdaLN 算模态专家吗？** 只是三套仿射，不是三套 Attn。专家在「怎么归一化」，不在「怎么开会」。

下一站：把 AdaLN、Attn、FFN 装成 50 层单流。
