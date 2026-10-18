# ACP · Agent Client Protocol

> 编辑器 / 客户端与编码 Agent 之间的开放协议。一句话：**MCP 是手，A2A 是工单，ACP 是屏幕**——把「Agent 在干什么」画进人正在用的界面。

由 Zed 于 2025 年提出并开源（形状照抄 LSP，JSON-RPC 2.0 + stdio），JetBrains、Neovim 社区等跟进；到 2026 年规范已到 **v1**（v2 在起草），官方 Agents 页列出 **40+ 个 Agent**、Clients 页列出上百个客户端，是编码 Agent 进编辑器的常见接缝（如 Kimi CLI 经 ACP 进 IDE）。名单见 [§四](#四生态谁支持-acp)，以 [ACP Registry](https://agentclientprotocol.com/get-started/registry) 为准。

配套 MVP：[mvp.py](./mvp.py)（client ↔ agent 的 initialize / session / update 流，无外部依赖）。

> **同名辨析**：IBM 早期也有一个 ACP（Agent Communication Protocol），已于 2025 年并入 [A2A](../a2a/)。今天说 ACP，默认指 **Agent Client Protocol**（客户端 ↔ Agent），不要和它混。

---

## 一、技术讲解

### 1.0 先看全景：三条接缝各管一段

```
                 人（盯着屏幕）
                      │
                      ▼
   ┌───────────┐  ACP 屏幕接缝  ┌───────────┐  MCP 手接缝  ┌─────────────┐
   │  Client   │◄─────────────►│   Agent   │◄───────────►│  MCP Server │
   └───────────┘                └─────┬─────┘              └─────────────┘
   编辑器 / TUI / 看板                 │ A2A 同事接缝
   Zed · Multica · JetBrains          ▼
                                另一个 Agent
```

一次 Agent 请求通常同时跨三条缝：人在屏幕前用 **ACP** 看它干活，它用 **MCP** 伸手干活，跨团队的活儿用 **A2A** 发工单。

记住箭头方向：ACP 是**双向**的——`session/prompt` 是 Client→Agent，而 `fs/*`、`terminal/*`、`session/request_permission` 是 **Agent→Client**。两边互为主客，这是它和单向 API 最大的差别（细节见 §1.3）。

每个编辑器想接每个编码 Agent，都是一次单独对接：**N 个 IDE × M 个 Agent = N×M 次适配**，且每家的「流式文字 / 工具卡片 / 权限弹窗 / diff 显示」都自己发明一遍。ACP 把这条缝标准化——它是 **LSP 的同构物**：LSP 让语言服务器插进任意编辑器，ACP 让 Agent 插进任意编辑器。

但两者不是一回事：**LSP 是无状态小请求**（补全、跳转，一次来回就完）；**ACP 是长事务**——有会话 id、有多轮、有副作用、要权限、要能取消。

| 角色 | 谁扮演 | 做什么 |
|---|---|---|
| **Client** | Zed / JetBrains / VS Code 插件 / 终端 UI | 显示消息流、渲染工具卡片、管权限、提供文件系统与终端 |
| **Agent** | 编码 Agent 进程（Claude Code、Codex、Kimi、自研 Harness） | 跑循环、发工具调用、回消息流与计划 |

底层：JSON-RPC 2.0 over stdio，**换行分帧**（不是 LSP 的 `Content-Length` 头）。细节见 §1.4。

### 1.1 会话生命周期

```
initialize            能力协商（Client: fs / terminal；Agent: prompt / mcp / loadSession）
  → session/new       开一个会话，拿到 sessionId（可带 cwd、mcpServers）
  → session/prompt    发一轮 user prompt（content blocks），流式回 session/update
  → session/cancel    用户点了停止
  → session/load      进程/编辑器重开后按 id 恢复会话
  → session/set_mode  切换模式（如「先问再改」与「自动改」）
```

### 1.2 `session/update` 通知（全部条带 `sessionId`）

| sessionUpdate | 用途 |
|---|---|
| `agent_message_chunk` | 给用户的文字流（打字机效果） |
| `agent_thought_chunk` | 思考过程，UI 折叠显示 |
| `tool_call` | 新建一个工具卡片：id、title、**kind**（read / edit / execute / search / delete / move / fetch / think / switch_mode / other）、locations、rawInput |
| `tool_call_update` | 卡片状态流转：`pending → in_progress → completed / failed`，带 rawOutput / content |
| `plan` | 步骤清单：`pending / in_progress / completed` + priority，UI 画成 todo 列表 |
| `usage_update` | token 与花费，实时上屏 |
| `available_commands_update` / `current_mode_update` / `config_option_update` | 斜杠命令、当前模式、可配置项同步 |

`session/prompt` 最终返回一个 **stopReason**：`end_turn`（正常说完了）、`cancelled`（用户停）、`refusal`（Agent 拒绝做）、`max_tokens` / `max_turn_requests`（触顶）。

### 1.3 Agent 反向调用 Client（客户端是「手」的提供者）

| 方法 | 用途 |
|---|---|
| `fs/read_text_file` / `fs/write_text_file` | 读写用户编辑器里的文件（带行号范围） |
| `terminal/create`、`terminal/output`、`terminal/wait_for_exit`、`terminal/kill`、`terminal/release` | 起命令、流式取输出、等退出、杀掉 |
| `session/request_permission` | **请求式权限**：带 options（allow_once / allow_always / reject_once / reject_always），由人拍板 |

内容块统一为 text / image / audio / resource / resource_link，所以「把当前选中的代码块喂给 Agent」和「Agent 吐一张图」走同一套结构。

关键设计：**ACP 不管 Agent 怎么想**。协议只保证「人能看见、能插手、能叫停」；循环、工具、压缩仍属 [Harness](../harness/) 与 [循环工程](../loop-graph/)。

### 1.4 底层：编码、分帧、传输

按层拆开看，ACP 的底座很薄，薄到可以手写：

| 层 | 是什么 |
|---|---|
| **编码层** | **JSON-RPC 2.0**，UTF-8。两类消息：**Method**（请求-响应，有 `id`）与 **Notification**（单向，无 `id`，永不回包） |
| **分帧层** | **换行分隔的 JSON**（NDJSON）：一条消息一行，以 `\n` 结尾，**消息内部不得含换行** |
| **传输层** | **stdio**（推荐，必须支持）：Client 把 Agent 当**子进程**起，Agent 从 stdin 读、往 stdout 写 |
|  | **Streamable HTTP**：v1 仍是草案；**自定义传输**允许（协议本身 transport-agnostic），只要保住 JSON-RPC 格式与生命周期 |
| **会话层** | `initialize` → `authenticate`（可选）→ `session/new` 或 `session/load` → `session/prompt` → `session/update` 流 → `stopReason` |
| **扩展层** | `_meta` 放自定义数据；`_` 前缀定义私有方法；`initialize` 里声明自定义 capability |

三条硬约束（实现时最容易踩）：

1. **stdout 是协议专线**：Agent 不许往 stdout 写任何非法 ACP 消息，日志必须走 stderr（Client 可捕获、转发或忽略）。
2. **stdin 同理**：Client 也不许往 Agent 的 stdin 塞别的东西。
3. **通知永不回包**：`session/update`、`session/cancel`、`elicitation/complete` 没有响应，出错也收不到 error——所以别在通知上等确认。

一帧长这样（stdio 上一行一条）：

```
{"jsonrpc":"2.0","id":1,"method":"session/prompt","params":{"sessionId":"s_1","prompt":[{"type":"text","text":"把 MAX_RETRY 改成 5"}]}}
{"jsonrpc":"2.0","method":"session/update","params":{"sessionId":"s_1","update":{"sessionUpdate":"agent_message_chunk","content":{"type":"text","text":"好"}}}}
```

**和 LSP 的差别**（形状照抄，分帧没照抄）：LSP 走 `Content-Length: N\r\n\r\n{json}` 的头部分帧，ACP 直接一行一条 JSON——更简单，代价是消息体里不能出现裸换行（JSON 字符串内的 `\n` 转义没问题）。

其他约定：所有**文件路径必须绝对**；**行号从 1 开始**；属性名用 camelCase，而 discriminator 字段的取值用 snake_case（如 `sessionUpdate: "tool_call_update"`）；错误走标准 JSON-RPC error 对象（`code` + `message`）。

---

## 二、功能作用

- **解耦 UI 与 Agent**：Agent 写一次，所有支持 ACP 的编辑器可用；编辑器接一次，所有 ACP Agent 可换。
- **可见性**：工具调用、文件改动、计划进度都是结构化卡片，而不是黑盒日志。
- **权限归位**：危险操作（`execute` / `delete`）由客户端弹窗裁决，Agent 不得自己偷偷执行。
- **人在环里的真接口**：不是「跑完给个总结」，而是中途能 cancel、能改模式、能拒一次。
- **会话持久**：`session/load` 让 IDE 重启后接着聊，diff 与计划都还在。
- **MCP 转发**：编辑器里配的 MCP server 可在 `session/new` 时交给 Agent，UI 与工具面不必各配一遍。

---

## 三、应用场景

| 场景 | 为什么用 ACP |
|---|---|
| IDE 里同时装多家编码 Agent | 一套 UI，Agent 可换（Zed / JetBrains / VS Code 插件） |
| 自研 Harness 想进编辑器 | 只实现 ACP 的 agent 侧，不必给每家 IDE 写插件 |
| 终端 UI / Web UI 复用同一个 Agent | Client 不同，Agent 进程不变 |
| 远端沙箱 Agent + 本地编辑器 | 本地 Client 提供 fs / terminal，Agent 在远端跑 |
| 企业统一工具面 | 编辑器配 MCP，随 `session/new` 下发给 Agent |
| 看板 / 工作区（[Multica](../multi-agent-research/multica.md)） | 一个 daemon 用 ACP 驱动本机 20+ 种 CLI（Claude / Codex / Cursor / CodeBuddy / dsh…），N×M 降成 N+M |
| 自动化 / 子 Agent（`dsh-subagent-acp`） | 父进程当 ACP client，把子 Agent 放在子进程里驱动——ACP 也能当 Agent↔Agent 的内部接缝 |
| IM / Notebook | 飞书、Telegram、Jupyter、marimo 都成了 Client；**人在哪，Client 就长在哪** |

### 3.1 案例：Multica 怎么用 ACP

本仓库 [Multica](../multi-agent-research/multica.md) 那套「人机共用看板」，执行面正是 ACP：

```
issue 看板（控制面） → daemon 认领 run → spawn 本机 CLI → 用 ACP 驱动 → 进度写回 issue
```

- **硬证据**：`server/pkg/agent/` 下躺着 `acp_session.go`、`acp_terminal.go`、`acp_usage.go`、`acp_deliverable.go`、`acp_effort.go`，外加每个 CLI 一个适配文件（`claude.go`、`codex.go`、`cursor.go`、`codebuddy.go`、`dsh.go`…）。
- **为什么必须用**：20+ 种 CLI 各说各话。没有 ACP，Multica 要写 20+ 套输出解析；有了 ACP，只写**一个 client**——这就是 N×M 降成 N+M 的现实例子。
- **它接得比「能对话」深**：terminal、usage、deliverable、reasoning effort 全部映射成自己的统一事件再上屏。
- **一个现实注脚**：`acp_session.go` 里专门写正则去判各家 runtime「会话已失效」的错误措辞——qodercli 说 `Invalid session identifier`，Hermes 说 `Session not found`，Kiro 说 `No session found with id`，Reasonix 说 `unknown session`；还得小心别把 `invalid token for session abc`（鉴权失败）误判成会话失效，否则会永久丢弃一条还活着的会话指针。结论很实在：**ACP 统一了信封，没统一各家实现的脾气。协议解决 N×M，但 error 文案这类脏活仍要客户端兜。**
- **同名陷阱**：网上另有一批同名 Multica（`axtrur/`、`gccrpm/`、`stillfox-lee/` 等），README 写的是 "A GUI client for ACP-compatible coding agents"，那是**纯桌面 ACP 客户端**形态（挂 OpenCode / Codex / Gemini CLI）。本仓库记录的 `multica-ai/multica` main 分支已长成看板 + daemon + 20+ CLI 的平台。两者都用 ACP，但不是一个层面的东西，引用时别混。

**不适合**：

- Agent 之间委派业务工单（那是 [A2A](../a2a/)）；
- Agent 调一个工具（那是 [MCP](../mcp/)）；
- 后台批处理 / 定时任务——没有人在屏幕前，直接调 Agent 的 SDK 或 CLI 即可，套 ACP 只是仪式。

---

## 四、生态：谁支持 ACP

> 名单取自 ACP 官方 Agents / Clients 页（2026 年快照）。生态一个月一个样，落地前以 [ACP Registry](https://agentclientprotocol.com/get-started/registry) 为准。

### 4.1 Agent 侧：40+，主体是终端 Harness

| 形态 | 代表 | 接入方式 |
|---|---|---|
| **终端 CLI / Harness**（本目录主场） | Claude Agent、Codex CLI、Gemini CLI、Kimi CLI、Qwen Code、OpenCode、Goose、Cline、OpenHands、Kiro CLI、Pi、OpenClaw、Factory Droid、Qoder CLI、VT Code、Minion Code | 多为原生；Claude Agent 走 Zed 的 SDK adapter，Codex CLI 走官方 adapter，Pi 走 `pi-acp` |
| **IDE / 商业产品** | Cursor、GitHub Copilot（公开预览）、Augment Code、Junie by JetBrains、Blackbox AI、Mistral Vibe、Poolside、AutoDev | 产品自己实现 agent 端，让别人家的 UI 也能驱动它 |
| **框架 / 自建** | fast-agent（`fast-agent-acp`）、Docker cagent、CUGA（`cuga-acp`）、Raven、Bub（`bub-acp-server`）、AgentPool、Stakpak、Muse Spark Code（非官方） | 把你自己的 Agent 包成 ACP agent |

对照本仓库 [Harness](../harness/) 那张六款表：Claude Code / Codex / Kimi / Pi / OpenClaw 均已在列，DeepSeek Harness 也被第三方客户端（Martty、Perch、Vibex 等）驱动——**终端先有，UI 后接**，这是 ACP 生态的真实生长顺序。

**ACP Registry** 是另一份更严格的策展名单（只收**支持鉴权**的 agent，约 40 个），客户端可一键安装，也能程序化拉取：

```bash
curl https://cdn.agentclientprotocol.com/registry/v1/latest/registry.json
```

Registry 里还出现了 Agents 页没列的：Amp、Auggie CLI（Augment）、IBM Bob、**CodeBuddy Code（腾讯云）**、Devin CLI、Google Antigravity、Grok Build（xAI）、**GLM Agent（智谱）**、MiniMax Code、Kilo、Cortex Code（Snowflake）、DeepAgents（LangChain）等。选型时两份都看：Agents 页看全，Registry 看「能装能用」。

### 4.2 国内厂商情况（含 CodeBuddy）

| Agent | 厂商 | 接入方式 |
|---|---|---|
| **CodeBuddy Code** | 腾讯云 | **原生**：`codebuddy --acp` 即起 ACP agent server（registry id `codebuddy-code`） |
| Kimi CLI | Moonshot | 原生，`kimi acp` |
| Qwen Code | 阿里 | `npx @qwen-code/qwen-code --acp` |
| GLM Agent | 智谱（社区包） | `npx glm-acp-agent` |
| MiniMax Code | MiniMax | `npx @minimax-ai/code acp` |
| Qoder CLI | 阿里 | `npx @qoder-ai/qodercli --acp` |
| **DeepSeek Harness** | 深度求索 | **半支持**：官方内置 `dsh-acp`（自动化向），交互式编辑器用法靠社区插件 |

#### DeepSeek Harness：内置的说一半，编辑器那半靠社区

本仓库 [Harness](../harness/) 六款表里唯一没进官方 Agents 页 / Registry 的就是它，所以别照着「名单里有没有」判断。实际情况分两层：

| 层 | 是什么 | 能干到哪 |
|---|---|---|
| **官方内置 `dsh-acp`**（`deepseek-ai/deepseek-harness` 的 `packages/acp/acp`，DSH 已内置、宿主可加载） | JSON-RPC stdio 的 **仅面向自动化**的 ACP server | 程序化客户端建 agent、发文本提示、收集已提交的 assistant 文本、按策略响应一次性权限请求、取消工作；仓库内主要使用者是 `dsh-subagent-acp`（**把子 agent 当 ACP 客户端驱动**） |
| **社区插件 `dsh-acp` / `deepseek-harness-acp` / `@dsh-enhanced/acp`** | 独立 stdio ACP v1 server，或 DSH profile 插件 | 补齐「交互式」那一半：`session/new`、`list`、`load`、`resume`、`close`、`delete`，流式渲染、技能加载，共享 `$DSH_HOME` 的凭据与会话日志（Web UI 里开的会话能在编辑器里接着用） |

结论：**「能不能在 Zed 里用 DeepSeek Harness」答案是能，但走的是社区适配器，不是官方注册条目**；官方内置那份是给 subagent / 自动化用的，恰好印证了 ACP 的另一条用法——**Agent 之间也能拿 ACP 当接缝**（子 agent 在子进程里跑，父进程当 ACP client）。

两个易混项：`DeepSeek-TUI`（hmbown 的第三方 TUI，`deepseek serve --acp` 可接 Zed）不是 DeepSeek 官方 Harness，且其首个 ACP 切片只有会话与提示，工具编辑 / checkpoint 回放未暴露；第三方客户端 Martty、Perch、Vibex 都声称能驱动 DeepSeek Harness，用的就是上面那层社区适配器。

#### CLI 命令速查

```bash
# ① 官方内置（自动化向，无交互式 UI 特性）
dsh --profile acp                  # 起 stdio ACP v1 server（仓库开发态是 pnpm dsh --profile acp）

# ② 社区适配器：装进 profile（与 Web UI 共享 $DSH_HOME）
dsh plugin --profile acp add -w @openma/deepseek-harness-acp
dsh --profile acp                  # 编辑器把 command 指向 dsh + --profile acp

# ③ 社区适配器：全局装成独立 stdio server
npm i -g @openma/deepseek-harness-acp
deepseek-harness-acp               # 行为由 CLI flags 或 DSH_* 环境变量调（model / 权限模式 / session root）
dsh-acp --setup                    # 让插件在每次启动时自动加载
```

```json
// ~/.config/zed/settings.json（独立 server 形态）
{ "agent_servers": { "DeepSeek Harness": { "command": "deepseek-harness-acp", "env": {} } } }
```

官方那份的能力边界值得记一下：**支持** `initialize`（v1 + `session/list` / `resume` / `close` + Streamable HTTP MCP）、`session/new`、`session/prompt`、`session/cancel`、`session/request_permission`、`session/set_config_option`；**明确不支持** `session/load`、删除、fork、modes、commands、plans、terminals、客户端 fs 操作、elicitation——所以别指望它给编辑器画计划卡片和终端面板。社区适配器补的正是这些。

**CodeBuddy Code 是原生实现，不是适配器**，值得单独看一眼：

```bash
codebuddy --acp                     # 以 ACP agent server 启动
```

```json
// ~/.config/zed/settings.json
{ "agent_servers": { "CodeBuddy Code": { "command": "codebuddy", "args": ["--acp"], "env": {} } } }
```

它接得也比较全：客户端声明了 `fs` / `terminal` 能力时，会把文件读写与终端工具**代理给客户端执行**；`authenticate` 响应的 `_meta['codebuddy.ai/userinfo']` 回传用户信息；建会话时主动推送可用 slash 命令。另有两点超出 stdio：Remote Control 的 Web UI 走 ACP over HTTP（`POST /api/v1/acp/connect` + SSE），HTTP API 也暴露了同一套端点。

注意它有**两条并行的 IDE 集成路线**：Zed 这类走 **ACP**；VS Code / Cursor / Windsurf / JetBrains 走 **`--ide` + 本地 MCP 服务器**（插件伴生进程），那条不是 ACP。

### 4.3 Client 侧：不止是编辑器

| 类 | 代表 |
|---|---|
| **编辑器 / IDE** | Zed（发起者，最完整）、JetBrains 全家、VS Code（ACP Client / ACP Pro / Multicoder 等扩展）、Neovim（CodeCompanion、avante.nvim、agentic.nvim、hermes.nvim）、Emacs（`agent-shell.el`）、Obsidian、Sublime Text、Qt Creator、Pulsar、Unity、Visual Studio（Poolside Assistant） |
| **CLI / TUI** | Toad、acpx、Martty、Hash、Hydra、Intelligent Terminal（Windows Terminal fork） |
| **桌面 / Web** | AcpAgent Client、Alchemist Coder、Jockey、Vibex、Capsule、Outmake、oxi、Superlite、ACP UI、Kepler（GitKraken）、Devin Desktop |
| **移动 / IM / 其他** | AgentDeck、Runmote、Happy、TermFold（手机上直接跑）；Slack / Telegram / 飞书 / 微信 / QQ 桥接（OpenACP、cc-connect、Lark ACP、WeChat ACP）；Notebook（marimo、Jupyter `agent-client-kernel`）；DuckDB 扩展 |
| **框架适配** | LangChain / Deep Agents ACP、LlamaIndex `workflows-acp`、Mastra `@mastra/acp`、Koog、Pydantic AI（ACP Kit）、LLMling-Agent |

### 4.4 四点观察

1. **原生 vs 适配器**：适配器（`claude-agent-acp`、`codex-acp`、`pi-acp`）是主流路径之一——Agent 自己一行协议代码都不写，靠一层薄壳进生态。判断「支持得好不好」，看的是适配器有没有把 plan / 权限 / diff locations 都接上，而不是有没有出现在名单里。
2. **Client 的边界已经不是「编辑器」**：TUI、桌面 App、手机、飞书机器人、Jupyter 都成了 Client。含义是——**人在哪，Client 就长在哪**；Harness 只要说 ACP，就被所有这些界面共用。
3. **协议版本要盯**：v1 稳定、v2 在起草（Prompt Lifecycle 等有变化）。客户端与 Agent 先做 `initialize` 的协议版本协商，不要把版本号写死。
4. **别按名单长短选型**：同一个 Agent 在不同客户端差距极大。验收三项能力——① tool_call 带 `locations`，diff 能跳转；② 危险 kind 真走 `request_permission`；③ `session/load` 能续跑。缺一项，那个 UI 只是个高级聊天窗。

---

## 五、一次会话长什么样

```
Client (编辑器)                          Agent (编码 Agent 进程)
  |-- spawn + initialize --------------->|
  | <-------------- agentCapabilities ---|
  |-------- session/new {cwd} ---------->|
  | <-------------- {sessionId} ---------|
  |-------- session/prompt {blocks} ---->|
  |                                      |  (循环开始)
  | <--- session/update: plan -----------|
  | <--- session/update: tool_call #1 ---|   kind=read, title="读 config.py"
  |--- fs/read_text_file --------------->|   Agent 反向调 Client
  | <--- tool_call_update #1 completed --|   content + locations
  | <--- tool_call #2 (kind=edit) -------|
  | <--- request_permission -------------|   ← Agent 反向请求
  |-------- allow_once ----------------->|
  |--- fs/write_text_file -------------->|
  | <--- tool_call_update #2 completed --|
  | <--- agent_message_chunk ------------|   "已把 MAX_RETRY 改成 5"
  | <-------------- stopReason=end_turn -|
```

注意箭头方向：**prompt 是 Client→Agent，`fs/*`、`terminal/*`、`request_permission` 是 Agent→Client**。两边互为主客，这是 ACP 和单向 API 最大的差别。

---

## 六、与相邻技术

| 技术 | 关系 |
|---|---|
| [MCP](../mcp/) | 互补且正交：MCP = Agent→工具（横向下游），ACP = Client→Agent（纵向上游）。同一个 Agent 常同时是 **MCP client + ACP agent** |
| [A2A](../a2a/) | A2A = Agent→Agent，对端是另一个大脑（工单）；ACP 的 Client 是一个**界面**，对端是人 |
| LSP | 同构不同域：LSP 是无状态补全/跳转，ACP 是有副作用的长事务 |
| [Harness](../harness/) | ACP 是把 Harness 的循环**投影到 UI** 的接缝；工具与权限模型仍在 Harness 里 |
| [Guardrails](../../reliability/guardrails/) | ACP 只负责「问人」，真正的最小权限白名单在护栏层，不能只靠弹窗 |
| [Eval](../../reliability/eval/) | `session/update` 流本身就是 trajectory，可直接落库做轨迹评测 |

三个协议一句话记住：**MCP 接手，A2A 接同事，ACP 接屏幕。**

---

## 七、落地建议

1. **先跑通三件套**：`initialize` → `session/new` → `session/prompt` + `session/update` 流式。别一上来做权限和模式。
2. **tool_call 必须带 `locations`**（文件 + 行范围）和正确的 `kind`，否则 UI 既不能跳转也不能判断危险等级。
3. **危险 kind 一律 `request_permission`**（`execute` / `delete` / 写工作区外文件），客户端是唯一裁决点，Agent 侧留「被拒后怎么继续」的分支。
4. **`cancel` 要真停**：不仅停止生成，还要杀在途命令、标记工具卡片 failed；否则 UI 假死，用户只能关进程。
5. **能力要能降级**：Client 没声明 `terminal` 就自己起 `bash`，没声明 `fs` 就走自己的文件工具——按能力协商写分支，不要假定 UI 全能。
6. **会话 id 落盘 + `session/load`**：IDE 崩溃和 Agent 升级都会打断长任务，恢复能力比新功能值钱。
7. **update 流进 trace**：和模型调用、MCP 调用打在同一条链路上（[Eval](../../reliability/eval/)），否则只能看到结果看不到过程。

---

## 八、延伸阅读

- 规范与 SDK：Agent Client Protocol（Zed 发起）官方站点与 `agent-client-protocol` 仓库
- 生态名单：官方 [Agents](https://agentclientprotocol.com/get-started/agents) / [Clients](https://agentclientprotocol.com/get-started/clients) / [ACP Registry](https://agentclientprotocol.com/get-started/registry)（一键安装 ACP agent）
- 对照：[mcp](../mcp/)、[a2a](../a2a/)、[harness](../harness/)、[loop-graph](../loop-graph/)
- 权限与人审：[guardrails](../../reliability/guardrails/)

---

## 九、本目录 MVP

`mvp.py` 用进程内对象模拟一次 ACP 会话：能力协商 → `session/new` → `session/prompt`（把 `MAX_RETRY` 从 3 改成 5）→ plan → 两次 tool_call（read / edit，中间走 `request_permission`）→ 消息流 → `end_turn`；结尾再演示 `session/cancel` 返回 `cancelled`。不调真实 LLM，用来看清协议形状。

---

## 十、可跑起来的客户端：真调 CodeBuddy CLI

| 文件 | 角色 |
|---|---|
| [codebuddy_acp_ui.py](./codebuddy_acp_ui.py) | **Client 侧**完整实现 + 终端 UI：把 `codebuddy --acp` 当子进程起，走 `initialize → session/new → session/prompt`，渲染 plan / 工具卡片 / 消息流 / usage，并实现 Agent 反向调用的 `fs/*`、`terminal/*`、`session/request_permission` |
| [mock_agent.py](./mock_agent.py) | **Agent 侧的假实现**（不联网、不调模型）：专给上面那个 UI 自检用——plan → tool_call → 权限 → `fs/write_text_file` → `terminal/create` → 消息流 → `end_turn` |

```bash
# ① 自检：不需要登录、不花钱
python3 codebuddy_acp_ui.py --cmd "python3 mock_agent.py" --cwd /tmp/acp_ws --yes --once \
    <<< "写个 hello.py 并跑通"

# ② 真跑 CodeBuddy（首次会走 authenticate，浏览器里登录）
python3 codebuddy_acp_ui.py --cwd ~/myproj                      # 交互式挑登录方式
python3 codebuddy_acp_ui.py --cwd ~/myproj --auth-method external  # Google / GitHub
python3 codebuddy_acp_ui.py --cwd ~/myproj --yes                # 权限自动放行
```

UI 内命令：`/quit` 退出 · `/new` 新会话 · `/tools` 列出本轮工具卡片 · `Ctrl-C` 发 `session/cancel`。

### 实测结论（2026-10-18，codebuddy 2.168.2，macOS）

- `initialize` 回 `protocolVersion: 1`；`agentCapabilities` 除标准的 `loadSession`、`mcpCapabilities.http/sse` 外，还有 CodeBuddy 的私有扩展：`delegateToolsSupport`、`multitaskSupport`、`metaPromptSupport`、`mainAgentSupport: false`——**能力位可以带私货**，客户端不认识就当不存在。
- `authMethods` 有四条：`iOA`、`external`（Google / GitHub）、`internal`（微信）、`selfhosted`（企业域）。都不带 `type`，按规范即默认 `agent` 类型，走协议驱动的 `authenticate({methodId})`；**未登录时 `session/new` 直接报 `-32000 Authentication required`（`data.category: auth`）**，所以客户端必须先把 `authenticate` 走通。
- `--acp` 的分帧在帮助里写作 **ndJsonStream**；`--acp-transport` 可选 `stdio`（默认）或 `streamable-http`；`--serve` 是另一条 ACP over HTTP + SSE 的路（不带 `--acp` 时 ACP 不走 stdio）。

### 两个实现要点（都是踩过的坑）

1. **`session/prompt` 期间 Agent 会反向发请求**，Client 必须在独立线程里处理这些请求，不能和「等响应」串在同一条读循环上——`mock_agent.py` 第一版就是这么把自己堵死的（请求发出后读循环被占，响应永远读不到）。真 Agent 也一样：权限请求是在 prompt 未返回时进来的。
2. **路径比较要 `realpath`**：macOS 上 `/tmp` 是 `/private/tmp` 的软链，直接用 `abspath` 比前缀会把工作区内的文件判成「越界」。
