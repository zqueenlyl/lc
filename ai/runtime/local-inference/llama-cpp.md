# llama.cpp 操作手册

> **版本口径**：本机实测 **v0.4.0（build 10809, commit `5266f24da`）**，2026-09-11，Apple M4 / Metal。
> **先看三条容易踩的变更**（老教程基本都过时了）：
> 1. **版本号已语义化**：llama.cpp 现在发 **v0.4.0**（2026-09-04），不再是过去的 `bXXXX`（内部 build 号仍保留，如 `b10809`）。
> 2. **官方主推统一入口 `llama <子命令>`**：`llama serve` / `llama cli`。旧的 `llama-server` / `llama-cli` 二进制**仍然存在且等价**，但官方 README 示例已全部改用新写法。
> 3. **官方安装页迁到 `llama.app`**，不再是仓库首页；`--no-mmap` / `--mlock` 已被 `-lm/--load-mode` 取代（详见 §5.4）。

## 0. 一句话定位

**llama.cpp 是本地推理的"引擎本体"**：纯 C/C++、无外部依赖、Metal/CUDA/ROCm/Vulkan/CPU 全后端、GGUF 格式的发源地。Ollama 和 LM Studio 底层都是它。

**什么时候选它而不是 Ollama / LM Studio**：

| 你的需求 | 选 llama.cpp 的理由 |
|---|---|
| 要精细控制每个参数 | 参数数量是 Ollama 的十倍级（`--load-mode`、`-ctk/-ctv`、`-fit`、`-sm/-ts` 多卡切分…） |
| 要脚本化 / 进 CI | 无守护进程、单文件二进制、`llama-bench` 直接输出可解析的基准表 |
| 要嵌进别的程序 | 提供 `libllama` C API，也被大量项目当依赖 |
| 要跑最新架构 / 最新量化 | GGUF 新格式与新模型架构**总是先在 llama.cpp 落地** |
| 只是想聊天 | ✖ 用 LM Studio 或 Ollama 更省事 |

---

## 1. 安装

```bash
# ① Homebrew（推荐，本机实测路径）
brew install llama.cpp
llama --version
# version: 0.4.0 (build 10809, commit 5266f24da)
# built with AppleClang 21.0.0.21000101 for Darwin arm64

# ② 官方安装脚本（llama.app 是新首页）
curl -LsSf https://llama.app/install.sh | sh

# ③ 预编译二进制：GitHub Releases 页下载对应平台包
# ④ Docker：ghcr.io/ggml-org/llama.cpp:server（CPU）/ :server-cuda（GPU）
```

**源码编译**（想开特殊后端或跟最新 commit）：

```bash
git clone https://github.com/ggml-org/llama.cpp && cd llama.cpp
cmake -B build
cmake --build build --config Release -j 8
# 产物：./build/bin/llama-cli、./build/bin/llama-server
```

macOS 相关要点：

- **Metal 与 Accelerate 默认开启**，不用加任何 flag；
- 编译期禁用 GPU：`cmake -B build -DGGML_METAL=OFF`；运行期完全禁 GPU：`--device none`（只写 `-ngl 0` 不够，GPU 仍可能参与部分计算）；
- 反复编译装 `ccache`（官方唯一推荐的构建加速）；
- 按仓库 `docs/build.md`：BLAS/Accelerate **只加速 batch > 32 的 prompt processing，不影响生成（decode）速度**——这是理解后续实测数字的关键。

> ⚠️ **brew 装的别用 `llama update`**：新 CLI 有 `update` 子命令（自更新），brew 安装由 brew 管版本，直接自更新会让 brew 的版本记录错乱。`brew upgrade llama.cpp` 更稳妥。

---

## 2. 新统一入口 `llama` 的子命令

`llama help all` 实测输出：

