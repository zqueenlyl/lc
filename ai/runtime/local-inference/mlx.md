# MLX / mlx-lm 操作手册

> 一句话：**Apple 官方数组框架 + LLM 工具箱**，四家里唯一能在 Mac 上**本机微调 LoRA**、也是唯一吃 `safetensors` 而非 GGUF 的那条路。
> 本文是**操作手册**（装什么 / 命令怎么敲 / 参数什么含义 / 实测多少），原理与选型见 [环节11-服务化与推理引擎详解](../../foundation/transformer/环节11-服务化与推理引擎详解.md)。
>
> **核查日期**：2026-09-12，**本机实测**（Apple M4 Pro / 48GB / macOS 26.6.2）：`mlx` 0.32.2 + `mlx-lm` **0.31.3**（PyPI 同期最新版）、Python 3.12.13。
> 实测模型：`mlx-community/Qwen3-0.6B-4bit`（4-bit，336MB）+ 自建 bf16 / 8-bit 变体。

---

## 0. 一句话定位

| 维度 | MLX / `mlx-lm` | llama.cpp | Ollama | LM Studio |
|---|---|---|---|---|
| 形态 | **Python 包 + CLI**（`mlx_lm.*`） | C++ CLI + HTTP 服务 | CLI + 常驻守护进程 | 桌面 GUI + 内置 server |
| 归属 | **Apple 官方**（`ml-explore/mlx`） | ggml-org 社区 | Ollama 公司 | LM Studio 公司 |
| 模型格式 | **safetensors**（含 MLX 4/8-bit 量化） | GGUF | GGUF（OCI 封装） | GGUF **+** MLX |
| 后端 | **Metal（统一内存，主打）**、CPU | Metal / CUDA / ROCm / CPU | Metal / CUDA / CPU | Metal / CUDA / CPU |
| **能微调 LoRA** | ✅ **本机原生**（`mlx_lm.lora`） | ❌（可训但非其定位） | ❌ | ❌ |
| 能在非 Apple 平台跑 | ⚠️ **为 Apple Silicon 设计**（Linux/CUDA 属实验性，别当生产跨平台方案） | ✅ | ✅ | ✅ |

**它真正的差异化是两件事**：① **本机微调**——`mlx_lm.lora` / `fuse` 把「量化底座 + LoRA + 合并导出」做成了三条命令，是四家里唯一开箱可训的；② **贴着 Apple 硬件写**——统一内存 + Metal 原生算子，同一份权重在 decode 上通常比 GGUF 路线更快（见 [benchmark.md](./benchmark.md)）。

**别把它当"又一个推理引擎"**：`mlx` 是类比 NumPy/PyTorch 的**数组框架**，`mlx-lm` 才是 LLM 工具箱。只推理的话它不是最省事的（Ollama 更省事）；要微调、要在 Python 里直接操作 logits/embedding，它才是答案。

---

## 1. 概念先分清：`mlx` 与 `mlx-lm`

| 包 | 是什么 | 本文关注点 |
|---|---|---|
| `mlx` | Apple 的**数组计算框架**（懒执行、统一内存、自带 autograd），相当于 Apple 的 NumPy | 只关心 `mx.default_device()` 是否为 GPU |
| `mlx-lm` | 基于 `mlx` 的**LLM 推理 + 微调工具箱**，提供 `mlx_lm.generate/server/convert/lora/fuse/...` | 本文主体 |
| `mlx-community`（HF 组织） | 社区**预量化模型仓库**（`mlx-community/Qwen3-0.6B-4bit` 之类） | 模型来源之一 |

```shell
# 确认 Metal 可用（最关键的一行）
python -c "import mlx.core as mx; print(mx.default_device())"
# 本机输出：Device(gpu, 0)   ← gpu 即 Metal；若是 Device(cpu, 0) 说明没吃到 GPU
```

---

## 2. 安装

### 2.1 推荐方式（本机实测口径）

Python 版本要求：**3.9+，但强烈建议 3.10~3.12**。本机用的是 `uv` 建的独立 venv：

