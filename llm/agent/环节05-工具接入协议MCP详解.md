# 环节 05 · 工具接入协议（MCP：把"一堆工具"变成"一个生态"）

> Agent 的"USB-C 口"：标准化"应用 ↔ 外部工具/数据源"的接入。
> 所属总揽：[Agent全链路总揽与环节拆解.md](./Agent全链路总揽与环节拆解.md) 环节 05。
> 相邻环节：MCP Server 提供的工具最终以 [环节 04 Function Calling](./环节04-工具调用详解.md) 格式喂给模型；一个工具要不要给、给谁用 → [环节 10](./环节10-生产级工程化详解.md)。
> 适合人群：后端/资深读者。当你手上工具超过三五个、或要接第三方系统时，MCP 就是你要的那层"总线"。

> ⚠️ **版本口径（务必先看）**：MCP 最新稳定版 **2026-07-28** 是一次**破坏性重构**——已**删除 `initialize` 握手与 `Mcp-Session-Id`**，协议核心**改为无状态**（新增 `server/discover`，版本/能力走每请求 `_meta`）。
> 本文主体（§2–§4.2/§4.4、§8）描述的是 **≤ 2025-11-25 经典模型**（有握手、有会话）；**新旧差异与迁移要点集中在 §4.5**。

---

## 1. 干什么

**MCP（Model Context Protocol，模型上下文协议）** 是一个**开放协议**，用来标准化 **"应用（Host）↔ 外部工具/数据源（Server）"** 的接入：发现（list）、调用（call）、资源读取（read）、提示词获取（get），全部走统一协议，不再为每个工具各写一套 SDK。

**为什么会有它**：每个外部系统（GitHub、数据库、浏览器、内部系统）都自己一套 API/认证/文档 → N 个工具 N 个适配器。MCP 让"能力提供方"写一个 Server、"应用方"用通用 Client 接，一次接入、处处可用（类比 **JDBC / USB-C**）。

> **与 Function Calling 的关系：不是竞争，是叠加。**
> - FC 管"模型怎么请求调用"——**模型能力层**（每轮对话内，模型侧格式）；
> - MCP 管"应用怎么发现并连接一堆工具"——**系统协议层**（进程/网络间，应用侧总线）；
> - MCP Server 提供的工具，最终仍以 FC 的 `tools` 格式被注册给模型调用。**两者各管一段，MCP 是 FC 的"工具供应链"。**

> **产物口径：环节交付 = 一套协议栈（Server/Client/SDK）+ 工具/资源目录 + 传输与鉴权配置**。落地时你通常只写 Server（提供能力）或用现成 Server（接 GitHub/DB/浏览器），Client 由 Agent 框架内置。

---

## 2. 架构角色

```
┌──────────────────────┐        JSON-RPC 2.0        ┌──────────────────────┐
│  Host（宿主应用）       │ ◀────────────────────────▶ │  MCP Server（能力方）  │
│  如 CodeBuddy / Claude │    MCP Client（1..N 个）    │  如 GitHub/DB/浏览器   │
│   Desktop / 你的 Agent │                            │                      │
│                       │   MCP Client 内嵌在 Host 里  │  Server 暴露：        │
│   Host 可同时连多个     │                            │   tools / resources   │
│   Server，每个 Server  │                            │   / prompts           │
│   建立独立 Client 连接  │                            │                      │
└──────────────────────┘                            └──────────────────────┘
```

| 角色 | 职责 | 类比 |
|---|---|---|
| Host | 用户侧应用，内嵌 MCP Client；负责把 Server 暴露的能力转成模型可用的 tools/resources | 电脑上的应用程序 |
| MCP Client | 与单个 Server 建立 1:1 连接、发请求、收响应 | 应用里的驱动 |
| MCP Server | 轻量程序，通过标准原语暴露能力（tools/resources/prompts） | 打印机/外设 |

**能力协商**：`initialize` 握手时双方声明 `capabilities`（能提供/支持什么），客户端据 Server 声明决定 UI 与行为——Server 说了有 `resources`，Host 才显示资源浏览入口。

---

## 3. 传输层

| 传输 | 形态 | 适用 |
|---|---|---|
| **stdio** | 本地子进程，走标准输入/输出 | 本地工具（文件系统、shell、代码库）；Host 拉起 Server 进程 |
| **Streamable HTTP**（HTTP+SSE 的演进形态） | 一个 HTTP endpoint，支持流式与非流式响应（SSE） | **远程 Server 的现代默认** |
| HTTP+SSE（早期版本） | 独立 POST endpoint + SSE 流 endpoint | 已被 Streamable HTTP 取代，见历史代码 |