| 子命令 | 作用 |
|---|---|
| `llama serve` | HTTP API 服务器（= 旧 `llama-server`） |
| `llama cli` | 交互式命令行（= 旧 `llama-cli`） |
| `llama completion` | 单次文本补全 |
| `llama download` | 下载模型（配合 `-hf`） |
| `llama bench` | 基准测试（= 旧 `llama-bench`） |
| `llama batched-bench` | 批量解码性能基准 |
| `llama quantize` | 量化（= 旧 `llama-quantize`） |
| `llama perplexity` | 困惑度 / KL 散度（= 旧 `llama-perplexity`） |
| `llama fit-params` | 计算"要多少参数才能把模型塞进显存" |
| `llama update` | 自更新（源码/脚本安装用） |
| `llama version` / `licenses` / `help` | 版本 / 第三方许可 / 帮助 |

**新旧混用完全可以**：实测 `llama-cli`、`llama-server`、`llama-bench`、`llama-quantize`、`llama-perplexity` 均仍在 `/opt/homebrew/bin/` 下，参数与 `llama <子命令>` 一致。老脚本不用改。

---

## 3. 模型从哪来（三条路）

```bash
# ① 直接从 Hugging Face 拉（最省事，会缓存到本地）
llama cli -hf ggml-org/GLM-4.7-Flash-GGUF:Q4_K_M
llama serve -hf ggml-org/Qwen3.5-0.8B-GGUF        # 不写 :quant 默认 Q4_K_M

# ② 下载但不推理
llama download -hf <用户>/<仓库>:<量化>
llama cli --cache-list                            # 看缓存里有哪些模型

# ③ 本地已有 GGUF
llama serve -m /path/to/model.gguf
```

`-hf` 细节（官方参数说明）：

- 格式 `<user>/<model>[:quant]`，quant 大小写不敏感，**默认 `Q4_K_M`**；仓库里没有 Q4_K_M 就回退到第一个文件；
- 有 mmproj（多模态投影）会**自动一并下载**，不想要加 `--no-mmproj`；
- 私有仓库用 `-hft <token>`（或环境变量 `HF_TOKEN`）；
- `--offline` 强制只用缓存、不联网；
- 环境变量：`LLAMA_ARG_HF_REPO`、`LLAMA_ARG_HF_FILE`。

**复用 Ollama 已下载的模型**（省一次下载）：Ollama 的 blob 就是**裸 GGUF**，可以直接当 `-m` 参数用——

```bash
BLOB=$(ollama show deepseek-coder-v2:lite --modelfile | awk '/^FROM /{print $2}')
head -c 4 "$BLOB"          # => GGUF   （确认是裸 GGUF）
llama serve -m "$BLOB"
```

⚠️ **但这是"看架构"的，不保证成功**。本机实测：`deepseek-coder-v2:lite` 加载成功，`qwen3.5:9b` 直接报
`error loading model hyperparameters: key qwen35.rope.dimension_sections has wrong array length; expected 4, got 3`。
原因是 Ollama 侧可能改写了 GGUF 元数据（或用了带 M-RoPE 的变体），而 llama.cpp 的校验更严。详见 §10 坑清单。

---

## 4. `llama cli` / `llama-cli` 用法

```bash
# 交互式对话
llama cli -m model.gguf -ngl 99 -c 8192

# 单次生成后退出
llama cli -m model.gguf -p "用一句话解释 KV Cache" -n 128 -st

# 连接已有的 server 当客户端（新增能力，不再自己起一个）
llama cli --server-base http://localhost:8080
```

