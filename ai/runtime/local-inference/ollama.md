# Ollama 操作手册

> **版本口径**：本机实测 **0.33.3**（2026-09-11，Apple Silicon）；撰写时官方最新为 **0.34.0**（2026-09-05 RC / 09-10 正式发布，核心变化：Ollama 模型可直接在 **ChatGPT Desktop** 内使用 + 结构化输出改进）。
> 官方文档已迁至 **https://docs.ollama.com**（仓库内 `docs/modelfile.md`、`docs/openai.md` 已 404，`docs/api.md` 顶部也标注迁移）。命令与默认值以本机 `--help` / `/api/version` 实测为准。

## 0. 一句话定位

**Ollama = llama.cpp 的"开箱即用"封装 + 模型分发 + 常驻服务**。它把「下载模型、选量化、套对话模板、起 OpenAI 兼容 API、管模型常驻」这些脏活全包了，代价是**参数控制粒度不如裸 llama.cpp**、**并发能力弱**。

| 对比项 | Ollama | 裸 llama.cpp | 结论 |
|---|---|---|---|
| 模型获取 | `ollama pull`，官方库 + 自动量化档 | 自己找 GGUF、自己下载 | Ollama 省事 |
| 对话模板 | 内置在模型包里，自动套 | 靠 `--chat-template` 或手动拼 | Ollama 不易踩模板坑 |
| 参数控制 | Modelfile 11 个 + API options（够用） | 全量（`-ngl`/`--cache-type-k`/`--parallel`…） | 要极限调优选 llama.cpp |
| 并发 | `OLLAMA_NUM_PARALLEL` 默认 **1** | `--parallel N` 直接控制 | 两者都别指望高并发 |
| 服务常驻 | 守护进程 + 模型 `keep_alive` 自动常驻 | 手动起 `llama-server` | Ollama 体感好得多 |

---

## 1. 安装与启动

```bash
# macOS（Homebrew）
brew install ollama

# macOS/Linux 一键脚本（官方）
curl -fsSL https://ollama.com/install.sh | sh

# 启动服务（brew 安装后也可用 brew services start ollama 常驻）
ollama serve          # 默认监听 127.0.0.1:11434

# 验证
curl -s http://127.0.0.1:11434/api/version     # => {"version":"0.33.3"}
ollama -v
```

**新版 CLI 多出的命令**（0.33.x 实测，老教程里没有）：

| 命令 | 作用 |
|---|---|
| `ollama launch` | 启动 Ollama 菜单或某个集成（新） |
| `ollama signin` / `signout` | 登录/登出 ollama.com（用云端模型、推私有模型需要） |
| `ollama stop <model>` | **立即从内存卸载**模型（比等 `keep_alive` 超时快） |

---

## 2. CLI 速查

```bash
ollama list                      # 本地已下载模型
ollama pull qwen3.5:9b           # 下载（支持断点续传）
ollama run qwen3.5:9b            # 交互聊天（无参数则进入 REPL）
ollama run qwen3.5:9b "你好"     # 单次提问
ollama ps                        # 当前驻留内存的模型
ollama show qwen3.5:9b           # 模型信息（参数/template/能力）
ollama show --modelfile qwen3.5:9b   # 反查 Modelfile（派生模型的起点）
ollama cp qwen3.5:9b my-alias    # 复制/改名
ollama rm my-alias               # 删除
ollama stop qwen3.5:9b           # 立即卸载
```

`ollama ps` 输出列（0.33.x，比老版本多了 `CONTEXT`）：

```
NAME           ID              SIZE     PROCESSOR    CONTEXT    UNTIL
qwen3.5:9b     xxx             14 GB    100% GPU     262144     4 minutes from now
```

- `SIZE` 是**实际驻留内存**（权重 + KV Cache），不等于磁盘上的模型大小；
- `PROCESSOR` 显示卸载比例（`100% GPU` / `48%/52% CPU/GPU`）——**排查"为什么慢"先看这一列**；
- `CONTEXT` 是生效的上下文长度（**是否被你自己的设置覆盖，看这里最准**）。

REPL 内常用 `/` 命令（以交互内 `/help` 输出为准）：

