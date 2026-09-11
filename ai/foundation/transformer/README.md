# Transformer · 自注意力与序列模型骨架

> 用 **self-attention** 让序列里每个位置直接看其他位置，训练可并行、长距离依赖路径短。一句话：**RNN 靠隐状态接力传话，Transformer 当场开会。**

代表：原论文 Encoder–Decoder（机器翻译）、BERT（Encoder-only）、GPT / 几乎所有现代 LLM（Decoder-only）。RNN / LSTM / GRU 是它取代的前代。

配套 MVP：[mvp.py](./mvp.py)（缩放点积注意力 + 因果掩码 + 和 RNN 隐状态衰减对比）。

> 环节主线（01–11 关卡地图）：见 [环节00-总揽与环节导航.md](./环节00-总揽与环节导航.md)。本页讲**机制本身**（attention / RNN 对比 / 选型），那边讲**一条主线 + 两个生命周期怎么串**。

---

## 一、技术讲解

序列建模要回答：当前位置该融合过去（以及可选的未来）哪些信息。

**RNN**（含 LSTM / GRU）：按时间步走，把历史压进一个隐向量 `h_t`：

```
h_t = f(h_{t-1}, x_t)
```

优点是实现直观、理论上能看任意长历史。硬伤有三：

1. **不能并行**：算 `h_t` 必须先有 `h_{t-1}`，训练一个长句就是一条深链。
2. **长距离衰减**：信息要一跳一跳传；即便 LSTM 用门缓解梯度消失，早期 token 仍容易被冲淡。
3. **路径长度 = 距离**：相隔 n 步的两个词，最短依赖路径也是 n。

Seq2seq 翻译后来加了 **注意力**（Bahdanau / Luong）：解码当前步去对编码器所有隐状态做加权求和。这是「按需查阅」，不再只靠一个向量背全文。

**Self-attention** 把同一套机制用在**同一条序列内部**。每个位置长出三个向量：

| 向量 | 角色 |
|---|---|
| **Q** Query | 我在找什么 |
| **K** Key | 我有什么可被匹配 |
| **V** Value | 匹配上之后贡献的内容 |

缩放点积注意力：

```
Attention(Q, K, V) = softmax(Q Kᵀ / √d_k) V
```

`√d_k` 防止点积随维度变大、softmax 挤成 one-hot。得到的权重矩阵就是「谁在看谁」。

**Multi-head**：把 `d` 拆成 h 组 QKV，各看一种关系（句法、指代、位置邻近……），再拼回去。单头容易塌成一种模式。

一层 Transformer 块（现代预训练常用 Pre-LN）：

```
x → LN → MultiHeadAttn → +x → LN → FFN → +x
```

注意力本身对 token **排列等变**，没有顺序概念，所以要加 **位置信息**（正弦编码、可学习 embedding、RoPE 等）。没有位置，模型分不清「猫吃鱼」和「鱼吃猫」。

三种装配：

| 结构 | 注意力方向 | 典型任务 |
|---|---|---|
| **Encoder–Decoder** | 编码双向；解码因果 + 交叉注意源文 | 原论文翻译 |
| **Encoder-only** | 双向 | BERT 理解 / 分类 / embedding |
| **Decoder-only** | 因果掩码（只能看自己和左边） | GPT、Claude、Qwen 等 LLM |

今天说的「大模型」，默认是 **Decoder-only Transformer + 下一 token 预测**。Encoder-only 还活在 embedding / rerank 里。

---

## 二、功能作用

- **并行训练**：一个 batch 里整句的注意力可一次算完（推理仍常自回归，一个 token 一轮）。
- **短路径长依赖**：任意两个位置一步就能互相看见（在窗口内）。
- **可解释的弱信号**：注意力权重不是因果证明，但调试「模型有没有看见那个约束」时比 RNN 隐状态好读。
- **统一骨架**：文本、[多模态](../multimodal/) token、甚至部分 [扩散](../generative/diffusion/) 骨干都往这套块上靠。
- **工程抓手**：上下文窗口、KV cache、注意力二次复杂度，都从这里来。

---

## 三、应用场景

| 适合 Transformer | 仍可能用 RNN / 卷积 |
|---|---|
| 语言建模、翻译、代码、长文档（窗口内） | 极强流式、状态极小的端侧传感器 |
| 需要全局混合的表征 | 严格逐步、序列很短的控制信号 |
| 预训练 + 迁移的基座 | 数据少、不想上注意力显存账单 |

2026 年新训基座几乎不会从 LSTM 起手。RNN 出现在课、老系统、以及「把历史压成固定状态」的小模块里，不是主力骨架。

---