- `-st/--single-turn`：只跑一轮就退出；不设且未预置 prompt 则进入交互模式；
- `-r/--reverse-prompt`：遇到指定串就停下并交回控制权（交互模式的关键参数）；
- `-mli/--multiline-input`：多行粘贴不用每行加 `\`；
- `--show-timings`：每次回复后打印耗时（看 tok/s 最直接的方式）。

---

## 5. `llama-server` 参数详解

### 5.1 上下文与批

| 参数 | 说明 |
|---|---|
| `-c, --ctx-size N` | 上下文大小。**默认 0 = 从模型元数据读** |
| `-n, --predict N` | 最多生成多少 token，`-1` 无限 |
| `-b, --batch-size N` | 逻辑批，默认 2048 |
| `-ub, --ubatch-size N` | 物理批，默认 512 |
| `--keep N` | 保留 prompt 开头 N 个 token 不丢 |

### 5.2 GPU 与多卡

| 参数 | 说明 |
|---|---|
| `-ngl, --gpu-layers N` | 卸载层数：数字 / `auto` / `all`（默认 auto） |
| `-dev, --device <d1,d2>` | 指定设备；`none` = 完全不用 GPU |
| `--list-devices` | 列出可用设备（排查"到底有没有用上 Metal"的第一步） |
| `-sm, --split-mode` | `none` / `layer`(默认) / `row` / `tensor` |
| `-ts, --tensor-split` | 多卡分配比例，如 `3,1` |
| `-fit, --fit [on\|off]` | **自动适配显存**，默认 on（目标余量 1024 MiB、最小 ctx 4096） |
| `-cmoe, --cpu-moe` / `-ncmoe, --n-cpu-moe N` | MoE 专家权重留在 CPU（跑大 MoE 的省钱技巧） |

### 5.3 线程与 CPU

| 参数 | 说明 |
|---|---|
| `-t, --threads N` | 生成线程数（默认 -1 自动；本机 M4 实测选了 10） |
| `-tb, --threads-batch N` | prompt 处理线程数 |
| `--threads-http N` | HTTP 处理线程数 |
| `--numa` | NUMA 优化（多路服务器） |

### 5.4 KV Cache 与加载模式（重点）

| 参数 | 说明 |
|---|---|
| `-ctk, --cache-type-k` | K 缓存类型，默认 `f16`；可选 `f32/f16/bf16/q8_0/q4_0/q4_1/iq4_nl/q5_0/q5_1` |
| `-ctv, --cache-type-v` | V 缓存类型，同上 |
| `-fa, --flash-attn [on\|off\|auto]` | Flash Attention，**默认 auto** |
| `-lm, --load-mode MODE` | **加载模式统一入口**：`auto`(默认 mmap) / `none` / `mmap` / `mlock` / `mmap+mlock` / `dio` |
| `-lzm, --lazy-mode MODE` | 按需读取部分张量（v0.4.0 新增，省冷启动时间） |
| `-kvo` / `-nkvo` | KV 是否卸载到 GPU（默认启用） |

> ⚠️ **参数变迁**：老教程里的 `--no-mmap` 和 `--mlock` **已经不存在**，统一到 `-lm/--load-mode`（`none` ≈ 不用 mmap，`mlock` ≈ 锁内存，`mmap+mlock` ≈ 两者都要）。抄老命令会直接报错。

### 5.5 采样（默认值取自官方参数表）

| 参数 | 默认 | 参数 | 默认 |
|---|---|---|---|
| `--temp` | 0.80 | `--repeat-last-n` | 64 |
| `--top-k` | 40 | `--repeat-penalty` | 1.00（关） |
| `--top-p` | 0.95 | `--presence-penalty` | 0.00 |
| `--min-p` | 0.05 | `--frequency-penalty` | 0.00 |
| `-s, --seed` | -1（随机） | `--dynatemp-range` | 0.00（关） |

采样器链：`--samplers`，默认 `penalties;dry;top_n_sigma;top_k;typ_p;top_p;min_p;xtc;temperature`。
约束生成：`--grammar`（GBNF 语法）、`-j, --json-schema`（JSON Schema 约束解码）。

### 5.6 服务与安全

| 参数 | 说明 |
|---|---|
| `--host` / `--port` | 默认 `127.0.0.1:8080`；`.sock` 结尾则绑定 UNIX socket |
| `-a, --alias STRING` | **模型别名**，API 里 `/v1/models` 返回的 `id`（不设就是文件路径，很难看，见 §9 实测） |
| `-np, --parallel N` | slot 数（并发请求数），默认 `-1` = auto（本机实测自动选了 **4**） |
| `-cb` / `-nocb` | 连续批处理，默认启用 |
| `--api-key KEY` | **API 密钥**（可逗号分隔多个 / `--api-key-file`） |
| `--cors-origins` | CORS 白名单 |
| `--metrics` | 开启 Prometheus 指标端点 `/metrics` |
| `--ssl-key-file` / `--ssl-cert-file` | HTTPS |
| `--models-dir` | **router 模式**：一个 server 托管多个模型，按 `model` 字段路由 |

> 🔒 **实测启动即有安全警告**：默认 `CORS is set to allow all origins ('*') and no API key is set`——即**默认无鉴权、允许任意跨域**。同机自用没问题，暴露到局域网/公网请务必加 `--api-key` 并显式设 `--cors-origins`。

### 5.7 思考型模型（reasoning）

| 参数 | 说明 |
|---|---|
| `-rea, --reasoning [on\|off\|auto]` | 是否思考，默认 auto（从模板检测） |
| `--reasoning-effort LEVEL` | `default/minimal/low/medium/high/xhigh/max` |
| `--reasoning-budget N` | 思考 token 预算（-1 不限，**0 立即结束**） |
| `--reasoning-format` | `none`（留在 content）/ `deepseek`（进 `reasoning_content`）/ `deepseek-legacy` |
| `--skip-chat-parsing` | 强制纯内容解析：推理与工具调用全部塞进 `content` |

> 与 Ollama 的 `think` 参数是同一个问题的两种叫法，预算机制比 Ollama 更细（可注入预算耗尽时的提示语 `--reasoning-budget-message`）。

---

## 6. HTTP 端点全清单

### OpenAI 兼容（`/v1/*`）

| 端点 | 说明 |
|---|---|
| `POST /v1/chat/completions` | 主力端点，支持流式、tools、vision |
| `POST /v1/chat/completions/control` | **实时控制**运行中的对话（目前唯一动作 `reasoning_end`） |
| `POST /v1/chat/completions/input_tokens` | 输入 token 计数（非官方端点，方便补充） |
| `POST /v1/completions` | 传统补全 |
| `POST /v1/responses` | OpenAI Responses API（内部转成 chat completions） |
| `POST /v1/embeddings` | 嵌入（要求 pooling ≠ none） |
| `GET /v1/models` | 模型列表（**固定单元素**） |

### Anthropic 兼容（新）

| 端点 | 说明 |
|---|---|
| `POST /v1/messages` | Anthropic Messages API（`max_tokens` 默认 4096；tools 需 `--jinja`） |
| `POST /v1/messages/count_tokens` | token 计数 |

### 原生端点（llama.cpp 独有，比 OAI 兼容层更强大）

| 端点 | 说明 |
|---|---|
| `POST /completion` | 原生补全，**参数最全、timings 最详细** |
| `POST /tokenize` / `detokenize` | 文本 ↔ token |
| `POST /apply-template` | 只套聊天模板看最终 prompt（**调试"答非所问"的利器**） |
| `POST /embedding` | 原生嵌入 |
| `POST /reranking` | 重排序（需 reranker 模型 + `--embedding --pooling rank`） |
| `POST /infill` | 代码 FIM 填充 |
| `GET /health` | 健康检查（**无需 API key**；503 = 模型加载中） |
| `GET /props` | 服务器属性：`build_info`、`total_slots`、`chat_template`、`modalities` |
| `GET /slots` | 各 slot 处理状态（并发排查用） |
| `GET /metrics` | Prometheus 指标（需 `--metrics`） |
| `POST /slots/{id}?action=save\|restore\|erase` | slot 的 KV cache 存取 |

**`/completion` 响应里的 `timings`**（性能分析核心）：

```
prompt_n                 本次实际处理的 prompt token 数
prompt_per_second        预填充速度
predicted_n              生成 token 数
predicted_per_second     解码速度  ← 你最关心的那个数
cache_n / tokens_cached  命中 prompt cache 的 token 数
stop_type                none / eos / limit / word
```

---

## 7. 可观测：`/metrics` 指标

启动加 `--metrics` 后在 `/metrics` 暴露（Prometheus 格式，指标前缀 `llamacpp:`）：

| 指标 | 含义 |
|---|---|
| `llamacpp:prompt_tokens_seconds` | 预填充吞吐（tokens/s） |
| `llamacpp:predicted_tokens_seconds` | 生吞成吐（tokens/s） |
| `llamacpp:requests_processing` | 正在处理的请求数 |
| `llamacpp:requests_deferred` | **被延后的请求数**（>0 说明 slot 不够，该调 `-np`） |
| `llamacpp:n_busy_slots_per_decode` | 每次 decode 的平均繁忙 slot 数（连续批处理效率） |
| `llamacpp:n_tokens_max` | 上下文使用高水位 |
| `llamacpp:spec_decode_num_accepted_tokens_total` | 投机解码被接受的草稿 token 数（配套 `..._draft_tokens_total` 算**接受率**） |

> router 模式下 `/metrics` 必须带 `?model={id}`，否则返回 400。

---

## 8. 关键调优速查

| 想优化 | 动什么 |
|---|---|
| 生成更快（decode） | 降量化位宽 / 换更小模型 / 确保 `-ngl all`。**decode 由内存带宽决定**，与线程数关系不大 |
| 长 prompt 更快（prefill） | `-b/-ub` 调大、`-tb` 加线程、确认 BLAS/Metal 生效。prefill 吃算力 |
| 省显存 | `-ctk q8_0 -ctv q8_0`（KV 量化）、降 `-c`、`-cmoe`（MoE 留 CPU） |
| 冷启动更快 | `-lzm`（按需读张量）、`-lm mmap` 保持默认、复用 prompt cache |
| 并发更高 | `-np N` + `-cb`（连续批处理）；但内存按 `N × ctx` 增长 |
| 自动别爆显存 | 保持 `-fit on`（默认） |
| 输出可复现 | `-s 42 --temp 0` |
| 结构化输出 | `-j schema.json` 或 `--grammar` |

---

## 9. 本机实测记录

**环境**：Apple M4 / Metal（`recommendedMaxWorkingSetSize ≈ 40200 MB`，`residency sets = true`），llama.cpp **v0.4.0 (build 10809)**，10 线程。
**模型**：`deepseek-coder-v2-lite`，16B MoE / 15.71B 参数，**Q4_0，8.29 GiB**（直接复用 Ollama 的 GGUF blob）。2026-09-11。

### 9.1 `llama-bench` 标准基准（`-p 512 -n 128 -ngl 99 -r 2`）

```
| model                          |       size |     params | backend    | threads |          test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | ------: | ------------: | -------------------: |
| deepseek2 16B Q4_0             |   8.29 GiB |    15.71 B | BLAS,MTL   |      10 |         pp512 |       1125.82 ± 1.70 |
| deepseek2 16B Q4_0             |   8.29 GiB |    15.71 B | BLAS,MTL   |      10 |         tg128 |        115.48 ± 1.48 |
```

**怎么读这张表**（这也是 llama.cpp 最值钱的能力——把别人的跑分和你的直接对齐）：

- `pp512` = **预填充** 512 token 的速度 → **1125.8 tok/s**；
- `tg128` = **生吞成吐**（token generation）速度 → **115.5 tok/s**；
- 两者差 **约 10 倍**，印证了"prefill 是算力密集 / decode 是带宽密集"：同样一个 token，把它"读进去"比"写出来"快一个数量级。
- 折算体感：**512 token 的 prompt 只要 0.45 秒**，之后每秒吐 115 个 token；长文要等的是 prefill，长回答要等的是 decode。

### 9.2 运行时实测（同一模型）

| 测量点 | llama.cpp 0.4.0 | 说明 |
|---|---|---|
| `/completion`（裸补全，10 token prompt） | prefill 90.0 tok/s，**decode 112.47 tok/s** | 短 prompt 的 prefill 数字无参考价值 |
| `/v1/chat/completions`（14 token prompt） | prefill 288.3 tok/s，**decode 109.89 tok/s** | 走 chat template，`finish_reason: stop` |
| 进程 RSS | **9.4 GB** | 权重 8.29 GiB + KV Cache（ctx 4096） |
| 冷加载 → listening | 约 **3.7 s** | 从日志时间戳推算 |
| `/props` | `build: b10809-5266f24da`，`total_slots: 4`，`n_ctx: 4096` | `-np` 默认 auto → 自动选了 **4** |
| `/v1/models` 的 `id` | `/Users/wzq/.ollama/models/blobs/sha256-5ff0…` | **没设 `--alias`，模型 id 就是文件路径**（客户端配置会很难看） |

### 9.3 横向对比：同模型，llama.cpp vs Ollama

同一个 GGUF 文件、同 prompt、同 `num_ctx=4096`、同 `temperature=0`：

| | llama.cpp 0.4.0 | Ollama 0.33.3 |
|---|---|---|
| decode tok/s（裸补全） | 112.47 | **117.12** |
| decode tok/s（chat 端点） | 109.89 | **117.93** |
| 驻留内存 | 9.4 GB | 9.4 GB（`size_vram` 9659 MB） |
| 默认并发 slot | 4（自动） | 1（`OLLAMA_NUM_PARALLEL` 默认） |

**结论（重要）**：**单请求吞吐上 Ollama 与裸 llama.cpp 几乎持平（差 <5%，Ollama 甚至略高）**。
所以"Ollama 慢"这个传言要拆开看——**它的封装开销不体现在单请求 decode 上**，而体现在：参数控制粒度（Ollama 的 Modelfile 只有 11 个参数）、并发调优能力、以及**默认 `NUM_PARALLEL=1` 导致的多请求排队**。

按 [环节11 §2.1](../../foundation/transformer/环节11-服务化与推理引擎详解.md) 的带宽公式核对：M4 统一内存带宽约 120 GB/s，Q4_0 的 16B MoE 每 token 需读激活参数约 1 GB 量级 → 理论量级 ~100 tok/s，实测 112–117 tok/s，**与带宽模型吻合**。

---

## 10. 坑清单

| 症状 / 现象 | 原因与解法 |
|---|---|
| `--no-mmap` / `--mlock` 报"unknown argument" | 老教程过时。改用 `-lm/--load-mode none\|mlock\|mmap+mlock` |
| `--draft` / `--draft-n` / `--draft-max` 报错 | 已移除，改用 `--spec-draft-n-max` / `--spec-ngram-*-n-max` |
| 抄 Ollama 的 blob 当 `-m` 用，报 `wrong array length` | **实测踩到**：`qwen3.5` 失败（`qwen35.rope.dimension_sections expected 4, got 3`），`deepseek-coder-v2` 成功。Ollama 的 blob 是裸 GGUF 但**元数据不一定被 llama.cpp 接受**，别把它当可靠互通手段 |
| 回答答非所问 / 重复乱码 | 聊天模板不匹配。先用 `POST /apply-template` 看实际 prompt，再 `--chat-template` 指定或覆盖 `--chat-template-file` |
| 用了工具调用但不触发 | 需要 `--jinja`（0.4.0 起**默认开启**，老版本要手动加）；部分模型还需覆盖模板 |
| 端口被占 / 上次没退干净 | 默认 8080；`--port` 改端口，或 `pkill -f llama-server` |
| 以为在跑 GPU，其实在跑 CPU | `--list-devices` 确认设备；`-ngl all`；注意 `-ngl 0` 不等于完全禁 GPU，要 `--device none` |
| 默认允许任意跨域、无鉴权 | 启动日志会警告 `CORS is set to allow all origins ('*') and no API key is set`；加 `--api-key` + `--cors-origins` |
| 客户端里模型名叫一大串路径 | 加 `-a, --alias my-model` |
| 多请求排队、`requests_deferred` 一直涨 | `-np` 调大 + 确认 `-cb` 开启；注意内存按 `np × ctx` 增长 |
| 上下文被静默截断 | `-c 0`（默认）时从模型元数据读；实际值看 `/props` 的 `n_ctx` |
| `llama update` 后 brew 版本记录错乱 | brew 安装的用 `brew upgrade llama.cpp`，别用自更新 |
| 想跑但显存不够 | 先 `llama fit-params` 算需要什么参数能装下，再决定 `-ngl` / 量化档 / `-cmoe` |

---

## 11. 工程建议

1. **模型统一留 GGUF 副本**：llama.cpp 是格式源头、参数最全、新架构最先支持。把它作为"兜底运行时"，Ollama / LM Studio 都可以从同一个 GGUF 导入。
2. **先用 `llama-bench` 定基线，再谈调优**：`pp512` / `tg128` 两个数就是你这台机器的性能身份证，之后任何改动（量化档、ctx、KV 类型）都能用同一口径回归。填进 `benchmark.md`（待写）。
3. **生产别用它**：`-np` + 连续批处理能撑小规模并发，但没有 PagedAttention / 抢占式调度 / 多副本编排。要服务化回 [环节11](../../foundation/transformer/环节11-服务化与推理引擎详解.md) 的 vLLM / SGLang。
4. **暴露到局域网就立刻加 `--api-key`**：默认配置是无鉴权 + 全开放 CORS。
5. **KV Cache 是显存第二大头**：先看 `/props` 的 `n_ctx`，再决定 `-ctk/-ctv` 是否降到 `q8_0`。

---

## 12. 高频追问

1. **llama.cpp 和 Ollama 什么关系？** Ollama 内部就是 llama.cpp（+ 自己的模型分发与守护进程）。实测两者单请求吞吐持平，Ollama 的差异在**易用性与并发默认值**，不在引擎速度。
2. **prefill 和 decode 为什么差 10 倍？** prefill 是矩阵乘（算力密集，可批处理，实测 1126 tok/s）；decode 每生成一个 token 都要把权重过一遍（带宽密集，实测 115 tok/s）。原理见 [环节10](../../foundation/transformer/环节10-推理解码与KV缓存详解.md)。
3. **`-ngl` 填多少？** `all` 或 `99`（不用记层数）。2026 年还有 `-fit on` 帮你自动算，爆显存风险小得多。
4. **GGUF 在 Ollama 和 llama.cpp 之间能直接复用吗？** **方向性结论：能复用但不是保证**。同一份 GGUF 文件两边都能读，但实测 qwen3.5 的元数据被 llama.cpp 拒收。跨运行时迁移前先试加载，别当作既定事实。
5. **为什么 decode 速度和 CPU 核心数关系不大？** 因为瓶颈在内存带宽不在算力；加线程只能改善 prefill。所以 Mac 上"更多核心"不如"更大带宽"。
6. **`llama-bench` 的 pp/tg 和我在业务里测的 tok/s 对不上？** 对得上才是巧合——bench 里 prompt 固定 512 token 且无 chat 模板；业务里 prompt 短、有模板、有系统提示。**bench 用于横向比较机器，不用于预测业务延迟**。

---

## 13. 数据来源

- 官方仓库（`ggml-org/llama.cpp`）：`tools/server/README.md`（端点与参数全表）、`tools/cli/README.md`、`docs/build.md`、根 `README.md`，2026-09-11 抓取
- 发布说明：**v0.4.0**（2026-09-04）——新增 Qwen3.8-Flash-Next / Nemotron-3-Puzzle 支持、按需张量读取（`lazy_mode`）、per-slot 上下文上限、视频输入选项，ggml 升级到 0.23.0
- 官方新首页：https://llama.app
- 本机实测：llama.cpp **0.4.0 (build 10809, `5266f24da`)** / Apple M4 / Metal / `deepseek-coder-v2-lite` Q4_0，2026-09-11

---

## 相关笔记

- 总览与选型：[本地推理运行时 · 操作手册](./README.md)
- 姊妹篇：[ollama.md](./ollama.md)（同模型对比数据见本文 §9.3）
- 原理与选型：[环节11-服务化与推理引擎详解](../../foundation/transformer/环节11-服务化与推理引擎详解.md)（§2.1 Mac 选型、§2.2 GGUF 与量化命名）
- KV Cache 与上下文成本：[环节10-推理解码与KV缓存详解](../../foundation/transformer/环节10-推理解码与KV缓存详解.md)
- 投机解码参数（`--spec-*`）：[Speculative Decoding](../speculative-decoding/README.md)
- 同系列：[lm-studio.md](./lm-studio.md)（GUI 优先的对照选手）、[mlx.md](./mlx.md)（Apple 原生 + 本机微调）
- 跨运行时实测数据与测法：[benchmark.md](./benchmark.md)（本文 §9.3 横向对比的完整版）
