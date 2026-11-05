# AG-UI · Agent–User Interaction Protocol

> 应用和 Agent 之间的开放事件流。一句话：**MCP 接手，A2A 接同事，ACP 接编辑器，AG-UI 接应用。**

由 CopilotKit 提出，规范已到 **1.0**。对端不限定浏览器：网页、终端、手机、Slack / Teams 都可以当 Client。本仓库 [trpc-agent-go](../case-studies/trpc-agent-go.md) 的 Gateway 也暴露这条缝。

同名辨析：A2UI 是「Agent 交一份 UI 组件树」的生成式界面规格。AG-UI 是「应用和 Agent 怎么把一轮对话流过去」的协议。两者可以叠在一起用。

---

## 一、协议只记四件事

**一轮 = 一次请求，回来一条有序事件流。** 应用发出唯一的上行消息 `RunAgentInput`。Agent 用事件回答，从 `RUN_STARTED` 到 `RUN_FINISHED` 或 `RUN_ERROR`。这一轮进行中，应用不能再插话。要继续，就用同一个 `threadId` 再开一轮。

**人能看见的东西都在这条流里。** 文字、工具调用、思考、共享状态、进度，没有旁路。把每次 input 和它的事件留档，就能重放当时 UI 知道什么。

**生产者必做的只有生命周期。** 其余事件家族是有话才说。消费者则必须收下全部八个家族；用不上的也是合法事件。

**传输只是装帧。** 默认是 `POST` JSON，响应 `text/event-stream`。另有 HTTP + protobuf 帧。同一套事件，换传输语义不变。

```
应用（网页 / 终端 / IM）
  │  RunAgentInput：threadId、runId、messages、tools、state
  ▼
AG-UI Client（SDK：校验、中间件）
  │  POST
  ▼
Agent 端点 + 框架桥（LangGraph / ADK / Mastra / 自研循环）
  │  RUN_STARTED → 文字 / 工具 / 状态 → RUN_FINISHED
  ▼
应用渲染、执行自己声明的工具、记下 state
```

协议里没有框架概念。桥负责把某家循环翻译成事件，所以一个 Client 可以面对多家 Agent。

| 角色 | 谁 | 干什么 |
|---|---|---|
| **Application** | 你的产品 | 画流、执行自己声明的前端工具、保管共享 state、决定哪一步要人点头 |
| **Client** | SDK | 发出 `RunAgentInput`，校验回来的事件，再交给应用 |
| **Agent 端点** | HTTP 服务 | 说某种传输 |
| **Bridge** | 适配层 | 把框架自己的事件译成 AG-UI 事件 |

---

## 二、`RunAgentInput`

应用 → Agent 的唯一消息。Agent 把它当成这次能看见的全部上下文。

| 字段 | 要点 |
|---|---|
| `threadId` / `runId` | 必填。线程是一段对话，run 是其中一轮 |
| `messages` | 必填。到目前为止的完整历史。协议没有另一条通道补以前的话 |
| `tools` | 应用自己的工具：名字、说明、参数 schema。由应用执行，不是 Agent 执行 |
| `context` | 要注入给模型看的说明–值对 |
| `state` | 这一轮开始时双方已经对齐的共享状态。缺省当 `{}` |
| `resume` | 回答上一轮打断。每一条打断都要有回应，漏掉不算放弃 |
| `forwardedProps` | 原样转交给 Agent，协议不解释 |
| `protocolVersion` | 本版实现应带上。`RUN_STARTED` 里 Agent 回自己的版本 |

认不出的字段剥掉后继续跑。已知字段格式错了，则在流开始前用 HTTP 错误拒绝，这一轮没有开始。

---

## 三、八个事件家族

| 家族 | 事件 | 谁用 |
|---|---|---|
| 生命周期 | `RUN_STARTED` / `RUN_FINISHED` / `RUN_ERROR`，`STEP_STARTED` / `STEP_FINISHED` | Client |
| 文字 | `TEXT_MESSAGE_START` / `CONTENT` / `END` | UI |
| 工具 | `TOOL_CALL_START` / `ARGS` / `END` / `RESULT`（或压缩的 `CHUNK`） | 应用 |
| 思考 | `REASONING_*` | UI。给用户看的是摘要，不是原始思维链 |
| 状态 | `STATE_SNAPSHOT` / `STATE_DELTA`，`MESSAGES_SNAPSHOT` | 应用的 store。快照整份替换，增量是 JSON Patch |
| 活动 | `ACTIVITY_SNAPSHOT` / `ACTIVITY_DELTA` | UI 上的进度块，留在消息序列里 |
| 子 Agent | `SUBAGENT_STARTED` / `FINISHED` / `ERROR` | Client。标明这段输出是谁产生的 |
| 透传 | `RAW` / `CUSTOM` | 应用自选。出口，不能变成第二套协议 |

`RUN_FINISHED` 的 `outcome`：

| outcome | 意思 |
|---|---|
| 缺省 / success | 这一轮做完了。若留下未回答的前端工具，写在 `pendingToolCallIds` |
| interrupt | 停下来问人。下一次 input 用 `resume` 逐条回答 |
| cancelled | 人叫停或触到上限。已经吐出的内容保留，不要当成成功，也不要当成失败 |

