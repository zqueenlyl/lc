# Pi · 极简编码 Agent harness

> 一句话：**把编码 Agent 的内核收到最小（四个工具），剩下的靠容器化隔离和可扩展机制，而不是靠内置一整套权限系统。**
>
> 仓库：https://github.com/earendil-works/pi ｜ MIT ｜ 作者 Mario Zechner（badlogic，libGDX 作者）

Pi 是 [harness 专题](../harness/) 里「最小核」取向的代表：官方定位 `A minimal terminal coding harness`，只公开 4 个核心工具（`read` / `write` / `edit` / `bash`）。它是 TypeScript monorepo，主页还强调自己是「self extensible coding agent」——**可自我扩展的编码智能体**。

---

## 一、Monorepo 的六个包

| 包 | 干什么 |
|---|---|
| `pi-coding-agent` | 交互式编码智能体 CLI |
| `pi-agent-core` | 智能体运行时：工具调用 + 状态管理（agent loop） |
| `pi-ai` | 统一多提供商 LLM API：OpenAI / Anthropic / Google 等 |
| `pi-tui` | 终端 UI 库，支持差分渲染 |
| `chord` | 独立的应用组合运行时：服务、复制状态、RPC、插件 |
| `pi-telemetry` | 厂商中立的遥测契约、参考适配器、类型化 schema |

技术栈：TypeScript + Bun（编译可执行文件）+ Vitest（测试）+ Biome（lint/format）+ Husky（git hooks），发布到 npm。

---

## 二、设计取向：最小核，而非全家桶

Pi 站在 [harness 专题](../harness/) 那张对照表的另一端——Claude Code 把编码工具做全、DeepSeek 把能力外置成插件，Pi 则是**把内核收到四个工具**：

| 取向 | 代表 | 权衡 |
|---|---|---|
| 全家桶 | Claude Code | 开箱能干活，和厂商绑定深，安全面大 |
| 一切皆插件 | DeepSeek Harness | 默认几乎只有执行原语，能力装上去 |
| **最小核** | **Pi** | 核小 → 安全面小、审计面小；但编码能力要靠生态/自扩展补 |

「核小」的直接好处：**审计面小**。四个工具的副作用一目了然，剩下的是你自己的环境问题，而不是「哪条内置命令有洞」。

---

## 三、权限模型：默认不内置，靠外部隔离

Pi 最反直觉的设计——**默认没有内置权限系统**来限制文件系统 / 进程 / 网络 / 凭证访问，它以启动它的用户和进程的权限运行。官方明确建议：要隔离就容器化，给了三条路：

| 模式 | 做法 |
|---|---|
| **Gondolin extension** | 主机保留 `pi` 和提供商认证，把内置工具和 `!` 命令路由到本地 Linux 微虚拟机 |
| **Plain Docker** | 整个 `pi` 进程跑在本地容器里 |
| **OpenShell** | 在策略控制的沙箱里跑整个 `pi` 进程 |

这和 commerce-agents 的「代码强制门禁」是**两种哲学**：commerce-agents 把安全做进 executor，Pi 把安全交给运行环境。选型时要想清楚你要的是「细粒度、内建的人审/围栏」，还是「极简内核 + 强隔离沙箱」。

---

## 四、工程与供应链安全

Pi 的 npm 依赖管理相当严格，值得关注：

- 直接外部依赖固定到精确版本；`.npmrc` 设 `save-exact=true`、`min-release-age=2`
- `package-lock.json` 是依赖唯一事实来源；发布包带 `npm-shrinkwrap.json` 锁传递依赖
- CI 用 `npm ci --ignore-scripts`；定期 `npm audit` + 签名审计

对「要长期跑在开发者终端里的 Agent」来说，供应链是攻击面——这跟 [guardrails 专题](../../reliability/guardrails/) 里的「插件接口公开前，权限模型必须先存在」是同一层担忧。

---

## 五、和 harness 专题的呼应

Pi 在本知识库里已经作为六款 Harness 之一收录（见 [harness §四](../harness/#四、六款知名-harness设计取向，非排名)）。本页是它的**展开**：它的「最小核 + 自扩展 + 靠沙箱隔离」三件事，正是 harness 专题里「最小核 vs 全家桶」「开源的是哪一层」两条设计取向的实例。

它和 [commerce-agents](./commerce-agents.md) 形成鲜明对照：

| 维度 | Pi | commerce-agents |
|---|---|---|
| 领域 | 编码 Agent（终端） | 电商业务 Agent |
| 安全哲学 | 极简核 + 外部沙箱 | 代码强制门禁 + 围栏 + 人审 |
| 语言/形态 | TypeScript CLI | Python 库 + 多运行时 |
| 信任来源 | 运行环境隔离 | executor 内建的 gates |

---

## 六、落地建议

1. 想自托管、要审计、能接受「最小工具集 + 自己搭沙箱」→ Pi 是很好的骨架。
2. 想要开箱即用、细粒度内建安全 → 更接近 Claude Code 或 commerce-agents 的取向。
3. 「self extensible」意味着它能改自己的工具链，上生产前先确认扩展入口的权限边界。

---

## 七、延伸阅读

- 官网 / 文档：`pi.dev`（docs 在 `pi.dev/docs/latest`）
- 容器化细节：`packages/coding-agent/docs/containerization.md`
- 相邻专题：[harness](../harness/)、[guardrails](../../reliability/guardrails/)、[loop-engineering](../loop-engineering.md)
- 三项目横向对比见本目录 [README](./README.md)
