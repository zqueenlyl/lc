# Structured Output · 结构化输出与 Function Calling

> 让模型吐出 **符合 schema 的 JSON / 工具调用**，下游代码可以解析、校验、重试，而不是用正则从散文里挖字段。

这是 Agent 工具循环、MCP tools、表单填写、数据抽取的共同底座。

配套 MVP：[mvp.py](./mvp.py)（JSON Schema 校验 + 失败修复循环）。

---

## 一、技术讲解

自然语言对人不友好对接 ERP。结构化输出把解码限制在合法空间：

1. **提示约束**：系统里贴 schema，软约束，会破。
2. **Function / Tool Calling**：模型产出 `name + arguments`，运行时执行。
3. **JSON Schema / Grammar 约束解码**：非法 token 直接不采样（最硬）。
4. **校验 + 修复**：先生成，失败把错误喂回去再生成（MVP 这条）。

2026 年厂商 API 普遍支持 `response_format` / `strict` tools。开源侧有 Outlines、xgrammar、guidance 等。

和 MCP 的关系：MCP 的 `inputSchema` 就是这一层；Host 把 schema 交给模型，再把 arguments 丢给 server。

---

## 二、功能作用

- **可编程**：类型安全地接数据库、工作流、UI。
- **可重试**：校验错误是结构化的（缺字段、类型错）。
- **少幻觉字段**：strict 模式下不能发明 schema 外的键（仍可能编造合法类型的值）。
- **工具循环**：思考 → call → 观察 → 再 call，全靠这一层。

---

## 三、应用场景

| 场景 | schema 例子 |
|---|---|
| 抽发票 | `{invoice_id, amount, date, tax}` |
| 路由意图 | `{intent, slots}` |
| Agent 工具 | MCP / OpenAI tools |
| UI 生成表单 | 字段枚举、范围 |
| 评测打分 | `{score, rationale, pass}` |

散文更适合：品牌文案、解释、安抚——先生成文本，必要时再附一个小 JSON 头。

---

## 四、常见坑

- **值幻觉**：schema 合法但 `order_id` 是编的 → 必须和系统对一下。
- **过深嵌套**：模型容易漏层，能扁则扁。
- **枚举过长**：上百个 enum 不如先分类再细选。
- **和思维链抢通道**：有的模型要先 think 再出 JSON，解析时只取最后一个对象。
- **日期 / 货币**：写清时区和最小单位（分 vs 元）。

---

## 五、与相邻技术

| 技术 | 关系 |
|---|---|
| [MCP](../../agent/mcp/) | tools 的入参层 |
| [Guardrails](../guardrails/) | schema 过了还有业务规则与安全 |
| [Eval](../eval/) | 字段级准确率比 BLEU 有用 |
| [Agent Skills](../../agent/agent-skills/) | 输出契约常写成 schema |

---

## 六、落地建议

1. 能用 **strict / grammar** 就不要只靠「请输出 JSON」。
2. 校验失败最多 2 次修复，再转人工或降级。
3. 对外 API 在边界再验一次，不信任模型。
4. 日志里存 raw 与 parse 结果，方便回归。
5. 数值字段用二次确认（再查库），不要只信抽取。

---

## 七、延伸阅读

- OpenAI Structured Outputs；JSON Schema；Outlines / xgrammar
- 正确率评测（无约束 vs 约束、跨模型 JSON 正确率数据）→ [正确率评测.md](./正确率评测.md)
- 对比：[mcp](../../agent/mcp/)、[guardrails](../guardrails/)

---

## 八、本目录 MVP

`mvp.py` 定义「退款申请」schema，故意先产出缺字段 / 类型错误的 JSON，校验器返回错误，修复器补全，直到通过或次数用尽。
