# 环节 07 · Omni Block 堆叠（组装成 33B）

> 全链路第七站。对照 Transformer [环节 07](../../../../foundation/transformer/环节07-Block堆叠与整体架构详解.md)：结构同样是「四件套 × N 层，参数不共享」。差别：无因果 mask、无 LM head、音画文本同一条流。
> 零件复习：Attention [环节04](../../../../foundation/transformer/环节04-Attention注意力详解.md)、FFN/SwiGLU [环节05](../../../../foundation/transformer/环节05-FFN激活与MoE详解.md)、RMSNorm [环节06](../../../../foundation/transformer/环节06-残差连接与归一化详解.md)。
> 所属总揽：[环节00](./环节00-总揽与环节导航.md)。上一站 [环节06](./环节06-AdaLN条件注入详解.md) → 下一站 [环节08](./环节08-双头与Flow训练目标详解.md)。
> 配套 Notebook：[环节07-Omni-Block堆叠演示.ipynb](./环节07-Omni-Block堆叠演示.ipynb)——骨架参数量级；「每层结构相同 ≠ 参数相同」。

---

## 1. 一个 Block = 仍是四件套，多了 AdaLN 皮

开源 `MiniMaxH3DiTBlock`：

```
x, t_emb, token_tags
  → RMSNorm + AdaLN(shift/scale)     # 按模态索引
  → Attention（RoPE 在 QK 上；共享 W）
  → 门控残差
  → RMSNorm + AdaLN
  → SwiGLU FFN（fc1 融合 gate/up，SiluAndMul，fc2）
  → 门控残差
```

**Attention / FFN 没有模态专用结构。** 官方为任务泛化主动丢掉 Hailuo-02 架构。

## 2. 开源骨架（全局只背这一次）

| 项 | 值 | 备注 |
|----|----|------|
| 层数 | 50 | 另 2 层 text Token Refiner |
| hidden | 5376 | |
| 头 | 56 × 128 | 开源 QKV 布局含 grouped 重排 |
| FFN | 14336 SwiGLU | 无 MoE |
| 总参 | 33B | AdaLN ≈ 13B |
| patch | (1,2,2) | 视频 |

粗算内容主干（示意，不含 Embedding 级小件）：

```
每层 Attn（MHA 近似 4 × 5376²）≈ 1.16×10⁸
每层 FFN（3 × 5376 × 14336）≈ 2.31×10⁸
×50 ≈ 17.3B
+ AdaLN 13B
+ 双头 / patch / time / refiner / Qwen 不计入 33B 的「Omni Transformer」口径
≈ 官方 33B 稠密单流
```

Qwen3-VL-32B 条件器是 **另一份** ~32B，推理栈常写「整栈约 69B、单分区盘约 134GB」。不要把 33B 当成「一张卡能装下的全部」。

## 3. 和 Decoder-only LLM 的三处相反

| | GPT 类 | H3 Omni |
|--|--------|---------|
| Mask | 因果，不能看未来 | **双向**，去噪必须看整段 |
| 循环 | 推理时序列变长 | 推理时序列长度冻结，变的是 \(t\) |
| 输出 | 每行一个词表分布 | 每行两个速度（再 mask 取视频行/音频行） |
| 专家 | 可选 MoE | 稠密；专家在任务混合而不在 FFN |

「当场开会」在 H3 里是字面意思：第 3 秒嘴型的视频 token 可以直接开会给第 3 秒的音频 token。

## 4. 一次前向（FL2VA 文生 10 秒）

```
噪声视频 [60, 24, 48, 84]  T,C,H,W  --patch 1×2×2--> 60480×96 --proj--> 60480×5376
噪声音频 --proj--> 每声道 ~400×5376（立体声 packed 可能翻倍）
文本第50层 --proj--> L×5376 --2层 refiner-->
pack + MM-RoPE
        │
        ▼  50 × Block
        │
        ▼  Final AdaLN + video_out/audio_out（两头都打在每一行上，再按 tag 取）
```

Ref2VA：多 pack 干净参考。没有第四套 Block。

## 5. 稀疏注意力

训练末段 native sparse，降长序列成本。**首发开源推理只有全注意力**；稀疏实现标后续单独发。模式/块大小未披露。

## 6. 工程要点

1. 「重复 50 层结构相同」≠ 参数共享。LoRA 的 `blocks.N.attn.qkv_proj` 每层一份。
2. 全注意力下 6 万 token 的 \(O(n^2)\) 是推理贵的主因，不是 33B 本身。
3. Ulysses/序列并行切的是 packed 行，必须和 `cu_seqlens` 一起切（vLLM 里有显式 SP prepare/gather）。

## 7. 面试追问

- **为什么不用 MMDiT 双流（FLUX 那种）？** 官方要任务泛化、结构尽量简单；文本已经作为 token 进单流。未披露消融。
- **33B 里最大头是 Attn 吗？** 不是。AdaLN 13B 往往大于单层 Attn 总和；内容主干里 FFN 仍大于 Attn。

下一站：最后两行线性变成「对错标准」。
