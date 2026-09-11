# LM Studio 操作手册

> 一句话：**把「选模型、下模型、调参数、开 API」全塞进一个 GUI** 的本地推理运行时——不想碰命令行时的默认答案。
> 本文是**操作手册**（装什么 / 点哪里 / 参数什么含义 / API 怎么调），原理与选型见 [环节11-服务化与推理引擎详解](../../foundation/transformer/环节11-服务化与推理引擎详解.md)。
>
> **核查日期**：2026-09-12（口径见文末「来源」）
> ⚠️ **本文无本机实测数据**：本机未安装 LM Studio（无 `LM Studio.app`、无 `lms`），故所有内容来自**官方文档仓库 `lmstudio-ai/docs` 的原文**，文档中未写明的一律标注「文档未给出」，不做推测填充。文中出现的版本快照为文档示例里的 `lms (v0.0.47)`。

---

## 0. 一句话定位

| 维度 | LM Studio | Ollama | llama.cpp | MLX |
|---|---|---|---|---|
| 形态 | **桌面 GUI** + 内置 server | CLI + 常驻守护进程 | C++ CLI + HTTP 服务 | Python 包 |
| 底层引擎 | **llama.cpp + MLX 双引擎可切换** | llama.cpp（封装） | 自身 | 自身（Apple 官方） |
| 模型格式 | **GGUF + MLX** | GGUF（OCI 封装） | GGUF | safetensors（含 4-bit） |
| 适合谁 | 不想敲命令、要可视化管理 | 一条命令跑起来 | 要完全掌控参数 | Apple 生态 + 本机微调 |
| 能否无 GUI 运行 | ✅（`llmster` 无头守护进程） | ✅ | ✅ | ✅ |

**它真正的差异化不是"GUI 好看"，而是两件事**：① **同时支持 GGUF 与 MLX 两套格式**（其它三家都是单格式）；② **`llmster` 让它能脱离 GUI 跑在服务器/CI 上**——所以「LM Studio 只能在桌面用」是过时认知。

---

## 1. 安装：先分清三个东西（最容易搞混的一节）

官方把它们拆成三个独立工具，名字相近但职责不同：

| 工具 | 类型 | 定位 | 何时用 |
|---|---|---|---|
| **LM Studio** | 桌面 GUI 应用 | 完整图形界面（聊天、下载、RAG、MCP、预设、内置 server） | 本机日常使用 |
| **llmster** | **无头守护进程**（headless daemon） | 独立后台服务，**不需要装桌面应用** | Linux 服务器 / 无显示器 GPU 机 / CI / 开机自启后台服务 |
| **`lms`** | 命令行工具（CLI） | 与**桌面应用或 llmster 两者**交互、终端里管理模型 | 脚本化、自动化、排查 |

关键关系：

- `lms` **随桌面应用或 llmster 的下载自动包含**，无需单独安装（开源 MIT：`github.com/lmstudio-ai/lms`）。
- ⚠️ **必须先至少启动过一次 LM Studio（或 llmster），`lms` 才可用**——这是官方文档显式写的前置条件，也是新手第一个坑。
- 若执行 `lms` 命令时 LM Studio 没在运行，**它会自动把 LM Studio 拉起来**。
- 环境要求（`llmster`）见官方 `developer/core/headless`；本文聚焦桌面应用 + `lms`。

---

## 2. 系统要求

| 平台 | 系统版本 | CPU / 芯片 | 内存 | 备注 |
|---|---|---|---|---|
| **macOS** | **14.0+** | **Apple Silicon（M1/M2/M3/M4）** | **建议 16GB+** | ⚠️ **Intel Mac 目前不支持** |
| Windows | — | x64（**必须支持 AVX2**）或 ARM（Snapdragon X Elite） | 建议 ≥16GB | 建议 GPU ≥4GB 独显 |
| Linux | **Ubuntu 20.04+**（AppImage） | x64（默认 AVX2）/ ARM64 | — | 高于 22 的版本官方称「未经过充分测试」 |

- **8GB 内存的 Mac 仍可能运行**，但官方建议只用**较小的模型 + 较小的上下文**。
- 文档层面**没有**「MLX 引擎 vs llama.cpp 引擎各自的硬件门槛」，也没有「内存档位 → 模型参数量」对照表。本机内存档位对应的模型选择，见 [环节11 §2.1](../../foundation/transformer/环节11-服务化与推理引擎详解.md)。

