# 本地推理压测：方法与本机实测

> 一句话：**「谁快」这个问题没有答案，除非先锁住口径**——本文先讲清 prefill / decode / TTFT / 峰值内存**怎么测才可比**，再给出同一台 Mac 上 llama.cpp / Ollama / MLX 的实测对照表。
> 前三篇是「怎么跑起来」（[llama-cpp.md](./llama-cpp.md) / [ollama.md](./ollama.md) / [lm-studio.md](./lm-studio.md) / [mlx.md](./mlx.md)），这篇是「跑起来之后，数字怎么读」。
>
> **核查日期**：2026-09-12，**全部为本机实测**
> 测试机：**Apple M4 Pro / 48GB 统一内存 / macOS 26.6.2**；官方内存带宽 **273 GB/s**（同代普通 M4 为 120 GB/s，**不要拿别的机型套本文结论**）
> 软件：llama.cpp v0.4.0 (build 10809, `5266f24da`) ｜ Ollama 0.33.3 ｜ `mlx-lm` 0.31.3 + `mlx` 0.32.2
> 主测模型：**Qwen3-0.6B**（三后端都有，用来做"同模型"对照）

---

## 一、先记住三个数：273 / 0.6 / 40960

在开始之前，先把本文全部结论压成三句话：

| # | 事实 | 含义 |
|---|---|---|
| 1 | 本机统一内存带宽 **273 GB/s** | decode 的理论天花板按这个算；`decode tok/s ≈ 273 ÷ 每 token 权重字节数`（**有效值通常只有 40%~90%**，见 §六） |
| 2 | 0.6B 模型的"固定开销"约 **1.6 ms/token** | 小模型不是带宽受限，是**每次 forward 的固定开销**（kernel 启动、采样、Python 循环）在主导。所以 **小模型的 tok/s 不能用来推算大模型** |
| 3 | Ollama 本机默认上下文给到 **40960（0.6B）/ 262144（9B）** | 一个 522MB 的 0.6B 模型，默认驻留 **5.6GB**——**KV Cache 才是本地推理内存的主体，不是权重** |

---

## 二、五个"不可比"陷阱（本节是全文最重要的一节）

### 陷阱 1：拿错指标 —— prefill 与 decode 是两种完全不同的负载

| 阶段 | 并行度 | 瓶颈 | 对量化敏感 | 对 batch 敏感 |
|---|---|---|---|---|
| **prefill**（处理 prompt） | 整段一次性并行 | **算力**（矩阵乘） | 低 | 低（本来就并行） |
| **decode**（逐 token 生成） | 每步 1 个 token | **内存带宽** | **高** | **高** |

所以：
- **「量化后快了多少」这句话只在 decode 上成立**（本机实测 4x 提升，见 §五）；
- **「batch 加大后吞吐涨了多少」也只在 decode 上成立**（本机实测 8 路 → 2.8×）；
- prefill 在两个维度上几乎不动（本机实测 512→8 路只从 5537 涨到 6362）。

误把 prefill 数字当"模型速度"、或把两个阶段的数字混在一张表里比，是最常见的错误。原理见 [环节11 §1](../../foundation/transformer/环节11-服务化与推理引擎详解.md)。

### 陷阱 2：没对齐上下文预算 —— Ollama 侧的数字会被 KV Cache 污染

**同一个 0.6B 模型，同一台机器，只改 `num_ctx`：**

| `num_ctx` | `ollama ps` 的 SIZE |
|---|---|
| 1024 | **671 MB** |
| 4096 | **1.0 GB** |
| 40960（本机默认） | **5.6 GB** |

差 **8 倍**。拿 5.6GB 去和 MLX 的 0.9GB 比"谁省内存"，比的是**上下文预算**，不是引擎。

⚠️ Ollama 的默认上下文**不是固定 4096**：官方文档（`docs.ollama.com/context-length`）给的是**按 VRAM 档位**取默认值（<24GiB → 4k；24–48GiB → 32k；≥48GiB → 256k），本机实测则进一步**被模型自身的最大上下文截断**：