远程 Server 鉴权走标准 **OAuth 2.1**（授权码流，含 PKCE）；本地 stdio 不走网络鉴权（进程由 Host 管控）。

> 状态说明：stdio **物理上有状态**（常驻进程 + 1:1 连接）；而 Streamable HTTP 的状态性随规范版本变化——**≤ 2025-11-25** 由 Server 自决（返回 `Mcp-Session-Id` 即有会话，生产多走无状态）；**2026-07-28 起协议层已删除会话机制**，任何请求均可落到任意实例。详见 §4.5。

---

## 4. 协议分层

### 4.1 消息层：JSON-RPC 2.0

统一 envelope（`jsonrpc:"2.0"` + `id`/`method`/`params`），支持 request/response/notification（无响应的通知）。生命周期 + 三大能力全跑在这层上。

### 4.2 生命周期（连接要先"握手"）

> ⚠️ **2026-07-28 起本节流程已被删除**：不再有 `initialize` / `notifications/initialized`；版本、capabilities、clientInfo 改为**每个请求在 `_meta` 中携带**，另新增 `server/discover` 供客户端前置探测。以下为经典模型（≤ 2025-11-25）。

- 客户端发 `initialize`：**版本协商**（双方 MCP 版本）+ **能力声明**（client capabilities / server capabilities）；
- Server 回 `InitializeResult`；
- 客户端发 `notifications/initialized` 通知完成初始化；
- **约束：initialize 之前不能发其他请求**（除了 ping）；版本不一致要按协议降级或拒绝。

### 4.3 三大能力原语

| 能力 | 干什么 | 核心方法 | 类比 |
|---|---|---|---|
| **tools** | 可执行动作（模型可调用的函数） | `tools/list`、`tools/call`、`notifications/tools/list_changed` | 电脑上的"应用功能" |
| **resources** | 可读取的数据/文件（文本、二进制、结构化），按 URI 寻址 | `resources/list`、`resources/templates/list`（URI 模板，如 `file://{path}`）、`resources/read`、`notifications/resources/updated` | "文件系统" |
| **prompts** | 可复用的提示词模板（用户可选的命令） | `prompts/list`、`prompts/get`、`notifications/prompts/list_changed` | "宏/快捷指令" |

**tools 与 resources 的分工**：能改世界（副作用）→ tools；只读数据源 → resources。模型通常**不会直接读 resource**（那是 Host 的功能），需要"把文件内容喂给模型"时 Host 先 `resources/read` 再作为上下文注入，或 Server 提供"读取"型工具。

### 4.4 通用与进阶方法

> ⚠️ **2026-07-28 变更**：`ping`、`logging/setLevel` 已删除（日志级别改为每请求 `_meta.logLevel`）；Server→Client 请求（`sampling` / `elicitation` / `roots`）改用 **MRTR** 模式，且 Roots / Sampling / Logging 三者整体**弃用**（≥12 个月窗口）。以下为经典模型。

- `ping`（保活）、`logging/setLevel`（日志级别，日志必须走 stderr——stdio 下不能污染协议流）；
- `completion/complete`（参数/URI 的自动补全，配合 templates）；
- `sampling/createMessage`：**服务端反向请求模型**（Server 想让模型帮忙生成内容时，通过 Host 代采样，可设权限拦截）——用于"Server 内嵌推理需求"的场景。

### 4.5 有状态还是无状态？（版本演进 + 高频追问）

> ⚠️ **这题的答案随规范版本变化，面试/答辩时必须先说清版本。**

| 规范版本 | 状态性 | 关键机制 |
|---|---|---|
| ≤ 2025-11-25（经典） | **有状态会话设计，会话可选** | `initialize` 握手 + `Mcp-Session-Id`；Server 不返回该头即无状态运行 |
| **2026-07-28（现行最新）** | **协议核心无状态** | 删除握手与会话 ID；版本/能力走每请求 `_meta`；新增 `server/discover` |

#### 4.5.1 现行版（2026-07-28）：MCP 已是无状态协议

**一句话**：握手和会话 ID 都被删除，任何请求都可落到**任意服务端实例**——协议层不再持有会话状态。