```
/set parameter num_ctx 8192     # 临时覆盖参数
/set system "你是一个严谨的助手"  # 临时改 system prompt
/show info                      # 查看当前模型信息
/clear                          # 清空对话上下文
/bye                            # 退出
```

---

## 3. 模型管理

**命名规则**：`model:tag`，可带命名空间（`example/model`），省略 tag 默认 `latest`。

**标签即量化档**：同一个模型不同 tag 往往是不同量化，例 `qwen3.5:9b`（默认档）vs 显式 `qwen3.5:9b-q4_K_M`。选档原则见 [环节11 §2.2 GGUF](../../foundation/transformer/环节11-服务化与推理引擎详解.md)：Q4_K_M 是通用性价比点，Q5/Q6 提升有限但显存涨，Q3 以下小模型容易崩。

**存储位置**：`~/.ollama/models`（macOS），内含 `blobs/`（真实权重层，按 sha256 命名）+ `manifests/`（模型清单）。改目录用 `OLLAMA_MODELS`。

**放进自己的 GGUF**（从 HF 下载的量化文件）：

```bash
# Modelfile
cat > Modelfile <<'EOF'
FROM ./Qwen3.5-9B-Q4_K_M.gguf
PARAMETER num_ctx 8192
PARAMETER temperature 0.7
EOF
ollama create my-qwen -f Modelfile
ollama run my-qwen
```

**量化已有模型**（新版本 `create` 支持 `--quantize`，官方推荐 `q4_K_M` / `q8_0`）：

```bash
ollama create my-q4 -f Modelfile --quantize q4_K_M
```

---

## 4. Modelfile（定制模型的蓝图）

### 4.1 指令清单

官方参考页收录 **8 个**指令（不区分大小写、顺序任意，仅 `FROM` 必需）：

| 指令 | 作用 |
|---|---|
| `FROM` | **必需**。来源三类：已有模型名 / safetensors 目录 / GGUF 文件路径 |
| `PARAMETER` | 运行时参数（见 4.2） |
| `TEMPLATE` | 完整提示模板，Go `text/template` 语法，变量 `.System` / `.Prompt` / `.Response` |
| `SYSTEM` | system message |
| `ADAPTER` | 挂 LoRA / (Q)LoRA 适配器（基础模型必须与微调时一致，否则行为不稳定） |
| `LICENSE` | 许可证文本，随模型分发 |
| `MESSAGE` | 预设对话历史（few-shot 引导），角色 `system`/`user`/`assistant` |
| `REQUIRES` | 声明所需最低 Ollama 版本（如 `REQUIRES 0.5.0`） |

> **文档滞后的两个指令**：本机 `ollama show --modelfile qwen3.5:9b` 实际输出了 `RENDERER qwen3.5` 与 `PARSER qwen3.5`，但官方 Modelfile 参考页**尚未收录**。它们是新版把「模板渲染」与「输出解析」从 `TEMPLATE` 里拆分出来的机制（对应不同模型家族的对话模板与 thinking 解析规则）。看到它们不要手改，用 `TEMPLATE` 覆盖更安全。

### 4.2 `PARAMETER` 列表（官方口径）

| 参数 | 默认值 | 说明 |
|---|---|---|
| `num_ctx` | 官方页写 2048，FAQ 的 `OLLAMA_CONTEXT_LENGTH` 写 4096 | **上下文窗口**。实际上模型包可自带更大默认（本机 `qwen3.5:9b` 实测生效 262144）→ **以 `ollama ps` 的 `CONTEXT` 列为准** |
| `temperature` | 0.8 | 越高越有创造性 |
| `top_k` | 40 | 候选集上限 |
| `top_p` | 0.9 | 核采样 |
| `min_p` | 0.0 | top_p 的替代方案（相对概率阈值） |
| `repeat_last_n` | 64 | 重复惩罚回溯范围（0 禁用，-1 = num_ctx） |
| `repeat_penalty` | 1.0 | 重复惩罚强度 |
| `seed` | 0 | 固定后相同输入产相同输出（可复现） |
| `stop` | — | 停止序列，**一行一条，可写多行** |
| `num_predict` | -1 | 最大生成 token（-1 无限，-2 生成到填满上下文） |
| `draft_num_predict` | 4（独立草稿模型时） | **投机解码**每步草稿 token 上限；设 0 可禁用；内嵌 MTP 张量需显式设置 |