---

## 3. 模型管理与目录

### 3.1 搜索与下载（Discover）

- 入口：**Discover 标签页**（macOS `⌘`+`2`，Windows/Linux `ctrl`+`2`）。
- 搜索框支持三种输入：**关键词**（`llama`、`gemma`、`lmstudio`）、**`user/model`** 形式、**直接粘贴完整 Hugging Face URL**。

### 3.2 量化档位怎么选

- 同一模型会列出多个版本，命名如 `Q3_K_S`、`Q_8`——`Q` = Quantization（量化）。
- 官方建议：**机器性能足够就选 4-bit 或更高**。
- 量化命名规则本身（Q4_K_M 每个字母什么含义）见 [环节11 §2.2](../../foundation/transformer/环节11-服务化与推理引擎详解.md)，LM Studio 文档不解释命名法。

### 3.3 模型目录

- **改目录**：**My Models 标签页** → 修改 models 目录。
- ⚠️ **官方文档未给出默认目录路径**（`download-model.md` 只讲了怎么改，没讲默认在哪）。**请以 My Models 标签页实际显示的路径为准**，不要照抄网上的传闻路径。
- `lms ls` 列出的就是「My Models 里配置的那个目录」下的模型。

---

## 4. GUI 关键设置

### 4.1 按模型保存默认加载参数（Per-model Defaults）

路径：**My Models 标签页 → 点击模型旁的齿轮 ⚙️ → 设置默认参数 → 下次加载生效**。

生效范围很重要：**该模型在应用任何位置被加载时都会用这套默认值，包括通过 `lms load` 命令行加载**——所以这是"让 CLI 和 GUI 行为一致"的正解。

官方列出的典型用途只有三类：**GPU offload、context size、是否启用 Flash Attention**。

### 4.2 加载参数全表（`LLMLoadModelConfig`）

下面这张表来自官方 API 参考（`llm-load-model-config`），是 GUI 高级设置背后的**字段级定义**。**全部 13 个字段均为可选**，官方文档**未声明任何字段的默认值**：

| 字段 | 类型 | 作用 | 注意 |
|---|---|---|---|
| `gpu` | `GPUSetting` | GPU 卸载/分配方式 | ⚠️ **没有** `gpuOffload` / `offloadRatio` 这种数值字段，语义全封装在 `GPUSetting` 里 |
| `contextLength` | number | 上下文窗口（token 数，**含 prompt + 回复**） | 溢出行为由 `contextOverflowPolicy` 决定 |
| `ropeFrequencyBase` | number | RoPE 基频 | 高级参数，高上下文下可能更好 |
| `ropeFrequencyScale` | number | RoPE 频率缩放 | 用于把上下文**外推**到训练长度之外 |
| `evalBatchSize` | number | 单批处理多少 token | 调大更快但内存同步上升 |
| `flashAttention` | boolean | Flash Attention | **V Cache 量化的前置条件** |
| `keepModelInMemory` | boolean | 即使部分层卸载也保留内存驻留 | 交互更快，但**整体 RAM 占用更高** |
| `seed` | number | 随机种子 | 要复现必设 |
| `useFp16ForKVCache` | boolean | KV Cache 用 FP16 存 | 显著降内存，精度略降 |
| `tryMmap` | boolean | mmap 映射模型文件 | ⚠️ **模型大于可用 RAM 时会频繁落盘，反而更慢** |
| `numExperts` | number | MoE 激活专家数 | **仅 MoE 模型有效** |
| `llamaKCacheQuantizationType` | 枚举 \| `false` | **Key** Cache 量化精度 | `false` = 关闭量化 |
| `llamaVCacheQuantizationType` | 枚举 \| `false` | **Value** Cache 量化精度 | ⚠️ **必须同时开 `flashAttention` 才生效** |

**三个高频误区**（都是从这张表纠正出来的）：

1. **KV Cache 量化不是单个开关**，而是 **K / V 两个独立字段**；老教程里说的 `llamaKVCacheType` 并不存在。
2. **V Cache 量化单独设了不生效**——它依赖 Flash Attention，必须一起开。
3. `tryMmap` **不是无脑加速**：模型大于可用内存时它会变成性能陷阱。

