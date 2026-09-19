# Multica · 人机混编工作区

> 不是 Agent 框架，也不自带模型。驱动你机器上已装的 Claude Code、Codex、Cursor、`dsh` 等 CLI；issue 是工作真相，agent 像同事一样被指派、评论、提 blocker、交审查。
>
> 仓库：https://github.com/multica-ai/multica ｜ 文档：https://multica.ai/docs ｜ [VISION.md](https://github.com/multica-ai/multica/blob/main/VISION.md)  
> 许可证：Apache 2.0 **加上**托管服务、商业嵌入和品牌的额外条款。

对照总判断见 [README](./README.md)。落地四段见 [sdlc.md](./sdlc.md)。它落地的是「工作系统」，不是「模型怎么推理」。

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

Agent **不会自己开工**。四种显式触发：

1. 指派 issue（最重：读描述 + 全部评论，可改状态和字段）
2. 评论里 `@` agent 或 squad
3. Chat（不挂 issue）
4. Autopilot（cron / 外部事件）

路径：issue 上下文 → 创建 **run** → 在线 runtime 认领 → 本机 spawn CLI → 进度写回 issue。  
Backlog 只是停车位，推到 Todo / In Progress 才入队。

产物靠 **issue 时间线 + execution log + Git PR**。run `completed` 只表示这一趟跑完，issue 是否完成看状态和人审。审查门默认进 review，不进 main。

---

## 授权与不确定

- 人签的是 issue / review，不是每个工具调用。Inbox 只在需要人拍板时打扰。
- 卡住标 `agent_blocked`，在评论里要信息。
- 瞬时故障自动重试；鉴权、额度、模型错误不自动重试。
- **默认不沙箱文件系统。** daemon 以 OS 用户权限跑，Claude/Codex 走 `bypassPermissions` / `danger-full-access`。隔离靠独立 Unix 用户、容器或 VM。
- 真正隔离的只有：每 run 独立 workdir、run 级 agent 状态、run 级 `MULTICA_TOKEN`。

架构：Next.js + Go + Postgres。代码和凭证不出那台装 daemon 的机器。可自托管（Docker / Helm）。

---

## 落到本目录的 SDLC

适合当「几十个仓的人机看板」：评审 / 拆解 / 实现 / 验收做成 issue 状态机，Squad leader 做路由，实现 agent 在本机 checkout 干活，人看 plan / diff / 测试 / 未决问题。

不替你做：服务→仓库→配置源索引、写域不重叠的任务规格、跨仓契约单一 owner、三级门控策略。这些做成 Skills、issue 模板和 Squad 规则，判断仍按 [README](./README.md)。