- `qwen3:0.6b`（`max_position_embeddings` = 40960）→ 默认 **40960**
- `qwen3.5:9b`（最大 262144）→ 默认 **262144**，`ollama ps` 显示驻留 **15 GB**

**结论：任何内存对比前先 `ollama ps` 看实际 `CONTEXT`，并显式设 `num_ctx`（或服务端 `OLLAMA_CONTEXT_LENGTH`）。**（本机 0.33.3 实测值与文档档位换算存在偏差，**一律以 `ollama ps` 实测为准**。）

### 陷阱 3："同模型"不等于"同精度/同体积"

`Qwen3-0.6B` 的 4-bit 有两种常见产物，**差 54%**：

| 产物 | 体积 | 量化算法 |
|---|---|---|
| MLX 4-bit（`mlx-community`） | **336 MB** | affine，group_size 64，全张量统一 4-bit |
| GGUF `Q4_K_M`（Ollama 内置） | **517 MB** | K-quant 混合精度（部分张量 6-bit） |

MLX 那份**更激进**，所以它跑得快里有一部分**不是引擎的功劳**。真正隔离引擎差异必须**锁精度**（本机补测了双方 16-bit 版本，见 §四）。

### 陷阱 4：冷启动 vs 热态

| 现象 | 本机数据 |
|---|---|
| Ollama 首次请求（含加载模型） | TTFT **868 ms** |
| 同一 prompt 第二次（命中 **prompt 前缀缓存**） | TTFT **23 ms** |
| MLX server 首次请求 | TTFT **172 ms** → 热态 **88 ms** |

**prompt 前缀缓存是最大的伪信号**：Omni 助手/多轮对话/RAG 都会复用 system prompt 与历史，命中缓存后 TTFT 可以掉到 1/30。**做 TTFT 对比时必须让每次请求的 prompt 前缀不同**（本机做法：在 prompt **开头**插入一个变化的 nonce——放结尾没用，前缀仍然命中）。

### 陷阱 5：软件版本

本地推理工具的参数名、默认值、量化方案迭代极快。本机 llama.cpp 已从 `bXXXX` 改为语义化 **v0.4.0**，`--no-mmap`/`--mlock` 被 `-lm/--load-mode` 取代；Ollama 0.33.3 与官方文档的上下文档位说明已出现偏差。**任何数字都必须连同版本号一起记，否则半年后无法复核。**

---

## 三、测什么、怎么测（口径对照表）

| 指标 | 定义 | llama.cpp | Ollama | MLX |
|---|---|---|---|---|
| **prefill 吞吐** | prompt 处理速度（tok/s） | `llama-bench -p 512` | `prompt_eval_count / prompt_eval_duration` | `mlx_lm.benchmark -p 512` |
| **decode 吞吐** | 生成速度（tok/s） | `llama-bench -n 128` | `eval_count / eval_duration` | `mlx_lm.benchmark -g 128` |
| **TTFT** | 请求发出 → 第一个 token | server 返回的 `timings.prompt_ms` | 需客户端 streaming 计时 | 需客户端 streaming 计时 |
| **TPOT** | 相邻 token 的平均间隔 | `timings.predicted_per_token_ms` | 同上 | 同上 |
| **峰值内存** | 进程/设备峰值占用 | ⚠️ `llama-bench` 不报 | `ollama ps` 的 `SIZE` | `mlx_lm.benchmark` 的 `peak_memory` |
| **冷加载耗时** | 从磁盘到可服务 | logs 时间戳 | `load_duration` | server 启动日志 |

**三条纪律**：

1. **裸引擎的吞吐用各自的 benchmark 工具**（`llama-bench` / `mlx_lm.benchmark`），它们有 warmup、多次取平均、无 HTTP 开销；
2. **服务端体验（TTFT/TPOT）用 streaming 客户端实测**，把每 token 的 HTTP/SSE 开销算进去——这两个数常常给出**相反的排名**（本机实测见 §四.3）；
3. **prompt / generation 长度必须写进结果里**，`p512` 和 `p168` 的 prefill 差 30%（本机实测：4287 vs 5568）。

