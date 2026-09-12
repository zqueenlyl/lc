# reliability · 治理与上线

> **定位**：决定**能不能上生产**。
> **口诀**：「讲拦错 / 打分 / 隔离 / 降级」→ 归这。

上级索引：[../README.md](../README.md) ｜ 学习地图：[../learning-path.md](../learning-path.md)

## 专题

| 专题 | 一句话 | 入口 |
|---|---|---|
| **Structured Output** | JSON Schema / Function Calling，让输出可机器消费 | [structured-output/](./structured-output/) |
| **Guardrails** | 输入过滤、工具门禁、输出校验、人审 | [guardrails/](./guardrails/) |
| **Sandbox** | 沙箱隔离执行：内核原语 / 隔离强度 / 文件系统 / 网络出口 / 凭证 / 逃逸加固 / 可观测验收 / 数据通道 / 平台化 / 跨平台机制 / 开销实测（环节系列 01–13 + 13 notebook） | [sandbox/](./sandbox/) |
| **Eval** | 自定义评测 + Trace；LLM 是考试，Agent 是上机 | [eval/](./eval/) |
| **Model Routing** | 按任务 / 成本 / 失败自动选模型 | [model-routing/](./model-routing/) |

## 四道闸门（上线前依次过）

```
输出可控 → 拦得住 → 量得出 → 贵了能降
structured-output → guardrails + sandbox → eval → model-routing
```

## 原理纵深（按序）

- 约束解码（非法 token 为什么不采样，structured-output 的机制底） → [./structured-output/约束解码原理.md](./structured-output/约束解码原理.md)
- 评测与可观测（含评测数据闭环、归因判断） → [../agent/环节09-评测与可观测详解.md](../agent/环节09-评测与可观测详解.md)
- 生产级工程化（重试 / 幂等 / 降级 / 灰度） → [../agent/环节10-生产级工程化详解.md](../agent/环节10-生产级工程化详解.md)
- 模型怎么选、怎么换 → [../foundation/transformer/模型评测与选型方法详解.md](../foundation/transformer/模型评测与选型方法详解.md)

## 相邻大类

- 塞什么进窗口 → [../knowledge/](../knowledge/)
- 跑得多快 / 多省 → [../runtime/](../runtime/)
