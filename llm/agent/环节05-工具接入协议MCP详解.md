# 环节 05 · 工具接入协议（MCP：把"一堆工具"变成"一个生态"）

> Agent 的"USB-C 口"：标准化"应用 ↔ 外部工具/数据源"的接入。
> 所属总揽：[Agent全链路总揽与环节拆解.md](./Agent全链路总揽与环节拆解.md) 环节 05。
> 相邻环节：MCP Server 提供的工具最终以 [环节 04 Function Calling](./环节04-工具调用详解.md) 格式喂给模型；一个工具要不要给、给谁用 → [环节 10](./环节10-生产级工程化详解.md)。
> 适合人群：后端/资深读者。当你手上工具超过三五个、或要接第三方系统时，MCP 就是你要的那层"总线"。

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

---

## 4. 协议分层

### 4.1 消息层：JSON-RPC 2.0

统一 envelope（`jsonrpc:"2.0"` + `id`/`method`/`params`），支持 request/response/notification（无响应的通知）。生命周期 + 三大能力全跑在这层上。

### 4.2 生命周期（连接要先"握手"）

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

- `ping`（保活）、`logging/setLevel`（日志级别，日志必须走 stderr——stdio 下不能污染协议流）；
- `completion/complete`（参数/URI 的自动补全，配合 templates）；
- `sampling/createMessage`：**服务端反向请求模型**（Server 想让模型帮忙生成内容时，通过 Host 代采样，可设权限拦截）——用于"Server 内嵌推理需求"的场景。

---

## 5. 错误码（JSON-RPC 约定 + MCP 扩展）

| 码 | 含义 |
|---|---|
| -32700 | 解析错误（请求不是合法 JSON） |
| -32601 | 方法未找到（method 不存在） |
| -32602 | 无效参数（params 不合法） |
| -32603 | 内部错误 |
| -32002 | 资源未找到（resources/read 目标不存在） |

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

1. **initialize 握手完成前不能发业务请求**；版本协商失败要优雅报错而非硬跑。
2. **stdio 传输下一切日志走 stderr**，污染 stdout 协议流 = 连接崩。
3. Server 的 tools/resources **默认最小授权**，高危操作留人工确认口子。
4. 第三方/社区 Server 接进来前要审计能力与权限（恶意 Server = 后门）。
5. tools 变了要发 `notifications/tools/list_changed`，让 Host 刷新清单，否则模型拿着旧清单调用报错。

---

## 9. 面试高频追问

1. MCP 解决什么问题？→ 工具接入碎片化：把"发现/调用/读资源"标准化，Host 一次接入多处复用（JDBC/USB-C 类比）。
2. MCP 与 Function Calling 是替代关系吗？→ 不是。FC 是模型侧调用协议（对话内），MCP 是应用侧接入总线（系统间）；MCP 的工具最终以 FC 格式呈现给模型。
3. MCP 三大能力是什么？→ tools（动作）、resources（只读数据源，URI 寻址）、prompts（复用模板）；跑在 JSON-RPC 2.0 + 生命周期（initialize）之上。
4. 怎么保证 MCP Server 安全？→ 可信来源 + 最小权限 + 高危操作人工批准 + 全量审计；SSRF/越权是远程 Server 的主要风险。
5. stdio 和 Streamable HTTP 各适合什么？→ 本地进程用 stdio（省鉴权）；远程服务用 Streamable HTTP + OAuth。

---

## 10. 相关链接

- 入口总揽：[Agent全链路总揽与环节拆解.md](./Agent全链路总揽与环节拆解.md)
- 模型侧怎么消费 Server 暴露的工具：→ [环节 04 工具调用详解](./环节04-工具调用详解.md)
- 高危工具人工确认（interrupt）：→ [环节 07 编排与循环控制详解](./环节07-编排与循环控制详解.md)
- 权限/审计/注入防护纵深：→ [环节 10 生产级工程化详解](./环节10-生产级工程化详解.md)
- 知识地图：[知识点.md](../知识点.md)（§2.7 MCP，含接口清单速记）
