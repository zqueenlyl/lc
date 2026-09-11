# DeepSeek API 接入与成本优化

> 调研时间：2026-09-11 ｜ 来源：DeepSeek 官方 API 文档（定价页 / Anthropic 兼容页 / Responses API 页 / 上下文缓存页），2026-09-11 检索快照
> 迭代极快，上线前请以 `GET /models` 与官方定价页校准。架构与演进逻辑见 [《DeepSeek 技术路线与架构演进》](./DeepSeek技术路线与架构演进.md)。

---

## 一、摘要（TL;DR）

DeepSeek 是目前**国内唯一同时提供三套协议入口**的平台（OpenAI Chat Completions / OpenAI Responses / Anthropic Messages），同一个模型既能被 OpenAI SDK 调、被 Claude Code 直接接管、也能走 Responses 式调用。

但它的"兼容"里藏了三个**静默行为**，是工程事故的高发区：

1. **模型名会被强制映射**——Anthropic 侧传入任何未识别的模型名都会**静默降级为 `deepseek-flash`**，日志里记的模型名不等于真实跑的模型
2. **不支持的参数被静默忽略**——不报错、不警告，配了以为生效
3. **最强档不看图**——`deepseek-v4-pro` 不支持图像理解，只有 `deepseek-flash` 支持

而成本侧的机会同样巨大：**缓存命中与未命中的单价差 30–50 倍**，这比换档位、比错峰的收益都大一个数量级。

---

## 二、模型规格速查

| 项 | `deepseek-flash` | `deepseek-v4-pro` |
|----|------------------|-------------------|
| 对应版本 | DeepSeek-V4.1-Flash | DeepSeek-V4-Pro-0813 |
| 上下文 | **1,048,576（1M）** | 1M |
| 最大输出 | **384K** | 384K |
| 并发上限 | **2500** | **500** |
| 默认模式 | 思考模式（可切非思考） | 思考模式（可切非思考） |
| **图像理解** | ✅ 支持 | ❌ **不支持** |
| JSON Output / Tool Calls | ✅ | ✅ |
| Responses API / Anthropic API | ✅ | ✅ |
| 对话前缀续写（Beta） | ✅ | ✅ |
| FIM 补全（Beta） | ✅ **仅非思考模式** | 同 |

**旧模型名现状**：`deepseek-v4-flash`、`deepseek-v4-flash-vision-exp` 仍可调用，但**对应模型已下线**，请求由 V4.1-Flash 承接并按 Flash 价计费。官方声明 **2026-09-14 之后继续提供 V4 Pro** 的 API 服务，计费不变。

> **选型陷阱**：直觉上"Pro 更强所以多模态也更强"——**恰好相反**。当前 Pro 档是纯文本/代码路线，看图必须走 `flash`。这是 DeepSeek 上最容易踩的选型误判。

---

## 三、三套协议入口

| 协议 | base_url | 端点 | 鉴权头 | SDK |
|------|----------|------|--------|-----|
| OpenAI Chat Completions | `https://api.deepseek.com` | `/chat/completions` | `Authorization: Bearer` | `openai` |
| **OpenAI Responses** | `https://api.deepseek.com` | `/responses` | `Authorization: Bearer` | `openai`（`client.responses.create`） |
| **Anthropic Messages** | `https://api.deepseek.com/anthropic` | `/messages` | **`x-api-key`** | `anthropic` |

三套协议对同一组模型提供不同"外壳"，选择依据：

| 场景 | 推荐协议 | 理由 |
|------|----------|------|
| 已有 OpenAI 生态代码 | Chat Completions | 零改动迁移 |
| 要用 Codex / 结构化 Agent 循环 | Responses | 官方针对性适配（`apply_patch` custom 工具） |
| 要用 Claude Code / Claude Desktop | Anthropic | 可直接改 `base_url` 接管 |

---

## 四、OpenAI Responses API：**完全无状态**