**TTFT/TPOT 的最小可用测法**（本机用的就是这段逻辑，约 20 行）：

```python
t0 = time.perf_counter()
for line in <SSE 流>:
    text = delta 里的 content / reasoning / reasoning_content
    if text and ttft is None:          # 第一个有内容的块
        ttft = time.perf_counter() - t0
total = time.perf_counter() - t0
tpot = (total - ttft) / (output_tokens - 1)
```

⚠️ 解析时要同时认三个字段：`content`、`reasoning`（MLX 用）、`reasoning_content`（llama.cpp 用）——只认 `content` 会把思考型模型的输出全判成空。

---

## 四、本机实测：Qwen3-0.6B 三后端对照

### 4.1 同档位（4-bit）：日常推荐配置下的对照

| 后端 | 引擎 | 权重 | prefill tok/s | decode tok/s | 峰值内存 | 取数方式 |
|---|---|---|---|---|---|---|
| **MLX** | `mlx-lm` 0.31.3 | 336 MB | 5568 | **349.3** | 0.918 GB | `mlx_lm.benchmark -p 512 -g 128 -b 1` |
| **llama.cpp** | v0.4.0 (b10809) | 492.75 MiB（517 MB） | **5820.7 ± 14.5** | 282.8 ± 4.1 | — | `llama-bench -p 512 -n 128 -r 3` |
| **Ollama** | 0.33.3（内部 llama.cpp） | 522 MB blob | — | 274.2 | 5.6 GB（默认 ctx）/ 1.0 GB（ctx 4096） | `/api/generate` 的 `eval_*` 字段 |

**读法**：
- **MLX decode 领先 llama.cpp 约 23.5%，prefill 落后约 4.3%**；
- **Ollama decode 与裸 llama.cpp 差 3.0%**——与 2026-09-11 在另一模型上的结论（115.5 vs 117，差 1%）一致。**「Ollama 慢」不是慢在单请求吞吐，而是慢在默认并发（`OLLAMA_NUM_PARALLEL=1`）与参数粒度**；
- 三者 prefill 都在 5.5k~5.8k 量级，说明 prefill 早就被算力打满，**换引擎几乎没用**。

### 4.2 同精度（16-bit）：把"量化算法差异"剔掉

| 后端 | 精度 | 权重 | prefill tok/s | decode tok/s |
|---|---|---|---|---|
| MLX | bf16 | 1.192 GB | 5521.7 | **162.8** |
| llama.cpp | F16 | 1.503 GB（1.40 GiB） | **5983.7 ± 92.3** | 149.7 ± 1.7 |
| 差值 | — | MLX 小 21% | MLX **−7.7%** | MLX **+8.8%** |

**这张表是本文最有价值的一行**：锁住精度后，**MLX 的 decode 优势从 23.5% 缩到 8.8%**，剩下的 15 个百分点来自"MLX 的 4-bit 比 `Q4_K_M` 更小"。

→ **比较「引擎」要看同精度；比较「你会怎么配」才看同档位。** 两个结论都对，但必须说清是哪一个。

### 4.3 服务端体验：TTFT / TPOT（同一 prompt ≈166 token，输出 ≈62 token）

| 运行时（端口） | TTFT | TPOT | 等效 decode | 备注 |
|---|---|---|---|---|
| `llama-server`（:8081） | **18–33 ms** | 3.79–3.93 ms | 254–264 tok/s | TTFT 最低 |
| Ollama（:11434） | 50–70 ms | 3.65–3.89 ms | 257–274 tok/s | |
| `mlx_lm.server`（:8080） | **116–150 ms** | **3.46–3.67 ms** | **272–289 tok/s** | TPOT 最低、TTFT 最高 |

**这张表推翻了 §4.1 的排名**：MLX 裸框架 decode 349 tok/s 最快，但**走 HTTP 服务后掉到 ~280**，与 GGUF 路线拉平。
→ **「MLX 比 llama.cpp 快 23%」只在裸调用/批处理时成立；一旦套上 server，优势基本被服务层开销吃掉。**