> 只在 **API 的 `options`** 里出现、不在 Modelfile 官方参数表里的还有：`num_gpu`、`num_thread`、`main_gpu`、`num_batch`、`numa`、`use_mmap`、`num_keep`、`typical_p`、`tfs_z`、`presence_penalty`、`frequency_penalty`、`penalize_newline`、`mirostat*`、`draft_num_predict`。想设这些就走 API `options`。

### 4.3 实用示例

```dockerfile
# 从已有模型派生 + 固定 system + 关思考 + 压上下文
FROM qwen3.5:9b

SYSTEM """你是一位严谨的中文技术助理。回答简洁，先给结论再给理由，涉及代码时给可运行示例。"""

PARAMETER temperature 0.3
PARAMETER num_ctx 8192          # 别用默认的超大上下文，KV Cache 吃内存
PARAMETER top_p 0.9
PARAMETER stop "<|im_end|>"
```

```bash
ollama create tech-assistant -f Modelfile
ollama run tech-assistant
```

**反查 + 二次派生**（想改某个定制模型）：

```bash
ollama show --modelfile tech-assistant > Modelfile.base
# 把其中的 FROM 改成 tech-assistant，再叠自己的 PARAMETER
```

---

## 5. 原生 API（`/api/*`）

服务地址 `http://127.0.0.1:11434`，**无鉴权**。所有 duration 字段单位为**纳秒**。

| 方法 | 端点 | 用途 |
|---|---|---|
| POST | `/api/chat` | 对话补全（主用） |
| POST | `/api/generate` | 单 prompt 补全 |
| GET | `/api/tags` | 列出本地模型 |
| GET | `/api/ps` | 列出已加载进内存的模型 |
| POST | `/api/show` | 模型详情（含 `capabilities`） |
| POST | `/api/pull` / `push` | 拉取 / 上传模型 |
| POST | `/api/create` | 从模型/GGUF/safetensors 创建（支持 `quantize`） |
| POST | `/api/copy` / DELETE `/api/delete` | 复制 / 删除 |
| POST | `/api/embed` | 生成嵌入（**取代** `/api/embeddings`） |
| GET | `/api/version` | 版本 |
| HEAD/POST | `/api/blobs/:digest` | 检查 / 推送 blob 层 |

### 5.1 `/api/chat` 请求字段

| 字段 | 说明 |
|---|---|
| `model` | 必填 |
| `messages` | `role` ∈ `system`/`user`/`assistant`/`tool`；`content`、`images`（base64）、`tool_calls`、`tool_name`、`thinking` |
| `tools` | JSON Schema 工具列表（模型需支持） |
| `think` | **思考型模型专用**：`true`/`false` 或 `"low"`/`"medium"`/`"high"`/`"max"` |
| `format` | `"json"` 或 **JSON Schema**（结构化输出，等价于约束解码） |
| `options` | 覆盖 Modelfile 参数（采样、`num_ctx` 等） |
| `stream` | `false` 返回单个对象 |
| `keep_alive` | 请求后模型在内存保留多久，默认 `5m` |

### 5.2 响应字段与性能口径

流式每片含 `message` + `done:false`；最终片额外给：

```
done_reason      stop / length / load / unload
total_duration   总耗时
load_duration    模型加载耗时   ← 冷启动 TTFT 的大头
prompt_eval_count      prompt token 数
prompt_eval_duration   预填充耗时
eval_count             生成 token 数
eval_duration          解码耗时
```

```bash
# 解码速度（tok/s）
eval_count / eval_duration * 1e9
```

### 5.3 两个好用的技巧