这是 DeepSeek Responses 实现最需要提前知道的一点：

| 参数 | 支持情况 |
|------|----------|
| `previous_response_id` | ❌ 不支持 |
| `conversation` | ❌ 不支持 |
| `store` | ❌ 不支持，响应中**恒为 `false`** |
| `prompt_cache_key` / `prompt_cache_retention` | ❌ 不支持；**缓存由系统自动管理** |
| `context_management` | ❌ 不支持 |
| `truncation` | ❌ 不支持——**输入超窗直接返回 400**，不会自动截断 |

**结论**：多轮对话必须**客户端自行回传完整上下文**（含 `function_call` / `function_call_output` / `reasoning` item）。这是与 OpenAI 官方 Responses API 最大的语义差异——**同名 API，不同状态模型**。

### 与 Chat Completions 的字段差异

| 维度 | Chat Completions | Responses |
|------|------------------|-----------|
| 输出上限 | `max_tokens` | **`max_output_tokens`** |
| 系统提示 | `messages[0].role=system` | **`instructions`**（`input` 与 `instructions` 至少传一个） |
| 文本格式 | `response_format` | **`text.format`** |
| 推理强度 | 顶层参数 | **`reasoning.effort`** |
| 流式结束 | `data: [DONE]` | **无语义 `[DONE]`**，以 `response.completed` / `.incomplete` / `.failed` 收尾，每个事件带**递增 `sequence_number`** |
| 角色 | system / user / assistant / tool | system / user / assistant / **developer**（视同 user） |

**支持的工具**：`function` 全支持；`custom` **仅**支持 `{"type": "custom", "name": "apply_patch"}`（供 Codex 兼容），**其他 custom 名称返回 400**；内置工具（`web_search` / `file_search` / `code_interpreter` / `computer_use` / `mcp`）**全部忽略**。

**静默忽略的顶层参数**：`parallel_tool_calls`（并行工具调用**始终开启**）、`max_tool_calls`、`background`、`metadata`、`include`、`prompt`、`service_tier`、`safety_identifier`、`stream_options` 等。

> 官方把"不支持的参数静默忽略"作为**兼容性设计**：现有 Responses 客户端无需修改即可接入。但工程上必须知道——**你不报错，不代表你生效**。

### 图片输入（Responses 侧）

- `input_image` 与 `image_url` / `file_id` **二选一**：都不传或都传均返回 **400**
- 图片**只允许**出现在 `user` / `developer` 消息与工具输出中；放 `system` / `assistant` 里返回 **400**
- 单请求最多 **600 张**；内联单张 ≤32 MiB，`file_id` 单张 ≤64 MiB
- `detail` 支持 `low` / `high` / `original` / `auto`

---

## 五、Anthropic 兼容：模型名映射是双刃剑

### 接入方式

```bash
export ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
export ANTHROPIC_API_KEY=${YOUR_API_KEY}
```

> 注意：官方页给出的是 **`ANTHROPIC_API_KEY`**。若你的客户端读的是 `ANTHROPIC_AUTH_TOKEN`，需要自行做变量映射。

### 模型名映射规则（官方明示）

| 你传入的模型名 | 实际提供服务的模型 | 计费口径 |
|----------------|-------------------|----------|
| `claude-opus*` | `deepseek-v4-pro` | 按 **V4 Pro** 价 |
| `claude-sonnet*` / `claude-haiku*` | `deepseek-flash` | 按 Flash 价 |
| **任何未识别的模型名** | **静默降级为 `deepseek-flash`** | 按 Flash 价 |

官方把这条当作**特性**：可以借此在 Claude Desktop 的 developer 模式下"绕过模型名限制"，只改 `base_url` + `api_key` 即接入。但反过来看——**你的日志里写的模型名，不一定是实际跑的模型**。做成本归因或效果归因时必须意识到这一点。

### 字段支持情况

