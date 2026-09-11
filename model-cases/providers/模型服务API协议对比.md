# 模型服务 API 协议对比

> 检索时点：**2026-09-11** ｜ 范围：主流模型服务的**协议层**（端点 / 鉴权 / 请求结构 / 流式 / 工具 / 错误）
> **口径约定**：`官方`=厂商官方文档；`社区`=第三方资料；`推断`=本文基于协议结构的分析。
> ⚠️ 协议字段随版本演进（尤其 Responses 族仍在快速迭代），**本文是结构地图而非字段字典**，落地时以官方 API Reference 为准。

---

## 一、三代协议：从"补全"到"有状态响应"

| 代际 | 代表 | 心智模型 | 多轮状态 | 典型端点 |
|------|------|----------|----------|----------|
| **第 1 代** Completions | `/v1/completions` | 文本续写 | 无 | prompt in → text out |
| **第 2 代** Chat Completions | OpenAI `/v1/chat/completions` | **无状态消息数组** | **客户端维护** | messages in → message out |
| **第 3 代** Responses / Interactions | OpenAI `/v1/responses`、Gemini Interactions、xAI `/v1/responses` | **有状态会话** | **服务端维护**（`previous_response_id`） | input in → 步骤序列 out |

### 为什么会有第 3 代（不是为了改而改）

| 第 2 代的痛点 | 第 3 代的解法 |
|---------------|----------------|
| 每轮重传全量历史 → 无法命中服务端缓存，token 与延迟双高 | 服务端持有历史 → **隐式缓存命中率提升**（Google 官方明确把"更高缓存命中率、更低费用"列为优势） |
| 工具调用要客户端手工拼 `tool_calls` → `role=tool` 回填 | 工具调用与结果变成**响应里的执行步骤**，可观测 |
| 推理模型的思维链无处安放 | 独立的 reasoning 输出项（含加密回传） |
| 多模态/文件/代码解释器各走各的接口 | 统一成一个"响应"里的 item 序列 |

### 现状对照（2026-09）

| 厂商 | 推荐协议 | 旧协议状态 |
|------|----------|------------|
| OpenAI | **Responses** | Chat Completions 为兼容路径（官方 Agents SDK 默认走 Responses，且**默认模型即 `gpt-5.6-luna`**） |
| xAI | **Responses** | Chat Completions 已标 **Legacy** |
| Google | **Interactions**（2026-06 GA，"建议所有新项目使用"） | `generateContent` 转 **legacy（仍完全支持）** |
| Anthropic | **Messages**（本就是"有状态风格"，但状态仍需客户端传历史） | — |
| 字节火山方舟 | **Responses**（官方提供迁移教程）+ Bot/Context API | `api/v3` OpenAI 形态继续可用 |
| **DeepSeek** | **Responses 与 Chat Completions 双线并行**（官方两条都支持，未把 Chat 标 Legacy） | 另有 **Anthropic `/anthropic`** 兼容入口 |
| 国内其余 | Chat Completions（OpenAI 兼容为主） | — |

> **结论**：协议层已经分成两个阵营——**Responses 阵营**（OpenAI / xAI / Google / 火山方舟）与 **Chat Completions 阵营**（Anthropic Messages 风格 + 国内大多数）。跨阵营迁移的成本远高于"换个 base_url"。
> **唯一的跨阵营特例是 DeepSeek**：同一家同时开通了 Responses、Chat Completions、Anthropic 三套入口（见 §3 补充）。

---

## 二、两种范式对比（决定架构）

| 维度 | 无状态（Chat Completions） | 有状态（Responses / Interactions） |
|------|----------------------------|-------------------------------------|
| 历史管理 | 客户端拼 `messages` 数组 | 服务端保存，传 `previous_response_id` / `previous_interaction_id` |
| 上下文裁剪 | 客户端自行截断/摘要 | 服务端 `context_management` + 压缩端点（如 `/responses/compact`、`compact_threshold`） |
| 缓存 | 只能靠显式缓存（cache key） | 隐式缓存命中率天然更高 |
| 数据留存 | 不落库（默认） | **默认落库**：Azure 侧保留 30 天；Gemini 付费 55 天 / 免费 1 天 |
| 合规开关 | — | `store=false`（注意：Google 侧 `store=false` **与后台执行不兼容且无法续接会话**） |
| 工具回传 | 手工拼 `role=tool` | 结构化「执行步骤」 |
| 迁移方向 | 适合对接只支持 Chat 的第三方 | 新项目默认 |