另附 `llama-server` 自己吐的 `timings`（最可靠的单项数据来源）：

```
prompt_n=168  prompt_ms=106.3   → prefill 1580.5 tok/s
predicted_n=128 predicted_ms=516.9 → decode 245.7 tok/s
```

⚠️ 注意 168-token 的 prefill 只有 **1580 tok/s**，而 512-token 时有 **5821 tok/s**——**短 prompt 的 prefill 被固定开销吃掉 3/4**。短 prompt 场景（单轮问答、分类）**别用 p512 的数字做容量规划**。

---

## 五、同模型量化档位对照（MLX，Qwen3-0.6B）

| 档位 | 权重文件 | bits/weight | prefill tok/s | decode tok/s | 峰值内存 | 相对 4-bit 的 decode |
|---|---|---|---|---|---|---|
| bf16 | 1.192 GB | 16 | 5521.7 | **162.8** | 1.960 GB | 1.00× |
| 8-bit | 0.633 GB | 8.50 | 5629.1 | **257.7** | 1.223 GB | 1.58× |
| 4-bit | 0.336 GB | 4.00 | 5568.4 | **349.3** | 0.918 GB | **2.15×** |

三个结论：

1. **prefill 完全不受量化影响**（5522 / 5629 / 5568，波动 <2%）——再次印证 §二.1 的"prefill 是算力受限"；
2. **decode 随权重大小近似反比**（173 → 248 → 349 tok/s @ 512 档位），这就是"量化提速"的全部机制；
3. **峰值内存也随权重量化下降**（1.96 → 1.22 → 0.92 GB）。

> 8-bit 的 `bits/weight` 是 `mlx_lm.convert` 自己打印的 **8.501**——因为还包含 scale/bias 等量化元数据。**标称 4-bit 不等于文件体积正好是 1/4**。

---

## 六、那张"带宽 ÷ 权重字节"的公式，什么时候能用？

理想公式是 `decode tok/s ≈ 内存带宽 ÷ 每 token 权重字节`。用它算 0.6B 4-bit：273 ÷ 0.336 = **812 tok/s**，实测只有 **349**。差了 2.3 倍。

原因：小模型的每次 forward 有一笔**与权重体积无关的固定开销**。把三档数据做线性拟合（`t` = 每 token 毫秒，`W` = 权重 GB）：

```
t_ms ≈ 1.6 + W / 261
```

| 场景 | W | 预测 t | 预测 tok/s | 实测 tok/s | 误差 |
|---|---|---|---|---|---|
| MLX bf16 | 1.192 GB | 6.15 ms | 162.6 | 162.8 | **+0.1%**（拟合点） |
| MLX 8-bit | 0.633 GB | 4.00 ms | 250 | 257.7 | +3.0% |
| MLX 4-bit | 0.336 GB | 2.86 ms | 349.6 | 349.3 | **−0.1%**（拟合点） |
| Ollama `qwen3.5:9b` Q4_K_M | 6.6 GB | 26.9 ms | 37.2 | **38.6** | −3.6% ← **跨引擎外推也成立** |

**斜率 261 GB/s ≈ 官方 273 GB/s 的 96%**，说明"带宽天花板"是对的；**截距 1.6 ms 才是小模型的真相**。

**有效带宽**（= 权重 × 实测 decode，看它离 273 有多远）：

| 场景 | 权重 | decode | 有效带宽 | 占峰值 273 GB/s |
|---|---|---|---|---|
| MLX 4-bit（0.6B） | 0.336 GB | 349.3 | 117 GB/s | 43% |
| GGUF `Q4_K_M`（0.6B） | 0.517 GB | 282.8 | 146 GB/s | 53% |
| MLX bf16（0.6B） | 1.192 GB | 162.8 | 194 GB/s | 71% |
| GGUF F16（0.6B） | 1.503 GB | 149.7 | 225 GB/s | 82% |
| Ollama `qwen3.5:9b` Q4_K_M | 6.6 GB | 38.6 | **255 GB/s** | **93%** |