**完全支持**：`max_tokens`、`stop_sequences`、`stream`、`system`、`temperature`（范围放宽至 `[0.0, 2.0]`）、`x-api-key`、`tools` 的 `name` / `description` / `input_schema`。

**部分生效（有条件）**：

| 字段 | 行为 |
|------|------|
| `thinking` | 支持，但 **`budget_tokens` 被忽略** |
| `output_config` | **仅 `effort` 生效** |
| `top_p` | **仅思考模式生效**，下限 **0.95**；非思考模式恒为 `1.0` |
| `image.source.type="file"` | 必须携带请求头 `anthropic-beta: files-api-2025-04-14` |
| `metadata` | 仅支持 `user_id` |

**被直接忽略**：`anthropic-version`、`anthropic-beta`（在 `/messages` 上）、`container`、`mcp_servers`、`service_tier`、`top_k`、**`cache_control`**（工具/内容块上的均是）、`citations`、`is_error`、`tool_choice.disable_parallel_tool_use`。

**完全不支持的内容块**：`document`、`search_result`、`redacted_thinking`、`code_execution_tool_result`、`mcp_tool_use`、`mcp_tool_result`、`container_upload`。

> **关键推论**：Anthropic 侧的 `cache_control` 断点**被忽略**——你无法通过显式标记来控制缓存。DeepSeek 的缓存是**前缀自动匹配**机制（见 §七），想让它生效，只能靠"把稳定内容放在 prompt 最前面"这种结构性手段。

---

## 六、思考模式

两个模型**默认开启思考模式**，可切换。开启写法（官方快速开始示例）：

```json
"thinking": {"type": "enabled"},
"reasoning_effort": "high"
```

| 项 | 说明 |
|----|------|
| 档位 | **low / high / max**（三档，2026-08-13 随 V4-Pro 一起引入） |
| Python SDK 传法 | `thinking` 需经 `extra_body=` 传入；`reasoning_effort` 作为普通关键字参数 |
| `temperature` | **思考模式下不生效** |
| `top_p` | 思考模式下生效且**下限 0.95**；非思考模式下恒为 1.0 |
| `reasoning_tokens` | 计入 `usage` 的**输出侧**（Responses 侧为 `output_tokens_details.reasoning_tokens`），**按输出价计费** |

> **账单预期管理**：默认开思考 + 思维链按输出价计费，意味着"以为只问了一句话"的调用也可能产生可观的输出 token。对延迟敏感或成本敏感的批量任务，**显式切非思考模式**是最直接的降本手段。
>
> 另：**FIM 补全（Beta）仅非思考模式支持**——代码补全场景要记得关思考。

---

## 七、上下文硬盘缓存

### 机制

| 项 | 说明 |
|----|------|
| 开关 | **默认对所有用户开启**，无需改代码 |
| 匹配单位 | **缓存前缀单元**——每条前缀是一个**独立的完整单元**，后续请求必须**完整匹配**该单元才能命中（不支持任意片段的部分命中） |
| 落盘时机 | ① 每次请求的**用户输入结束位置**与**模型输出结束位置**各产生一个单元；② 系统检测到多次请求的**公共前缀**时落盘；③ 长输入/输出中按**固定 token 间隔**截取落盘 |
| 构建耗时 | 秒级 |
| 有效期 | **非固定 TTL**：不再使用后自动清空，一般为**几小时到几天** |
| 命中保证 | **不保证 100% 命中**（尽力而为） |

受注意力机制影响（V3.2 起的滑窗 / 稀疏注意力），前缀的存取与判别方式与纯全注意力模型不同。

### 观测字段

```json
"usage": {
  "prompt_cache_hit_tokens": 20000,
  "prompt_cache_miss_tokens": 1000
}
```

Responses 侧对应 `input_tokens_details.cached_tokens`。

### 工程含义

缓存的命中判据是"**前缀逐 token 完全一致**"。因此：

