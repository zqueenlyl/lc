# 环节 04 · Encoder 与 Packed 序列（Embedding 那一站）

> 全链路第四站：三路信号变成同一条 `(N, 5376)` 序列。对照 Transformer [环节 02 Embedding](../../../../foundation/transformer/环节02-Embedding查表详解.md)：LLM 是 `id → 查表`；H3 是 `latent/hidden → 线性投影`，再 **pack**。
> 所属总揽：[环节00](./环节00-总揽与环节导航.md)。上一站 [环节03](./环节03-双VAE详解.md) → 下一站 [环节05 MM-RoPE](./环节05-MM-RoPE详解.md)。
> 配套 Notebook：[环节04-Encoder与Packed序列演示.ipynb](./环节04-Encoder与Packed序列演示.ipynb)——玩具 pack 与 `token_tags`。

---

## 1. 干什么

开源口径：

- 文本 → **H3-Encoder**
- 视觉 → Encoder **和** VisualVAE（语义 + 像素级）
- 音频 → **仅** AudioVAE

Encoder = **完整** Qwen3-VL-32B 预训练权重（Apache-2.0 叠在 H3 许可证里）。取出 **第 50 层** hidden，`text_dim=5120`，LM head 闲置。不要换上游 Qwen tokenizer：本仓加了 `<d>` 等特殊 token。

文本进 Omni Transformer 前还过 **2 层 Token Refiner**（标准 pre-norm 块，**无 AdaLN、无 RoPE**）——条件文本先自己对齐，再和音画坐在同一张桌上。

## 2. 三条投影（开源形状）

| 来源 | 输入维 | 投影 | 输出 |
|------|--------|------|------|
| 视频 patch | 96 | `video_patch_proj` | 5376 |
| 音频 latent | 32 | `audio_patch_proj` | 5376 |
| Qwen hidden | 5120 | `condition_proj` | 5376 |

若干输入/输出线性在 FSDP 路径保持 **fp32**（SGLang：不为省那点精度破坏数值）。

## 3. Packed 序列长什么样

```
[ 目标视频 token（噪声，要预测速度）
| 文本 / IR token（干净条件）
| 目标音频 token（噪声）
| （Ref2VA）参考图/视频/音频 token（干净） ]
```

每行一个 `token_tag`：`0=video, 1=text, 2=audio`，padding `-1`。开源 AdaLN 索引：

```
combined_index = inverse_timestep_index * 3 + clamp(token_tag, min=0)
```

同一扩散时间步、三种模态，各拿一套 scale/shift/gate（[环节 06](./环节06-AdaLN条件注入详解.md)）。

**FL2VA vs Ref2VA 的本质差**在这一站：不是换 Attn 公式，是 pack 进去的干净条件块不同。首尾帧 = 把对应时间位置的视频 token 换成（或额外加上）干净的关键帧 latent。参考视频 = 整段干净 token 当上下文。V2V 动作迁移同此。

## 4. 对照 LLM Embedding 的三句话

1. **没有词表查表**给像素。连续向量进线性层。
2. **条件文本仍是离散 token**，走 Qwen 的 embedding + 50 层，再投影。所以 H3 的「词表」其实在 Qwen 侧。
3. pack 之后 Attention **双向**看见所有行（去噪需要未来帧）。这和 GPT 因果 mask 相反——见 [环节 07](./环节07-Omni-Block堆叠详解.md)。

## 5. 实例：FL2VA 文生 10 秒的长度量级

```
60480 视频 + L 文本（IR 则 L~4K）+ 每声道 ~400 音频（立体声 packed 可能翻倍）≈ 6.5 万行量级
每行 5376 维
```

引入多模态上下文后，官方说序列长度方差约 **×3**，理解（长文本/多参考）和生成（固定大视频块）workload 异质——这是 [环节 09](./环节09-训练管线详解.md) 拆调度的原因。

## 6. 工程要点

1. 必须用官方 `build_packed_sequence` / `build_row_timesteps`。自己 `torch.cat` 是社区微调静默毁权重的主因。
2. `load_components()` 不带 workflow 会拉 **两份** Transformer。
3. 微调可以只训 DiT、冻结 Encoder/VAE，先把目标视频 latent 和文本第 50 层缓存到盘。

## 7. 面试追问

- **为什么取第 50 层不是最后一层？** 官方只给事实不给消融；多模态里中间层常更「可对齐」。未披露对比表。
- **音频为什么不进 Qwen？** 开源路径如此；语义关系靠 IR 文本描述 + 音频 latent 自注意力。

下一站：这 6 万行若没有位置，Attn 分不清「第 3 秒左上角」和「第 3 秒的声」。