### 4.3 并行请求（Continuous Batching）

- 路径：**模型加载器 → 打开 "Manually choose model load parameters" → 选模型 → 打开 "Show advanced settings" → 设 `Max Concurrent Predictions`**。
- **默认值：4**。官方未给出取值范围与内存影响说明。
- 原理是 **continuous batching**：多个请求被**动态合并进同一个 batch**，而不是排队。
- ⚠️ **限制很硬**：**目前仅支持 llama.cpp 引擎，MLX 引擎「即将支持」**。前置条件是 **GGUF runtime 升级到 llama.cpp v2.0.0**。
- 这项对应 llama.cpp 的并行槽位（`--parallel` / `n_parallel`），但**官方文档没有给显式参数映射表**（属于语义对应，非文档明文）。
- 验证方式：用聊天界面的 **Split View** 同时发两个请求并排看。

> 与 [ollama.md](./ollama.md) §7 对照：Ollama 的 `OLLAMA_NUM_PARALLEL` **默认 1**（多请求排队），LM Studio 这块**默认 4**——这是两者并发体验差异的直接来源。

### 4.4 投机解码

- 门槛：先切到 **Power User 模式或更高**（模式说明见官方 `user-interface/modes`）。
- 路径：**加载模型 → 聊天侧边栏 `Speculative Decoding` 区域 → 选 `Draft Model`** → 直接聊天即启用。
- **硬性前提**：草稿模型与主模型**必须拥有相同的词汇表（vocabulary）**。
- 官方给的配对示例：

| 主模型 | 草稿模型 |
|---|---|
| Llama 3.1 8B Instruct | Llama 3.2 1B Instruct |
| Qwen 2.5 14B Instruct | Qwen 2.5 0.5B Instruct |
| DeepSeek R1 Distill Qwen 32B | DeepSeek R1 Distill Qwen 1.5B |

- **草稿模型最大尺寸参考**（再大就没收益）：主模型 3B → **无**；7B → 1B；14B → 3B；32B → 7B。
- **加速效果强依赖 prompt 类型**（这是最实用的一条）：
  - 高效：**确定性/离散任务**（如问二次方程求根公式，0.5B 和 70B 给出的答案都一样，草稿几乎必被接受）；
  - 低效：**开放式创作**（"写个以『门吱呀一声开了』开头"的故事，下个词有无数种合理走向，接受率极低）；
  - **草稿模型不够快或建议质量差时，速度可能反而下降**，且一定更耗资源。
- 本目录另有专篇讲原理与自建方案：[Speculative Decoding](../speculative-decoding/README.md)。

### 4.5 model.yaml（模型声明规范）

LM Studio 官方模型目录（`lmstudio.ai/models`）的真实底座，用一个**可移植文件**描述一个模型及其**所有变体**：

| 字段 | 必填 | 作用 |
|---|---|---|
| `model` | ✅ | 逻辑标识符，格式 `publisher/model`（如 `qwen/qwen3-8b`） |
| `base` | | 指向**具体**模型文件，每项含唯一 `key` + `sources`（`type: huggingface` / `user` / `repo`） |
| `metadataOverrides` | | 覆盖元数据（`domain` / `architectures` / `paramsStrings` / `contextLengths` / `vision` / `reasoning` / `trainedForToolUse` 等）—— ⚠️ **仅用于展示，不产生任何功能性改变** |
| `config` | | **烘焙默认运行参数**，分 `operation`（推理时）与 `load`（加载时），两者都是 `fields: [{key, value}]` |
| `customFields` | | 在 UI 暴露模型专属开关，`effects: [{type: setJinjaVariable, variable: xxx}]` |

核心价值：**把「一个模型名对应十几个量化/格式版本」收敛成一个逻辑模型**——例如 `qwen/qwen3-8b` 可同时映射到 `qwen3-8b-gguf`、`qwen3-8b-mlx-4bit`、`qwen3-8b-mlx-8bit` 三个实际仓库。

`config` 中已知可用的 key（文档中实际出现的）：

```yaml
config:
  operation:
    fields:
      - key: llm.prediction.topKSampling
        value: 20
      - key: llm.prediction.temperature
        value: 0.7
      - key: llm.prediction.minPSampling   # 值可为结构化对象 {checked: true, value: 0}
        value: 0
  load:
    fields:
      - key: llm.load.contextLength
        value: 42690
```

