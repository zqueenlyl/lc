# mini-swe-agent · 把编码 Agent 压到 100 行

> 一句话：**除了 bash 之外没有任何工具，历史完全线性，每个动作都是一次独立的 `subprocess.run`——用这三个「不做」换掉整套 Agent 脚手架，SWE-bench Verified 仍有 >74%。**
>
> 仓库：https://github.com/SWE-agent/mini-swe-agent ｜ MIT ｜ Princeton & Stanford（SWE-bench / SWE-agent 原班人马，Kilian Lieret + Carlos E. Jimenez）
> 快照：**v2.4.6**（`src/minisweagent/__init__.py`，main 分支 2026-09-03）

它是 [harness 专题](../harness/) 里那条「**最小核 vs 全家桶**」光谱的极端端点：Pi 是「收到四个工具」，mini-swe-agent 是「**只留一个工具，而且不用模型的 tool-calling 接口**」。它更重要的身份是 **SWE-bench 官方的 Bash Only 榜指定外壳**——也就是说，你在 [eval](../../reliability/eval/) 里看到的很多模型分数，就是跑在这 100 行上的。

---

## 一、它到底在回答什么问题

README 的原话是：「**如果我们的 Agent 简单 100 倍，却依然几乎一样好用，会怎样？**」

2024 年的 SWE-agent 强调了大量专用工具与 Agent-Computer Interface；一年后模型变强，作者的结论是：**很多脚手架不再必要**。于是 mini 做了三个刻意的减法：

| 减法 | 换了什么 |
|---|---|
| **只有 bash 一个工具** | 不需要模型支持 tool-calling；沙箱里**一个包都不用装** |
| **历史完全线性** | 每一步只是往 messages 里 append；**trajectory == 喂给模型的 messages**，调试与微调都变简单 |
| **动作 = 一次 `subprocess.run`** | 没有常驻 shell 会话；换成 `docker exec` / `modal` 只需替换一个函数，横向扩容零成本 |

第三点是作者自己最强调的一条（docs `faq.md` 里单开一节 "Why is not needing a running shell session such a big deal?"）：

1. 常驻 shell 里「命令什么时候结束」没有可靠判据（试过看 PID、看提示符回到行首，都 flaky）；
2. 模型一条坏命令能把整个 shell 会话打死，然后怎么办？
3. 中断会话里正在跑的命令会污染 shell 自身，后续所有输出都不可信。

代价也直白：**不能 `cd`、不能 `export`**，每次动作都在新子 shell 里。作者的回答是「你不需要」——每条命令前自己加 `cd /path && ...` 或 `MY_ENV_VAR=X`。

---

## 二、结构：三个 Protocol + 三摞可换实现

`src/minisweagent/__init__.py` 只干一件事：定义三个 Protocol，靠 duck typing 工作（想做静态类型检查时才需要看它们）。

```
        Model（怎么问、怎么解析出动作）
           ↑
Agent ────┤                                  → 三个都能单独换
           ↓
        Environment（动作在哪执行、返回什么）
```

| 目录 | 内容 | 可换的实现 |
|---|---|---|
| `agents/` | `default.py`（DefaultAgent，主循环）· `interactive.py`（加人在环） | 继承 `AgentConfig` / `DefaultAgent` 即可 |
| `models/` | `litellm_model.py`（默认）、`openrouter_*`、`portkey_*`、`requesty_*`；`*_textbased_*` / `*_response_*` 变体 | litellm 覆盖的几乎全部模型 |
| `environments/` | `local.py`（`subprocess.run`）· `docker.py` · `singularity.py`（apptainer）· `extra/bubblewrap.py` · `extra/swerex_docker.py` · `extra/swerex_modal.py` · `extra/contree.py` | 本地 / docker / podman / singularity / bubblewrap / Modal |
| `run/` | `mini.py`（CLI）· `hello_world.py`（最小 Python 绑定）· `benchmarks/swebench.py`、`programbench.py` · `utilities/inspector.py`（轨迹浏览器） | — |
| `config/` | YAML + Jinja2 模板：`default.yaml` / `mini.yaml` / `mini_textbased.yaml` / `benchmarks/*.yaml` | `-c` 递归合并 |