| 变更 | SEP | 说明 |
|---|---|---|
| 删除 `initialize` / `notifications/initialized` | SEP-2575 | 版本、capabilities、clientInfo 改为**每请求 `_meta`**（`io.modelcontextprotocol/protocolVersion`、`clientCapabilities`、`clientInfo`）；版本不符返回 `UnsupportedProtocolVersionError` |
| 删除协议级会话与 `Mcp-Session-Id` | SEP-2567 | 列表类端点不再随连接变化；跨调用状态改用**服务器自铸句柄** |
| 新增 `server/discover` | SEP-2575 | Server **MUST** 实现，公布版本/能力/身份（接管原握手的协商职责） |
| Server→Client 请求 → **MRTR** | SEP-2322 | 结果返回 `resultType:"input_required"` + `inputRequests` + `requestState`，客户端带 `inputResponses` **重试原请求** |
| GET 端点 + `resources/subscribe` → **`subscriptions/listen`** | SEP-2575 | 单条长生命周期 POST 响应流，按类型订阅 list_changed / resource 变更 |
| 删除 `ping`、`logging/setLevel`、`Last-Event-ID` | SEP-2575 | 日志级别改每请求 `logLevel`；断流即丢在途请求，客户端 **MUST** 用新请求 ID 重发 |
| 列表/资源结果加必填 `ttlMs` + `cacheScope` | SEP-2549 | 用"带 TTL 的缓存/轮询"部分取代订阅式推送 |
| 强制 `Mcp-Method` / `Mcp-Name` 头 | SEP-2243 | 网关/限流器**无需解析 body** 即可路由；头与 body 不一致则拒绝请求 |
| Roots / Sampling / Logging **弃用** | SEP-2577 | ≥12 个月弃用窗口；Sampling 官方建议改为**直连 LLM 供应商 API** |
| 资源缺失错误码 `-32002` → `-32602` | SEP-2164 | 对齐 JSON-RPC 标准码 |

**动机**：旧版远程部署要 **粘性会话 + 共享会话存储 + 网关 DPI**；新版可直接跑在**普通轮询负载均衡**之后，适配 serverless / 边缘部署。

**"无状态协议，有状态应用"**：删掉协议层会话 ≠ 应用必须无状态。官方推荐**显式句柄**模式——工具返回 `basket_id` / `browser_id`，模型在后续调用中作为**普通参数**回传。官方认为这往往更强：模型能**跨工具组合句柄、对其推理、在步骤间交接**，这是藏在传输元数据里的会话状态做不到的——**把状态显式暴露给模型，而不是藏起来**。

#### 4.5.2 经典版（≤ 2025-11-25）：有状态会话设计，但会话可选

**一句话**：MCP **按"有状态会话"设计**（`initialize` 握手 + `Mcp-Session-Id`），但**会话是可选项**——Server 可无状态运行，代价是丢掉"服务端主动"类能力。分层看：

| 层 | 状态 | 说明 |
|---|---|---|
| JSON-RPC 2.0 消息层 | **无状态** | 每条 request/response/notification 自包含，靠 `id` 关联 |
| 协议生命周期层 | **有状态** | `initialize` 协商版本 + capabilities，形成会话（见 §4.2） |
| stdio 传输 | **天然有状态** | 常驻子进程、1:1 长连接 |
| Streamable HTTP 传输 | **可选（生产多走无状态）** | Server 返回 `Mcp-Session-Id` → 有状态；不返回 → 无状态 |

**会话机制（Streamable HTTP）**：
- Server 可在 `InitializeResult` 的响应头返回 `Mcp-Session-Id`（全局唯一、加密安全，如 UUID/JWT，仅可见 ASCII `0x21~0x7E`）；
- 客户端此后**所有请求必须携带**该头，缺失 → `400 Bad Request`；
- Server 可随时终止会话，终止后带该 id 的请求返回 `404`，客户端**必须重新 `initialize`**；
- 客户端可发 `DELETE + Mcp-Session-Id` 主动结束；
- **Server 不返回该头 = 不建立 MCP 会话**（规范中无"无状态模式"一词，这是"不分配 session id"的自然结果）。

**无状态会失去什么**：

| 能力 | 无状态 |
|---|---|
| `tools/list` / `tools/call` / `resources/read` | ✅ 正常 |
| JSON-RPC 格式、SSE 流式 | ✅ 保留 |
| **sampling / elicitation / roots**（Server → Client 反向请求） | ❌ 全部禁用 |
| **非请求通知**（资源变更、日志推送） | ❌ 不支持：通知必须是某次 POST 的直接响应 |
| **resources 订阅**（subscribe / updated） | ❌ 不支持 |
| 断流恢复/重放、并发客户端隔离、重连重置状态 | ❌ 弱化或没有 |