⚠️ 注意：**官方这一页标的是 `Draft`（草稿）**，且明确说「更多细节与最新 schema 见规范仓库」`github.com/modelyaml/modelyaml`。文档中**没有**给出 `llm.load.gpuOffload` / `llm.load.flashAttention` 之类的 `load` 命名空间全量键，也未说明文件存放路径与读取优先级——要用到这些请以规范仓库为准。

---

## 5. `lms` CLI 全命令

### 5.1 命令地图

| 分组 | 命令 | 用途 |
|---|---|---|
| **本地模型** | `lms ls` | 列出磁盘上的模型（对应 My Models 目录） |
| | `lms ps` | 列出**已加载进内存**的模型 |
| | `lms get` | 搜索并下载模型 |
| | `lms load` | 加载模型进内存 |
| | `lms unload` | 卸载模型 |
| | `lms import` | 把模型文件导入 LM Studio |
| | `lms chat` | 终端内交互式对话 |
| **服务** | `lms server start / status / stop` | 启停本地 HTTP 服务器 |
| | `lms log stream` | 流式查看收发请求日志 |
| **运行时** | `lms runtime` | 管理与更新推理运行时（引擎本体） |
| **守护进程** | `lms daemon up / down / status / update` | 管理无头守护进程（llmster） |
| **设备互联** | `lms link enable / disable / status / set-device-name / set-preferred-device` | 管理 LM Link |
| **开发与发布（Beta）** | `lms clone` / `push` / `dev` / `login` | 克隆/上传 artifact、插件开发服务器、登录 |

> 注意：`lms --help` 的输出里**没有** `daemon` 和 `link`，但文档的快速链接表把它们列为正式命令入口——说明该页快照与当前版本存在差异，**以本机 `lms --help` 为准**。

### 5.2 `lms load` 参数全表

| 参数 | 类型 | 说明 |
|---|---|---|
| `[path]` | string | 模型路径；不提供会**提示你选择** |
| `--gpu` | string | 卸载多少到 GPU。**取值只有 `0-1`、`off`、`max`** |
| `--context-length` | number | 上下文 token 数 |
| `--identifier` | string | 为已加载模型指定标识符，**供 API 的 `model` 字段引用** |
| `--ttl` | number | 闲置该**秒数**后自动卸载 |
| `--estimate-only` | flag | **只打印资源估算然后退出，不加载** |
| `--host` | string | 操作**远程** LM Studio 实例（需同子网可达） |

⚠️ **`--gpu` 没有 `auto` 这个取值**：文档明写合法值是 `0-1`/`off`/`max`，而「不指定时 LM Studio 自动决定最优 GPU 使用方式」是**缺省行为**，不是一个可传的值。网上流传的 `--gpu auto` 会报错。

```shell
lms load <model_key>                        # 基本加载
lms load <model_key> --gpu max              # 全部层卸到 GPU
lms load <model_key> --gpu 0.5              # 50% 卸载
lms load <model_key> --context-length 4096  # 指定上下文
lms load <model_key> --identifier "my-model"  # API 里用这个名字引用
lms load <model_key> --ttl 3600             # 闲置 1 小时自动卸载
lms load --estimate-only gpt-oss-120b       # 先看内存够不够，别硬上
```

`--estimate-only` 的实际输出形态（官方示例）：

```
Model: openai/gpt-oss-120b
Estimated GPU Memory:   65.68 GB
Estimated Total Memory: 65.68 GB

Estimate: This model may be loaded based on your resource guardrails settings.
```

估算器会把 `--context-length`、`--gpu`、**是否 Flash Attention**、**是否 vision 模型**等因素一并计入——这是它在同类工具里少见的好功能：**下载 40GB 模型之前先花两秒确认真装不下**。

### 5.3 `lms unload`

| 参数 | 说明 |
|---|---|
| `[model_key]` | 要卸载的模型；不提供会提示选择 |
| `--all` | 卸载**所有**已加载模型 |
| `--host` | 针对远程实例 |

---

## 6. 本地 server 与 API

### 6.1 启动