**选型建议（本文推断）**：新项目若只用一家头部厂商，直接上有状态协议；若必须多厂商冗余，**协议抽象层要按"最小公共子集"设计**，并把有状态能力当作可选增强（见 §6）。

---

## 三、逐家协议速查

| 厂商 | 端点 | 鉴权 | 系统提示位置 | 输出长度字段 | 结构化输出 | 流式 |
|------|------|------|--------------|--------------|------------|------|
| **OpenAI Responses** | `POST /v1/responses` | `Authorization: Bearer sk-...` | **`instructions`（顶层）** | **`max_output_tokens`** | **`text.format`** | SSE，事件 `response.output_text.delta` |
| **OpenAI Chat** | `POST /v1/chat/completions` | Bearer | `messages[0].role="system"` | `max_tokens` / `max_completion_tokens` | `response_format` | SSE `data: [DONE]` |
| **Azure OpenAI** | `/openai/v1/responses`（**v1 API 必需**） | **`api-key` 头** 或 Entra ID `Bearer`（scope `https://ai.azure.com/.default`） | `instructions` | `max_output_tokens` | `text.format` | SSE |
| **Anthropic Messages** | `POST /v1/messages` | `x-api-key` + `anthropic-version` | **顶层 `system`** | **`max_tokens`（必填）** | 无原生 schema 模式（靠 tool 或提示） | SSE（`message_start` / `content_block_delta` / `message_delta`） |
| **Anthropic on Bedrock** | `InvokeModel` / `InvokeModelWithResponseStream` | SigV4 | 顶层 `system` | `max_tokens` 必填 | — | 流式操作 |
| **Gemini generateContent** | `POST /v1beta/models/{model}:generateContent` \| `:streamGenerateContent` | API Key（query 或 header） | `systemInstruction` | `generationConfig.maxOutputTokens` | `responseSchema` / `responseMimeType` | `streamGenerateContent` |
| **Gemini Interactions** | `interactions.create` / `get` / `delete` | API Key | **`system_instruction`（互动级，每轮重传）** | `generation_config` | 同左 | SDK 流式 |
| **xAI** | `POST /v1/responses`（`https://api.x.ai/v1`） | Bearer；另支持 **mTLS** | 同 Responses 家族 | `max_output_tokens` | 同 Responses | SSE |
| **Bedrock Converse** | `Converse` / `ConverseStream` | SigV4 | `system` 数组 | `inferenceConfig.maxTokens` | `outputConfig` | `ConverseStream` |
| **智谱 BigModel** | `POST /api/paas/v4/chat/completions` | Bearer | `messages` | `max_tokens` | `response_format` | SSE |
| **Kimi Moonshot** | `POST /v1/chat/completions` | Bearer（可加 `X-Msh-Request-Nonce`） | `messages` | **`max_completion_tokens`（`max_tokens` 已弃用）** | `response_format` | SSE |
| **火山方舟 Ark** | `POST /api/v3/chat/completions`（另有 Responses 路由） | Bearer `ARK_API_KEY` | 依协议族 | 依协议族 | 支持（**推荐 `json_schema` 模式**） | SSE |
| **腾讯混元** | `POST /v1/chat/completions` | Bearer | `messages` | `max_tokens`（默认 4096） | — | SSE（`stream_options.include_usage`） |
| **百度千帆** | `POST /v2/chat/completions` | Bearer `bce-v3/ALTAK-...` | `messages` | `max_tokens` | — | SSE |
| **讯飞星火** | `POST /v1/chat/completions` | Bearer（**APIPassword**，各版本不同） | `messages` | `max_tokens`（按档位上限不同） | `response_format: {type: json_object}` | SSE |
| **DeepSeek** | `/chat/completions`、**`/responses`**、**`/anthropic`**（**三套**） | OpenAI 侧 `Authorization: Bearer`；Anthropic 侧 **`x-api-key`** | `messages`（Chat）／`instructions`（Responses）／顶层 `system`（Anthropic） | `max_tokens`（Anthropic 侧**必填**）／`max_output_tokens`（Responses） | `response_format` 或 `text.format` | SSE |
| **Mistral** | `POST /v1/chat/completions` | Bearer | `messages` | `max_tokens` | `response_format`（含 `json_schema`） | SSE |