```shell
# ① 建 venv（uv 0.11.4；也可用 python3.12 -m venv）
uv venv --python 3.12 ~/.venvs/mlx-lm

# ② 装 mlx-lm（会顺带拉 mlx）
~/.venvs/mlx-lm/bin/python -m ensurepip        # uv venv 默认无 pip
~/.venvs/mlx-lm/bin/python -m pip install -U mlx-lm
# 或者用 uv：uv pip install --python ~/.venvs/mlx-lm/bin/python -U mlx-lm
```

装完 `~/.venvs/mlx-lm/bin/` 下会出现一组命令：`mlx_lm.generate`、`mlx_lm.server`、`mlx_lm.convert`、`mlx_lm.lora`、`mlx_lm.fuse`、`mlx_lm.benchmark` 等（见 §3）。

⚠️ **本机的坑**：系统 `python3` 是 **3.9**，直接 `python3 -m pip install mlx-lm` 会踩依赖解析问题；同时 3.9 标准库 **不跟随 HTTP 308 重定向**（`urllib.error.HTTPError: 308`），用它下载 HF 模型会直接失败。**一律用 venv 里的 Python 3.12**。

### 2.2 装完的版本快照（本机）

| 包 | 版本 |
|---|---|
| `mlx` | 0.32.2 |
| `mlx-lm` | **0.31.3**（2026-09-12 查 PyPI，即最新稳定版） |
| `transformers` | 5.17.0 |
| `huggingface-hub` | 1.31.0 |
| `hf-transfer` / `hf-xet` | 0.1.9 / 1.6.0 |
| Python | 3.12.13 |

---

## 3. 子命令地图（`mlx_lm` 统一入口）

`mlx_lm` 本身是个分发器，17 个子命令：

| 分组 | 子命令 | 用途 |
|---|---|---|
| **推理** | `generate` | 单轮生成（CLI 主力） |
| | `chat` | 终端交互式对话 |
| | `server` | OpenAI 兼容 HTTP 服务 |
| | `cache_prompt` | 预计算并缓存 prompt 的 KV |
| **模型转换** | `convert` | HF（PyTorch）→ MLX，可顺带量化 |
| | `fuse` | 把 LoRA adapter 合并进底座；可 `--export-gguf` |
| | `upload` / `share` | 上传 HF / 起共享链接 |
| **微调** | `lora` | LoRA / DoRA / 全参微调 |
| **量化进阶** | `awq` / `gptq` / `dwq` / `dynamic_quant` | AWQ / GPTQ / 蒸馏权重量化 / 动态混合精度 |
| **评测** | `benchmark` | 吞吐压测（比 `generate` 的打印数字可靠，见 §5.3） |
| | `perplexity` / `evaluate` | 困惑度 / LM eval harness |
| **管理** | `manage` | 查看已缓存模型、清理 |

```shell
~/.venvs/mlx-lm/bin/mlx_lm --help     # 只打印子命令清单，不带参数细节
~/.venvs/mlx-lm/bin/mlx_lm.generate --help   # 看某个子命令的参数
```

---

## 4. 模型从哪来：两条路

### 4.1 路 A：直接下 `mlx-community` 预量化模型（推荐）

`mlx-community` 上有大量「已转成 MLX 并量化好」的仓库，命名规律 `mlx-community/<模型>-<比特>bit`。本机用的：

```shell
~/.venvs/mlx-lm/bin/hf download mlx-community/Qwen3-0.6B-4bit \
  --local-dir ~/mlx-models/Qwen3-0.6B-4bit
```

### 4.2 ⚠️ 镜像下载的坑（本机踩实）

国内走 `hf-mirror.com` 是常规操作，但 **`hf` CLI 在本机实测里会在 safetensors 上"假死"**：

| 现象 | 说明 |
|---|---|
| 小文件（tokenizer/config）秒下 | `Fetching 11 files` 很快到 10/11 |
| **最后的大权重文件卡住** | `.incomplete` 长期为 **0 字节**；换 `HF_HUB_ENABLE_HF_TRANSFER=1`、`HF_HUB_DISABLE_XET=1` 均无效 |
| 同时用 `curl` 直连同一 URL | **40 MB/s，320MB 的权重大约 8 秒下完** |

结论：**镜像带宽没问题，是客户端（xet/hf_transfer 路径）在卡**。稳定做法是「小文件用 `hf`，大权重用 `curl -L`」：

