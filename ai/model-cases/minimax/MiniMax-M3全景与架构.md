# MiniMax-M3 全景与架构

> 调研时间：2026-09-18 ｜ 范围：MiniMax **M 系列**对话旗舰 `MiniMaxAI/MiniMax-M3`，不是 H 系视频、不是 Speech / Music3
> 口径：官方发布博客、HF 模型卡、[MSA 论文 arXiv:2606.13392](https://arxiv.org/abs/2606.13392)、[MaxProof arXiv:2606.13473](https://arxiv.org/abs/2606.13473)。产品线地图见 [《MiniMax 全景与产品线》](./MiniMax全景与产品线.md)。
> 聊天接口字段仍有 SPA 抓取缺口，端点级以 [providers · MiniMax](../providers/各大厂商代表模型总览.md#36-minimax) 为准，未核实处不编造。

---

## 一、摘要（TL;DR）

1. **M3 是原生多模态 MoE 对话模型**：约 **428B** 总参、每 token 激活约 **23B**，窗口 **1M**。图和视频是**输入**（理解），输出仍是文本。出片请走 H3。
2. **长上下文靠 MiniMax Sparse Attention（MSA）**，不是把 H3 里「后续再开源」的稀疏注意力套过来。MSA 有独立论文；M3 模型卡相对 M2、在 1M 上宣称 prefill **9×**、decode **15×**、每 token 算力约 **1/20**。
3. **思考三档**：请求参数 `thinking` = `enabled` / `adaptive` / `disabled`。官方推荐采样 `temperature=1.0`、`top_p=0.95`。
4. **MaxProof 是测试时框架，不是另一份权重。** 生成 / 校验 / 修补能力 merge 进发布的 M3；推理时用种群进化搜索。带 MaxProof 的 IMO 2025 / USAMO 2026 分数不要当成「单次 greedy」口径。
5. **谱系**：M2 → M2.1 / M2.5 → M2.7（2026-03，自称参与自身进化）→ **M3**（2026-06）。旧档还在 HF，不要和 M3 混 ID。

**核心判断**：M 系的论文完整度明显高于 H3——注意力机制和数学证明 TTS 都有 arXiv。缺的是一份「M3 训练全账」式总报告（数据配比、卡时、MoE 路由超参仍以模型卡 + 博客为主）。

---

## 二、产品面

| 面 | 入口 |
|----|------|
| 权重 | HF [`MiniMaxAI/MiniMax-M3`](https://huggingface.co/MiniMaxAI/MiniMax-M3)；另有 `MiniMax-M3-MXFP8` |
| Agent 产品 | MiniMax Agent / MiniMax Code（官方称与 M3 一起训） |
| API | 全球 `platform.minimax.io` ｜ 国内 `platform.minimaxi.com` |

本地推理栈（模型卡）：SGLang cookbook、vLLM recipes、Transformers、KTransformers、unsloth、ATOM（MXFP4/MXFP8）。

`config.json` 架构名：`MiniMaxM3SparseForConditionalGeneration` / `model_type: minimax_m3_vl`。稀疏块：`sparse_block_size=128`、`sparse_topk_blocks=16`、`sparse_num_index_heads=4`；前几层关闭稀疏（`sparse_attention_freq` 前三项为 0）。vLLM 侧社区说明需 `--block-size 128`，与块大小对齐。

---

## 三、MiniMax Sparse Attention（MSA）

论文定位：在 GQA 上做**块级内容稀疏**，故意做薄，方便在各代 GPU 上落地。推理核：[github.com/MiniMax-AI/MSA](https://github.com/MiniMax-AI/MSA)。

```
Query
  ├─ Index Branch（轻量）：给每个 GQA 组打分，Top-k 个 KV 块（默认 k=16，块 128 token）
  │     局部块必留；训练时 KL 对齐 Main 的组平均分布，Index 梯度与 Main 断开
  └─ Main Branch：只在选中块上做精确 block-sparse attention
GPU：exp-free Top-k；KV-outer 聚 Q，一块 KV 只读一次
```

论文数字（**109B 原生多模态试验台**，不是 428B M3 本体；H800）：相对 GQA，1M 上每 token 注意力算力 **28.4×** 下降；墙钟 prefill **14.2×**、decode **7.6×**。M3 模型卡上的 9× / 15× 是**相对前代 M2、在 M3 配置下**的产品口径，不要和论文试验台混成一张表。

官方博客相对 DSA / MoBA 的主张：块切得更细、有效覆盖更高；算子用「KV 在外、聚 Q」，自述比开源 Flash-Sparse-Attention / flash-moba 快 4× 以上。这是厂商对比，未在本页复现。

机制对照见 [长上下文工程详解](../../foundation/transformer/长上下文工程详解.md) §2.3（内容相关稀疏）。DeepSeek DSA 是 indexer 打分式；MSA 是 **GQA 组独立的块 Top-k**。不要把两套超参互换。

---

## 四、原生多模态与 Agent

博客口径：

- **从 Step 0 混合模态训**，图/视频与文本语义空间一起长；并称 interleaved 真实数据比合成数据更好 scale，为此重做了文本预训练管线。
- 能力组合官方自我定位：长窗 + 代码/Agent + 原生多模态，开源权重里「三个都给」的当时仅 M3（厂商叙事，截至发布博客）。
- 能 **computer use**（桌面操作）。MiniMax Code 的 Agent Team：拆任务、Producer+Verifier 对抗循环。
- 编码评测（博客数字，脚手架与超时见原文脚注）：SWE-Bench Pro 59.0%；Terminal-Bench 2.1 66.0%；SWE-fficiency 34.8%；KernelBench Hard 28.8%；MCP Atlas 74.2%。

博客里的长程演示（**单次内部任务，不是标准榜**）：12 小时复现 ICLR 论文；约 24 小时、147 次提交把 Hopper FP8 GEMM 峰值利用率 7.6% → 71.3%。用来理解「1M + Agent」要一起用，不能当 SLA。

---

## 五、MaxProof（测试时，不是新模型）

[博客 2026-06-09](https://www.minimax.io/blog/minimax-maxproof-math-proof-evolution) / [arXiv:2606.13473](https://arxiv.org/abs/2606.13473)。

训练侧三个专家（证明生成、校验、按批评修补）再 merge 进发布的 M3。推理侧 MaxProof 把同一份权重当成 generator / verifier / refiner / ranker，种群搜索 + 锦标赛选出一条证明。

带 TTS 的成绩（论文）：IMO 2025 **35/42**、USAMO 2026 **36/42**（过人类金牌线）。M3 博客里的数学表另有「最多 10 轮、512k 输出」的评测设定。引用分数时必须写清是否开 MaxProof。

---

## 六、许可证与未披露

HF 标 `minimax-community`。第三方对 LICENSE 的转述含非商用默认、商用需显著「Built with MiniMax M3」、年营收超约 2000 万美元须事先书面授权。**领土是否与 H3 一样排除美/欧/英/韩：以 M3 仓库 LICENSE 原文为准，不要从 H3 条款抄过来。**

| 项 | 状态 |
|----|------|
| 完整 M3 训练报告（token 量、卡时、专家数、路由） | 未见独立长报告；MSA / MaxProof 只覆盖切片 |
| 1M 的**有效**窗口（vs 标称） | 未给 MRCR 类衰减曲线 |
| `thinking=adaptive` 的判定规则 | 未披露 |
| 图/视频输入的抽帧、分辨率、token 计价 | 本快照未在 API 正文核实 |
| M2.7「自我进化」的可复现实验协议 | 博客叙事，未开训练日志 |

---

## 七、参考来源

- [MiniMax M3 发布博客](https://www.minimax.io/blog/minimax-m3)
- [HF MiniMaxAI/MiniMax-M3](https://huggingface.co/MiniMaxAI/MiniMax-M3)
- [MiniMax Sparse Attention](https://arxiv.org/abs/2606.13392) · [MSA 核](https://github.com/MiniMax-AI/MSA)
- [MaxProof](https://arxiv.org/abs/2606.13473) · [MaxProof 博客](https://www.minimax.io/blog/minimax-maxproof-math-proof-evolution)
- [M2.7 博客](https://www.minimax.io/blog/minimax-m27)
- 视频线：[H3 全景](./MiniMax-H3全景与架构.md)