### 补充：DeepSeek 的三套协议入口（唯一的三协议厂商）

| 入口 | 路径 | 鉴权 | 关键差异 |
|------|------|------|----------|
| OpenAI Chat | `/chat/completions` | `Authorization: Bearer` | 标准 Chat Completions 形态 |
| **OpenAI Responses** | `/responses` | `Authorization: Bearer` | 有状态（`previous_response_id`）、`instructions`、`text.format` |
| **Anthropic** | `/anthropic` + `/messages` | **`x-api-key`** | 顶层 `system`、`max_tokens` 必填、工具用 `input_schema` |

**Anthropic 兼容侧的字段行为**（官方逐条列出，是"静默忽略"的重灾区）：

| 字段 | 行为 |
|------|------|
| `anthropic-version` | **忽略**（不校验、不报错） |
| `anthropic-beta` | `/messages` **忽略**；**Files API 端点必须携带** `files-api-2025-04-14` |
| `top_k` | 忽略 |
| `temperature` | 支持，范围 **[0.0 ~ 2.0]**（比 Anthropic 官方 0~1 更宽） |
| `top_p` | ⚠️ **仅思考模式生效（下限 0.95）；非思考模式恒为 1.0** |
| `thinking` | 支持，但 **`budget_tokens` 被忽略** —— 只能开关，不能控预算 |
| `output_config` | **仅支持 `effort`** |
| `metadata` | **仅 `user_id`**，其余忽略 |
| `cache_control` / `citations` | **忽略** → 意味着 **prompt caching 实际不生效**、引用不返回 |
| `container` / `mcp_servers` / `service_tier` | 忽略 |
| `tools[].input_schema` | 支持；`disable_parallel_tool_use` **忽略** |
| content 类型 | ✅ `text`、`image`（base64 / url / file）、`thinking`、`tool_use`、`tool_result`、`server_tool_use`、`web_search_tool_result`；❌ `document`、`search_result`、`redacted_thinking`、`code_execution_tool_result`、`mcp_tool_use`、`container_upload` |
| **模型名** | **被强制重映射**：`claude-opus*`→`deepseek-v4-pro`，`claude-sonnet*`/`claude-haiku*`→`deepseek-flash`，**未识别名称一律静默降级为 `deepseek-flash`**（详见 [模型总览 §3.5](./各大厂商代表模型总览.md#35-deepseek)） |

**工程含义（本文推断）**：
- `cache_control` 被忽略 → **"Anthropic 客户端的 prompt caching 在这里是空转"**，成本模型要重算。
- `top_p` 在非思考模式下**传什么都没用**（恒 1.0），调参调不动不是你的 bug。
- 模型名映射意味着**你写的 `claude-sonnet-4-6` 实际跑的是 `deepseek-flash`** —— 日志里的模型名与真实模型不一致，出现"计费对不上 / 效果对不上"时要先想到这一层。

---

## 四、十个最容易踩的协议差异

### 4.1 系统提示的位置（迁移第一坑）

同一个"你是客服助手"，在四家要写在四个地方：

```
OpenAI Responses  → { "instructions": "..." }
OpenAI Chat       → { "messages": [{"role":"system", ...}] }
Anthropic         → { "system": "...", "messages": [...] }        // 顶层独立字段
Gemini Interactions → { "system_instruction": "..." }               // 且是"互动级"，每轮都要重传
Bedrock Converse  → { "system": [{"text": "..."}] }                 // 数组形式
```

**后果**：迁移时若不改，系统提示会被当成用户消息塞进对话——不报错，但**指令优先级与角色定位全变**，表现为"模型不听话"。

### 4.2 输出长度参数的名字（四套命名）

| 参数名 | 使用者 |
|--------|--------|
| `max_tokens` | Anthropic（**必填**）、Bedrock Converse 的 `inferenceConfig`、智谱、混元、千帆、星火、Mistral |
| `max_completion_tokens` | OpenAI Chat（新写法）、**Kimi** |
| `max_output_tokens` | OpenAI Responses、Azure Responses、xAI |
| `generationConfig.maxOutputTokens` | Gemini generateContent |

**坑**：Kimi 已用 `max_completion_tokens` 替代 `max_tokens`，**旧字段被静默忽略**——沿用老代码不会报错，只会按默认上限生成（K3 默认 131072），成本与延迟直接失控。

### 4.3 工具调用的三层差异

| 层 | 差异点 |
|----|--------|
| **定义** | OpenAI：`{type:"function", name, description, parameters}`（注意 **Responses 里 function 定义是"扁平的"**，不再套 `function` 对象）；Anthropic：`{name, description, input_schema}`（**叫 `input_schema` 不叫 `parameters`**）；Gemini：`functionDeclarations` |
| **选择策略** | OpenAI `tool_choice`: `none`/`auto`/`required`/指定函数；Anthropic `tool_choice.type`: `auto`/`any`/`tool`（**`any` 而非 `required`**） |
| **结果回传** | OpenAI Responses：`{type:"function_call_output", call_id, output}`；OpenAI Chat：`{role:"tool", tool_call_id, content}`；Anthropic：`{role:"user", content:[{type:"tool_result", tool_use_id, content}]}` |

**Anthropic 特别注意**：`tool_result` 是包在 **user 消息**里的内容块，不是独立 role。

### 4.4 结构化输出

| 形态 | 支持情况 |
|------|----------|
| `response_format: {type:"json_object"}` | Chat Completions 家族普遍支持（但需在提示里也说明要输出 JSON） |
| `response_format: {type:"json_schema", json_schema:{name, strict, schema}}` | 部分厂商支持；**OpenRouter 归一化后也暴露此形态** |
| Responses 的 `text.format` | Responses 家族（OpenAI / Azure / xAI） |
| 火山方舟 | 支持结构化输出（beta），官方**推荐 `json_schema` 模式** |
| **不支持时的行为** | 有的报 400（部分提供方接受 JSON 但不接受 `json_schema`），有的静默降级 —— **必须显式探测** |

详见 [structured-output 专题](../../ai/structured-output/README.md)。

### 4.5 流式：SSE 的三处不一致

| 差异点 | 说明 |
|--------|------|
| 结束标记 | OpenAI 家族以 `data: [DONE]` 结束；Anthropic 无 `[DONE]`，靠 `message_stop` 事件 |
| usage 位置 | OpenAI 需开 `stream_options.include_usage`；**OpenRouter 在 `[DONE]` 前最后一个 chunk 返回 usage 且该 chunk 的 `choices` 非空**（delta 无内容，仅重复 `finish_reason`） |
| 注释载荷 | **OpenRouter 明确要求忽略 SSE 流里的 "comment" 载荷**——naive 解析器会崩 |

### 4.6 流式中的错误：HTTP 200 也可能失败

- **Azure OpenAI 官方口径**：流式过程中出错时，HTTP 状态码**仍是 200**，错误通过流内的 `error` 事件传递；映射关系为 `server_error→500`、`too_many_requests→429`、`forbidden→403`、`user_error→400`。
- **官方还明确**：**失败的流式响应不收取 token 费用**，但应用必须自己检测流内 error 并优雅重启。
- **实践含义**：所有流式客户端都必须实现"流内错误检测"，仅判断 HTTP 状态码是不够的。

### 4.7 思维链（reasoning）的回传

| 形态 | 厂商 |
|------|------|
| `reasoning_content` 独立字段 | 智谱（官方扩展字段） |
| `reasoning` / `text.format` 中的 reasoning item | OpenAI Responses |
| `thinking` 内容块 | Anthropic（另有 beta：interleaved thinking、thinking 加密、`dev-full-thinking`） |
| `reasoning.encrypted_content` | OpenAI（**无状态 `store=false` 时必须请求该字段并在下一轮回传推理项**，否则推理连续性丢失） |
| `reasoning.effort` 分级 | OpenAI（含 `minimal`/`max`）、Mistral（`none`~`xhigh`）、xAI（可配）、Anthropic 用 `effort` 替代 thinking 预算 |

**关键**：Responses 家族里 `reasoning.mode` / `reasoning.context` **是 Responses 专属**，走 Chat Completions 会被忽略（官方 SDK 会警告，开启严格校验则报错）。

### 4.8 缓存：显式 vs 隐式

| 类型 | 机制 | 代表 |
|------|------|------|
| **隐式缓存** | 服务端自动识别前缀，命中即打折 | Responses/Interactions 的有状态模式天然受益（Google 官方列为优势） |
| **显式/可指定缓存** | 传 cache key 控制缓存边界 | Mistral `prompt_cache_key`（**缓存 token 按输入价 10% 计费**）；OpenAI `prompt_cache_retention` / `prompt_cache_options` |
| **平台侧前缀缓存** | 平台提供的前缀/会话缓存 | 火山方舟「前缀缓存」「Session 缓存」 |
| **自动前缀缓存（命中/未命中两套价）** | 服务端自动匹配前缀，**命中价远低于未命中价** | **DeepSeek**：flash 命中 0.02 vs 未命中 1 元（≈ **1/50**）、v4-pro 0.15 vs 4.5 元（≈ **1/30**）；另有**空闲/高峰双价**（空闲 5 折） |

**工程含义**：把**稳定内容放前、易变内容放后**（系统提示 → 工具定义 → 少变上下文 → 用户输入），是跨厂商通用的省钱手段，与是否用有状态协议无关。

### 4.9 错误与限流：两套世界观

| 世界观 | 特征 | 代表 |
|--------|------|------|
| **HTTP 语义派** | 4xx/5xx + `error` 对象；429 触发退避 | OpenAI / Anthropic / Gemini / Mistral / 千帆 |
| **200 + 业务码派** | HTTP 常为 200，错误藏在响应体 | **MiniMax**（`base_resp.status_code`）、**讯飞星火**（`code` 字段） |

**星火的错误码是国内最可编程的一套**（官方）：`10007` 流量受限、`10013` 输入审核不通过、`10014` 输出敏感、`10907` token 超限、`11201` 日流控、`11202` 秒级流控、`11203` 并发流控 —— 三类限流分开，可做差异化退避策略。

**限流可观测性**：千帆提供 `X-Ratelimit-Limit/Remaining-Requests`、`...-Input-Tokens`、`...-Output-Tokens`（配额 0~60s 刷新）；OpenRouter 提供 `rate_limits.updated` 事件；智谱 GLM-Realtime 的 `usage` **暂时返回 0**（无法自核计费）。

### 4.10 批处理与异步

| 能力 | 说明 |
|------|------|
| Batch API | OpenAI / Anthropic / Mistral / xAI / 火山方舟均有；**Gemini 的 Interactions API 尚不支持 Batch**（generateContent 支持） |
| 后台执行 | Gemini `background=true`（与 `store=false` **不兼容**）；OpenAI 有 background mode（官方称与流式组合仍有性能问题） |
| 长任务超时 | **Bedrock 对 Claude 3.7/4 系列推理超时为 60 分钟**，而 AWS SDK 默认 read timeout 仅 1 分钟 —— 官方要求至少调到 3600 秒 |

---

## 五、"假兼容"陷阱清单（OpenAI 兼容 ≠ 行为一致）

这是本文最想强调的一节：**OpenAI 兼容是"字段名兼容"，不是"语义兼容"**。

| 陷阱 | 具体表现 | 案例 |
|------|----------|------|
| **同名不同义** | `stop` 的停止位置相反 | **腾讯混元**：OpenAI 停在匹配内容**之前**，混元停在**之后**（官方明示）；官方称未来可能改为对齐 |
| **不支持则静默忽略** | 传了不生效也不报错 | **OpenRouter** 官方：模型不支持的参数（如非 OpenAI 模型的 `logit_bias`）**被忽略**，其余转发 |
| **失败则静默丢弃** | SDK 层面丢字段 | **OpenAI Agents SDK**：走 Chat Completions 时会**静默丢弃** Responses 专属字段 |
| **字段被弃用但保留** | 老写法不报错、按默认值走 | **Kimi** `max_tokens` 弃用 → `max_completion_tokens` |
| **取值域更窄** | 合法取值被判非法 | **智谱** `temperature` ∈ (0,1)，**不支持 0**；**Anthropic** 4.5+ `temperature` 与 `top_p` **不可同时指定** |
| **响应结构不同** | 解析路径不一样 | **MiniMax** 原生回复在 `choices[0].messages[]`（数组）而非 `message`；**Anthropic** 的 tool 结果包在 user 消息里 |
| **错误封装不同** | 200 里藏错误 | **MiniMax / 星火** |
| **finish_reason 归一化** | 原始值与归一值并存 | **OpenRouter** 归一为 `tool_calls`/`stop`/`length`/`content_filter`/`error`，原始值保留在 `native_finish_reason` |
| **消息 `name` 字段被拼接** | 语义被改写 | **OpenRouter**：对非 OpenAI 模型把 name 以 `{name}: {content}` 前置拼接 |
| **模型名被强制重映射** | 请求的模型 ≠ 真实跑的模型，日志与计费对不上 | **DeepSeek 的 Anthropic 兼容侧**：`claude-opus*`→`deepseek-v4-pro`，**未识别模型名静默降级为 `deepseek-flash`**（官方明示） |
| **参数"看起来支持"但空转** | 接受字段却不生效 | **DeepSeek Anthropic 侧**：`cache_control` 被忽略（**prompt caching 不生效**）、`thinking.budget_tokens` 被忽略、`top_p` 非思考模式恒为 1.0 |

**防御性做法（本文建议）**：
1. 接入新厂商时，**先跑一组"协议一致性探针"**：系统提示位置、`stop` 语义、`max_tokens` 是否生效、`temperature=0` 是否合法、工具调用 round-trip、结构化输出是否被接受、错误码形态。
2. 网关层开启**严格校验**（如 OpenAI Agents SDK 的 `strict_feature_validation=True`），把"静默丢字段"变成**开发期报错**。
3. 用量核对自己埋点，不依赖平台 `usage`。

---

## 六、多厂商接入架构：三种方案

| 方案 | 做法 | 优点 | 代价 | 适合 |
|------|------|------|------|------|
| **A. 直连 + 自建适配层** | 每厂商一个 adapter，统一到内部 IR | 完全可控、可按需用厂商独有能力 | 维护成本随厂商数线性增长 | 厂商数少（≤3）、需要独有能力的核心链路 |
| **B. 自建网关（LiteLLM 等）** | 对外 OpenAI 格式，网关做协议转换 | 统一鉴权/计费/限流/负载均衡；LiteLLM 支持 **100+ 提供方**、虚拟密钥、多部署负载均衡 | 受网关能力边界限制；Responses 专属能力可能失落 | 厂商数多、以 Chat Completions 为主的业务 |
| **C. 聚合服务（OpenRouter 等）** | 直接用第三方聚合端点 | 免运维、自动故障回退、一个 key 打通 | 加一层延迟与成本；厂商独有参数被忽略；数据经第三方 | 早期验证、长尾模型兜底 |

**共性原则**：
- 对外暴露的**内部契约**应取"最小公共子集"（messages + tools + stream），厂商独有能力通过 `extra_body` 透传。
- **协议归属要显式建模**：把"是否支持有状态续接"作为能力位，而不是假设所有厂商都能 `previous_response_id`。
- **降级链**要按能力声明，而不是按厂商名硬编码。
- **路由策略与协议转换是两层**：选哪个模型 / 哪个档位 / 失败切谁属于 [model-routing](../../ai/model-routing/README.md)（含 fallback 防重试风暴）；本文只负责"跨厂商字段怎么翻译"。

---

## 七、迁移清单：Chat Completions → Responses

| # | 改动点 | 从 → 到 |
|---|--------|---------|
| 1 | 路径 | `/v1/chat/completions` → **`/v1/responses`**（Azure 需 `/openai/v1/`，v1 API 必需） |
| 2 | 消息容器 | `messages` → **`input`**（支持字符串简写或 `input_text`/`input_image`/`input_file` 的 item 数组） |
| 3 | 系统提示 | `messages[role=system]` → **`instructions`** |
| 4 | 多轮 | 客户端拼历史 → **`previous_response_id`**（或手动回填 output items，二选一，别混用） |
| 5 | 结构化输出 | `response_format` → **`text.format`** |
| 6 | 工具结果 | `{role:"tool"}` → **`{type:"function_call_output", call_id, output}`** |
| 7 | 长度与状态 | `max_tokens` → `max_output_tokens`；按需 `store`（数据留存合规）、`context_management`（服务端压缩） |
| 8 | 流式解析 | `choices[0].delta.content` → **`response.output_text.delta`** 事件；补流内 error 处理 |
| 9 | 思维链 | 若用 `store=false`，需请求 `reasoning.encrypted_content` 并回传 |

**迁移后的收益（官方口径）**：更高隐式缓存命中率、更低费用、可观测的执行步骤、服务端压缩长上下文。

---

## 八、参考来源

**官方**
- [OpenAI Agents SDK · 模型（Responses vs Chat Completions、Responses 专属字段）](https://openai.github.io/openai-agents-python/zh/models/)
- [Azure OpenAI Responses API（端点、字段、流式错误映射、内容筛选、保留 30 天）](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/responses)
- [Bedrock · Claude Messages API 请求与响应（字段、stop_reason、beta 头、超时）](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-anthropic-claude-messages-request-response.html)
- [Bedrock · Claude Messages API 概览（预填充、多模态、超时建议）](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-anthropic-claude-messages.html)
- [Bedrock · Converse API（统一接口）](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html)
- [Gemini API · Interactions（GA、状态管理、保留期、与 generateContent 的差异）](https://ai.google.dev/gemini-api/docs/interactions)
- [Gemini API · generateContent 参考](https://ai.google.dev/api/generate-content)
- [xAI Grok API（Responses 为推荐、Chat Completions 为 Legacy、mTLS）](https://docs.x.ai/docs/overview)
- [Mistral API（prompt_cache_key 计费、结构化输出、工具类型扩展）](https://docs.mistral.ai/api/)
- [阿里云百炼 · OpenAI 兼容接口（支持/不支持参数）](https://help.aliyun.com/zh/model-studio/developer-reference/compatibility-of-openai-with-dashscope)
- [智谱 BigModel · OpenAI 兼容接口（temperature 约束、reasoning_content）](https://docs.bigmodel.cn/cn/guide/develop/openai/introduction)
- [Moonshot · Chat API（max_completion_tokens 弃用替代、Partial Mode、签名头）](https://platform.moonshot.cn/docs/api/chat)
- [腾讯云 · 混元 OpenAI 兼容接口（stop 语义差异、stream_options、并发限制）](https://cloud.tencent.com/document/product/1729/111007)
- [百度智能云 · 千帆文本生成（Bearer API Key、X-Ratelimit 头）](https://cloud.baidu.com/doc/qianfan-api/s/3m7of64lb)
- [讯飞开放平台 · 星火 HTTP 接口（鉴权、内置 web_search、错误码）](https://www.xfyun.cn/doc/spark/HTTP调用文档.html)
- [DeepSeek API 文档（OpenAI + Anthropic 双兼容）](https://api-docs.deepseek.com/zh-cn/)
- [DeepSeek · 模型 & 价格（1M 上下文 / 384K 输出、并发上限、空闲·高峰双价、缓存倍差）](https://api-docs.deepseek.com/zh-cn/quick_start/pricing)
- [DeepSeek · 使用 Anthropic API（模型名映射规则、字段忽略清单、Claude Code / Desktop 接入）](https://api-docs.deepseek.com/zh-cn/guides/anthropic_api)
- [火山方舟 · 模型列表与 Responses 迁移](https://www.volcengine.com/docs/82379/1330310)
- [OpenRouter · API Reference（归一化、静默忽略、usage.cost、路由字段）](https://openrouter.ai/docs/api-reference/overview)
- [LiteLLM Proxy（统一端点、100+ 提供方、虚拟密钥）](https://docs.litellm.ai/docs/proxy/quick_start)
- [vLLM · OpenAI 兼容服务器（含 /v1/messages 的 Anthropic 兼容）](https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html)

**社区**
- OpenAI Responses 与 Chat Completions 演进、Claude 模型 ID 规范等报道（仅作线索）

---

## 相关笔记

- [各大厂商代表模型总览.md](./各大厂商代表模型总览.md) —— 模型层：谁有什么模型
- [model-routing](../../ai/model-routing/README.md) —— 路由层：选模型、失败切换、升级策略
- [环节04-工具调用详解](../../llm/agent/环节04-工具调用详解.md) —— 工具调用的原理与设计
- [structured-output 专题](../../ai/structured-output/README.md) —— 结构化输出的工程实践
- [环节11-服务化与推理引擎详解](../../llm/transformer/环节11-服务化与推理引擎详解.md) —— 自托管服务化协议栈
- [Qwen-Omni 实时接入与工程实践](../qwen/Qwen-Omni实时接入与工程实践.md) ｜ [GLM 音视频通话接入与工程实践](../glm/音视频通话接入与工程实践.md) —— WebSocket 实时协议的两种范式

---

*文档完 · 2026-09-11*