```shell
# 大文件用 curl 直连（-L 必须，镜像会 302/308 跳到 xet CDN）
curl -L -o ~/mlx-models/Qwen3-0.6B-4bit/model.safetensors \
  https://hf-mirror.com/mlx-community/Qwen3-0.6B-4bit/resolve/main/model.safetensors

# 校验：比对文件名里的 etag（=sha256）与本地哈希
shasum -a 256 ~/mlx-models/Qwen3-0.6B-4bit/model.safetensors
```

⚠️ **`urlretrieve` / 非原子直写会留下"半截文件"**：若下载中断，磁盘上是一个长度不足的 `model.safetensors`，而按「文件存在就 skip」判重的脚本会把它当成已完成 → 得到损坏模型。**重下前必须先 `rm -f` 目标文件**。

### 4.3 路 B：自己转 —— `mlx_lm.convert`

输入可以是**任意标准 HF 仓库**（PyTorch safetensors，无需先转 MLX）：

```shell
# 不量化，只转格式（fp16/bf16）
mlx_lm.convert --hf-path Qwen/Qwen3-0.6B --mlx-path ~/mlx-models/Qwen3-0.6B-mlx-bf16

# 转格式 + 8-bit 量化
mlx_lm.convert --hf-path Qwen/Qwen3-0.6B -q --q-bits 8 --mlx-path ~/mlx-models/Qwen3-0.6B-8bit
```

参数表：

| 参数 | 说明 |
|---|---|
| `--hf-path` / `--model` | 输入：本地目录或 HF repo id |
| `--mlx-path` | 输出目录（**必给**） |
| `-q` / `--quantize` | 开启量化 |
| `--q-bits` | 每权重比特数（常用 4 / 8） |
| `--q-group-size` | 量化分组大小（默认 64，与 `mlx-community` 预量化仓库一致） |
| `--q-mode` | **`affine`（默认）/ `mxfp4` / `nvfp4` / `mxfp8`** —— 浮点 4-bit 格式（MX/NV FP4）需新硬件指令，用前先确认芯片支持 |
| `--quant-predicate` | **混合比特配方**：`mixed_2_6` / `mixed_3_4` / `mixed_3_6` / `mixed_4_6`（敏感层给高比特） |
| `--dtype` | 非量化参数的保存类型（默认跟 `config.json` 的 `torch_dtype`） |
| `-d` / `--dequantize` | 反向：量化模型还原成浮点 |
| `--upload-repo` | 转完直接推 HF |

**本机实测**：0.6B 模型 `-q --q-bits 8` → 输出日志 `Quantized model with 8.501 bits per weight`，**耗时约 1.2 秒**，产物 615MB（原始 bf16 为 1.1GB，4-bit 版为 336MB）。

---

## 5. 推理

### 5.1 `mlx_lm.generate`（CLI 主力）

```shell
mlx_lm.generate --model ~/mlx-models/Qwen3-0.6B-4bit \
  --prompt "用一句话说明什么是 KV Cache" \
  --max-tokens 128 --temp 0.3
```

| 参数 | 说明 |
|---|---|
| `--model` | 本地目录或 HF repo id；**不给会用默认 `mlx-community/Llama-3.2-3B-Instruct-4bit` 去下载** |
| `-p/--prompt` | 提示词；`-` 表示从 stdin 读 |
| `-m/--max-tokens` | 最大生成 token 数 |
| `--temp` / `--top-p` / `--min-p` / `--top-k` | 采样参数 |
| `--xtc-probability` / `--xtc-threshold` | XTC 采样（剔高概率 token 换多样性），默认关闭 |
| `--system-prompt` | system 消息，套进 chat template |
| `--ignore-chat-template` | **裸跑 prompt**（调试 base 模型用，聊天场景误用会答非所问） |
| `--use-default-chat-template` | 忽略模型自带模板，用内置默认模板 |
| `--chat-template-config` | 给模板传 JSON 参数（如 `enable_thinking`） |
| `--adapter-path` | 挂 LoRA adapter |
| `--max-kv-size` | KV cache 上限（超了会滚动窗口） |
| `--kv-bits` / `--kv-group-size` / `--quantized-kv-start` | **KV Cache 量化**（`kv-bits=8` 可显著降长上下文内存） |
| `--prompt-cache-file` | 复用 prompt 的 KV |
| `--draft-model` / `--num-draft-tokens` | **投机解码**（草稿模型需与主模型**同词表**） |
| `--quantize-activations` | 激活也量化（省内存，需硬件支持） |

