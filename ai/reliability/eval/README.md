# Eval · 评测与可观测

> 用 **你们自己的任务集 + 线上 trace** 衡量系统，而不是只报 MMLU。
> 先分清两件事：**LLM 评测 ≈ 学校考试（看模型智商）**；**Agent 评测 ≈ 上机考试（看模型 × Harness 能不能在环境里把活干完）**。

配套 MVP：[mvp.py](./mvp.py)（技能契约回归 + 学校考试 / 上机考试对照）。

---

## 一、Agent 评测为什么比 LLM 评测更难

| | **LLM 评测** | **Agent 评测** |
|---|---|---|
| 类比 | 学校考试 | 计算机上机考试 |
| 评什么 | **主要评模型本身**（「智商」、知识、卷面答案） | **评模型 × [Harness](../../agent/harness/) 的执行能力** |
| 通俗 | 这题会不会做 | 在受控考场里能不能交卷、过验收 |
| 题目从哪来 | Benchmark / 评测集 = **一套试卷** | **Task + Environment** = 上机题 + 受控考场 |
| 考生是谁 | 模型对着 Prompt 作答 | **Model × Harness** = 考生 + 解题系统 |
| 答卷长什么样 | 一段文本 | **Tool / Artifact** = 工具操作 + 最终交付（补丁、PR、文件） |
| 怎么判分 | Reference / Rubric + Rule / Judge（参考答案、评分标准、阅卷） | **Trajectory / Test** = 过程记录 + 验收测试 |

LLM 评测可以把「一道考题」收成 `(prompt, reference)`，离线、可复现、好刷榜。Agent 多了三层麻烦：

