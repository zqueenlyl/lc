# 环节 04 · 补充 · FlashAttention（IO 感知的精确加速）

> 定位：[环节 04 · Attention](./环节04-Attention注意力详解.md) 的深水区补充——回答"同一个注意力公式，为什么所有现代引擎都要换成 FlashAttention 来算"。
> 一句话：**不改数学结果，只改访存方式**——分块（tiling）+ 在线 softmax（online softmax），让 O(n²) 的中间矩阵永远不落盘。
> 适用读者：读完环节 04 §5 数值走查、想弄清"快在哪、等价性怎么保证、decode 为什么受益小"的人。
> 版本口径（2026-09-13）：算法层（tiling / online softmax）多年稳定；FA2/FA3 的 kernel 细节与利用率数字随硬件代际变化，引用前回官方仓库核一遍。

---

## 0. 一句话定位

**FlashAttention 是一种"怎么算注意力"的 I/O 优化**：把 Q/K/V 拆成小块，在 GPU 片上高速缓存（SRAM）里逐块算完注意力，**精确等价**于标准实现，但中间的 n×n 大矩阵（S、P）从不写回慢速显存（HBM）。

先划清三条边界（最常被混淆的）：

| 维度 | FlashAttention 是什么 | 不是什么 |
|---|---|---|
| 数学 | **精确等价**，训练可用 | 不是稀疏/线性注意力那类近似 |
| 结构 | 不改 Q/K/V 定义 | 不属于 MHA/GQA/MLA 那条"改结构"的家族线 |
| 瓶颈 | 砍 HBM 往返（访存优化） | 不减少计算量（FLOPs 基本不变） |

---

## 1. 为什么慢：标准实现的 HBM 往返

GPU 存储是分层的，带宽差一个数量级：

| 存储 | 容量（A100 量级） | 带宽 |
|---|---|---|
| SRAM（片上，每 SM） | ~192 KB/SM | ~19 TB/s |
| HBM（显存） | 40–80 GB | ~1.5–2 TB/s |

标准注意力按环节 04 §2 的公式"照着矩阵写"，至少三次大矩阵落盘：

```
S = Q·Kᵀ/√d   ← 读 Q,K（各 n·d），写 S（n²）      ← 第一次 n² 落盘
P = softmax(S) ← 读 S（n²），写 P（n²）            ← 第二、三次
O = P·V       ← 读 P,V，写 O                        ← 第四、五次
```

n=32k 时，一个头的 S/P 各 1G 元素——**显存既装不下，带宽也扛不住**。而注意力本身是 memory-bound（矩阵乘的 FLOPs 早就被 Tensor Core 吃满过，卡在搬运上），所以砍访存就是砍时间。