## 四、RNN / LSTM / Transformer 怎么选（心智模型）

| 维度 | RNN / GRU | LSTM | Transformer |
|---|---|---|---|
| 历史怎么存 | 一个（或少量）隐向量 | 细胞状态 + 门 | 每个 token 自己的 K/V，按需加权 |
| 训练并行 | 差 | 差 | 好（序列长度维） |
| 长距离 | 易丢 | 好于朴素 RNN，仍接力 | 窗口内一步到位 |
| 推理显存 | 小 | 小 | KV cache 随长度涨 |
| 复杂度（长度 n） | O(n) 逐步 | O(n) | 注意力 O(n²)，是长上下文的税 |

LLM 服务里的 **KV cache**：已经算过的 K、V 存下来，新 token 只算自己的 Q 再和历史 K 做点积。所以「接着聊」比「把整段对话当新上下文重算」便宜，直到窗口或显存顶满。这正是 [Context Engineering](../../knowledge/context-engineering/) 要管窗口的原因。

---

## 五、与相邻技术

| 技术 | 关系 |
|---|---|
| [MoE](../moe/) | 通常只替换块里的 FFN；注意力还在 |
| [Multimodal](../multimodal/) | 图/音切成 token，进同一个 Transformer |
| [SLM](../slm/) | 同一骨架，层数/宽度更小，或再量化 |
| [PEFT / LoRA](../peft-lora/) | 常先挂在注意力的 Q/V 上 |
| [Reasoning](../reasoning/) | 推理模型仍是 Transformer，多的是测试时算力和 RL |
| [Speculative Decoding](../../runtime/speculative-decoding/) | 加速的是自回归逐步解码，不是换骨架 |
| [Context Engineering](../../knowledge/context-engineering/) | 窗口 = 注意力能看见的范围；超了等于没看见 |

---

## 六、落地建议

1. **先建立默认图景**：线上聊天模型 ≈ 堆叠 decoder-only 块 + 因果掩码 + 语言模型头。不必为了写业务去手搓一层。
2. **窗口当物理定律**：prompt 塞不进窗口，不是「模型笨」，是注意力根本没看见。超长材料走 [RAG](../../knowledge/rag/) / 摘要，而不是祈祷。
3. **算成本和延迟时分开两笔**：训练看并行；在线解码看逐步前向 + KV 显存。长对话的税在 cache，不在「参数量」一句。
4. **双向 vs 因果不要混**：用 BERT 类模型做补全/聊天会看到「未来」；用 GPT 类做句向量要 pooling / 专用 embedding 模型。
5. **调试「忽略了前文约束」**：先查截断、系统提示是否还在窗口、是否被中间工具结果挤掉，再怀疑权重。

---

## 七、延伸阅读

- Vaswani et al., *Attention Is All You Need*（2017）
- Bahdanau 注意力、LSTM（Hochreiter & Schmidhuber）、GPT / BERT 论文
- 位置：RoPE；长上下文：稀疏 / 线性注意力、MLA（见 [MoE](../moe/) 里的 DeepSeek 路线）
- 环节式长文：11 环节关卡地图见 [环节00-总揽与环节导航](./环节00-总揽与环节导航.md)
- 对比：[moe](../moe/)、[multimodal](../multimodal/)、[context-engineering](../../knowledge/context-engineering/)

---

## 八、本目录 MVP

`mvp.py` 用「猫 吃 了 鱼 它」演示：打印双向注意力「谁看谁」（吃同时看猫和鱼）、加上因果掩码后变成下三角，再对比 RNN 隐状态衰减——句尾代词「它」仍可一步回指「猫」。不依赖 numpy / torch。

环节 01–04 另配 notebook：

- [环节01-Tokenizer分词演示.ipynb](./环节01-Tokenizer分词演示.ipynb)：从零实现字符级 / 字节级 BPE，复现手推合并表，实测词表大小与压缩率的边际收益、字节兜底与 bytes/token。
- [环节02-Embedding查表演示.ipynb](./环节02-Embedding查表演示.ipynb)：编号的三个假象、查表 ≡ one-hot × W_E、梯度只回传命中的行，并用共现 + PPMI 亲手把"猫狗"训近。
- [环节03-位置编码演示.ipynb](./环节03-位置编码演示.ipynb)：排列等变、绝对位置"没卡"、实验 A/B 与通用验证、单档撞车与多档频率表、PI 频率重映射。
- [环节04-Attention演示.ipynb](./环节04-Attention演示.ipynb)：纯 Python 复现 §5 走查、√d_k 饱和实验、并行 ≡ 逐词、多头切维、KV Cache 显存账、FlashAttention 在线 softmax。
