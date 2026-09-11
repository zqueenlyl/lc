# Computer Use · 电脑 / 浏览器操控

> 让模型看屏幕（截图 / a11y 树 / DOM），输出鼠标键盘动作，把「不会提供 API 的软件」变成工具。一句话：**没有 MCP 的应用，就用眼睛和手。**

OpenAI Computer Use、Anthropic Computer Use、浏览器 Agent（Operator / 各类 Browser Use）、桌面 RPA 与这一路同源。

配套 MVP：[mvp.py](./mvp.py)（网格桌面 + 动作循环，不驱动真实鼠标）。

---

## 一、技术讲解

传统 Agent 只能调「有 schema 的工具」。大量工作卡在：

- 旧 ERP / 内部后台没有 API；
- 验证码、多步表单、第三方 SaaS 控制台；
- 「打开网页对比三个供应商价格」。

Computer Use 的循环：

```
感知 (截图 / DOM / a11y) → 推理下一步 → 动作 (click/type/scroll) → 再感知
```

三种感知，精度和成本不同：

| 感知 | 输入 | 优点 | 缺点 |
|---|---|---|---|
| **像素截图** | 图 + 可选网格坐标 | 通吃任何 UI | token 贵、分辨率敏感、难测 |
| **a11y / 无障碍树** | 角色、名字、状态 | 稳、可选择器 | 自绘 Canvas / 游戏失效 |
| **DOM / 选择器** | CSS / xpath / Playwright | 网页最稳 | 只覆盖浏览器 |

2026 年生产上常见 **混合**：网页走 Playwright 选择器，桌面走 a11y，兜底再截图。动作空间要小而稳：`click(x,y)` / `click(role,name)` / `type` / `key` / `scroll` / `wait`，再加 `done`。

安全是第一设计约束：模型一旦能点「转账」「删除生产」，等于拥有操作者会话。必须和 [Guardrails](../../reliability/guardrails/) 绑死。

---

## 二、功能作用

- **补齐工具空白**：把无 API 系统接进 Agent。
- **端到端验收**：自己走一遍用户路径，给 [Eval](../../reliability/eval/) 当真实环境断言。
- **跨应用流程**：邮箱 → 表格 → 后台，无需每家都做 MCP。
- **人机协同**：敏感页暂停，人点完再让模型继续（和 LangGraph interrupt 同类）。

---

## 三、应用场景

| 场景 | 推荐感知 | 备注 |
|---|---|---|
| 填内部工单 / 报销 | DOM 或 a11y | 选择器比截图稳 |
| 竞品网页调研 | Playwright + 截图兜底 | 注意站点 ToS |
| QA 回归 | DOM + 断言 | 比纯像素可维护 |
| 桌面客户端运维 | 截图 + a11y | 先白名单窗口 |
| 验证码 / 支付 | **不要全自动** | 必须人审 |

不适合：能提供 MCP / API 的系统（直接调工具更便宜、更稳）；高频交易或生产变更的无人值守。

---

## 四、动作循环要点

1. **状态要可回放**：每步存截图哈希、动作、前后 URL，否则无法 debug。
2. **步数上限 + 循环检测**：同一控件点 3 次无变化就停。
3. **坐标归一化**：截图分辨率和实际屏幕不一致是第一大坑。
4. **等待**：动完等网络 / 动画，否则下一步感知是旧画面。
5. **目标检验**：用「页面文本是否包含 X」而不是「模型说做完了」。

---

## 五、与相邻技术

| 技术 | 关系 |
|---|---|
| [MCP](../mcp/) | 有官方工具优先 MCP；Computer Use 是没有协议时的后备 |
| RPA（UiPath 等） | 规则脚本 vs 模型决策；可混合：模型选分支，RPA 跑稳点 |
| Playwright / Selenium | 最常见的网页执行器 |
| [Multimodal](../../foundation/multimodal/) | 像素路线依赖多模态感知 |
| [Eval](../../reliability/eval/) | 任务完成率、步数、非法动作率是核心指标 |

---

## 六、落地建议

1. 先锁 **一个站点 + 一条黄金路径**，不要一上来「通用电脑助手」。
2. 域名 / 窗口白名单；禁止系统设置、钱包、生产 K8s 控制台。
3. 写操作二次确认；只读调研可以松一点。
4. 选择器优先，截图兜底；测试用假页面，不要盯着会变的生产 DOM。
5. 和 [Voice](../../runtime/voice-realtime/) 组合时，动作确认要用语音回读关键字段。

---

## 七、延伸阅读

- OpenAI Computer Using Agent / Anthropic Computer Use 文档
- Browser Use、Playwright MCP、OSWorld / WebArena 评测集
- 对比：[mcp](../mcp/)、[multimodal](../../foundation/multimodal/)、[guardrails](../../reliability/guardrails/)

---

## 八、本目录 MVP

`mvp.py` 用字符网格模拟桌面：窗口里有「搜索框 + 提交 + 结果」。Agent 循环：观察 → 规则策略选动作 → 执行，直到结果区出现目标文本。展示感知-行动闭环，不驱动真实 OS。