> 根因：无状态下每个 HTTP 请求创建**全新的 Server 上下文**，Client 对反向请求的回复会作为**新 POST** 到达，Server 无法把它与当初发起询问的 handler 关联。有状态靠"让 handler 在多次 HTTP 往返间存活"解决。（**2026-07-28 用 MRTR + `requestState` 从根上绕开了该约束**——信息全在 payload 里，所以任意实例都能接手重试。）

**工程取舍**：
- **生产默认推荐无状态**（官方 C# SDK 建议 `Stateless = true`；华为云 AgentArts 默认 `stateless_http=True`）——因为绝大多数 Server 提供的是"纯函数式工具"；
- 好处：水平扩展**无需粘性会话**、serverless 友好、Server 重启无感、内存按请求而非按会话（有状态默认上限 10k 会话 × 2h 空闲超时）；
- **红线**：一旦 `initialize` 响应带上 `Mcp-Session-Id`，客户端就**被迫**走会话 → 必须先确认部署侧有**粘性路由**，多实例 + 轮询 LB 会直接 404。

#### 4.5.3 版本无关的三条硬结论

1. **JSON-RPC 消息层一直是无状态的**（自包含 envelope + `id` 关联）；
2. **stdio 传输物理上有状态**（常驻子进程、1:1 连接）——即便协议层已无会话；
3. **2026-07-28 之后，"要不要维护状态"变成纯应用层决策**：协议不再提供会话机制，状态靠**显式句柄**或外部存储承载。

**口诀**：只做"列工具、调工具、读资源" → 无状态天然够用；需要跨调用上下文 → **传句柄**（新）或开会话（旧）；需要服务端主动推送/询问 → 旧版靠有状态，新版靠 **MRTR + `subscriptions/listen`**。

---

## 5. 错误码（JSON-RPC 约定 + MCP 扩展）

| 码 | 含义 |
|---|---|
| -32700 | 解析错误（请求不是合法 JSON） |
| -32601 | 方法未找到（method 不存在） |
| -32602 | 无效参数（params 不合法） |
| -32603 | 内部错误 |
| -32002 | 资源未找到（resources/read 目标不存在）——⚠️ **2026-07-28 起改为 `-32602`**（SEP-2164，对齐 JSON-RPC） |

> **2026-07-28 错误码重分区**：`-32000 ~ -32019` 保留给实现自定义（现有 SDK 用法获豁免），`-32020 ~ -32099` 归规范——`HeaderMismatch` → `-32020`、`MissingRequiredClientCapability` → `-32021`、`UnsupportedProtocolVersion` → `-32022`。

---

## 6. 安全与授权（接外部系统的红线）

- **授权模型**：Host 对每个工具/资源做"用户可见 + 可批准"控制——高危操作（写文件、执行命令、发消息）在调用前请求用户批准（Human-in-the-loop），批准前 Server 不执行；
- **Server 连接是提权点**：一个被攻破/恶意的 Server 等于给 Agent 开了后门——只连可信 Server；Server 最小权限（只给该给的 API token）；对第三方 Server 的能力先审后接；
- **数据边界**：resources 暴露了什么文件/库，Host 要能按用户/会话配置白名单，防止"读越权文件喂给模型"（[环节 10](./环节10-生产级工程化详解.md)）；
- **审计**：tools/call 全量留痕（与 [环节 4 §4](./环节04-工具调用详解.md) 同一套审计需求）。

---

## 7. 落地实践

### 7.1 什么时候该上 MCP

| 情况 | 决策 |
|---|---|
| 只接 1~2 个自家工具 | 可以不 MCP，直接 FC（[环节 4](./环节04-工具调用详解.md)） |
| 工具多 / 跨系统 / 团队间共享工具 | 上 MCP：一次实现、多 Host 复用 |
| 要接第三方现成生态（GitHub/DB/浏览器等） | 直接用官方/社区 Server，别自己写 |

### 7.2 自研 Server 要点

- 用官方 SDK（TypeScript/Python/Go 等）起步，别裸写 JSON-RPC；
- 能力先小后大：先 tools，需要再上 resources/templates/prompts；
- `capabilities` 如实声明，别夸（Host 按声明渲染 UI，声明错用户就迷糊）；
- 远程部署：Streamable HTTP + OAuth；本地：stdio 最省事；
- 开发调试用官方 **MCP Inspector**（可视化看连接/请求/响应）。