**本机实测（Qwen3-0.6B-4bit）**：

| 场景 | 输出 |
|---|---|
| 中文 prompt，64 tokens | `Prompt 14 tokens, 17.7 tok/s` / `Generation 64 tokens, **380.8 tok/s**` / Peak **0.416 GB** |
| 代码 prompt，150 tokens，temp 0.7 | `Generation 150 tokens, **392.1 tok/s**` / Peak **0.442 GB** |

⚠️ **`generate` 打印的 prefill 数字别拿来做横向对比**：14~16 个 token 的 prompt 处理时间是**首 token 冷启动**（graph 编译 + 权重首次触达）主导的，17.7 tok/s 完全不能代表 prefill 能力。要用压测口径请走 `mlx_lm.benchmark`（§5.3）。

### 5.2 `mlx_lm.chat`

终端交互式对话，进出都是 chat template。适合快速验证模板是否正确（模型若答非所问/复读，多半是模板问题）。参数与 `generate` 基本一致。

### 5.3 `mlx_lm.benchmark`（**推荐用它取数**）

```shell
mlx_lm.benchmark --model ~/mlx-models/Qwen3-0.6B-4bit -p 512 -g 128 -n 3 -b 1
```

| 参数 | 说明 |
|---|---|
| `-p/--prompt-tokens` | prompt 长度 |
| `-g/--generation-tokens` | 生成长度 |
| `-b/--batch-size` | 批大小（测**连续批处理**吞吐） |
| `-n/--num-trials` | 重复次数（会先 warmup） |
| `--prefill-step-size` | prefill 分块大小（默认 2048） |
| `--quantize-activations` / `--pipeline` / `--delay` | 激活量化 / 用流水线并行替代张量并行 / 试验间隔 |

**本机实测（Qwen3-0.6B-4bit，`-p 512 -g 128`）**：

| batch | prompt tok/s（prefill） | generation tok/s（decode，**合计**） | 峰值内存 |
|---|---|---|---|
| 1 | **5537** | **351.7** | 0.918 GB |
| 4 | 6297 | 799.2（≈200/路） | 1.451 GB |
| 8 | 6362 | 975.3（≈122/路） | 1.695 GB |

两点观察：① **prefill 与 batch 几乎无关**（算力受限，本来就把整批并行算掉）；② **decode 总吞吐随 batch 近似线性涨、单路变慢**——这正是连续批处理用「单请求延迟」换「系统吞吐」的经典形态。对照 `OLLAMA_NUM_PARALLEL=1` 的默认值，能解释为什么同模型下 Ollama 并发表现差。

### 5.4 `mlx_lm.server`（OpenAI 兼容）

```shell
mlx_lm.server --model ~/mlx-models/Qwen3-0.6B-4bit --port 8080
```

| 参数 | 说明 |
|---|---|
| `--model` | 启动时加载的模型（必须是本地目录或可解析的 repo id） |
| `--host` / `--port` | 默认 `127.0.0.1` / **`8080`**（注意不是 1234） |
| `--adapter-path` | 挂 LoRA |
| `--draft-model` / `--num-draft-tokens` | 投机解码 |
| `--chat-template` / `--use-default-chat-template` / `--chat-template-args` | 模板控制（`--chat-template-args '{"enable_thinking":false}'` 可关思考） |
| `--temp` / `--top-p` / `--top-k` / `--min-p` / `--max-tokens` | **请求未指定时的默认采样参数**；`temp` 默认 **0.0**（贪心）、`max-tokens` 默认 **512** |
| `--decode-concurrency` / `--prompt-concurrency` | 可批处理的并发 decode / prompt 条数，默认 **32 / 8** |
| `--prompt-cache-size` / `--prompt-cache-bytes` | KV cache 池中可保留的条目数 / 字节上限 |
| `--prefill-step-size` | 默认 2048 |
| `--allowed-origins` | CORS，默认 `*` |
| `--log-level` / `--pipeline` / `--trust-remote-code` | 日志 / 流水线并行 / 信任远端代码 |