```bash
# ① 只加载模型不生成（预热，消除首请求的 load_duration）
curl -s http://127.0.0.1:11434/api/chat -d '{"model":"qwen3.5:9b","messages":[]}'
#    → done_reason: "load"

# ② 立即卸载（等价于 ollama stop）
curl -s http://127.0.0.1:11434/api/chat -d '{"model":"qwen3.5:9b","messages":[],"keep_alive":0}'
#    → done_reason: "unload"
```

`GET /api/ps` 的关键字段：`expires_at`（预计卸载时间，由 `keep_alive` 决定）、`size_vram`（**实际驻留内存**，含 KV Cache）。

---

## 6. OpenAI 兼容层（换 `base_url` 就能用）

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1/", api_key="ollama")  # key 必填但被忽略
```

官方措辞是"compatibility with **parts of** the OpenAI API"——**部分兼容**。

| 端点 | 支持情况 |
|---|---|
| `/v1/chat/completions` | ✅ 最全：streaming、JSON mode、seed、vision、**tools**、`reasoning_effort`、`logprobs`、`n`、`logit_bias` |
| `/v1/completions` | ✅ 但 **`prompt` 只接受字符串**，且不支持 vision / tools |
| `/v1/models`、`/v1/models/{model}` | ✅ `created` = 最近修改时间，`owned_by` 默认 `library` |
| `/v1/embeddings` | ✅ `input` 支持字符串 / 字符串数组 / token 数组 / 嵌套数组 |
| `/v1/responses` | ⚠️ v0.13.3 起支持，但**仅非有状态**（不支持 `previous_response_id`、`conversation`） |
| `/v1/files`、`/v1/assistants`、`/v1/batches`、`/v1/audio/*`、`/v1/moderations` | ❌ 未实现 |

**两个必须知道的绕道**：

```bash
# ① OpenAI 口径没有 num_ctx → 只能靠 Modelfile 固化上下文长度
cat > Modelfile <<'EOF'
FROM qwen3.5:9b
PARAMETER num_ctx 32768
EOF
ollama create qwen3.5-32k -f Modelfile
# 之后 API 里 model 填 qwen3.5-32k

# ② 给只认 gpt-3.5-turbo 的旧客户端做"冒充"
ollama cp qwen3.5:9b gpt-3.5-turbo
```

**鉴权**：本地**完全没有**鉴权校验，`api_key` 随便填。**不要把 11434 端口暴露到公网**；必须对外时前面挂反向代理自己做 Bearer 校验，并用 `OLLAMA_HOST` 控制监听地址。

---

## 7. 环境变量

| 变量 | 默认值 | 说明 |
|---|---|---|
| `OLLAMA_HOST` | `127.0.0.1:11434` | 监听地址（改 `0.0.0.0:11434` 才能跨机访问） |
| `OLLAMA_MODELS` | `~/.ollama/models` | 模型存储目录 |
| `OLLAMA_CONTEXT_LENGTH` | **4096** | 默认上下文长度（模型自带默认可覆盖） |
| `OLLAMA_KEEP_ALIVE` | `5m` | 模型保活时长（请求级 `keep_alive` 优先级更高） |
| `OLLAMA_NUM_PARALLEL` | **1** | 单模型并行请求数。内存需求按 `NUM_PARALLEL × CONTEXT_LENGTH` 增长 |
| `OLLAMA_MAX_LOADED_MODELS` | `3 × GPU 数`（纯 CPU 为 3） | 同时驻留模型数上限 |
| `OLLAMA_MAX_QUEUE` | 512 | 忙时排队上限，超出返回 **503** |
| `OLLAMA_FLASH_ATTENTION` | 支持则自动开 | `=1` 强制开 / `=0` 关；省长上下文显存 |
| `OLLAMA_KV_CACHE_TYPE` | `f16` | KV 量化：`q8_0`（约省一半，几乎无损）/ `q4_0`（约省 3/4，有损） |
| `OLLAMA_ORIGINS` | 仅 `127.0.0.1`、`0.0.0.0` | 跨域白名单（浏览器扩展要显式加 `chrome-extension://*` 等） |
| `OLLAMA_NO_CLOUD` | 未禁用 | 纯本地模式（等价 `~/.ollama/server.json` 的 `"disable_ollama_cloud": true`） |
| `HTTPS_PROXY` | 无 | 拉模型走代理（**不建议设 `HTTP_PROXY`**，可能断开客户端连接） |

**macOS 怎么设**：

```bash
# ① GUI 应用：写入 launchd 环境后重启 Ollama 应用
launchctl setenv OLLAMA_HOST 0.0.0.0:11434

# ② 命令行/brew service：直接 export，或写进 brew services 的环境
export OLLAMA_KEEP_ALIVE=30m
```

**三个最值得调的**：

1. `OLLAMA_NUM_PARALLEL` 默认 1 → **多请求是排队的**，不是并行。要并发就调大，但要按公式加内存。
2. `OLLAMA_KV_CACHE_TYPE=q8_0` → 长上下文场景几乎免费的显存收益。
3. `OLLAMA_CONTEXT_LENGTH` + `ollama ps` 的 `CONTEXT` 列 → 上下文是**内存第一杀手**，别开着 256K 却只用 8K。

---

## 8. 本机实测记录

**环境**：macOS / Apple Silicon，Ollama **0.33.3**，模型 `qwen3.5:9b`（Q4_K_M，9.7B，磁盘 6.6 GB）。2026-09-11。

**耗时与吞吐**（`/api/chat` 非流式，`num_predict` 80~120）：

| 指标 | 数值 | 备注 |
|---|---|---|
| 冷加载 `load_duration` | **4.68 s** | 首次请求的 TTFT 大头 |
| Prefill 速度 | 53.6 tok/s | prompt 仅 16 token，样本太小仅供参考 |
| **Decode 速度** | **38.5 ~ 38.7 tok/s** | 三次测量高度一致；与 [环节11 §2.1](../../foundation/transformer/环节11-服务化与推理引擎详解.md)"8B Q4 基础款约 20~40 tok/s"吻合 |
| 驻留内存 `size_vram` | **14.2 GB** | ⚠️ 权重仅 6.6 GB → **KV Cache 占了约 7.6 GB** |
| 生效上下文 `CONTEXT` | **262144** | 模型包自带默认，远超实际需要 |

**思考型模型的实测坑**（重要）：`qwen3.5` 默认开启 thinking，且 thinking 与 `content` 是**两个字段**。

| 请求 | 结果 |
|---|---|
| 默认（think 开），`num_predict: 80` | `content` **为空字符串**，`thinking` 吃满 80 token，`done_reason: "length"` → 程序里表现为"模型没回答" |
| `think: false`，`num_predict: 120` | `content` 正常返回（45 token，`done_reason: "stop"`），速度 38.68 tok/s，响应**无 `thinking` 键** |
| `think: "low"`，问 `1+1=?`，`num_predict: 200` | `thinking` 写满 652 字符仍未产出 `content`，200 token 耗尽 → **即使 low 档也要给足预算** |

**结论**：接思考型模型时，`num_predict` 要按"thinking + 正式回答"两段总量给；或明确 `think: false` 用于低延迟/结构化场景。

---

## 9. 坑清单

| 症状 | 原因 / 解法 |
|---|---|
| 请求返回了，但 `content` 是空的 | **思考型模型 budget 被 thinking 吃光**。给足 `num_predict`，或 `think: false`（本机实测，见 §8） |
| 并发上不去，多请求排队 | `OLLAMA_NUM_PARALLEL` 默认 **1**；调大但要按 `NUM_PARALLEL × CONTEXT_LENGTH` 加内存 |
| 首 token 特别慢 | 冷启动 `load_duration`（实测 4.7 s）。预热：空 `messages` 发一次请求 |
| 内存占用远超模型体积 | KV Cache。查 `ollama ps` 的 `size_vram` 与 `CONTEXT`，压 `num_ctx` / 开 `KV_CACHE_TYPE=q8_0` |
| 速度慢但 `PROCESSOR` 显示有 CPU 份额 | 部分层没卸到 GPU。`ollama ps` 的 `PROCESSOR` 列直接看比例 |
| OpenAI SDK 报 404 | `base_url` 少写 `/v1` |
| 客户端设不了上下文长度 | OpenAI 口径无 `num_ctx`，必须 Modelfile + `ollama create`（§6） |
| 长文档被截断 | 上下文被默认值限制，先看 `ollama ps` 的 `CONTEXT` 实际值 |
| 服务忙时返回 503 | `OLLAMA_MAX_QUEUE` 排队溢出，该扩并行或加限流 |
| 浏览器/前端直连被 CORS 拒 | `OLLAMA_ORIGINS` 白名单 |
| 模型一直占着内存 | `keep_alive` 默认 5m；`ollama stop <model>` 立即卸载 |
| 暴露公网被白嫖 | **本地无鉴权**，必须反代 + 自己加鉴权 |

---

## 10. 工程建议

1. **本地开发统一走 OpenAI 兼容层**：代码里只配置 `base_url` 与模型名，就能在 Ollama / LM Studio / llama.cpp / 云端之间切换。
2. **上下文按需显式固化**：默认值不可信（官方文档自身就有 2048 / 4096 两个口径，模型包还可能自带 262144），**用 `ollama ps` 验证**，需要长上下文就 `Modelfile` 固化一个带 `num_ctx` 的派生模型。
3. **思考型模型分两个入口**：交互问答走 think 默认；结构化抽取 / 分类 / 路由走 `think: false` + `format` JSON Schema，又快又稳。
4. **别拿它做生产服务化**：并发弱、无鉴权，定位是"本地开发 + 个人/边缘"。生产回 vLLM / SGLang（见 [环节11](../../foundation/transformer/环节11-服务化与推理引擎详解.md)）。

---

## 11. 高频追问

1. **Ollama 和 llama.cpp 什么关系？** Ollama 底层就是 llama.cpp（GGUF + Metal/CPU）；它额外做了模型分发、Modelfile 抽象、守护进程与模型常驻管理。参数控制是子集。
2. **为什么并发差？** `OLLAMA_NUM_PARALLEL` 默认 1，且没有 PagedAttention / Continuous Batching 那一套生产级调度。
3. **`keep_alive` 有什么用？** 换模型频繁的 Mac 上，它决定模型在内存里活多久——决定了你是"秒回"还是每次都吃 4.7 s 加载。
4. **怎么给本地服务加鉴权？** Ollama 不提供，得自己反代（Nginx/Caddy/网关校验 Bearer）。
5. **KV Cache 到底多大？** 实测 9.7B Q4 在 256K 上下文下 KV 占约 7.6 GB，比权重（6.6 GB）还大。公式与 GQA/MLA 的影响见 [环节10](../../foundation/transformer/环节10-推理解码与KV缓存详解.md)。
6. **开放权重模型跑本地，能力够吗？** 分场景：分类 / 抽取 / 改写 / 代码补全够；复杂推理与长文档仍需云端。选型见 [模型评测与选型方法详解](../../foundation/transformer/模型评测与选型方法详解.md)。

---

## 12. 数据来源

- 官方文档站：https://docs.ollama.com（`/api`、`/modelfile`、`/faq`、`/api/openai-compatibility`），2026-09-11 抓取
- 仓库 API 文档：https://github.com/ollama/ollama/blob/main/docs/api.md（顶部已标注迁移）
- 版本发布：Ollama 0.34.0（2026-09-05 RC / 09-10 发布）——"Ollama models can now be used directly in ChatGPT Desktop"
- 本机实测：Ollama 0.33.3 / Apple Silicon / `qwen3.5:9b` Q4_K_M，2026-09-11

---

## 相关笔记

- 总览与选型：[本地推理运行时 · 操作手册](./README.md)
- 原理与选型对比：[环节11-服务化与推理引擎详解](../../foundation/transformer/环节11-服务化与推理引擎详解.md)（§2.1 Mac 选型、§2.2 GGUF）
- KV Cache 与上下文成本：[环节10-推理解码与KV缓存详解](../../foundation/transformer/环节10-推理解码与KV缓存详解.md)
- 姊妹篇（同模型横向对比）：[llama-cpp.md](./llama-cpp.md)
- 同系列待写（尚未创建，故不做链接）：`lm-studio.md` ｜ `mlx.md` ｜ `benchmark.md`