---

## 8. 工程红线（必守）

1. **initialize 握手完成前不能发业务请求**；版本协商失败要优雅报错而非硬跑。（经典版 ≤ 2025-11-25；**2026-07-28 起握手已删除**，改为每请求 `_meta` 校验协议版本，不符返回 `UnsupportedProtocolVersionError`）
2. **stdio 传输下一切日志走 stderr**，污染 stdout 协议流 = 连接崩。（2026-07-28 后日志级别走每请求 `_meta.logLevel`，`logging/setLevel` 已删除）
3. Server 的 tools/resources **默认最小授权**，高危操作留人工确认口子。
4. 第三方/社区 Server 接进来前要审计能力与权限（恶意 Server = 后门）。
5. tools 变了要发 `notifications/tools/list_changed`，让 Host 刷新清单，否则模型拿着旧清单调用报错。（2026-07-28 起统一走 `subscriptions/listen`；列表结果带 `ttlMs`/`cacheScope`，亦可依赖 TTL 缓存刷新）
6. **（2026-07-28 新增）Streamable HTTP 必须发送 `Mcp-Method` / `Mcp-Name`，且与 body 一致**——不一致会被拒绝；网关据此路由，不要再依赖解析请求体。
7. **（2026-07-28 新增）断流不可续传**：`Last-Event-ID` / SSE event ID 已删除，连接断开即在途请求丢失，客户端必须用**新请求 ID 重发**。

---

## 9. 面试高频追问

1. MCP 解决什么问题？→ 工具接入碎片化：把"发现/调用/读资源"标准化，Host 一次接入多处复用（JDBC/USB-C 类比）。
2. MCP 与 Function Calling 是替代关系吗？→ 不是。FC 是模型侧调用协议（对话内），MCP 是应用侧接入总线（系统间）；MCP 的工具最终以 FC 格式呈现给模型。
3. MCP 三大能力是什么？→ tools（动作）、resources（只读数据源，URI 寻址）、prompts（复用模板）；跑在 JSON-RPC 2.0 之上。（经典版还有 `initialize` 生命周期；**2026-07-28 起握手已删除**）
4. 怎么保证 MCP Server 安全？→ 可信来源 + 最小权限 + 高危操作人工批准 + 全量审计；SSRF/越权是远程 Server 的主要风险。
5. stdio 和 Streamable HTTP 各适合什么？→ 本地进程用 stdio（省鉴权）；远程服务用 Streamable HTTP + OAuth。
6. MCP 是有状态还是无状态？→ **先答版本**：≤ 2025-11-25 是"有状态会话设计、会话可选"（`initialize` + `Mcp-Session-Id`；JSON-RPC 消息层无状态、stdio 天然有状态）；**2026-07-28 起协议核心已无状态**——握手与会话 ID 均被删除，版本/能力走每请求 `_meta`，跨调用状态改用**服务器自铸句柄**，反向交互改 **MRTR**（`input_required` + `requestState`）。详见 §4.5。
7. MCP 2026-07-28 最大的变化是什么？→ **无状态化重构**：删 `initialize` 握手与 `Mcp-Session-Id`，新增 `server/discover`，Server→Client 请求改 MRTR，订阅统一 `subscriptions/listen`，列表结果加 `ttlMs`/`cacheScope`，Roots/Sampling/Logging 弃用——远程 Server 不再需要粘性会话与共享会话存储，可直接跑在普通轮询负载均衡之后。

---

## 10. 相关链接

- 入口总揽：[Agent全链路总揽与环节拆解.md](./Agent全链路总揽与环节拆解.md)
- 模型侧怎么消费 Server 暴露的工具：→ [环节 04 工具调用详解](./环节04-工具调用详解.md)
- 高危工具人工确认（interrupt）：→ [环节 07 编排与循环控制详解](./环节07-编排与循环控制详解.md)
- 权限/审计/注入防护纵深：→ [环节 10 生产级工程化详解](./环节10-生产级工程化详解.md)
- 协议版本演进：[MCP 版本演进与变更特性](../../ai/mcp/版本演进.md)（2024-11 → 2026-07 各版变更 + 迁移建议）
- 知识地图：[知识点.md](../知识点.md)（§2.7 MCP，含接口清单速记）