**端点全清单（读源码核实，非文档推测）**：

| 端点 | 方法 | 说明 |
|---|---|---|
| `/v1/models` | GET | 返回**一个**模型，`id` = 启动时的 `--model` 值（本地路径或 repo id） |
| `/health` | GET | 返回 `{"status": "ok"}` |
| `/v1/chat/completions` | POST | 聊天补全 |
| `/chat/completions` | POST | 同上（**无 `/v1` 前缀的别名**） |
| `/v1/completions` | POST | 传统文本补全 |
| 其它一切路径 | — | **404**（没有 `/v1/embeddings`、没有 `/v1/responses`、没有 `/metrics`） |

**请求里 `model` 字段的规则（重要坑）**：

- 服务端逻辑是 `requested_model = body.get("model", "default_model")`，然后把该值当作**模型路径去 `load()`**；
- 因此合法取值只有三个：**启动时的 `--model` 原值**、别名 **`"default_model"`**、**不传该字段**；
- 填一个别的名字（例如抄了 Ollama 的 `qwen3`）→ 服务端会**尝试去 Hugging Face 拉这个 repo**，返回 `401 / Repository Not Found`，而不是「模型不存在」之类的本地报错。

```shell
# 非流式
curl http://127.0.0.1:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"default_model","messages":[{"role":"user","content":"你好"}],"max_tokens":64}'

# 流式
curl -N http://127.0.0.1:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"default_model","messages":[{"role":"user","content":"你好"}],"max_tokens":64,"stream":true}'
```

**本机实测输出特征**（与"标准 OpenAI"的差异，接客户端时要注意）：

| 项 | 观察 |
|---|---|
| 响应头 | `system_fingerprint` 形如 `0.31.3-0.32.2-macOS-26.6.2-arm64-...`（`mlx-lm` + `mlx` 版本 + 平台） |
| 思考型模型 | 回复里出现**非标准字段** `message.reasoning`；`max_tokens` 太小会被思考过程吃光，此时 `message.content` **可能整个缺失**，严格校验的客户端会炸 |
| 流式 | 标准 SSE `data: {...}` + 结尾 `data: [DONE]`；**每条消息前有 `: keepalive N/10` 注释行**，解析器需容忍注释行 |
| `usage` | 含 `prompt_tokens_details.cached_tokens` |

**优雅停止**：`kill <pid>`（SIGTERM）可靠，端口立刻释放。**本机实测 SIGINT（Ctrl-C 的 `kill -INT`）在数秒内未退出**，脚本里请直接用 SIGTERM。

---

## 6. 微调：`mlx_lm.lora` + `mlx_lm.fuse`（**差异化能力**）

### 6.1 数据格式

`--data` 指向一个目录，内含 `train.jsonl` / `valid.jsonl` / `test.jsonl`（三个都要有，`test` 只在 `--test` 时用）。每行一条样本，两种写法：

```json
{"messages": [{"role": "user", "content": "什么是KV Cache？"}, {"role": "assistant", "content": "..."}]}
```
```json
{"prompt": "什么是KV Cache？", "completion": "..."}
```

⚠️ 混用两种格式会在切分/掩码阶段出问题；**同一份数据只用一种**。也可以直接给 HF dataset 名字（如 `mlx-community/wikisql`）。

### 6.2 训练

```shell
mlx_lm.lora --model ~/mlx-models/Qwen3-0.6B-4bit --train \
  --data /tmp/lora-data --adapter-path /tmp/lora-adapters \
  --iters 20 --batch-size 1 --num-layers 4 --max-seq-length 512 \
  --learning-rate 1e-5 --steps-per-report 5 --steps-per-eval 20 --val-batches 1
```

| 参数 | 说明 |
|---|---|
| `--train` / `--test` | 训练 / 训完在 test 集评测 |
| `--fine-tune-type` | **`lora`（默认）/ `dora` / `full`（全参）** |
| `--optimizer` | `adam` / `adamw` / `muon` / `sgd` / `adafactor` |
| `--num-layers` | 微调多少层，默认 **16**，`-1` = 全部 |
| `--mask-prompt` | prompt 部分不计入 loss（指令微调常用） |
| `--batch-size` / `--iters` / `--learning-rate` | 训练超参 |
| `--grad-accumulation-steps` / `--grad-checkpoint` | 等效大 batch / 梯度检查点省内存 |
| `--max-seq-length` / `--clear-cache-threshold` | 序列长度上限 / 分配器缓存过大时清理 |
| `--adapter-path` | adapter 存/取路径 |
| `--resume-adapter-file` / `--save-every` | 断点续训 / 定期保存 |
| `--report-to` / `--project-name` | `wandb` / `swanlab` 上报 |
| `-c/--config` | 用 YAML 配置文件替代全部命令行参数 |