最小可用形态只有四行（`run/hello_world.py` 的骨架）：

```python
agent = DefaultAgent(LitellmModel(model_name=...), LocalEnvironment())
agent.run("Write a sudoku game")
```

---

## 三、主循环：读懂这 100 行就读懂了 Agent

`agents/default.py` 的核心是一个 `while True`：

```python
while True:
    try:
        self.step()                       # query() → execute_actions()
        self.n_consecutive_format_errors = 0
    except FormatError as e:              # 解析不出动作 → 把错误当 observation 喂回去
        ...
    except InterruptAgentFlow as e:       # Submitted / LimitsExceeded / UserInterruption
        self.add_messages(*e.messages)
    except Exception as e:                # 真异常 → 记一条 exit 消息后抛出
        ...
    finally:
        self.save(self.config.output_path)   # 每一步都落盘轨迹
    if self.messages[-1].get("role") == "exit":
        break
```

几个值得抄的设计：

- **终止条件写在环境里，不写在 prompt 里**：`LocalEnvironment._check_finished()` 检测到输出首行是 `echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT` 且 `returncode == 0`，抛 `Submitted`，后续行作为 submission。**「完成」是一次真实的命令执行，不是模型自我声明。**
- **四类上限全在 `query()` 入口检查**：`step_limit` / `cost_limit`（默认 `$3`）/ `wall_time_limit_seconds` / `max_consecutive_format_errors`（默认 3）——对应本库 [agent README §六](../README.md#六、常见死法比模型笨更常见) 里的「空转」与「账单爆炸」。
- **异常即消息**：`exceptions.py` 里 `Submitted` / `LimitsExceeded` / `TimeExceeded` / `UserInterruption` / `FormatError` 全部继承 `InterruptAgentFlow`，构造时自带要写进历史的 messages。**「失败」也被序列化进 trajectory**，而不是只在日志里。
- **每一步都 `save()`**：`finally` 里落盘，进程被 kill 也留得下轨迹。

---

## 四、动作怎么从模型输出里出来

v2 提供两条解析路径，由 config 选择：

| 配置 | 解析方式 | 文件 |
|---|---|---|
| `config/default.yaml` | 纯文本：从三反引号块里抠命令（围栏标记写作 `mswea_bash_command`） | `models/utils/actions_text.py` |
| `config/mini.yaml` | 真正的 tool call：`bash(command=...)` | `models/utils/actions_toolcall.py` |
| `config/mini_textbased.yaml` | 文本模式（给不支持 tool-calling 的模型用） | — |

**推荐阅读的是 `config/default.yaml` 里的 `format_error_template`**：当模型输出格式错了，它不报错重试，而是把「你上一轮因为 `finish_reason=length` 被截断了 / 找到 N 个动作但要求恰好 1 个」这段**诊断信息当成 observation 喂回去**。这是本库 [reliability/structured-output](../../reliability/structured-output/) 里「把失败转成可行动观察」的现实样本。

观察侧同样有一处工程细节：**输出超过 10000 字符就截断成 head 5000 + tail 5000，并明确告诉模型「省略了多少字符、请换个输出更少的命令」**——不是悄悄截断，是把截断这件事本身告诉模型（见 `observation_template`）。

---

## 五、环境层：换沙箱 = 换一个 `execute()`

`Environment` Protocol 只有三个方法（`execute` / `get_template_vars` / `serialize`），所以换执行后端几乎没有成本：

| 实现 | 机制 | 备注 |
|---|---|---|
| `local.py` | `subprocess.run(shell=True)` | 默认 `timeout=30`；`start_new_session=True` + 超时 `os.killpg`，**杀整个进程组，不留孤儿** |
| `docker.py` | `docker run -d ... sleep 2h` 起常驻容器，之后每条命令 `docker exec` | `container_timeout=2h`、`run_args=["--rm"]`、`interpreter=["bash","-lc"]`、`__del__` 里异步清理 |
| `singularity.py` | apptainer | HPC 场景 |
| `extra/bubblewrap.py` | bwrap 命名空间隔离 | 无 root / 无 daemon |
| `extra/swerex_docker.py` / `swerex_modal.py` | 走 [SWE-ReX](https://github.com/swe-agent/swe-rex) 远程执行 | 评测大规模并发用 |

把「**动作无状态**」和这张表合起来看，mini 的沙箱哲学就清楚了：**它不内建任何权限系统**（和 [Pi](./pi.md) 一样），但它把「一次动作 = 一次独立调用」这件事做到极致，于是**隔离强度完全由 Environment 决定**——本地跑就是裸机风险，换成 docker 就是容器级，换成 Modal 就是远端沙箱。安全边界不在 Agent 里，在 `environment_class` 这一个配置项上。

⚠️ 一个容易忽略的点：`LocalEnvironment.get_template_vars()` 会把 `os.environ` **整体并入模板变量**，供 Jinja2 模板渲染。默认模板只用了 `{{system}} {{release}} {{version}} {{machine}}`（`platform.uname()`），但**自定义模板若引用了环境变量名，就等于把宿主环境变量带进了 prompt**。改模板时留意，别让密钥有可乘之机。

---

## 六、人在环：human / confirm / yolo 三档

`agents/interactive.py` 只继承了 `DefaultAgent` 并覆写 `query()` / `step()` / `execute_actions()`，就得到了一套人机协同：

| 模式 | 行为 | 斜杠命令 |
|---|---|---|
| `confirm`（默认） | 模型的每条命令先问人；命中 `whitelist_actions` 正则的白名命令直接放行 | `/y` 切 yolo |
| `yolo` | 不确认直接执行（`-y` / `--yolo`，CI 里用） | `/c` 切回确认 |
| `human` | 人直接下命令，模型看着 | `/u` |

配套细节：

- 拒绝命令不是「跳过」，而是**把人的拒绝理由作为一条 user 消息写进历史**（`UserRejection`），模型下一轮能看到为什么被拒。
- agent 想结束时若 `confirm_exit=True`，人可以直接追加新任务（`UserNewTask`）——**一次运行可以连续接多个任务**。
- `LimitsExceeded` 时，**有终端就现场问新的 step / cost 上限**；检测到 stdin 不是 tty（CI / 沙箱）就直接干净退出并保存轨迹（代码里对 `EOFError` 崩溃做了显式防护）。

这比「有 / 没有人审」二选一精细得多，可以直接对照 [guardrails 专题](../../reliability/guardrails/) 的 L1/L2 分级。

---

## 七、配置即一切

`run/mini.py` 的 `main()` 干的事只有：把 `-c` 给的多个 spec 与命令行参数 **递归合并**成一个 config dict，再交给 `get_model` / `get_environment` / `get_agent`。

```bash
mini -c mini.yaml -c model.model_kwargs.temperature=0.5    # YAML + 点号路径覆盖
mini -c swebench.yaml agent.mode=yolo                       # 换基准配置并关确认
```

⚠️ 官方特意在 help 里标红：**一旦指定 `-c`，默认 config 就不再加载**，必须显式写回 `-c mini.yaml`。

模板用 Jinja2 且 `undefined=StrictUndefined`，**引用不存在的变量直接报错而不是静默填空**——这是 prompt 模板该有的默认行为。

---

## 八、轨迹与评测（这才是它的主场）

一次运行的产物是一个 JSON（`trajectory_format: "mini-swe-agent-1.1"`），结构扁平：

```json
{
  "info": {"model_stats": {"instance_cost": ..., "api_calls": ...},
           "config": {"agent": {...}, "agent_type": "...", "environment": {...}},
           "mini_version": "2.4.6", "exit_status": "Submitted", "submission": "..."},
  "messages": [ ... 完整的线性历史 ... ]
}
```

`info.config` 把**当次运行的全部配置**原样存进去，`exit_status` 区分 `Submitted` / `LimitsExceeded` / `TimeExceeded` / `RepeatedFormatError`——**「为什么停」和「做成了什么」都是结构化字段**，可以直接拿来做错误分析。这正是本库 [eval](../../reliability/eval/) 里说的「Agent 评测是上机，不是考试」所需的最小数据契约。

评测侧：`run/benchmarks/swebench.py` 做批量并发，`config/benchmarks/swebench.yaml` 是一份很好的**基准配置范本**：

| 项 | 值 | 含义 |
|---|---|---|
| `step_limit` | 250 | 上机题的步数上限 |
| `cost_limit` | 3 | 单题 $3 封顶 |
| `cwd` | `/testbed` | 固定工作目录 |
| `environment_class` | `docker` | 每题一个容器 |
| submission | `echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT && cat patch.txt` | **交的是 git patch，不是「我觉得修好了」** |

另外 `mini-extra inspector` 提供轨迹浏览器，`run/benchmarks/programbench.py` 对应更新的 ProgramBench（从零写软件产物，而非修仓）。

---

## 九、和本库其它案例的对照

四个案例正好是四种信任来源：

| 维度 | mini-swe-agent | [Pi](./pi.md) | [commerce-agents](./commerce-agents.md) | [trpc-agent-go](./trpc-agent-go.md) |
|---|---|---|---|---|
| 领域 | 编码 / 评测基线 | 编码（终端） | 电商业务 | 通用平台 |
| 工具数 | **1（bash）** | 4 | 业务工具集 | 框架全套 |
| 安全边界 | **换 Environment = 换隔离** | 极小核 + 外部沙箱 | executor 内建门禁 / 围栏 / 人审 | 框架内建可观测 + 评估 |
| 历史形态 | **严格线性** | 树状 JSONL（可分支） | 会话 + 溯源 | Session + Memory |
| 语言 | Python（约 100 行核） | TypeScript | Python | Go |

两处最值得记的对照：

- **mini vs Pi**：都「不内建权限系统、靠环境隔离」，但**上下文策略相反**——Pi 用树状会话 + 压缩摘要支持长程分支，mini 坚持线性不压缩，换来「轨迹 == prompt」的可复现性。做**评测 / 微调数据**选 mini 的形态，做**长时程人机协作**选 Pi 的形态。
- **mini vs SWE-agent**（同门大哥）：官方建议 **默认选 mini**，只在「要试验不同工具集 / 不同 history processor / 要极强 YAML 配置」时才上 SWE-agent。

---

## 十、落地建议

1. **要一条自己的 Agent 基线，先抄这个循环**：三个 Protocol + 一个 `while True` + 四类上限，比任何框架都好改。
2. **做 RL / 微调数据时，线性历史是刚需**（trajectory 直接就是训练样本），mini 的形态比带压缩 / 分支的外壳合适。
3. **拿它当「模型能力」的测量工具**：Bash Only 榜把所有模型锁在同一外壳上，比的是模型不是脚手架——这正是 [eval](../../reliability/eval/) 里强调的「坐标要写全」。
4. **上生产前必须换 Environment**：本地 `LocalEnvironment` 是裸机权限，`docker` / `bubblewrap` / Modal 三选一，别裸跑。
5. **别指望它做长程协作**：无 `cd` / 无 `export`、无记忆、无压缩，长任务会撞上下文天花板。它的设计目标是**短、可复现、可批量**，不是陪你改一整天代码。

---

## 十一、延伸阅读

- 官网 / 文档：https://mini-swe-agent.com/latest/ （FAQ 里 "Why no shell session" 一节必读）
- 最小 Agent 教程：https://minimal-agent.com/
- 控制流图解：`https://mini-swe-agent.com/latest/advanced/control_flow/`
- 上手：`uvx mini-swe-agent`（匿名虚拟环境，不污染当前环境）
- 相邻专题：[harness](../harness/)、[loop-graph](../loop-graph/)、[sandbox](../../reliability/sandbox/)、[eval](../../reliability/eval/)、[guardrails](../../reliability/guardrails/)
- 四项目横向对比见本目录 [README](./README.md)
