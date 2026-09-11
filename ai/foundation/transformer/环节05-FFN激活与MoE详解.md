# 环节 05 · FFN（Feed-Forward Network，前馈网络）/ 激活函数 / MoE（逐 token 加工）

> 全链路第五站：Attention 负责"搬运信息"，FFN 负责"加工信息"——参数量大头在这里。
> 所属总揽：[环节00-总揽与环节导航.md](./环节00-总揽与环节导航.md) 环节 05。
> 相邻环节：上一站 [环节 04 · Attention](./环节04-Attention注意力详解.md) → 下一站 [环节 06 · 残差连接与归一化](./环节06-残差连接与归一化详解.md)（结构上 FFN 与 Attention 同在一个 Block 内）。

---

## 1. 干什么

Attention 只做"词与词的信息搬运"，**不做复杂的逐点变换**。若只堆 Attention，深层网络的每个位置仍是输入的加权组合，表达力不足。FFN 对每个 token 的向量**独立做一次大宽度的非线性变换（nonlinear transformation）**（升维 → 激活 → 降维），是模型"思考加工"发生的地方，也是**参数量大头**（约占 2/3）。

核心直觉：Attention 让 token **互相看**（跨位置），FFN 让每个 token **自己深想**（逐点变换，position-wise）——两者交替构成一层 Block 的完整语义。

---

## 2. 怎么干（标准结构）

```
FFN(x) = W_down · σ(W_up · x)
W_up 把 d 维升到 ~4d（或 8/3·d），σ 为激活函数，W_down 再降回 d
```

> 注：LLaMA/Qwen 等主流实现采用带门控（gated）的变体，参数量是标准版的三组矩阵（见 §3 的 SwiGLU）。

---

## 3. 激活函数（activation function）与方法对比

| 激活 | 公式/要点 | 优点 | 缺点 | 使用 |
|---|---|---|---|---|
| ReLU | max(0,x) | 极简、快 | 负半轴死区、训练不稳 | 老 Transformer |
| GELU | x·Φ(x)（高斯近似） | 平滑、负值有小梯度，深层更稳 | 稍贵 | BERT 及早期 GPT |
| **SwiGLU** | 门控线性单元（gated linear unit，GLU）：`FFN(x) = (SiLU(x·W_gate) ⊙ (x·W_up))·W_down` | 门控 = 让网络"决定放多少信息过"，效果公认最好 | 多一组矩阵、参数量+ | LLaMA/Qwen/DeepSeek 全系事实标准 |

**为什么 SwiGLU 成了事实标准**：它把"激活"升级成"门控"——一个线性投影（linear projection）的输出（经 SiLU（Sigmoid Linear Unit）= x·σ(x)）去**控制另一个线性投影放行多少**（即门控 gating）。信息流有了"阀门"，网络能学着只在需要时放行，深层表达能力与训练稳定性都更好。代价是多一组 `W_gate`，参数量约 +1/3。

> 面试点：问"激活函数选型"，答 ReLU（快但不稳）→ GELU（平滑）→ **SwiGLU（门控，主流）**；顺带能说出 LLaMA 三层组合的"便宜/稳/好"逻辑会加分（配合 [环节 06](./环节06-残差连接与归一化详解.md)）。

---

## 4. MoE（Mixture of Experts，混合专家：把 FFN 换成多个专家）

### 4.1 为什么需要 MoE

稠密模型（dense model）每层 FFN 只有一个，所有参数每个 token 都得算（**参数 = 激活参数（activated parameters）**）。模型要变大，推理算力与显存同步爆炸。MoE 的路线：**总参数大幅增大，但每个 token 只激活一小部分**——用显存换"大容量 + 小激活"。

### 4.2 怎么干

```
MoE 层：K 个"专家 FFN" + 1 个 Router（门控）
Router(x) 输出对每个专家的打分 → 取 Top-K → 按分数加权混合被选中专家的输出
部署：专家并行（EP）把专家摊到多卡
```

DeepSeek 的工程变体（DeepSeekMoE，V3 采用）：**细粒度（fine-grained）专家 + 共享专家（shared experts）**（部分专家常驻必算，处理通用模式）+ **无辅助损失（auxiliary loss，aux-loss）负载均衡（load balancing）**（用偏置（bias）/路由（router）调度替代传统 aux-loss，避免训练不稳定）。

### 4.3 稠密 vs MoE 对照

| | 稠密 | MoE |
|---|---|---|
| 总参数 | 全部激活 | **大（如 671B）** |
| 每 token 激活 | 全部 | 少（DeepSeek-V3 约 37B/671B） |
| 单 token 推理算力 | 高 | 低（≈ 只算激活部分） |
| 显存 | 小 | **大（所有专家必须驻留）** |
| 训练 | 稳 | 需负载均衡（防专家坍缩：个别专家被宠坏、其余饿死） |
| 吞吐（throughput）与成本 | 基准 | 同成本容量大，服务端性价比高 |

**取舍口诀**：MoE = **用显存换"大容量 + 小激活"**。为什么 DeepSeek 671B 能单机低成本推理：MLA（KV 极小，见 [环节 04](./环节04-Attention注意力详解.md)）+ MoE（每 token 激活 ~37B）+ 引擎调度（见 [环节 11](./环节11-服务化与推理引擎详解.md)）。

### 4.4 MoE 的典型坑

1. **专家坍缩（expert collapse）/ 负载不均**：Router 偏爱少数专家 → 其余饿死 → 需要负载均衡策略（aux-loss 或无辅助损失变体）；
2. **显存驻留**：所有专家必须常驻显存，小显存单卡跑不动 MoE 大模型；
3. **路由抖动（routing instability）**：不同 token 走不同专家，影响批量矩阵乘（matrix multiplication）的效率与缓存局部性（cache locality）。

---

## 5. 面试高频追问

1. FFN 与 Attention 的分工？→ 前者逐 token 非线性加工（参数大头），后者跨位置交换信息。
2. SwiGLU 相比 GELU/ReLU 好在哪里？→ 门控机制让网络决定信息放行量，表达力与稳定性更好；代价是参数 +1/3。
3. MoE 的"大参数小激活"是什么 trade-off？→ 用显存（驻留全部专家）换推理算力（每 token 只算 Top-K 专家）。
4. 专家坍缩怎么防？→ 负载均衡：aux-loss、共享专家兜底、无辅助损失路由（DeepSeek 路线）。
5. 为什么 MoE 对服务端更友好？→ 同成本下容量更大，激活参数少 → 单位算力吞吐高。

---

## 6. 相关链接

- 入口总揽：[环节00-总揽与环节导航.md](./环节00-总揽与环节导航.md)
- 上一站：[环节 04 · Attention 注意力](./环节04-Attention注意力详解.md)
- 下一站：[环节 06 · 残差连接与归一化](./环节06-残差连接与归一化详解.md)
- 主流模型落点：DeepSeek（MoE + MLA）见 [learning-path.md](../../learning-path.md) 1.2 / 1.7
- 知识地图：[learning-path.md](../../learning-path.md)
