# 提示工程（Prompt Engineering）

> 这一次调用**怎么问清楚**。总览：[README.md](./README.md)。窗口里装什么 → [context-engineering.md](./context-engineering.md)。转圈直到测绿 → [loop-engineering.md](./loop-engineering.md)。
>
> 技法细讲（System 四要素、Few-shot、结构化输出三层闭环）在 [环节 02](../环节02-提示与上下文工程详解.md)，不在本篇重复。本篇只标定它在工程栈里的位置。

---

## 一、这一层管什么

提示工程打磨**一次推理**：角色、任务、约束、输出格式。人还在回路里——写提示、看结果、改提示。

| 要素 | 回答 |
|---|---|
| 角色 | 你是谁 |
| 任务 | 这一次干什么 |
| 约束 | 不许做什么 |
| 格式 | 按什么结构答（最好能被程序消费） |

和下一层的分界：措辞、示范、Schema 约定属于本层；**选哪些源、砍哪些、排什么顺序、花多少 token** 属于 [上下文工程](./context-engineering.md)。

---

## 二、何时停在这一层

- 一次调用就能交差（分类、抽取、改写、出草稿）。
- 失败主要是「没听懂 / 格式不对」，改提示或加校验就能稳。
- 不需要工具、不需要根据环境反馈再试。

结构化输出：Prompt 约定最弱；JSON Mode 管「是 JSON」；Function Calling / 约束解码管「符合 Schema」。生产默认走 [structured-output](../../reliability/structured-output/) 的引导 → 校验 → 修复，不要只靠「请输出 JSON」。

---

## 三、升级信号

| 现象 | 下一层 |
|---|---|
| 该看的没在、不该看的塞爆、每轮重复付费 | [上下文工程](./context-engineering.md) |
| 要调工具、要权限、要产品外壳 | [Harness](./harness-engineering.md) |
| 「再改一版提示」其实是人在替系统重试 | [循环工程](./loop-engineering.md) |

提示工程不会过时。升级之后它变成循环里**每一跳**的局部指令（系统提示、工具 schema、节点 prompt），不再是整份工作的调度器。