**本机实测（4-bit 底座 + LoRA = QLoRA，0.6B、20 iters、`--num-layers 4`）**：

| 项 | 数据 |
|---|---|
| 可训练参数 | **0.121%**（0.721M / 596.05M） |
| 训练损失 | Iter 5 → 5.255，Iter 20 → **2.706** |
| 验证损失 | 起始 5.178 → Iter 20 **2.771** |
| 速度 | ~34 it/s、~1769 tokens/s（Iter 10 之后稳定） |
| 峰值内存 | **0.563 GB**（`mlx` 分配器口径）/ 进程 max RSS 691MB |
| 总耗时 | **8.37 秒** |

**在 4-bit 量化底座上直接训 LoRA（QLoRA）是默认能力**，不需要先把底座还原成 fp16——这是它比"先转 GGUF 再想训练"省事的地方。

### 6.3 合并与导出：`mlx_lm.fuse`

```shell
# 把 adapter 合进底座（保留量化）
mlx_lm.fuse --model ~/mlx-models/Qwen3-0.6B-4bit \
  --adapter-path /tmp/lora-adapters --save-path ~/mlx-models/Qwen3-0.6B-4bit-lora
```

| 参数 | 说明 |
|---|---|
| `--save-path` | 输出目录 |
| `--dequantize` | 顺带**还原成浮点**（要导出 GGUF 时通常需要） |
| `--export-gguf` | **导出 GGUF** |
| `--gguf-path` | GGUF 输出路径（默认 `ggml-model-f16.gguf`） |
| `--upload-repo` | 推到 HF |

**本机实测的硬限制**：`--export-gguf` 在 `mlx-lm 0.31.3` 里**只支持 `model_type` 为 `llama` / `mixtral` / `mistral` 的模型**，其它架构直接抛
`ValueError: Model type qwen3 not supported for GGUF conversion.`
——所以"MLX 能导出 GGUF"是真的，但**覆盖范围很窄**，别指望拿它做通用的格式桥。

另可用 `generate --adapter-path /tmp/lora-adapters` 直接挂 adapter 推理（本机实测可用，40 tokens / 309.7 tok/s / Peak 0.373 GB），不必先 fuse。

---

## 7. 与 GGUF 路线的取舍

| 你的目标 | 选 MLX | 选 GGUF（llama.cpp / Ollama） |
|---|---|---|
| Mac 上**本机微调 LoRA** | ✅ 唯一开箱路径 | ❌ |
| 要在 Python 里改 logits / 拿 embedding / 自定义采样 | ✅ 直接是 `mlx` 数组 | ⚠️ 得走 server 或绑 `llama-cpp-python` |
| 极限参数控制（mmap、线程、NUMA） | ❌ 参数面窄 | ✅ |
| 一条命令跑起来 / 生态与工具链 | ❌ | ✅ Ollama |
| 跨平台（Linux/Windows/CUDA） | ❌ 绑 Apple | ✅ |
| 单请求 decode 吞吐 | ✅ 通常更快（见 [benchmark.md](./benchmark.md)） | ⚠️ 略低 |
| 模型格式可复用性 | ❌ safetensors 自成一套 | ✅ 三家共享 |

**一句话**：**要训 / 要在 Python 里玩张量 → MLX；只要跑 → GGUF 那条线更省事**。同一台 Mac 上两者并存是最优解——`mlx-community` 一份、Ollama 一份，客户端只换 `base_url`（端口不同：MLX 默认 **8080**，Ollama **11434**，LM Studio **1234**）。

---

## 8. 坑（踩到就往这里补）