1. **环境**：同样的题，文件系统、网络、时间、工具版本一变，轨迹全变。
2. **耦合**：换 Harness（工具集、权限、子 Agent）等于换「解题系统」，分数不能记在裸模型头上。SWE-bench / Terminal-Bench / [AA Coding Agents](https://artificialanalysis.ai/?coding-agents=execution-time) 测的都是这条链。
3. **过程 vs 结果**：只看最终一句回复会放过程作弊（胡乱 `rm`、抄答案文件）；只看轨迹不看验收，又会放过「步骤很忙但测试红」。

所以有效评测不是再堆一张更大的试卷，而是三个因子相乘：

```
有效评测 = 真实、有区分度的题目
        × 公平、可复现的环境
        × 清晰、可验证的判分
```

缺任何一项：题目假 → 刷榜无用；环境漂 → 分数不可比；判分虚（「回答要有帮助」）→ 不能当门禁。

---

## 二、SWE-bench：上机考试的代表榜

官网：[swebench.com](https://www.swebench.com/)。题目来自真实 GitHub issue：给仓库 + 问题描述，Agent 改代码，**单元测试变绿才算 Resolved**。指标是 **% Resolved**（解开了百分之多少条实例），不是「回答像不像人」。

这正好对应上一节三件套：真实 issue（有区分度）× Docker 化仓库（可复现考场）× 测试套件（可验证判分）。

### 榜怎么分，别拿错表比

| 子集 | 规模 | 是什么 | 什么时候看 |
|---|---|---|---|
| **Full** | 2294 | 原始集：12 个 Python 仓的真实 issue | 论文、完整难度；贵、慢 |
| **Verified** | 500 | 人工筛过、题意更清楚（2024 与 OpenAI 合作） | **业界最常引用的那张表** |
| **Lite** | 300 | 为省钱裁的子集 | 自跑、迭代 Harness 时 |
| **Bash Only** | 500 | Verified 题，但 **所有模型锁在同一套 mini-SWE-agent 环境** | 要比模型、不想被「谁家 Harness 更强」干扰时看这张（官网默认 Verified 视图常走这条） |
| **Multilingual** | 300 | 42 仓、9 种语言 | 不只会修 Python |
| **Multimodal** | 480 | issue 里带图（截图、UI） | 视觉 + 代码 |

同一模型在 Full / Verified / Bash Only 上数字不能横比。**Bash Only 的存在，就是承认分数 = 模型 × Harness × 环境**；把外壳钉死后，剩下才比较像比模型。

开源权重在官网上有标记；「SWE-bench 团队跑过或核过」的条目可信度更高。厂商自报、自带豪华 Agent 脚手架的数字，要当广告读。

### 家族里不止一张修 issue 榜

| 名字 | 和 SWE-bench 的关系 |
|---|---|
| **mini-SWE-agent** | 官方约 100 行 Python 的最小外壳；用来证明核可以很瘦（曾在 Verified 上打到可引用的分数） |
| **SWE-agent** | 官方自己的编码 Harness（有历史 SOTA 记录） |
| **SWE-smith** | 用来**训练**软件工程 Agent 的数据 / 配方 |
| **CodeClash** | 比的是目标导向开发，不是「修这一张 issue」 |
| **ProgramBench** | 从零写出有意义的软件产物（2026 补充，不是修仓） |

读榜时把坐标写全：`SWE-bench Verified + Bash Only + mini-SWE-agent` 和 `某闭源产品默认 Agent 在 Verified 上自报` 不是同一个实验。

本地 / 自己的仓永远比这张榜重要：SWE-bench 是别人的 12 个 Python 仓，不是你的业务代码。

---

## 三、生产里评测有三块

公开榜单测的是模型通识，不是你的退款 SOP、也不是工具是否被乱调。落地时拆开：

| 块 | 问题 | 手段 |
|---|---|---|
| **离线集** | 改 prompt / 换模型 / 换 Harness 会不会回退 | 金标问答、工具轨迹、安全红队、上机任务 |
| **裁判** | 没有唯一答案时怎么打分 | 规则 / 程序校验 / 验收测试优先；LLM-as-judge 需抽检 |
| **线上 trace** | 真实用户路径哪里挂 | span：LLM、MCP、A2A、护栏、检索、工具 |

Agent 要比聊天多记：选了哪个工具、参数、重试次数、是否违反 skill、产物是否过测试。MCP 适合 per-tool 审计；A2A 适合 per-hop TaskCompletion。Realtime 要在流中途抽检，不能等整段结束。

好的用例是 **可执行的断言**，不是「回答要有帮助」这种散文。

---

## 四、功能作用

- **改动有闸门**：合并前跑回归，像单测。
- **选型有数**：模型 A/B、Harness、路由策略用同一套集。
- **事故可复盘**：trace id 串起模型输入、工具、护栏决策。
- **防评测作弊**：定期换隐藏集、防 prompt 过拟合公开题；上机环境要版本钉死。

---

## 五、应用场景

| 场景 | 更像哪边 | 指标例子 |
|---|---|---|
| 裸模型选品 | 学校考试 | GPQA、Arena Elo、智力指数 |
| RAG | 两者之间 | 引用是否在检索块内、答对率、空检索拒答率 |
| 编码 Agent | 上机考试 | 任务完成率、测试绿、多余工具、平均步数 / 耗时 |
| 护栏 | 上机 + 红队 | 攻击漏拦率、良性误拦率 |
| 路由 | 学校考试当特征 | 分流后质量不掉点的比例、成本 |
| Computer Use | 上机考试 | 路径完成、非法域点击 |
| 结构化抽取 | 学校考试（有 schema） | 字段级 F1 |

---

## 六、用例怎么写

技能 / SOP 契约（偏 Agent，但环境很轻）：

```
id: refund-missing-order
priority: P0
input: "帮我退款"
context: {}
expect:
  skill: refund
  status: blocked
  ask_contains: 缺字段
```

上机任务还要多钉三样：**环境镜像或夹具**、**允许的工具**、**验收命令**（例如 `pytest`）。P0 不过不能发版；P1 允许已知失败但要记账。

---

## 七、与相邻技术

| 技术 | 关系 |
|---|---|
| [Harness](../../agent/harness/) | Agent 分数 = 模型 × 外壳；换循环就要重测 |
| [Guardrails](../guardrails/) | 护栏决策应成为 span，进入同一条 trace |
| [Model Routing](../model-routing/) | 路由策略用 eval 证明「省钱且不掉点」 |
| [Reasoning](../../foundation/reasoning/) | 报告准确率时必须带 thinking 预算 |
| [Agent Skills](../../agent/agent-skills/) | 「是否遵守硬规则」是便宜的程序裁判 |
| LangSmith / Langfuse / Braintrust | 常见产品化实现 |
| 单测 | 确定性逻辑用单测；生成用 eval 集；上机用夹具 + 测试 |

---

## 八、落地建议

1. 先做 **20 条 P0 黄金路径**（能程序断言），再谈平台。
2. 能程序断言 / 跑测试的不要上 LLM judge（数学、schema、是否调用某工具、pytest 红绿）。
3. 报 Agent 分数时写明 **模型 + Harness + 环境版本**，否则不可比。
4. Judge 要抽 5–10% 人工校准，否则分数会漂。
5. 线上采样 + 离线回放，两边同一 schema；失败用例自动入库。

---

## 九、延伸阅读

- OpenTelemetry GenAI semantic conventions
- [SWE-bench 官网](https://www.swebench.com/)：Verified / Bash Only / Lite / Multilingual / Multimodal
- Terminal-Bench / OSWorld：另一类上机考场
- MMLU-Pro / GPQA / Arena：学校考试代表
- 对比：[harness](../../agent/harness/)、[guardrails](../guardrails/)、[agent-skills](../../agent/agent-skills/)

---

## 十、本目录 MVP

`mvp.py` 两段：

1. **学校考试**：对固定问答题做参考答案比对。
2. **上机考试 + 技能门禁**：退款技能 4 条契约（P0/P1）；另有一个迷你仓库，必须 `edit` 后验收测试变绿，并检查轨迹里真的动过工具。