**规律：模型越大，有效带宽越接近峰值。** 所以：
- **0.6B / 1B 这类小模型，用「带宽 ÷ 权重」推算会高估 2 倍以上**；
- **7B 以上**（本机 9B 已达 93%）才可以用这条公式做粗估；
- 推论：**在同一台机器上，模型越大，"换引擎"能带来的差异越小**——都被内存带宽压平了。

---

## 七、批处理扩展（MLX 4-bit，`-p 512 -g 128`）

| batch | prefill tok/s | decode 合计 tok/s | **单路** decode | 峰值内存 |
|---|---|---|---|---|
| 1 | 5537 | 351.7 | **351.7** | 0.918 GB |
| 4 | 6297 | 799.2 | 199.8 | 1.451 GB |
| 8 | 6362 | 975.3 | **121.9** | 1.695 GB |

- **系统吞吐**：8 路 batch → **2.77×**；
- **单请求延迟**：351.7 → 121.9 tok/s，**慢 2.9 倍**；
- **内存**：只涨 1.85×（KV 才是个头）；
- **prefill**：与 batch 近乎无关（5537 → 6362，+15%）。

这就是连续批处理的本质：**用单请求延迟换系统吞吐**。对照 Ollama 默认 `OLLAMA_NUM_PARALLEL=1`、LM Studio 默认 `Max Concurrent Predictions=4`，能直接解释三家并发体感差异。

---

## 八、内存拆解：权重 vs KV Cache

### 8.1 KV Cache 的算法

```
每 token KV 字节 = 2(K/V) × n_layers × n_kv_heads × head_dim × dtype 字节数
总 KV 字节      = 每 token KV 字节 × 上下文长度
```

**本机验证（`qwen3:0.6b`，28 层 / 8 个 KV 头 / head_dim 128 / fp16）**：

| 项 | 值 |
|---|---|
| 公式值 | 2 × 28 × 8 × 128 × 2 = **112 KiB/token** |
| 实测值（`num_ctx` 1024→4096，SIZE 671MB→1.0GB） | (1.0−0.671) GB ÷ 3072 ≈ **112 KiB/token** |
| 于是 40960 上下文的 KV | 112 KiB × 40960 = **4.5 GiB** |
| 对照 `ollama ps` | **5.6 GB**（≈ 权重 0.5GB + KV 4.5GB + 运行时开销） |

**公式在这里是完全对得上的**。也正因如此：

> **0.6B 的模型、522MB 的权重，默认吃 5.6GB 内存——其中 80% 是 KV Cache。**

⚠️ 小跨度测量会被 `ollama ps` 的 0.1GB 精度淹没（本机 9B 模型 4096→16384 只从 5.5GB 涨到 6.0GB，噪声与信号同量级）；**量 KV 要拉大跨度**（本机 9B 用 4096 vs 默认 262144：5.5GB → 15GB，才看得清那 ~9.5GB 的 KV）。

### 8.2 4-bit 权重的体积经验值（本机实测模型）

| 模型 | 参数量 | Q4 体积 | **每 B 参数体积** |
|---|---|---|---|
| `qwen3:0.6b` | 0.6B | 0.52 GB | **0.87 GB/B** |
| `deepseek-coder-v2:lite`（MoE） | 16B | 8.9 GB | 0.56 GB/B |
| `qwen3.5:27b` | 27B | 17 GB | **0.63 GB/B** |
| `qwen3.5:9b` | 9B | 6.6 GB | 0.73 GB/B |

**规律：参数量越小，每 B 的体积越大**（小模型的 embedding / 输出头占比高，且通常不做 4-bit）。规划内存时：
- **1B 以下**：按 **0.8~0.9 GB/B** 估；
- **7B~30B**：按 **0.6~0.75 GB/B** 估；
- **MoE**：按**总参数量**估体积，但**按激活参数量**估速度。

### 8.3 Mac 内存档位矩阵

预算规则：**权重 + KV + 系统**，本机 Metal 报出的 `recommendedMaxWorkingSetSize = 40200 MB`（48GB 机型），**超过这个值就会开始大量换页，速度断崖**。