```shell
lms server start                    # 默认：绑定 127.0.0.1，端口沿用「上次使用过的端口」
lms server start --port 3000        # 显式指定端口
lms server start --cors             # 启用 CORS（Web 前端直连需要）
lms server start --bind 0.0.0.0     # 监听所有 IPv4 接口（局域网可访问）
```

| 参数 | 说明 |
|---|---|
| `--port` | number。⚠️ **不传时用的是「上次使用过的端口」，不是固定值**——脚本里务必显式指定 |
| `--cors` | flag，**未设置时 CORS 处于禁用状态**。官方警告：启用有安全风险，建议同时启用认证 |
| `--bind` | 绑定地址。默认 `127.0.0.1`（仅本机）；`0.0.0.0` = 所有 IPv4 接口。也可用环境变量 **`LMS_SERVER_HOST`** |

配套：`lms server status` 看状态，`lms server stop` 停服，`lms log stream` 实时看收发日志。

### 6.2 OpenAI 兼容端点

**base_url = `http://localhost:1234/v1`**（官方文档示例均假设端口为**默认 1234**）。

| 端点 | 方法 | 说明 |
|---|---|---|
| `/v1/models` | GET | 列出模型 |
| `/v1/chat/completions` | POST | 聊天补全，**支持文本 + 图像输入** |
| `/v1/completions` | POST | 传统文本补全 |
| `/v1/embeddings` | POST | 嵌入向量 |
| `/v1/responses` | POST | **Responses API**——LM Studio 支持 Codex 就是靠它 |

客户端切换成本几乎为零：

```diff
 from openai import OpenAI
 client = OpenAI(
+    base_url="http://localhost:1234/v1"
 )
```

```diff
- curl https://api.openai.com/v1/chat/completions \
+ curl http://localhost:1234/v1/chat/completions \
   -H "Content-Type: application/json" \
   -d '{
-     "model": "gpt-4o-mini",
+     "model": "<LM Studio 里的模型标识符>",
      "messages": [{"role": "user", "content": "Say this is a test!"}],
      "temperature": 0.7
   }'
```

`model` 字段填 **LM Studio 的模型标识符**——用 `lms load --identifier` 固定成好记的名字，比让 API 吃文件路径清爽得多（同 [llama-cpp.md](./llama-cpp.md) 里 `-a/--alias` 的坑）。

除 OpenAI 兼容层外，LM Studio 还提供：**原生 REST API**（`/api/v0/*`，含 load / unload / download / stateful-chats / streaming-events）与 **Anthropic Messages 兼容**（`/v1/messages`）。

> ⚠️ 官方这一页是 **Overview**，**没有**逐条列出「哪些字段被忽略 / 部分支持」。要精确兼容性边界必须逐页看 `openai-compat/*` 子文档，别默认 100% 兼容（对照 [模型服务API协议对比](../../model-cases/providers/模型服务API协议对比.md) 里的「假兼容」清单）。
> ⚠️ 已知的文档空白：**`lms server start` 是否会自动加载模型**，官方文档**未说明**。

### 6.3 跨机访问与安全

```shell
lms server start --bind 0.0.0.0     # 方案 A：监听所有接口
export LMS_SERVER_HOST=0.0.0.0      # 方案 B：环境变量
```

- **任何非 `127.0.0.1` 的绑定都会把服务暴露到 localhost 之外**，官方明确建议**启用认证**（`developer/core/authentication`）后再开。
- `--cors` 同理：默认关闭，开了才允许浏览器跨域直连，开了就要考虑谁能调你的模型。
- 反向操作也支持：`lms load <model> --host <host>` 可以从本机去操作**远端** LM Studio 实例。

---

## 7. 与其他运行时的取舍

| 你的处境 | 建议 | 理由 |
|---|---|---|
| 就是要本机聊天、不想敲命令 | **LM Studio** | GUI 下载 + 齿轮调参 + 内置 server 一条龙 |
| 想 `docker run` 式零配置 | Ollama | 生态与命令更简单（[ollama.md](./ollama.md)） |
| 要脚本化、要抠每一个参数 | llama.cpp | 参数最底层（[llama-cpp.md](./llama-cpp.md)） |
| Apple Silicon 上要**微调 LoRA** | MLX | LM Studio 不做训练 |
| 要**高并发**服务化 | **以上都不合适** | 回 NVIDIA + vLLM / SGLang（[环节11 §2](../../foundation/transformer/环节11-服务化与推理引擎详解.md)） |
| 有台无显示器的 Linux 服务器 | **llmster**（就是 LM Studio 的无头形态） | 不需要 GUI，可开机自启 |