1. **`mlx_lm.server` 里 `model` 字段填错 → 401 而不是报「模型不存在」** → 服务端会把它当成 HF repo id 去拉取。合法值只有「启动时的 `--model` 原值」「`default_model`」「不传」。见 §5.4。
2. **`hf` CLI 在镜像上下不动大权重** → 小文件正常、`.incomplete` 长期 0 字节；换 `HF_HUB_ENABLE_HF_TRANSFER=1` 或 `HF_HUB_DISABLE_XET=1` 都无效。**改用 `curl -L`**（本机 40 MB/s）。
3. **下载中断留下半截 `model.safetensors`** → 非原子直写 + 「存在即跳过」的判重 = 静默损坏。**重下前先 `rm -f`**，并比对 etag/sha256。
4. **系统 `python3`（3.9）不跟随 308 重定向** → 用它跑下载脚本会 `urllib.error.HTTPError: 308`。**用 venv 里的 3.12**。
5. **`generate` 打印的 prefill tok/s 很低（十几 tok/s）** → 是冷启动 + graph 编译，不是引擎慢；要取数用 `mlx_lm.benchmark`。
6. **填了 `model` 却"加载到别的模型"** → `--model` 缺省会去下 `mlx-community/Llama-3.2-3B-Instruct-4bit`，务必显式指定。
7. **思考型模型只返回 `reasoning`、`content` 为空** → `max_tokens` 被思考过程吃光（非流式时尤其明显）。给足预算，或用 `--chat-template-args '{"enable_thinking":false}'` 关掉。
8. **流式解析器被 `: keepalive N/10` 卡住** → 那是 SSE 注释行，不是 JSON，解析前要跳过。
9. **`--export-gguf` 报 `Model type xxx not supported`** → 0.31.3 只支持 `llama` / `mixtral` / `mistral`。
10. **`kill -INT` 停不掉 server** → 本机实测 SIGINT 数秒内不退出，用 `kill`（SIGTERM）。
11. **端口记错** → MLX server 默认 **8080**，不是 Ollama 的 11434、也不是 LM Studio 的 1234。
12. **`uv venv` 里没有 `pip`** → `python -m pip` 直接报 `No module named pip`；先 `ensurepip`，或全程用 `uv pip`。
13. **长上下文 OOM** → 开 `--kv-bits 8` 量化 KV，或设 `--max-kv-size` 限窗口；KV cache 才是长上下文内存主体（对照 [benchmark.md](./benchmark.md) 里的内存拆解）。
14. **`mlx_lm.fuse --export-gguf` 用在量化模型上** → 即便架构支持，也通常需要 `--dequantize`；量化权重不能直接写 GGUF。

---

## 9. 工程建议

1. **取性能数字一律用 `mlx_lm.benchmark`，不要用 `generate` 的输出**——后者的 prefill 数字被冷启动污染，写进报告会误导。
2. **模型统一放一个目录（本机 `~/mlx-models/`）并按 `模型-比特` 命名**，让「同模型的 4/8/bf16 三档」并排存在，压测时直接换 `--model` 就能出对照表。
3. **服务端固定 `"model": "default_model"`** 当契约：客户端代码写死这个字符串，换底座只改启动命令。
4. **微调先跑 20 iters 的烟测**（0.6B 只要 8 秒）：确认数据格式、loss 在降、adapter 能存，再上真数据集——数据格式错误在长训练里很贵。
5. **要跨运行时复用模型，选 GGUF 那条线**；MLX 的 safetensors 不通用，只能用 `fuse --export-gguf` 且架构受限。
6. **长上下文场景先量 KV 再做决定**：`--kv-bits 8` 往往是"几乎不掉点、内存砍半"的那一档（详见 [环节10-推理解码与KV缓存详解](../../foundation/transformer/环节10-推理解码与KV缓存详解.md)）。
7. **别把 `mlx_lm.server` 当生产服务**：启动时会打印 `mlx_lm.server is not recommended for production as it only implements basic security checks.`，且无认证、无鉴权、无 `/metrics`。

---

## 10. 高频追问

1. **MLX 和 llama.cpp 在 Mac 上谁快？**
   同模型同口径实测：Qwen3-0.6B **MLX 4-bit decode 349.3 tok/s**、**GGUF Q4_K_M（llama-bench）282.8 tok/s**，MLX 快约 24%，且权重文件更小（336MB vs 493MiB）。完整表与测法见 [benchmark.md](./benchmark.md)。
