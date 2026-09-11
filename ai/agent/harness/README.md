# Agent Harness · 编码智能体外壳

> Harness 是套在模型外面的 **运行时**：组上下文、暴露工具、跑命令、验证结果、决定要不要再转一圈。一句话：**模型是发动机，Harness 是底盘和方向盘。**

Claude Code / Codex / Cursor Agent / DeepSeek Harness 比的往往不是「谁家模型分数高」，而是这层循环怎么设计。和 [循环工程](../loop-engineering.md) 同一件事：你写的是循环，不是单次提示。

配套 MVP：[mvp.py](./mvp.py)（`read` / `write` / `edit` / `bash` 四件套 + 插件槽，不调外部 API）。

---

## 一、技术讲解

没有 Harness 的模型只会聊天。有 Harness 之后变成：

```
目标 → 组上下文 → 选工具/动作 → 在真实环境执行 → 看输出 → 验证 → 再转或停
```

四件东西常被混叫「tool」，抽象粒度并不一样：

| 抽象 | 是什么 | 例子 |
|---|---|---|
| **Tool** | 模型可点的一个 schema 函数 | `Read`、`Bash`、`WebSearch` |
| **Action** | 一次环境副作用，可能由 Tool 组合出来 | 改文件、跑测试、发消息 |
| **Subagent** | 带着缩小工具集去跑一段子循环 | `explore` / `plan` / `coder` |
| **Runtime Primitive** | 运行时自己提供的能力，不一定出现在 tool 列表里 | 权限沙箱、ACP、插件加载、会话恢复 |

所以 **Tool 数量 ≠ Harness 强弱**。Pi 只公开 4 个核心工具，Claude Code 工具很全，DeepSeek 走「一切皆插件」——比的是取向，不是个数。

和相邻层的分界：

| 层 | 负责 | 不是 Harness |
|---|---|---|
| 模型 | 推理、写补丁、选工具 | GPT / Claude / Kimi |
| [MCP](../mcp/) | 工具怎么插进来 | 标准插头 |
| [Skills](../agent-skills/) | 这类任务按什么 SOP 做 | 菜谱 |
| **Harness** | 循环、权限、默认工具、子 Agent、产品形态 | 本专题 |
| IDE 产品 | 编辑器 UX、补全、多模型切换 | Cursor / Copilot 编辑器面 |

Cursor 是 IDE 产品，里面可以跑某家 Harness；Claude Code 本身就是 Harness。选产品时先问「我要编辑器还是要终端循环」。

---

## 二、功能作用

- **把模型接到真实仓库**：读文件、改文件、跑测试，而不是只吐代码块。
- **收敛循环**：失败有日志、有步数上限、有「测过了才算完」。
- **权限边界**：哪些目录可写、能否联网、要不要人点确认。
- **可扩展**：插件 / MCP / 子 Agent，而不是把所有能力焊死在二进制里。
- **可迁移**：开源 Harness 换模型；闭源 Harness 换不了外壳，只能换里面的模型档。

---

## 三、应用场景

| 场景 | Harness 侧重点 |
|---|---|
| 大重构 / 修测试 | 完整文件工具 + 长循环 + 子 Agent（Claude Code / Codex 取向） |
| 自托管、审计、改内核 | 开源 + 最小工具集或插件化（Pi / DeepSeek） |
| 从 IM / 聊天里派活 | 网关 + 消息工具（OpenClaw） |
| IDE 里改当前文件 | 产品把 Harness 嵌进编辑器（ACP、VS Code 扩展） |
| 「一切皆插件」实验 | 默认工具极瘦，能力全走插件注册（DeepSeek 定位） |

不适合：把 Harness 当聊天窗口用（浪费循环）；也别用「工具个数」给六家排座次。

---

## 四、六款知名 Harness（设计取向，非排名）

快照来自公开定位与默认执行原语对照（2026）。形态和许可证会变，**看取向**。