**容易被忽略的定位差异**：LM Studio 是四家里**唯一同时吃 GGUF 和 MLX 两种格式**的，所以在 Apple Silicon 上它可以用 `lms runtime` 切换引擎，直接对比两套后端——这让它顺带成了一个**跨格式对照台**。

---

## 8. 坑（踩到就往这里补）

1. **`lms` 报「命令找不到」或没有反应** → 你还没启动过 LM Studio / llmster。官方前置条件就是「必须先运行一次」。
2. **`lms load --gpu auto` 报错** → `auto` 不是合法取值，合法值是 `0-1` / `off` / `max`；「自动」是不传时的默认行为。
3. **脚本里端口对不上** → `lms server start` 不传 `--port` 会用**上次用过的端口**，不是固定 1234。自动化务必显式 `--port`。
4. **前端 fetch 直接报 CORS 错** → 默认 CORS 是**关闭**的，要 `lms server start --cors`。
5. **设了 V Cache 量化却没效果** → 忘了开 `flashAttention`，V Cache 量化依赖它。
6. **本地并发上不去** → `Max Concurrent Predictions` **默认 4**，但**只有 llama.cpp 引擎支持连续批处理，MLX 引擎尚不支持**。
7. **开了投机解码反而更慢** → 草稿模型选太大 / prompt 是开放式创作。3B 及以下主模型**无收益**；主模型 7B 配 1B、14B 配 3B、32B 配 7B 是官方参考上限。
8. **改了 `metadataOverrides` 却没有任何行为变化** → 它**只是展示字段**，不影响运行。要改行为得动 `config`。
9. **大模型加载时系统卡死** → 用 `lms load --estimate-only` 先估算；再回调 `contextLength` / KV 量化 / `tryMmap`。
10. **`tryMmap` 开了更慢** → 模型比可用 RAM 大时，mmap 会导致频繁磁盘访问，官方明确提示这个反效果。
11. **`--bind 0.0.0.0` 直接暴露到局域网** → 没配认证就是把 GPU 借给整个网段。
12. **Intel Mac 装不上** → 官方**不支持** Intel Mac（macOS 侧只支持 M1–M4）。
13. **`lms --help` 与文档对不上** → 文档快照里 `daemon` / `link` 未出现在 `--help` 输出中，说明文档与实现存在版本漂移，**永远以本机 `--help` 为准**。

---

## 9. 工程建议

1. **把 `--identifier` 当契约用**：加载时固定成 `--identifier my-model`，客户端代码里就写死这个 `model` 值，换权重不用改代码（等价于 llama.cpp 的 `-a/--alias`）。
2. **加载参数用 Per-model Defaults 固化，不要写进启动脚本**：这样 GUI 手动加载和 `lms load` 行为一致，消除"为什么命令行跑出来不一样"的幽灵问题。
3. **上大模型前先 `--estimate-only`**：这是 LM Studio 相对其它三家最实用的一条命令，把 OOM 从"加载时爆炸"提前到"两秒内知道"。
4. **`--ttl` 是共享机器的救命参数**：`--ttl 3600` 让闲置模型自动卸载，避免同事跑了个 70B 把你的内存占满。
5. **无头服务器用 llmster 而不是硬跑 GUI**：官方就是为此设计的（CI、无显示 GPU 机、开机自启）。
6. **要跨机共享就把安全补齐**：`--bind 0.0.0.0` + 认证 + 明确谁在用；纯本机开发保持默认 `127.0.0.1` 最省心。
7. **别把它当服务端高并发方案**：默认并发 4、MLX 后端还不支持批处理，生产高并发请回 vLLM/SGLang。

---

## 10. 高频追问

1. **LM Studio 和 Ollama 到底差在哪？**
   底层都是 llama.cpp（LM Studio 另外还有 MLX 引擎）。差别在**交互面与默认值**：LM Studio 是 GUI 优先、并发默认 4、支持 GGUF+MLX 双格式；Ollama 是 CLI 优先、`OLLAMA_NUM_PARALLEL` 默认 1、只吃 GGUF。**单请求吞吐两者应该接近**（同引擎），并发表现不同是默认值造成的。

