# 本地推理运行时 · 操作手册（Local Inference Runtimes）

> 一句话：把「模型权重 → 本机一个可用的 OpenAI 兼容接口」这条路**亲手走通**，覆盖 **llama.cpp / Ollama / LM Studio / MLX**。
> 本目录是**操作与实测**（安装 / 命令 / 参数 / 压测 / 排错），不是原理讲解。

## 与相邻文档的分工（先看这个，别重复造轮子）

| 想看什么 | 去哪 |
|---|---|
| 推理引擎**原理**（Prefill/Decode、KV Cache、PagedAttention、Continuous Batching）与**选型对比** | [环节11-服务化与推理引擎详解](../../foundation/transformer/环节11-服务化与推理引擎详解.md) §1–§2 |
| Mac / Apple Silicon 的**选型结论**（统一内存、带宽天花板、谁别装） | 同上 §2.1 |
| GGUF 为什么存在、量化命名 Q4_K_M 怎么读 | 同上 §2.2 |
| 端侧小模型的**场景与策略**（该不该上本地） | [SLM 小模型与端侧](../../foundation/slm/README.md) |
| 投机的草稿模型怎么配合 | [Speculative Decoding](../speculative-decoding/README.md) |
| **怎么装、怎么跑、参数怎么调、实测多少 tok/s、报错怎么解** | **本目录** ← |

---

## 一、运行时谱系（四个主角）

| 运行时 | 形态 | 加速后端 | 吃的模型格式 | 典型使用者 |
|---|---|---|---|---|
| **llama.cpp**（新入口 `llama cli` / `llama serve`；旧名 `llama-cli` / `llama-server` 仍在） | C++ 命令行 + 自带 HTTP 服务 | Metal / CUDA / ROCm / CPU（+ BLAS） | GGUF | 想完全掌控参数、脚本化、最小依赖 |
| **Ollama** | 命令行 + 常驻守护进程（内部就是 llama.cpp） | Metal / CUDA / CPU | GGUF（自己封装成 OCI 层） | 要"零配置、一条命令跑起来" |
| **LM Studio** | 桌面 GUI + 内置本地 server | Metal / CUDA / CPU | GGUF / MLX | 不想碰命令行、要可视化管理模型 |
| **MLX / `mlx-lm`** | Apple 官方 Python 包（含 `mlx_lm.server`） | Metal（统一内存，Apple 官方优化） | safetensors（含 4-bit 量化版） | Apple 生态、要**在本机微调** LoRA |

**关于 "llama" 的歧义**：本目录中一律拆成两类——`llama.cpp`（引擎本体，含 `llama-server`）与 Llama 模型家族（权重来源，见 [landscape.md](../../landscape.md)）。Ollama 单独成篇，因为它虽是 llama.cpp 封装，但交互面完全不同。

---

## 二、按需求选路径

| 你的目标 | 走哪条 | 一句话 |
|---|---|---|
| 只想在 Mac 上聊天 | LM Studio 或 Ollama | GUI 拖模型 / `ollama run` 一条命令 |
| 要个本地 API 给程序调 | `llama-server` / `ollama serve` / LM Studio 内置 server / `mlx_lm.server` | 四家都给 `:PORT/v1/chat/completions` |
| 要精细控制（线程数、上下文、KV 量化、mmap） | llama.cpp | 参数最多、文档最底层 |
| Apple 原生 + 要微调 | MLX（`mlx-lm`） | Mac 上唯一实用的 LoRA 训练路径 |
| 要高并发服务化 | **不要用本目录任何一个** | 回 NVIDIA + vLLM / SGLang，见环节11 §2 |

---

## 三、共同底座（三条认知，先记住再看操作）

1. **格式收敛在 GGUF（MLX 除外）**：llama.cpp / Ollama / LM Studio 三家的模型可以互相复用（Ollama 需导入），下载一次多处用。⚠️ **但"能复用"不是保证**：实测 Ollama 的 blob 是裸 GGUF，`deepseek-coder-v2` 能被 llama.cpp 直接加载，`qwen3.5:9b` 却因 `rope.dimension_sections` 元数据不兼容被拒（见 [llama-cpp.md](./llama-cpp.md) §10）——跨运行时迁移前先试加载。GGUF 细节见环节11 §2.2。
2. **接口收敛在 OpenAI 兼容**：四家都暴露 `/v1/chat/completions`（+ `/v1/models`），所以**客户端只换 `base_url` 就能切换引擎**——这正是本地开发的核心红利。
3. **体感速度由内存带宽决定**：`decode tok/s ≈ 内存带宽 ÷ 每 token 需要读过的权重字节数`。所以"量化位数↓ + 模型↓"直接换速度，与 CPU 核心数关系没那么大（prefill 才吃算力）。数字对照见环节11 §2.1。