| 统一内存 | 建议留给模型的 | Q4 能跑的量级 | 上下文预算 | 备注 |
|---|---|---|---|---|
| 16 GB | ~10 GB | ≤ 7B | 4k–8k | 0.6B/3B 才是甜点；8B 要盯 KV |
| 24 GB | ~16 GB | ≤ 14B | 8k | |
| 32 GB | ~22 GB | ≤ 27B / 30B-A3B | 16k | MoE 比 dense 划算 |
| **48 GB（本机）** | **~34 GB** | ≤ 32B dense / 30B MoE | 32k 起 | 本机已装 27B Q4（17GB） |
| 64 GB | ~46 GB | ≤ 70B Q4（勉强） | 8k–16k | KV 要压得很紧 |
| 128 GB | ~95 GB | 70B Q8 / 100B+ MoE Q4 | 32k+ | |

⚠️ **矩阵里的"量级"是按权重算的，KV 必须单独加**：32k 上下文对一个 32 层的 8B 模型就可能是 2~4 GB。**先按 §8.1 的公式估 KV，再决定上下文给多大**——本机 9B 默认 262144 上下文直接吃掉 9.5GB 就是活例子。

---

## 九、怎么复现（本机命令清单）

```shell
# ---- 统一约定 ----
BLOB_Q4=~/.ollama/models/blobs/sha256-7f4030143c1c477224c5434f8272c662a8b042079a0a584f0a27a1684fe2e1fa  # qwen3:0.6b Q4_K_M
GGUF_F16=~/.ollama/models/blobs/sha256-bc2421370aa09f86eedd8e57e5b5ff3d1200f4638623c749c2ec820c3b5bff97  # qwen3:0.6b-fp16
MLX4=~/mlx-models/Qwen3-0.6B-4bit

# ---- 裸引擎吞吐 ----
llama-bench -m $BLOB_Q4 -p 512 -n 128 -r 3
llama-bench -m $GGUF_F16 -p 512 -n 128 -r 3
~/.venvs/mlx-lm/bin/mlx_lm.benchmark --model $MLX4 -p 512 -g 128 -n 3 -b 1
~/.venvs/mlx-lm/bin/mlx_lm.benchmark --model $MLX4 -p 512 -g 128 -n 2 -b 8   # 批处理扩展

# ---- 服务端 TTFT/TPOT ----
/opt/homebrew/bin/llama serve -m $BLOB_Q4 --port 8081 -ngl 99 -c 4096
~/.venvs/mlx-lm/bin/mlx_lm.server --model $MLX4 --port 8080
ollama serve                                  # :11434

# ---- 内存 ----
ollama ps                                     # 看 SIZE / PROCESSOR / CONTEXT
curl -s localhost:11434/api/generate -d '{"model":"qwen3:0.6b","prompt":"hi","stream":false,"options":{"num_predict":4,"num_ctx":4096}}' >/dev/null

# ---- MLX 量化档位（自建） ----
~/.venvs/mlx-lm/bin/mlx_lm.convert --hf-path ~/mlx-models/Qwen3-0.6B-hf -q --q-bits 8 --mlx-path ~/mlx-models/Qwen3-0.6B-8bit
```

**报告数字时必须一起写的东西**：机型 + 内存档位 + 所有软件版本 + 模型 + 量化档位 + prompt/generation 长度 + batch + 上下文长度 + 冷/热态。

---

## 十、坑