2. **`lms` 和 LM Studio 是什么关系？**
   `lms` 是 CLI，**随 app 或 llmster 自动安装**，两者都能驱动。它不是独立工具，也不是必须单独装的包。

3. **没有显示器的服务器上能用吗？**
   能，用 **`llmster`**（无头守护进程），**不需要下载桌面应用**。官方列的场景就是 Linux 服务器、无显示 GPU 机、CI/CD、开机自启。

4. **默认端口是多少？**
   官方 OpenAI 兼容文档说 **1234**；但 `lms server start` 文档说**不传 `--port` 就用「上次使用过的端口」**。两者结合的正确理解是：**首次是 1234，之后会沿用历史值**——所以别赌，显式指定。

5. **KV Cache 量化在哪开？**
   API 层是 `llamaKCacheQuantizationType` / `llamaVCacheQuantizationType` **两个**字段（不是单个 `kvCacheQuantization`），另有 `useFp16ForKVCache` 布尔开关；**V 侧量化必须配 `flashAttention`**。

6. **为什么我设了并发还是排队？**
   确认用的是 **llama.cpp 引擎**（连续批处理目前只支持它），并确认 GGUF runtime 已升到 **llama.cpp v2.0.0**。

7. **model.yaml 改了没生效？**
   分清字段职责：`metadataOverrides` **只影响展示**；要改运行行为得写 `config.operation` / `config.load`。

8. **怎么让它和我的程序对接？**
   它暴露 **OpenAI 兼容 + Anthropic 兼容 + 原生 REST** 三套接口。最省事的做法：客户端只改 `base_url=http://localhost:1234/v1`，把 `model` 填成你 `--identifier` 定的名字。

---

## 11. 来源

- LM Studio 官方文档仓库 [`lmstudio-ai/docs`](https://github.com/lmstudio-ai/docs)，本文核对的具体页面：
  - `0_app/1_basics/lmstudio-vs-llmster-vs-lms.md` — 三个工具辨析、`lms` 随 app 分发、必须先启动一次
  - `0_app/0_root/system-requirements.md` — 平台/芯片/内存要求、Intel Mac 不支持
  - `0_app/1_basics/download-model.md` — Discover、量化选择建议、改模型目录
  - `0_app/5_advanced/per-model.mdx` — Per-model Defaults 入口与生效范围
  - `0_app/5_advanced/parallel-requests.md` — Max Concurrent Predictions 默认 4、仅 llama.cpp
  - `0_app/5_advanced/speculative-decoding.md` — 模式门槛、词表要求、配对表、prompt 依赖性
  - `0_app/3_modelyaml/index.md`（标 `Draft`）— model.yaml 五字段结构与示例
  - `3_cli/index.mdx` — 全部顶层子命令
  - `3_cli/0_local-models/load.md` — `lms load` / `unload` 参数全表、`--estimate-only` 示例
  - `3_cli/1_serve/server-start.mdx` — `--port` / `--cors` / `--bind` 与安全提示
  - `1_developer/3_openai-compat/index.mdx` — 端点清单、base_url、端口 1234
  - `1_python/_7_api-reference/llm-load-model-config.md` — 13 个加载配置字段定义
- 规范与实现：[`modelyaml/modelyaml`](https://github.com/modelyaml/modelyaml)（model.yaml schema）、[`lmstudio-ai/lms`](https://github.com/lmstudio-ai/lms)（MIT）

> ⚠️ 官方文档站**所有页面均未标注发布日期/版本号**，唯一的版本线索是 CLI 页示例输出里的 `lms (v0.0.47)`。LM Studio 迭代较快，**参数名与默认值请以本机 `--help` 与实际界面为准**。

---

## 相关笔记

- 同系列：[llama-cpp.md](./llama-cpp.md)（引擎本体与参数底层）、[ollama.md](./ollama.md)（CLI 优先的对照选手）、[mlx.md](./mlx.md)（Apple 原生 + 本机微调）
- 跨运行时实测数据与测法：[benchmark.md](./benchmark.md)
- 原理与选型：[环节11-服务化与推理引擎详解](../../foundation/transformer/环节11-服务化与推理引擎详解.md)
- 加速策略：[Speculative Decoding](../speculative-decoding/README.md)
- 返回目录：[README.md](./README.md)