流必须以 `RUN_STARTED` 或 `RUN_ERROR` 开头。`RUN_ERROR` 是 Agent 自己报告失败，HTTP 状态已经发出去了，不能靠 `200` 判断成功。连接断开又没有收尾事件，是截断，不是取消。消费者不要自己补一个 `RUN_FINISHED`。

---

## 四、传输：HTTP + SSE

```
POST /agent
Content-Type: application/json
Accept: text/event-stream

{"threadId":"thr-1","runId":"run-1","messages":[…]}

HTTP/1.1 200
Content-Type: text/event-stream

data: {"type":"RUN_STARTED","threadId":"thr-1","runId":"run-1"}

data: {"type":"TEXT_MESSAGE_START","messageId":"msg-1","role":"assistant"}

data: {"type":"TEXT_MESSAGE_CONTENT","messageId":"msg-1","delta":"好。"}

data: {"type":"TEXT_MESSAGE_END","messageId":"msg-1"}

data: {"type":"RUN_FINISHED","threadId":"thr-1","runId":"run-1"}
```

每条 SSE 的 `data` 正好是一个 JSON 事件。消费者忽略 `event:`、`id:`、`retry:`，并容忍 `: keep-alive` 注释。这条绑定不用 `Last-Event-ID`。断了就不能从中间接上，续跑是新的 `runId`，input 里带上应用已经留下的消息和 state。

流打开之前的拒绝（JSON 坏了、校验失败、鉴权失败）是 HTTP 错误，没有事件流。

---

## 五、两种「问人」，不要混

协议在一轮之中没有从应用回到 Agent 的通道。所以两件事都要等下一轮。

| | 前端工具 | 打断 interrupt |
|---|---|---|
| Agent 怎么停 | 发出 `TOOL_CALL_*`，自己不回 `TOOL_CALL_RESULT`，以 success 结束，并列出 `pendingToolCallIds` | `RUN_FINISHED` 的 outcome 是 interrupt，带上要人填的 `id`、说明、可选的 `responseSchema` |
| 应用怎么答 | 下一次 `messages` 里放一条 tool 消息，用 `toolCallId` 对上。拒绝也要回答 | 下一次 input 的 `resume`，按 `interruptId` 逐条回答或明确放弃 |
| 典型 | 前端自己画图、跳转、查一下本页状态 | 批准转账、补一个凭证、在几个选项里挑一个 |

Agent 自己执行的工具在同一轮里用 `TOOL_CALL_RESULT` 回答。参数在 `TOOL_CALL_END` 之前只是前缀，不要提前执行。参数文本当不可信输入。有副作用的调用先问人。

```
应用                         Agent
 |-- RunAgentInput {tools:[confirm]} ->|
 |<--------- TOOL_CALL_* confirm ------|
 |<--------- RUN_FINISHED success -----|   pendingToolCallIds: [call-1]
 |  （人点头，应用执行）
 |-- 下一轮 messages 含 tool 结果 ---->|
 |<--------- RUN_STARTED … FINISHED ---|
```

---

## 六、和 ACP

两条都是「屏幕接缝」，形状不同。

| | [ACP](../acp/) | AG-UI |
|---|---|---|
| 对端 | 编辑器。要文件、终端、diff | 应用。要聊天、共享状态、前端工具 |
| 连接 | JSON-RPC。一条 stdio 上多个 session，一轮 prompt 挂着不返回 | 一次 POST，一条事件流，然后连接结束 |
| 运行中回程 | Agent 可以立刻调 `fs/*`、`terminal/*`、`request_permission` | 没有。答案放进下一轮 `RunAgentInput` |
| 必做 | `initialize`、`session/new`、`session/prompt`、`session/update` | 生产者只保证 `RUN_STARTED` / `RUN_FINISHED` |

编辑器里改代码，用 ACP。产品页面里嵌一个助手，用 AG-UI。

---

## 七、与相邻技术

| 技术 | 关系 |
|---|---|
| [MCP](../mcp/) | MCP 是 Agent → 工具。AG-UI 的 `tools` 是应用交给 Agent 调用、由应用自己执行的那一批 |
| [A2A](../a2a/) | A2A 的对端是另一个 Agent。AG-UI 的对端是人用的界面 |
| [ACP](../acp/) | 见上一节。同是屏幕，ACP 长在编辑器，AG-UI 长在应用 |
| A2UI | 生成式 UI 组件。AG-UI 负责把这一轮流过去，A2UI 负责流里的界面长什么样 |
| [Harness](../harness/) | 循环、权限、工具仍在 Harness。AG-UI 只规定循环怎么投影到界面 |

---

## 八、延伸阅读

- 规范：[Overview](https://docs.ag-ui.com/introduction)、[1.0 架构](https://docs.ag-ui.com/spec/1.0/architecture)、[事件](https://docs.ag-ui.com/spec/1.0/events)、[HTTP + SSE](https://docs.ag-ui.com/spec/1.0/basic/transports/http-sse)
- 对照：[mcp](../mcp/)、[a2a](../a2a/)、[acp](../acp/)
- 本仓库实现侧：[trpc-agent-go](../case-studies/trpc-agent-go.md)
