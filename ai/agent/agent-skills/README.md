# Agent Skills · 技能包

> 把「某一类任务该怎么做」封装成可发现、可版本化、可复用的说明书 + 脚本，而不是把流程写死在 Agent 源码里。一句话：**MCP 给手，Skills 给菜谱。**

Cursor / Claude 的 `SKILL.md`、各家 Agent 的 skill / playbook / SOP 注入，都是同一类东西。2026 年它从「提示词片段」变成了工程资产。

配套 MVP：[mvp.py](./mvp.py)。

---

## 一、技术讲解

Agent 底座（模型 + 工具 + 记忆）是通用的。真正拉开差距的是 **领域流程**：

- 怎么从 TAPD 链接抽出可编码需求；
- code review 按哪几个维度、什么算 Blocking；
- 发版前检查哪些门禁。

如果这些写在主 prompt 或硬编码 `if/else` 里，技能一多就膨胀，也无法按任务按需加载。

Skill 的典型形态：

```
skill-name/
  SKILL.md          # 何时触发、步骤、禁止事项、输出契约
  scripts/          # 可选：确定性脚本（校验、转换）
  references/       # 可选：规范长文，按需再读
```

运行时 Host 只先读 **短描述 / frontmatter** 做路由；命中后再把正文（和需要的 reference）塞进上下文。这是 [Context Engineering](../../knowledge/context-engineering/) 的一种具体做法：**按需加载程序记忆**。

好的 Skill 同时约束模型与执行器：

- **触发**：用户说了什么 / 当前阶段是什么才启用；
- **步骤**：先读谁、再写谁、禁止跳步；
- **工具边界**：只用列出的 MCP / 脚本；
- **完成定义**：产出哪个文件、哪些字段必填。

---

## 二、功能作用

- **可组合**：主 Agent 保持瘦，能力靠装技能扩展。
- **可评审**：流程变更走 diff / PR，而不是改一团隐藏 prompt。
- **节省窗口**：不把 50 份 SOP 全塞进系统提示。
- **人机同一套**：人类也能按 SKILL.md 操作，降低「只有模型知道规矩」。
- **与记忆分层**：Skill = 程序记忆（怎么做）；[Memory](../../knowledge/memory/) = 情景 / 语义（做过什么、用户是谁）。

---

## 三、应用场景

| 场景 | Skill 里写什么 |
|---|---|
| 需求澄清 | 必问字段、输出 `requirements.md` 模板 |
| 代码审查 | 维度、Blocking 标准、禁止作者自审 |
| 数据标注 / 客服 SOP | 话术、升级条件、禁说清单 |
| 合规检查 | 必须跑的脚本、失败即停 |
| IDE 助手 | 「用户提到 /foo 才读这份 skill」 |

不适合：一次性探索、没有稳定 SOP 的开放研究（先别固化）。

---

## 四、一份 Skill 建议写清的块

1. **名称 + 一句话**（给路由器用）
2. **触发条件**（包含 / 排除）
3. **硬规则**（绝不能不做 / 绝不能做）
4. **步骤**（可检查的顺序）
5. **输入 / 输出契约**（文件路径、字段）
6. **工具与脚本**（允许列表）
7. **失败怎么停**（缺字段就问人，不要猜）

---

## 五、与相邻技术

| 技术 | 关系 |
|---|---|
| System Prompt | 全局人格与红线；Skill 是按任务加载的章节 |
| [MCP](../mcp/) | Skill 规定何时调哪些 tool |
| [A2A](../a2a/) | 跨 Agent 的 skill 出现在 Agent Card 上 |
| [Memory](../../knowledge/memory/) | 程序记忆 vs 情景记忆 |
| [Context Engineering](../../knowledge/context-engineering/) | Skill 是受控的上下文模块 |
| [Eval](../../reliability/eval/) | 用「是否遵守 skill 硬规则」做回归 |

---

## 六、落地建议

1. 先写 **完成定义**，再写步骤，避免散文技能。
2. 正文控制在模型能一次读完的长度；细节放 `references/`。
3. 确定性校验用脚本，不要让模型「目测 JSON 合不合法」。
4. 技能要可测试：给 3 个用户说法，断言路由命中 / 不命中。
5. 禁止事项写成硬规则，比「建议不要」有效得多。

---

## 七、延伸阅读

- 本仓库用户侧已有大量 Cursor / Claude Skill 实践（需求澄清、CR、TAPD）
- 对比：[context-engineering](../../knowledge/context-engineering/)、[mcp](../mcp/)、[memory](../../knowledge/memory/)

---

## 八、本目录 MVP

`mvp.py` 内置两份 skill（退款 SOP、发布检查），按用户话路由，逐步执行硬规则；缺字段就停下来问人，而不是编造。
