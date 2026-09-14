# Harness 工程（Harness Engineering）

> 模型外面的**运行时外壳**：组上下文、暴露工具、跑命令、验证门、决定要不要再转。总览：[README.md](./README.md)。怎么开（验证闭环）→ [loop-engineering.md](./loop-engineering.md)。产品对比与四件套细讲 → [../harness/](../harness/)。
>
> 本篇只标定栈内位置。Harness 是车；Loop 是怎么开；图是立交和地图。

---

## 一、这一层管什么

没有 Harness 的模型只会聊天。有了之后变成：

```
目标 → 组上下文 → 选工具/动作 → 在真实环境执行 → 看输出 → 验证 → 再转或停
```

| 层 | 负责 | 不是 Harness |
|---|---|---|
| [提示](./prompt-engineering.md) / [上下文](./context-engineering.md) | 这一跳问什么、窗口装什么 | 文案与预算 |
| **Harness** | 工具、权限、沙箱、默认循环、产品形态 | 本层 |
| [循环](./loop-engineering.md) | 一份工作何时算完（完成定义 + 验证器） | 设计，不是底盘零件表 |
| [图](./graph-engineering.md) | 多条循环怎么接线；事实怎么共享 | 立交 / 地图 |

Tool 数量 ≠ Harness 强弱。Pi 四个核心工具、Claude Code 工具很全、DeepSeek 一切皆插件——比的是取向。

---

## 二、何时停在这一层

- 已经有工具和权限，任务是「单线程写 → 测 → 修」，验证器是测试。
- 要选编码 Agent 产品（Claude Code / Codex / Cursor Agent），先比外壳再比模型。

循环设计（五段、开闭环、执行者不当裁判）写在 [loop-engineering.md](./loop-engineering.md)，不要把「我们有个 Agent 产品」当成「我们已经有循环工程」。

---

## 三、升级信号

| 现象 | 下一层 |
|---|---|
| 人还在当调度器：看输出、改提示、再点一次 | [循环工程](./loop-engineering.md) |
| 并行子 Agent、人审必须是节点、按边重试 | [执行图](./execution-graph.md) |
| 跨会话要对齐「同一个客户」 | [上下文图](./context-graph.md) |