FlashAttention 的思路：**把 n² 的中间矩阵"流式"算掉**——每次只把一个小块的 K/V 搬进 SRAM，和已在 SRAM 里的 Q 块算完 softmax 修正与加权求和，结果（O 块）才写回 HBM。HBM 访存量从 Θ(nd + n²) 降到 Θ(n²d²/M)（M = SRAM 大小，[FA1 论文](https://arxiv.org/abs/2205.14135)）；显存占用从 O(n²) 降到 O(n)。

---

## 2. 两个关键技巧

### 2.1 分块（tiling）

把序列切成块：Q 按 query 维切，K/V 按 key 维切。对一个 Q 块，循环扫所有 K/V 块，每轮在 SRAM 里算出局部 S 块——问题来了：**softmax 本来是"看全行"的归一化，只看到一块怎么归一？**

### 2.2 在线 softmax（online softmax）——等价性的全部秘密

给每行维护三个 running 量：

```
m：至今见过的最大分数（防 exp 溢出，等价于标准 softmax 的 max 减法）
l：至今的指数和（分母，未定版）
acc：至今的加权输出（分子，未定版 O = acc / l）
```

每来一个新块，先"看看有没有更大的数出现"，再把旧的账全部按比例修正：

```
m_new = max(m_old, m_block)
α     = e^(m_old − m_new)                        # 旧账的修正因子（≤1）
l_new = α·l_old + Σ_j e^(s_j − m_new)
acc_new = α·acc_old + Σ_j e^(s_j − m_new)·v_j    # 旧的加权输出整体缩 α
```

扫完所有块：**O = acc / l**。

为什么精确等价：标准 softmax 对每行做 `e^(s_i − max)/Σe^(s_j − max)`——online 版只是把"先知道 max 再算"改成"边算边修正 max"。任何时刻的 (m, l, acc) 都是"假设后面没有更大的数"时的正确账；一旦出现更大的数，α 一次性把历史账全部换算到新基准，最终结果与一次算完整行**逐位相同**。

> 记忆钩子：**max 是锚，l 是分母，acc 是分子；新块来了 → 换锚（α）→ 补账（l、acc）→ 最后除一次。** 手推最容易错的一步就是忘了给旧 acc 乘 α。

### 2.3 反向传播怎么办

训练需要梯度。FA 的做法：**不存 n² 的 P，只存最后的 O 和归一化统计量（m, l）**，反向时用重计算（recompute）在 SRAM 里重新算出所需的 P 块——用少量重算（约 +1 次 forward 的 FLOPs 的一部分）换掉 n² 显存。这就是"训练也能用"的原因。

---

## 3. 数值走查：把环节 04 §5 的行 2 分两个块重算

**设定**（与 [环节 04 §5](./环节04-Attention注意力详解.md) 完全同款玩具）：位置 c（行 2）可见 a、b、c 三个 token，分数 `s = [0, 0, 0.5]`，V 就是三个词向量 a=[1,0,0,0]、b=[0,1,0,0]、c=[0,0,1,0]。

标准 softmax（§5 已算过）：

```
l = 1 + 1 + e^0.5 = 3.64872
O2 = [1, 1, 1.64872, 0] / 3.64872 = [0.27407, 0.27407, 0.45186, 0]
```

现在按 **B=2 分块**：块 1 = {a, b}（分数 [0, 0]），块 2 = {c}（分数 [0.5]）。

**初始**：m = −∞，l = 0，acc = [0,0,0,0]。

**块 1（分数 [0, 0]）**：

```
m_blk = 0          →  m = max(−∞, 0) = 0
l = e^0 + e^0 = 2
acc = 1·a + 1·b = [1, 1, 0, 0]
```

**块 2（分数 [0.5]）**——出现更大的数，触发换锚：

```
m_blk = 0.5        →  m = max(0, 0.5) = 0.5
α = e^(0 − 0.5) = 0.60653          # 旧账整体缩
l = 0.60653·2 + e^(0.5−0.5) = 1.21306 + 1 = 2.21306
acc = 0.60653·[1,1,0,0] + 1·c = [0.60653, 0.60653, 1, 0]
```

**收尾**：

```
O2 = acc / l = [0.60653, 0.60653, 1, 0] / 2.21306 = [0.27407, 0.27407, 0.45186, 0]
```

**与标准 softmax 逐位一致**（§5 行 2，末位 ±1 为舍入差）。这就是"精确等价"的肉眼版证明：分块 + 换锚修正，最后除以总 l，账永远是对的。

纯 Python 验证：

```python
import math
s_blocks = [[0.0, 0.0], [0.5]]                 # 两块分数
v = {0:[1,0,0,0], 1:[0,1,0,0], 2:[0,0,1,0]}    # a, b, c
m, l, acc = -math.inf, 0.0, [0.0]*4
for bi, blk in enumerate(s_blocks):
    for j, s in enumerate(blk):
        idx = sum(len(b) for b in s_blocks[:bi]) + j   # 全局位置
        m_new = max(m, s)
        alpha = math.exp(m - m_new) if m != -math.inf else 0.0
        w = math.exp(s - m_new)
        l = alpha*l + w
        acc = [alpha*a + w*x for a, x in zip(acc, v[idx])]
        m = m_new
O = [a/l for a in acc]
print([round(x, 5) for x in O])   # [0.27407, 0.27407, 0.45186, 0]
```

> 对照：[环节04-Attention演示.ipynb](./环节04-Attention演示.ipynb) 的 FlashAttention 单元用同一套 (m, l, acc) 走查过整行矩阵版，可逐格跑。

---

## 4. FA1 → FA2 → FA3：演进只改"怎么排兵"

算法内核（§2 的 tiling + online softmax）三代不变，变的是 GPU 上的并行与流水线排布：

| 版本 | 年份/硬件 | 改了什么 | 收益 |
|---|---|---|---|
| **FA1** | 2022 / A100 | tiling + online softmax + 反向重计算，确立"IO 感知"范式 | 注意力真速（2–4×），显存 O(n²)→O(n)；利用率 ~25–40% |
| **FA2** | 2023 / A100+ | **沿序列维也并行**（长序列吃满 SM）、减少非 matmul FLOPs、调 warp 分工减少共享内存往返 | 正向比 FA1 快约 2×，利用率 ~50–73% |
| **FA3** | 2024 / H100 | warp specialization + 异步流水线（TMA/WGMMA 把搬运与计算重叠）、FP8 量化支持（带周期性反量化保精度） | H100 上比 FA2 再快 1.5–2× |

一句话：**FA1 解决"不做无用搬运"，FA2 解决"SM 吃不满"，FA3 解决"搬和算不等相互等"。**

---

## 5. 推理侧定位：prefill 受益大，decode 受益小

接 [环节 11](./环节11-服务化与推理引擎详解.md) §1 的两阶段框架：

| 阶段 | 瓶颈 | FlashAttention 的作用 |
|---|---|---|
| **Prefill** | 计算密集 + n² 中间矩阵落盘 | **主战场**：整条 prompt 一次算，S/P 矩阵最大，砍访存收益最明显；长上下文 prefill 显存从 O(n²) 降为 O(n)，长 prompt 才"装得下" |
| **Decode** | 访存密集——每步只算 1 个 query，时间花在读 KV Cache 上 | 受益小：query 侧只有 1 行，n² 中间矩阵本来就只有 1 行，没有"大矩阵落盘"问题；decode 的药方是 PagedAttention（显存布局）、GQA/MLA（砍 KV 体积）、批处理（带宽摊薄） |

与相邻优化的正交关系（可全部叠加）：

```
FlashAttention：改"注意力怎么算"（访存）      —— 所有现代引擎默认启用
PagedAttention：改"KV Cache 怎么放"（显存碎片） —— vLLM 系
GQA / MLA    ：改"KV Cache 存多少"（结构）      —— 模型出厂即定
投机解码      ：改"一步走多远"（算法）          —— 见 [环节 10](./环节10-推理解码与KV缓存详解.md)
```

---

## 6. 常见坑

1. **以为它让 decode 也快很多**——decode 瓶颈是 KV 读取带宽（[环节 11](./环节11-服务化与推理引擎详解.md) §1），FA 主要加速 prefill 与训练。
2. **以为它是近似算法**——精确等价，训练/评测可放心替换。
3. **手推 online softmax 忘了给旧 acc 乘 α**——换锚不修旧账，结果直接错（§3 块 2 那一步）。
4. **benchmark 前没确认真的启用了**——老 GPU（FA2 需 Ampere+）、非常规 head_dim、CPU 后端，很多框架会静默回退到朴素实现。
5. **短序列收益小**——n 小时 n² 中间矩阵本来就不大，HBM 往返不是瓶颈，别拿 n=512 的实验否定 FA。
6. **MLA 与 FA 的适配 historically 有摩擦**——DeepSeek MLA 的 KV 压缩形态与标准 FA kernel 的假设不完全对齐，各家引擎走的是吸收进 kernel（如 FlashMLA）或展开后走 FA 的不同路线，选型时按引擎文档确认。

---

## 7. 面试高频追问

1. **FlashAttention 为什么快？** IO 感知：注意力是 memory-bound，标准实现把 n² 的 S/P 反复读写 HBM；FA 分块 + 在线 softmax 让中间矩阵只在 SRAM 内流转，HBM 访存 Θ(nd+n²)→Θ(n²d²/M)，显存 O(n²)→O(n)。
2. **和稀疏/线性注意力是一类吗？** 不是。它们改数学（近似、丢远距离直连），FA 改访存方式，结果逐位一致——这也是它能进训练栈的原因。
3. **在线 softmax 怎么保证精确等价？** 维护 (m, l, acc) 三量，新块出现更大分数时用 α=e^(m_old−m_new) 把历史账整体换锚（§2.2 公式），最终除一次 l——数学上就是标准 softmax 的 max 减法，只是把"先知道 max"改成"边算边修"。
4. **训练时反向传播没有 P 矩阵怎么办？** 只存 O 和 (m, l)，反向重计算 P 块，用少量重算换 n² 显存。
5. **FA2 相对 FA1 快一倍的原因？** 并行排布：FA1 按 batch×head 并行，长序列时 SM 吃不满；FA2 沿序列维也切并行 + 减少非 matmul FLOPs + 优化 warp 分工。
6. **decode 阶段为什么不用指望它？** decode 每步只有 1 个 query，中间矩阵只有 1 行，无 n² 落盘问题；瓶颈在 KV Cache 读取带宽，归 PagedAttention/GQA/批处理管（§5）。

---

## 8. 相关笔记

- 主环节：[环节 04 · Attention 注意力](./环节04-Attention注意力详解.md)（§3 家族表中 FlashAttention 的定位行）
- 配套 Notebook：[环节04-Attention演示.ipynb](./环节04-Attention演示.ipynb)（在线 softmax 整行走查，本文 §3 是其"分块版"）
- 生成侧细节：[环节 10 · 推理解码与 KV 缓存](./环节10-推理解码与KV缓存详解.md)（投机解码 / KV 账）
- 服务化视角：[环节 11 · 服务化与推理引擎](./环节11-服务化与推理引擎详解.md)（prefill/decode 两阶段与优化清单）
- 参考：FlashAttention 论文 [arXiv:2205.14135](https://arxiv.org/abs/2205.14135)、FA2 [arXiv:2307.08691](https://arxiv.org/abs/2307.08691)、官方仓库 [Dao-AILab/flash-attention](https://github.com/Dao-AILab/flash-attention)