1. **把 prefill 和 decode 混在一张表里** → 两者一个算力受限一个带宽受限，结论会相反。
2. **不设 `num_ctx` 就比内存** → Ollama 侧可能默认吃到 5.6GB（0.6B）或 15GB（9B）。
3. **用 `generate` 打印的 prefill 数字做横向对比** → 短 prompt 下它是冷启动主导的（MLX 实测打印 17.7 tok/s，实际 prefill 能力 5500+）。
4. **TTFT 对比时 prompt 前缀相同** → 命中 prompt 前缀缓存，TTFT 从 868ms 掉到 23ms。
5. **把「同模型」当成「同权重」** → MLX 4-bit（336MB）与 GGUF `Q4_K_M`（517MB）差 54%。
6. **只认 SSE 里的 `content` 字段** → MLX 用 `reasoning`、llama.cpp 用 `reasoning_content`，思考型模型会被判成"零输出"。
7. **`llama-bench` 单次结果当真** → 输出自带 `±`，本机实测同一模型 `tg128` 在 266.6 与 282.8 之间波动（±3%）。至少 `-r 3`。
8. **在跑着别的模型（Ollama 常驻）时压测** → 统一内存被占，Metal 会被迫换页，数字直接失真。**压测前先 `ollama stop` 全部模型**。
9. **拿短 prompt 的 prefill 数字做容量规划** → 168 token 时 1580 tok/s，512 token 时 5821 tok/s，差 3.7 倍。
10. **用小模型的 tok/s 外推大模型** → 0.6B 有效带宽只有峰值的 43%，9B 能到 93%，线性外推会严重高估。
11. **忘了报版本号** → 本地推理工具的默认值与量化方案一变，历史数字就不可复核。

---

## 十一、工程建议

1. **报告只写"三件套"**：`prefill tok/s` @ 指定 prompt 长度 + `decode tok/s` + `峰值内存` @ 指定上下文。缺一个都会被误读。
2. **锁精度比锁模型更重要**：要下"谁快"的结论，双方都跑 16-bit；要下"我该用哪个"的结论，才用各自推荐的量化档位。
3. **Ollama 上生产前必做两件事**：显式设 `OLLAMA_CONTEXT_LENGTH`（别让它按 VRAM 档位给你 256k），显式设 `OLLAMA_NUM_PARALLEL`（默认 1，并发全排队）。
4. **内存容量规划先算 KV，再选模型**：`KV = 2 × n_layers × n_kv_heads × head_dim × dtype × ctx`，这个数常常和权重同量级甚至更大。
5. **小模型别指望"换引擎提速"**：0.6B 上三家 HTTP 服务端 decode 都在 254~289 tok/s（差 14%），差异主要被固定开销吃掉；**要么换更小的量化，要么换更大的 batch**。
6. **对延迟敏感就用 short-prompt 口径实测**：TTFT 排名在短 prompt 下由服务框架决定（本机 llama-server 18ms vs MLX server 116ms），与预填充算力无关。
7. **每次压测前清场**：`ollama stop` 全部模型、关掉其它 server、确认 `ollama ps` 为空——本机 48GB 统一内存一旦被占，数字就没意义了。

---

## 十二、高频追问

1. **Mac 上到底哪个推理引擎最快？**
   分三层答：**裸框架 decode** MLX 领先（同精度 +8.8%，同 4-bit 档 +23.5%）；**裸框架 prefill** llama.cpp 略优（+7.7%）；**HTTP 服务端** 三家拉平（254~289 tok/s，差 <14%）。**"最快"取决于你问的是哪一层。**
2. **Ollama 比 llama.cpp 慢多少？**
   单请求 decode 差 **1%~3%**（本机两次独立实测：115.5 vs 117、282.8 vs 274.2）。它的劣势在**默认值**：`OLLAMA_NUM_PARALLEL=1`（排队）、默认上下文按 VRAM 档位拉满（KV 爆炸）。
3. **量化到 4-bit 能快多少？**
   本机 MLX 同模型实测：**decode 2.15×**（162.8 → 349.3 tok/s）、**峰值内存降到 47%**（1.96 → 0.92 GB）。但 **prefill 几乎不变**（±2%）——量化只治带宽瓶颈。
4. **为什么我的 tok/s 比文章里低一半？**
   按可能性排序：① 上下文给太大（KV 撑爆内存换页）；② 层没卸到 GPU（`-ngl` 太小 / offload 没开）；③ 机器上还跑着别的模型；④ prompt 太短（固定开销占比高）；⑤ prompt 前缀缓存没命中/命中的方向搞反了。
5. **batch 加大能提速多少？**
   本机 MLX 0.6B：**8 路 → 系统吞吐 2.77×，单路延迟慢 2.9×**，内存只涨 1.85×。**吞吐换延迟**，必须分清你要哪个。