| 做法 | 后果 |
|------|------|
| 把系统提示 / 工具定义 / 固定文档放最前面 | ✅ 稳定命中 |
| 前缀里塞**时间戳、随机 ID、用户昵称** | ❌ **整条前缀作废**，命中率归零 |
| 多轮对话中每轮在前面插入新内容 | ❌ 破坏前缀连续性 |
| 首轮不命中就放弃 | ⚠️ 公共前缀会在第 2 次请求时落盘，**第 3 次**才可能命中，需要容忍冷启动 |

---

## 八、定价与成本优化

### 价格表（元 / 百万 token）

| 计费项 | flash 空闲 | flash 高峰 | v4-pro 空闲 | v4-pro 高峰 |
|--------|-----------|-----------|------------|------------|
| 输入·缓存**命中** | 0.02 | 0.04 | 0.15 | 0.30 |
| 输入·缓存**未命中** | 1 | 2 | 4.5 | 9.0 |
| 输出 | 4 | 8 | 13.5 | 27.0 |

- **高峰时段**：北京时间 **周一至周五 09:00–12:00、14:00–18:00**；其余（夜间、周末、午休 12:00–14:00）均为**空闲**，价格为高峰的 **5 折**
- **缓存倍差**：flash 命中 vs 未命中 ≈ **1 : 50**；v4-pro ≈ **1 : 30**
- 扣费顺序：**赠送余额优先**于充值余额

### 降本优先级（按收益排序）

| 优先级 | 手段 | 量级 | 说明 |
|--------|------|------|------|
| **1** | **提高缓存命中率** | **30–50×** | 把稳定前缀（系统提示 / 工具定义 / 长文档）结构化前置；剔除前缀中的动态字段 |
| 2 | 错峰调度 | **2×** | 批处理 / 离线任务排到夜间或周末 |
| 3 | 档位选择 | **3.4–4.5×** | pro/flash 输入差 4.5×、输出差 3.375×；能不用 pro 就不用 |
| 4 | 关思考模式 | 视输出占比 | 思维链按输出价计费 |
| 5 | 压缩上下文与输出 | 线性 | 常规手段 |

### 成本算例

**场景**：固定前缀 20K tokens（系统提示 + 工具定义），每轮变化内容 1K，输出 500 tokens，每天 10,000 次调用，使用 `deepseek-flash`，空闲时段。

| 方案 | 输入命中 | 输入未命中 | 输出 | 日成本 |
|------|---------|-----------|------|--------|
| 无缓存 | 0 | 210M × 1 元 = 210 元 | 5M × 4 元 = 20 元 | **230 元** |
| **缓存全命中** | 200M × 0.02 元 = **4 元** | 10M × 1 元 = 10 元 | 20 元 | **34 元** |

**降幅约 85%**。若同时把任务从高峰改到空闲，再降 50% → **17 元**（相对原始 230 元，累计降 92.6%）。

> 这组数字说明了为什么"缓存优先"是 DeepSeek 上第一优先级：**它的效果远超选档位和错峰之和**。

---

## 九、工程坑清单

