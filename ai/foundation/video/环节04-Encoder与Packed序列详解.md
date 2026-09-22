# 视频生成 · 环节 04 · 编码器与 Packed 序列

> 开源数字默认 MiniMax-H3 Base；机制对 2024 后潜空间 DiT / flow（类型 D/E）通用。总揽：[环节00](./环节00-总揽与环节导航.md)。类型见 [演化路线](./生视频模型演化路线与类型.md)。
> 全链路第四站：视频 latent、音频 latent、文本 hidden 三路，各过一个线性投影升到 5376 维，再 **pack** 成同一条 `(N, 5376)` 序列。音画能同环去噪、口型能对上，物理前提就是它们真的坐在同一条序列里。
> 所属总揽：[环节00](./环节00-总揽与环节导航.md)。上一站 [环节03](./环节03-双VAE详解.md) → 下一站 [环节05 MM-RoPE](./环节05-MM-RoPE详解.md)。
> 配套 Notebook：[环节04-Encoder与Packed序列演示.ipynb](./环节04-Encoder与Packed序列演示.ipynb)——玩具 pack 与 `token_tags`。

---

## 1. 干什么

开源口径：

- 文本 → **H3-Encoder**
- 视觉 → Encoder **和** VisualVAE（语义 + 像素级）
- 音频 → **仅** AudioVAE

Encoder = **完整** Qwen3-VL-32B 预训练权重（Apache-2.0 叠在 H3 许可证里）。取出 **第 50 层** hidden，`text_dim=5120`，LM head 闲置——这里只要它对语言和画面的理解向量，不要它的输出分布。不要换上游 Qwen tokenizer：本仓加了 `<d>` 等特殊 token。

文本进 Omni Transformer 前还过 **2 层 Token Refiner**（标准 pre-norm 块，**无 AdaLN、无 RoPE**）——条件文本先自己对齐，再和音画坐在同一张桌上。

## 2. 三条投影（开源形状）

| 来源 | 输入维 | 投影 | 输出 |
|------|--------|------|------|
| 视频 patch | 96 | `video_patch_proj` | 5376 |
| 音频 latent | 32 | `audio_patch_proj` | 5376 |
| Qwen hidden | 5120 | `condition_proj` | 5376 |

三路都是**连续向量过线性层**，没有任何查表环节：像素和波形本来就不是离散符号。真正带「词表」的只有条件文本那一路，而那套词表在 Qwen 侧，不在 DiT 里。

若干输入/输出线性在 FSDP 路径保持 **fp32**（SGLang：不为省那点精度破坏数值）。

## 3. Packed 序列长什么样

```
[ 目标视频 token（噪声，要预测速度）
| 文本 / IR token（干净条件）
| 目标音频 token（噪声）
| （Ref2VA）参考图/视频/音频 token（干净） ]
```

一条序列里同时混着**要去噪的行**和**干净的条件行**，靠标签区分。每行一个 `token_tag`：`0=video, 1=text, 2=audio`，padding `-1`。开源 AdaLN 索引：

```
combined_index = inverse_timestep_index * 3 + clamp(token_tag, min=0)
```

同一扩散时间步、三种模态，各拿一套 scale/shift/gate（[环节 06](./环节06-AdaLN条件注入详解.md)）。

pack 之后注意力是**双向**的：每一行都能看见所有行。去噪必须这样——要判断第 3 秒的某个格子该往哪走，得看见第 5 秒的画面和整段声音。

**FL2VA vs Ref2VA 的本质差**在这一站：不是换 Attn 公式，是 pack 进去的干净条件块不同。首尾帧 = 把对应时间位置的视频 token 换成（或额外加上）干净的关键帧 latent。参考视频 = 整段干净 token 当上下文。V2V 动作迁移同此。

## 4. 实例：FL2VA 文生 10 秒的长度量级

```
60480 视频 + L 文本（IR 则 L~4K）+ 每声道 ~400 音频（立体声 packed 可能翻倍）≈ 6.5 万行量级
每行 5376 维
```

引入多模态上下文后，官方说序列长度方差约 **×3**：只写一句 prompt 的请求，和挂了 9 张图 3 段视频的请求，行数不在一个档位上。「读长 IR / 多参考」（理解型负载）和「写 6 万视频 token」（生成型负载）性质也不同——这是 [环节 09](./环节09-训练管线详解.md) 要拆调度的原因。

## 5. 工程要点

1. 必须用官方 `build_packed_sequence` / `build_row_timesteps`。自己 `torch.cat` 是社区微调静默毁权重的主因：行序、`token_tags`、每行的 timestep 索引三者必须一致。
2. `load_components()` 不带 workflow 会拉 **两份** Transformer。
3. 微调可以只训 DiT、冻结 Encoder/VAE，先把目标视频 latent 和文本第 50 层缓存到盘。

## 6. 面试追问

- **为什么取第 50 层不是最后一层？** 官方只给事实不给消融；多模态里中间层常更「可对齐」。未披露对比表。
- **音频为什么不进 Qwen？** 开源路径如此；音频的语义关系靠 IR 文本描述，波形细节靠 AudioVAE latent 在序列里自注意力。

下一站：这 6 万行若没有位置，注意力分不清「第 3 秒左上角」和「第 3 秒的声」。