| 名称 / 厂商 | 形态 | 开放程度 | 官方定位 | 默认工具集 / 执行原语 |
|---|---|---|---|---|
| **DeepSeek Harness**（Developer Preview） | Web + Terminal（CLI）运行时 | 开源，MIT | Everything is a plugin / 一切皆插件 | 无官方统一工具数；最小预设 `bash`、`str_replace_editor`，其它预设可配出完整编码能力 |
| **Claude Code**（Anthropic） | Terminal（CLI）+ IDE + Web | 闭源商业 | Work with Claude directly in your codebase | 完整编码工具：`Bash`、`Read`、`Write`、`Edit`、`Glob`、`Grep`、`WebFetch`、`WebSearch`、`Agent` 等 |
| **Codex**（OpenAI） | Terminal（CLI）+ Cloud / ChatGPT 入口 | CLI 开源，Apache-2.0 | Inspect, edit, and run code from your terminal | 核心执行：`Shell`、`patch-edit`、`Web Search` 等，并提供规划 / 运行时原语 |
| **Kimi Code**（Moonshot） | Terminal（CLI），经 ACP 进 IDE | 开源，MIT | The Starting Point for Next-Gen Agents | 无官方统一工具数；覆盖文件读写、`Shell`、搜索与 Web；提供 `coder` / `explore` / `plan` 等 Agent / 子 Agent |
| **Pi**（Mario Zechner） | Terminal（CLI） | 开源 | A minimal terminal coding harness | 明确 4 个核心工具：`read`、`write`、`edit`、`bash` |
| **OpenClaw**（社区） | 本地 IM 网关 + Terminal（CLI） | 开源 | Your assistant, on your devices, in your chats | 约 12 类内置：`exec`、`read`、`write`、`edit`、`web_search`、`browser`、`message` 等 |

对照时记住：DeepSeek 把能力外置成插件；Pi 把内核收到四件套；Claude Code 把编码工具做全并绑自家模型；Codex 的 CLI 开源但云入口是产品；Kimi 强调子 Agent 角色；OpenClaw 强调「人在聊天软件里指挥本地助手」。

和 [landscape §4.2](../../landscape.md#42-编程-agent--ide2026-主战场) 的关系：那里列的是用户打开的**产品**（含 Cursor、Copilot）；这里列的是循环怎么转的**外壳**。一个产品里可以嵌一个 Harness。

---

## 五、设计取向怎么读

1. **最小核 vs 全家桶**：Pi / DeepSeek 最小预设 vs Claude Code 默认工具很全。核小则安全面小、插件生态要自己长；核大则开箱能干活、和厂商绑定深。
2. **插件 vs 内置**：一切皆插件 = 默认几乎只有执行原语，编码能力是装上去的。
3. **单循环 vs 子 Agent**：Kimi 的 `explore` / `plan` / `coder` 是把舰队循环做成一等公民，见 [循环工程](../loop-engineering.md)。
4. **人从哪发指令**：纯 CLI、IDE（ACP）、Web、IM 网关，决定权限模型和上下文从哪来。
5. **开源的是哪一层**：Codex 开的是 CLI；Claude Code 外壳不开；DeepSeek / Kimi / Pi / OpenClaw 外壳可改。模型往往仍是 API。

---

## 六、与相邻技术

| 技术 | 关系 |
|---|---|
| [循环工程](../loop-engineering.md) | Harness 是循环的工业实现 |
| [MCP](../mcp/) | 很多 Harness 用 MCP 扩工具；有的用私有 tool schema |
| [Agent Skills](../agent-skills/) | 菜谱；Harness 决定何时加载、能否跑脚本 |
| [Computer Use](../computer-use/) | 无 API 时用键鼠；有仓库时优先文件工具 + `bash` |
| [Guardrails](../../reliability/guardrails/) | 命令白名单、目录沙箱、联网开关 |
| [Eval](../../reliability/eval/) | SWE-bench / Terminal-Bench 测的是「模型 + Harness」，不是裸模型 |

公开榜上同一模型换 Harness，分数可以差一截。看 [Artificial Analysis Coding Agents](https://artificialanalysis.ai/?coding-agents=execution-time) 时，比的是整条链，不是裸模型的学校考试。为什么难评，见 [Eval](../../reliability/eval/)。

---

## 七、落地建议

1. 先定 **形态**：只在终端、要进 IDE、还是要从飞书/Slack 派活。
2. 默认工具从 **读 / 改 / 跑** 三件套长起，确认沙箱后再加浏览器和消息。
3. 验证步骤写进循环（测试命令、禁止「模型说修好了」），不要只靠生成质量。
4. 需要换模型、要审计循环 → 偏开源 Harness；要开箱体验、接受绑定 → 闭源产品。
5. 插件接口一旦公开，权限模型必须先于插件市场存在。

---

## 八、延伸阅读

- 本仓库：[loop-engineering.md](../loop-engineering.md)、[mcp](../mcp/)、[agent-skills](../agent-skills/)
- 评测：[SWE-bench](https://www.swebench.com/)、[Terminal-Bench](https://www.tbench.ai/)、AA Coding Agents
- 产品文档：Claude Code、Codex CLI、各开源仓库 README（以当时上游为准）

---

## 九、本目录 MVP

`mvp.py` 模拟 Pi 式四件套（`read` / `write` / `edit` / `bash`），外加 DeepSeek 式插件槽（再注册一个 `run_tests`）。规则策略当「模型」：读文件、改掉错误常量、跑测试直到绿。展示 Harness 循环，不调用真实 LLM。