| # | 坑 | 后果 | 规避 |
|---|----|------|------|
| 1 | Anthropic 侧未识别模型名**静默降级**为 flash | 日志模型名 ≠ 真实模型，效果/成本归因错误 | 显式传 `claude-opus*`（要 Pro 时）或直接传 DeepSeek 模型名并记录实际档位 |
| 2 | `deepseek-v4-pro` **不支持图像理解** | 传图后行为异常或能力缺失 | 多模态一律走 `deepseek-flash` |
| 3 | **默认开思考模式** | 延迟与输出 token 账单高于预期 | 对延迟/成本敏感的批量任务显式关闭 |
| 4 | 思考模式下 `temperature` 不生效、`top_p` 下限 0.95 | 采样参数调不动 | 非思考模式下调参，或接受官方推荐值 |
| 5 | Responses API **无状态**，`previous_response_id` 无效 | 以为服务端存了会话，实际上下文丢失 | 客户端自持全量上下文回传 |
| 6 | Responses **不支持 `truncation`** | 超窗直接 **400** | 客户端自己截断 |
| 7 | Responses **静默忽略**不支持参数 | 配了不生效，无任何提示 | 对照官方支持清单逐项核对 |
| 8 | Responses 的 `custom` 工具**非 `apply_patch` 名称返回 400** | 自定义工具名直接报错 | 自定义工具用 `function` 类型 |
| 9 | Anthropic 侧 **`cache_control` 被忽略** | 以为能显式控制缓存断点 | 靠结构性前置前缀，别用 cache_control |
| 10 | 前缀含时间戳 / 随机 ID | 缓存命中率归零 | 动态内容一律后置 |
| 11 | FIM 补全在思考模式下不可用 | 代码补全报错或退化 | FIM 场景关思考 |
| 12 | 图片放 `system` / `assistant` 消息 | Responses 侧返回 **400** | 只放 `user` / `developer` / 工具输出 |
| 13 | 依赖标称 1M 上下文做容量规划 | 256K 后检索质量明显下滑 | 有效区间按 **128K–256K** 规划（见架构篇 §六） |

---

## 十、面试高频追问

1. **为什么模型的"兼容 API"往往不是真兼容？**
   兼容层通常只实现**请求/响应结构的子集**，并对不支持项做"静默忽略"而非报错（为了降低迁移摩擦）。因此字段级行为、状态语义（DeepSeek Responses 完全无状态）、参数生效条件（思考模式下的 temperature）都可能与原生实现不同。**判断兼容性要看字段级映射表，而不是看端点路径。**

2. **上下文缓存为什么能便宜 50 倍，代价是什么？**
   复用已计算的 KV，省掉 prefill 的算力与显存。代价是：① 匹配必须**完整命中前缀单元**，任何前缀扰动都会击穿；② 缓存是**尽力而为**，不保证命中；③ 有效期不固定（几小时到几天），跨天场景不可依赖。工程上要把它当作"**概率性的折扣**"而非"确定性的优化"。

3. **错峰定价的设计意图是什么？**
   把可延迟的批处理负载引导到低谷时段，提高集群利用率。对工程侧意味着**任务可调度性直接换算成成本**——把离线 eval、文档批处理、数据标注跑在夜间，成本立减一半。

4. **"最强档不看图"这种反直觉设计说明了什么？**
   档位命名对标的是**综合能力**，而非全能力维度覆盖。多模态与文本/代码路线往往是不同的训练配方（V4-Pro 走纯文本 Agent 路线，视觉能力由 V4.1-Flash 承接），**不能按"高配=全能力超集"来假设**。选型必须按能力矩阵逐项核对。

---

## 十一、数据来源

**官方（DeepSeek API Docs，2026-09-11 检索）**

- [模型 & 价格](https://api-docs.deepseek.com/zh-cn/quick_start/pricing)
- [更新日志](https://api-docs.deepseek.com/zh-cn/updates)
- [使用 Anthropic API](https://api-docs.deepseek.com/zh-cn/guides/anthropic_api)
- [使用 Responses API](https://api-docs.deepseek.com/zh-cn/guides/responses_api)
- [上下文硬盘缓存](https://api-docs.deepseek.com/zh-cn/guides/kv_cache)

---

## 十二、相关笔记

- [《DeepSeek 技术路线与架构演进》](./DeepSeek技术路线与架构演进.md) —— 谱系时间线、MLA/DSA/CSA+HCA 三代架构、训练与推理基础设施
- [`providers/各大厂商代表模型总览.md`](../providers/各大厂商代表模型总览.md) —— §3.5 模型规格速查
- [`providers/模型服务API协议对比.md`](../providers/模型服务API协议对比.md) —— 三代协议演进、十类字段差异、"假兼容"陷阱