6. **怎么快速估一个模型在我机器上能不能跑？**
   `权重 ≈ 参数量 × 0.7 GB`（Q4）+ `KV = 2 × n_layers × n_kv_heads × head_dim × 2 × ctx`，两者相加再留 25% 给系统。本机 Metal 的工作集上限是 `recommendedMaxWorkingSetSize = 40200 MB`。LM Studio 用户可直接 `lms load --estimate-only` 让它算（见 [lm-studio.md](./lm-studio.md) §5.2）。
7. **TTFT 和 TPOT 哪个更重要？**
   看场景：**流式聊天**看 TTFT（用户等第一个字）；**长文本生成/代码生成**看 TPOT（总时长 = TTFT + n × TPOT，n 大时 TPOT 主导）。RAG 长上下文场景 TTFT 往往被 prefill 主导（本机 168 token 的 prefill 就要 106ms）。

---

## 十三、来源与数据说明

- **全部为 2026-09-12 本机实测**（Apple M4 Pro / 48GB / macOS 26.6.2）：
  - `llama-bench`（llama.cpp v0.4.0, build 10809, `5266f24da`）：Qwen3-0.6B `Q4_K_M` / `F16`，`-p 512 -n 128 -r 3`
  - `mlx_lm.benchmark`（mlx-lm 0.31.3 / mlx 0.32.2）：`-p 512 -g 128 -n 3 -b {1,4,8}`
  - `ollama ps` / `/api/generate`（Ollama 0.33.3）：`qwen3:0.6b`、`qwen3.5:9b`
  - TTFT/TPOT：自写 streaming 探针（python `urllib`，SSE 逐块计时），三个运行时各 3 次
- **历史基线复用**（2026-09-11 同机实测，见 [ollama.md](./ollama.md) §8 本机实测记录 / [llama-cpp.md](./llama-cpp.md) §9.3 横向对比）：`qwen3.5:9b` Q4_K_M decode 38.6 tok/s、冷加载 4.68s、驻留 14.2GB；`deepseek-coder-v2-lite` pp512 1125.8 / tg128 115.5，同模型 Ollama 117 tok/s
- 规格：[Apple MacBook Pro 技术规格](https://support.apple.com/en-us/121553)（M4 Pro 273 GB/s、M4 Max 410 GB/s；普通 M4 为 120 GB/s）
- Ollama 上下文默认策略：官方文档 <https://docs.ollama.com/context-length>（按 VRAM 档位 4k/32k/256k）
- 原理：[环节11-服务化与推理引擎详解](../../foundation/transformer/环节11-服务化与推理引擎详解.md)（§1 Prefill/Decode、§2.1 Mac 选型）、[环节10-推理解码与KV缓存详解](../../foundation/transformer/环节10-推理解码与KV缓存详解.md)

> ⚠️ **这些数字只对本机（M4 Pro / 48GB）有意义**。换机型（尤其是带宽不同的 M4 / M4 Max）绝对值会整体平移，**但"prefill 与 batch 无关""有效带宽随模型变大而升高""KV 是内存主体"这三个结构性结论是普适的**。

---

## 相关笔记

- 总览与选型：[本地推理运行时 · 操作手册](./README.md)
- 同系列：[llama-cpp.md](./llama-cpp.md)（`llama-bench` 用法）、[ollama.md](./ollama.md)（并发默认值）、[lm-studio.md](./lm-studio.md)（`--estimate-only` 估算）、[mlx.md](./mlx.md)（本机微调路径）
- 原理与选型：[环节11-服务化与推理引擎详解](../../foundation/transformer/环节11-服务化与推理引擎详解.md)
- KV Cache 与上下文成本：[环节10-推理解码与KV缓存详解](../../foundation/transformer/环节10-推理解码与KV缓存详解.md)
- 端侧小模型策略：[SLM 小模型与端侧](../../foundation/slm/README.md)
- 加速技术：[Speculative Decoding](../speculative-decoding/README.md)
- 量化后的精度回归：[模型评测与选型方法详解](../../foundation/transformer/模型评测与选型方法详解.md)