2. **MLX 是"推理框架"还是"训练框架"？**
   都是。`mlx` 是通用数组框架（有 autograd），`mlx-lm` 在这之上提供了推理**和** LoRA/DoRA/全参微调。四家里唯一能本机训的。
3. **一定要用 `mlx-community` 的预量化模型吗？**
   不必。`mlx_lm.convert` 能吃任何标准 HF PyTorch 仓库，自己指定 `--q-bits` / `--q-mode` / `--quant-predicate`。
4. **4-bit 底座还能训 LoRA 吗？**
   能，就是 QLoRA。本机实测在 `Qwen3-0.6B-4bit` 上直接训，可训练参数占比 0.121%。
5. **MLX 能把模型导出成 GGUF 给 llama.cpp 用吗？**
   有 `mlx_lm.fuse --export-gguf`，但 **0.31.3 只支持 `llama` / `mixtral` / `mistral` 三种 `model_type`**，Qwen 系直接报错。别当通用格式桥。
6. **MLX 的 OpenAI 兼容端点有哪些？**
   只有 `/v1/models`(GET)、`/health`(GET)、`/v1/chat/completions`(POST)、`/chat/completions`(POST)、`/v1/completions`(POST)。**没有 embeddings / responses / metrics**。需要这些就别选它。
7. **量化档位怎么选？**
   本机同模型实测：bf16 → 8-bit → 4-bit，decode **162.8 → 257.7 → 349.3 tok/s**，峰值内存 **1.960 → 1.223 → 0.918 GB**。4-bit 是默认甜点；对精度敏感再上 8-bit。数据见 [benchmark.md](./benchmark.md)。
8. **为什么 prefill 和 batch size 几乎无关？**
   因为 prefill 是**算力受限**（整批一次性并行算完），decode 是**内存带宽受限**（逐 token 读全部权重）。这是 [环节11 §1](../../foundation/transformer/环节11-服务化与推理引擎详解.md) 的核心结论，本机数据再次印证。

---

## 11. 来源

- 官方仓库：[`ml-explore/mlx-lm`](https://github.com/ml-explore/mlx-lm)、[`ml-explore/mlx`](https://github.com/ml-explore/mlx)、文档站 <https://ml-explore.github.io/mlx-lm/>
- 预量化模型：Hugging Face 组织 [`mlx-community`](https://huggingface.co/mlx-community)（本机用 `mlx-community/Qwen3-0.6B-4bit`）
- 版本核对：PyPI `mlx-lm` 元数据（2026-09-12 查得最新 **0.31.3**，与本机一致）
- 本机实测环境：Apple **M4 Pro / 48GB** / macOS 26.6.2 / `mlx` 0.32.2 + `mlx-lm` 0.31.3 / Python 3.12.13
- 命令参数以本机 `mlx_lm.<sub> --help` 输出为准（2026-09-12）；`--export-gguf` 的支持架构来自 `mlx_lm/fuse.py` 源码；`server` 端点与 `model` 字段行为来自 `mlx_lm/server.py` 源码

> ⚠️ `mlx-lm` 迭代很快（子命令与参数名会变），**跑之前先 `--help` 确认**；本文数据是本机单机单次实测，绝对值随热/冷启动、内存压力波动，**看趋势比看绝对值重要**。

---

## 相关笔记

- 总览与选型：[本地推理运行时 · 操作手册](./README.md)
- 姊妹篇：[llama-cpp.md](./llama-cpp.md)（同模型 GGUF 对照）、[ollama.md](./ollama.md)、[lm-studio.md](./lm-studio.md)
- 跨运行时实测数据与测法：[benchmark.md](./benchmark.md)
- 原理与选型：[环节11-服务化与推理引擎详解](../../foundation/transformer/环节11-服务化与推理引擎详解.md)（§2.1 Mac 选型、§2.2 GGUF 与量化命名）
- KV Cache 与长上下文成本：[环节10-推理解码与KV缓存详解](../../foundation/transformer/环节10-推理解码与KV缓存详解.md)
- 端侧小模型策略：[SLM 小模型与端侧](../../foundation/slm/README.md)
- 投机解码：[Speculative Decoding](../speculative-decoding/README.md)