---

## 四、本目录文档规划

| 文档 | 内容 | 状态 |
|---|---|---|
| [llama-cpp.md](./llama-cpp.md) | ✅ **已完成**。v0.4.0 语义化版本与新 `llama` 统一入口、`-hf` 直拉 HF、server 参数全表（含 `--load-mode` 取代 `--no-mmap` 等变迁）、端点全清单、`llama-bench` 基线、**同模型 vs Ollama 横向对比**、13 条坑 | 2026-09-11 |
| [ollama.md](./ollama.md) | ✅ **已完成**。CLI 速查、Modelfile 指令（含文档未收录的 `RENDERER`/`PARSER`）、原生 `/api/*` 与 OpenAI 兼容层、环境变量、思考型模型 `think` 实测、12 条坑、本机 0.33.3 实测数据 | 2026-09-11 |
| `lm-studio.md` | 模型目录与下载、GUI 关键设置（上下文长度 / GPU offload / KV 量化）、内置 server 与 Local Server API、跨机访问 | 待写 |
| `mlx.md` | `mlx-lm` 安装、HF 模型转换与 4-bit 量化、`generate` / `server` / `lora` 微调、与 GGUF 路线的取舍 | 待写 |
| `benchmark.md` | 跨运行时对比方法：TTFT / TPOT / 峰值内存 怎么测才可比、同模型同 prompt 的实测记录表、Mac 内存档位矩阵 | 待写 |

> **未加链接 = 尚未创建**：待写文档只写文件名（行内代码），不做 Markdown 链接，否则点击时会报「无法解析不存在的文件」；写完后改回相对链接。
>
> 新增运行时（如 vLLM 本地试跑、`candle`、MLC-LLM）时，按同格式加一篇并在上表登记。

---

## 五、「跑通了」的验证清单（每篇写完都要过一遍）

1. `curl http://127.0.0.1:PORT/v1/models` 能列出模型；
2. `/v1/chat/completions` 非流式能返回完整 JSON；
3. `"stream": true` 能逐块吐出（前端打字机效果的前提）；
4. 中文与代码 prompt 各跑一次，检查**对话模板**是否正确（模板错了表现为答非所问或乱码重复）；
5. 记录**峰值内存占用**与 **tok/s**，填进 `benchmark.md`（待写）；
6. 把进程按文档里的方式**优雅停掉**（否则端口被占，下次启动报错）。

---

## 六、坑位索引（踩到就往对应文档里补）

| 症状 | 大概率原因 |
|---|---|
| 启动报端口占用 | 上一个服务没退干净 / Ollama 守护进程常驻 |
| 回答乱码、自问自答、重复 | 对话模板（chat template）不匹配，或未套模板裸跑 base 模型 |
| 速度远低于预期 | 层没卸到 GPU（llama.cpp 的 `-ngl` 太小 / LM Studio offload 没开） |
| 长对话中途开始胡言乱语 | 上下文超了或发生了静默截断，检查实际 `n_ctx` 与 KV 量化 |
| 加载大模型直接 OOM/系统卡死 | 模型 + KV Cache 超过统一内存，降量化档位或降上下文 |
| 量化后能力明显下降 | 小模型 + 低比特特别敏感，需按 [eval](../../reliability/eval/README.md) 回归 |

---

## 相关笔记

- 原理与选型：[环节11-服务化与推理引擎详解](../../foundation/transformer/环节11-服务化与推理引擎详解.md)
- 端侧策略：[SLM 小模型与端侧](../../foundation/slm/README.md)
- 加速技术：[Speculative Decoding](../speculative-decoding/README.md)、[模型路由](../../reliability/model-routing/README.md)
- 量化回归验收：[模型评测与选型方法详解](../../foundation/transformer/模型评测与选型方法详解.md)
- 知识地图：[learning-path.md](../../learning-path.md)（1.4 推理 / 1.5 部署）

> 核查日期：2026-09-11。本地推理工具迭代很快（参数名、默认值、模型格式都可能变），**命令以文中标注的版本与本机实测为准**，跑之前先 `--help` 确认。
