# Multica · 人机混编工作区

> 不是 Agent 框架，也不自带模型。驱动你机器上已装的 Claude Code、Codex、Cursor、`dsh` 等 CLI；issue 是工作真相，agent 像同事一样被指派、评论、提 blocker、交审查。
>
> 仓库：https://github.com/multica-ai/multica ｜ 文档：https://multica.ai/docs ｜ [VISION.md](https://github.com/multica-ai/multica/blob/main/VISION.md)  
> 许可证：Apache 2.0 **加上**托管服务、商业嵌入和品牌的额外条款。  
> 依据：仓库 README、[AGENTS.md](https://github.com/multica-ai/multica/blob/main/AGENTS.md)、官方 docs。

对照总判断见 [README](./README.md)。落地四段见 [sdlc.md](./sdlc.md)。它落地的是「工作系统」，不是「模型怎么推理」。

一句话：服务器像看板和调度器；daemon 像坐在你电脑旁边的同事。代码、CLI 登录态、本机目录默认不出那台执行机。

---

## 模式

核心是 **Issue + Squad（Leader 路由）**，不是 Swarm 群聊。

- 单 agent：issue 指派给某个 agent，它当正式 assignee。
- Squad：一个 leader agent + 若干成员（人或 agent）。指派给 squad **不会**全员同时开工；先叫醒 leader，由它决定下一步给谁。
- 并行：同一 issue 上，assignee 和被 `@` 的另一个 agent 可以各跑一条 run。同 agent 对同一 issue 的 queued/dispatched 去重。
- 技能：playbook，挂到多个 agent 上。

和 OpenAI Manager / Anthropic Orchestrator-Workers 同构：leader 管路由，不自动加并发。文档原话：Squads 解决「活给谁」，不把多个 agent 合成一个新 agent。

---

## 任务怎么下发

Agent **不会自己开工**。四种显式触发，路径相同，上下文重量不同：

| 入口 | 何时 | 上下文重量 |
|---|---|---|
| 指派 issue | assignee = agent/squad，且离开 backlog | 最重：读描述 + 全部评论，可改状态和字段 |
| 评论 `@` | 不改 assignee | 处理这一条请求 |
| Chat | 不挂 issue | 每条消息一条 run |
| Autopilot | cron / webhook / 手动 | 可建 issue 再跑，或 run-only（后者不自动重试） |

路径：issue 上下文 → 创建 **run** → 在线 runtime 认领 → 本机 spawn CLI → 进度写回 issue。  
Backlog 只是停车位，推到 Todo / In Progress 才入队。`/note` 只留言不唤醒。

Squad 时多一跳：指派 squad → 只给 leader 入队 → leader 发带精确 mention 的委派评论 → 被 `@` 的成员各自一条 run。Leader 停，不自己实现。成员回帖或阶段闸关闭后再叫醒 leader；有人显式 `@` 时 leader 让路。

产物靠 **issue 时间线 + execution log + Git PR**。run `completed` 只表示这一趟跑完，issue 是否完成看状态和人审。审查门默认进 `in_review`，不进 main。

---

## 授权与不确定

- 人签的是 issue / review，不是每个工具调用。Inbox 只在需要人拍板时打扰；agent 不用 Inbox。
- 卡住标 `agent_blocked`，在评论里要信息。
- 瞬时故障自动重试（常规最多 2 次，工具网络中断最多 3 次）；鉴权、额度、模型错误不自动重试。
- **默认不沙箱文件系统。** daemon 以 OS 用户权限跑，Claude/Codex 走 `bypassPermissions` / `danger-full-access`。这是无人值守开关，不是对话口令。隔离靠独立 Unix 用户、容器或 VM。
- 真正隔离的只有：每 run 独立 workdir、run 级 agent 状态、run 级 `MULTICA_TOKEN`（最长 24h，子进程默认继承）。agent 自定义环境盖不掉：`MULTICA_TOKEN`、`MULTICA_TASK_ID`、`MULTICA_AGENT_ID`、`MULTICA_WORKSPACE_ID`、`MULTICA_SERVER_URL`。

并发：daemon 默认最多 20 条 run，每个 agent 最多 6，取较小值。

---

## 四层部署

```
Web · Desktop · iOS · CLI · Slack/飞书
                 │
                 ▼
          Go 控制面 (Chi + WebSocket)
                 │
          PostgreSQL 17
                 │  任务经 WS / 轮询下发
                 ▼
          本机 Daemon  ──spawn──►  26 种 Agent CLI
```

Chi 接普通 API（建 issue、改指派）；WebSocket 是长连接（下发任务、心跳、页面实时更新）。可自托管（Docker / Helm）。

| 层 | 跑什么 | 栈 | 看见什么 |
|---|---|---|---|
| 接入面 | Web / Desktop / iOS / CLI / 频道 | Next.js 16、Electron、Expo、Go CLI | issue、评论、Inbox、run 进度 |
| 控制面 | 排队、鉴权、写回、心跳判定在线 | Go Chi + gorilla/websocket + sqlc | 工作区、agent 配置、run 记录、`custom_env` |
| 数据面 | 持久化与检索 | PostgreSQL 17（`pgcrypto` + `pg_trgm`） | issue 时间线、成员、技能包元数据 |
| 执行面 | 认领 run、spawn 本地 CLI | daemon × 一种 AI 工具 = 一个 runtime | 源码、密钥、HOME 下的 `gh` / `aws` / `kubectl` |

Runtime **不是**容器。一台装了 Claude 和 Codex、加入两个工作区的电脑，会注册 4 个 runtime。心跳 15s；异常退出后大约 3 分钟标离线。

`custom_env` 存在服务器、执行时下发，是「代码不出机」的例外。

### 代码仓怎么切

依赖方向：`views → core + ui`；core 与 ui 互不引用。

| 路径 | 职责 | 硬边界 |
|---|---|---|
| `apps/web` | Next.js 路由与 Web 专属 UI | 框架 API 留在这里 |
| `apps/desktop` | Electron；启动并托管本机 daemon | 导航走 desktop platform adapter |
| `apps/mobile` | 独立 Expo 客户端 | 不走 web/desktop 共享 store |
| `packages/views` | Web/Desktop 共享页面 | 禁 `next/*`、禁定义 store |
| `packages/core` | API client、Query、Zustand | 无 UI、无 `localStorage` |
| `packages/ui` | 无业务的 UI 原语 | 禁 `@multica/core` |
| `server/cmd/server` | Go API 进程 | Chi + WS |
| `server/cmd/multica` | 人和 agent 共用的 CLI | run 内用 `MULTICA_TOKEN` 署名 |
| `server/pkg/agent` | 各 CLI 协议适配与 spawn | 默认测试不得碰用户已装 CLI |

---

## 领域对象

Workspace 是容器。Issue 记一件活。Agent 是可复用配置，不是常驻进程。每次触发才产生一条 run，由 runtime 认领。

| 对象 | 角色 | 要点 |
|---|---|---|
| Workspace | 租户边界 | 人与 agent 同空间。角色 `owner` / `admin` / `member`。Agent 另有 Access，不跟角色走 |
| Issue | 工作真相 | 描述、讨论、状态、执行史。指派人可以是成员、agent 或 squad。`backlog` 只停车 |
| Agent | 同事身份 | 名字、instructions、模型、skills、Access、绑定的 runtime。被指派或 `@` 才会跑 |
| Squad | 路由，不加并发 | Leader（必须是 agent）+ 成员（人或 agent）。指派 squad 只叫醒 leader |
| Skill | 玩法包 | `SKILL.md`，可挂多个 agent。Instructions = 这个人是谁；skill = 这类活怎么做。更新从后续 run 生效 |
| Project | 一组 issue + 仓库/目录上下文 | issue 最多属一个 project；子 issue 状态互不影响；可按 stage 分批叫醒父 assignee |
| Run | 一次执行记录 | 一条触发对应一条 run。`completed` ≠ issue 完成 |
| Runtime | 机器 × 工具 | 一台电脑上的一种 CLI，按工作区注册。默认可私有 |
| Inbox | 人的通知 | 只在需要拍板时打扰 |

Issue 状态说「这件活有没有做完」；run 状态说「这一趟跑没跑完」。Server 一般不因 run 起停自动改 issue 状态——agent 自己用 CLI 改。例外：失败且无其它 run 时 `in_progress` 回滚到 `todo`；带 close intent 的 GitHub PR 合入后标 `done`。

| Issue | 含义 | Run | 含义 |
|---|---|---|---|
| `backlog` | 停车，不触发 | `queued` / `deferred` | 等 runtime 认领或定时 |
| `todo` | 范围清楚，等开工 | `dispatched` | 已认领，正在起 CLI |
| `in_progress` | 正在做 | `waiting_local_directory` | workdir 被别的 run 锁住 |
| `in_review` | 有结果等人审 | `running` | CLI 在跑 |
| `blocked` | 卡住，评论里要信息 | `completed` | 这一趟正常结束 |
| `done` / `cancelled` | 终态；`done` 通常人签 | `failed` / `cancelled` | 出错或被停 |

---

## 落到本目录的 SDLC

适合当「几十个仓的人机看板」：评审 / 拆解 / 实现 / 验收做成 issue 状态机，Squad leader 做路由，实现 agent 在本机 checkout 干活，人看 plan / diff / 测试 / 未决问题。

| SDLC 段 | 建议结构 | 落在 Multica 上 |
|---|---|---|
| 评审 | 单 agent + skills | 一个 agent 吃 issue；skill 放仓索引 / 禁区；人把状态从评审门推走 |
| 拆解 | 仍是一个 Lead | Lead agent 写子 issue / 阶段闸；契约 issue 只派一个 owner |
| 实现 | Squad leader 路由 | Leader 只路由；实现 agent 在本机 checkout；普通 PR 进 `in_review` |
| 验收 | Evaluator 对 `acceptance` | 另派验收 agent 或人审；`done` 默认留给人，不因 run `completed` 自动合主干 |

不替你做：服务→仓库→配置源索引、写域不重叠的任务规格、跨仓契约单一 owner、三级门控策略。这些做成 skills、issue 模板和 squad 规则，判断仍按 [README](./README.md) / [sdlc.md](./sdlc.md)。
