# AIMA 4e 术语中英对照表

> **方法论**：`book-translation` skill（`~/.workbuddy/skills/book-translation/SKILL.md`）§3 术语判定流程 —— 通用规则不在此重复。
> **配套文件**：`AIMA-翻译项目配置.md`（源文件定位、专有名词、陷阱实例、信源边界）；`log.md`（勘误台账：已修正错误 E / 原书疑误 O / 待核 P，术语类勘误见其 §3）。
> **本文件**：只放**对照数据** —— 术语总表 + 小节标题对照。翻译时先查本表，未命中再按 skill §3 四步流程处理并回填本表。

- **源**：`Artificial-Intelligence-A-Modern-Approach-4th.pdf`（AIMA 4e，1127 页）
- **参考译本**：人民邮电出版社 2022-12 中译本（译者：张博雅、陈坤、田超、顾卓尔、吴凡、赵申剑）
- **版本**：v1.4 / 2026-10-07

## 目录

- [§1 术语总表](#1-术语总表) —— 7 类约 150 条，按主题分组
- [§2 第 11–18 章小节标题中英对照](#2-第-1118-章小节标题中英对照) —— 120 条，含三级
- [§3 第 1–6 章（Part I & II）术语补充](#3-第-16-章part-i--ii术语补充) —— 导论/智能体/搜索/CSP/博弈，约 450 条
- [§4 第 7–11 章（Part III）术语补充](#4-第-711-章part-iii术语补充) —— 逻辑/知识表示/规划，约 380 条
- [§5 第 19–28 章（Part V–VII）术语补充](#5-第-1928-章part-vvii术语补充)

---

## 1. 术语总表

> 标注 ✅ = 已与中译本核对一致；⚠️ = 学界有分歧，本表为准并注明备选；🚫 = 明确禁用的译法。

### 1.1 概率基础（12–14 章）

| English | 中文 | 备注 |
|---|---|---|
| probability | 概率 | |
| joint distribution | 联合分布 | 全称为 full joint distribution 时译**完全联合分布** |
| marginalization / summing out | 边缘化 / 求和消元 | |
| normalization | 归一化 | |
| unconditional independence | 无条件独立 | 🚫 不译"绝对独立""绝对值独立" |
| conditional independence | 条件独立 | |
| pairwise independent | 两两独立 | |
| mutually independent | 相互独立 | ⚠️ **两两独立 ≠ 相互独立**，不可混用 |
| prior / posterior | 先验 / 后验 | |
| likelihood | 似然 | |
| evidence | 证据 | |
| query variable | 查询变量 | |
| hidden variable | 隐变量 | |
| Bayes' rule | 贝叶斯法则 | ✅ 不译"贝叶斯定理""贝叶斯公式" |
| naive Bayes | 朴素贝叶斯 | ✅ |
| Markov blanket | 马尔可夫毯 | ✅（中译本确认） |
| factor | 因子 | |
| CPT (conditional probability table) | 条件概率表 | |
| polytree / singly connected | 多树 / 单连接 | ⚠️ 二者指同一结构，🚫 不译"单连通" |
| inference | 推断 | ⚠️ 13.3 用"推断"，13.4 用"推理"（书名/章节名从原书） |
| sampling | 采样 | |
| rejection sampling | 拒绝采样 | |
| likelihood weighting | 似然加权 | |
| Gibbs sampling | 吉布斯采样 | |
| MCMC | MCMC | 缩写保留 |
| variable elimination | 变量消元 | |
| clustering / junction tree | 聚类 / 联接树 | |
| treewidth | 树宽 | |
| do-operator | do 算子 | |
| back-door criterion | 后门准则 | |
| causal network | 因果网络 | |
| intervention | 干预 | |

### 1.2 时序模型（14 章）

| English | 中文 | 备注 |
|---|---|---|
| transition model | 转移模型 | |
| sensor model | 传感器模型 | |
| filtering / prediction / smoothing | 滤波 / 预测 / 平滑 | |
| most likely sequence | 最可能序列 | 🚫 不译"最可能解释(MAP)"；MAP 是另一概念 |
| HMM (Hidden Markov Model) | 隐马尔可夫模型 | |
| Viterbi | 维特比 | |
| Kalman filter | 卡尔曼滤波器 | |
| Gaussian | 高斯 | |
| covariance | 协方差 | |
| DBN (dynamic Bayesian network) | 动态贝叶斯网络 | |
| particle filtering | 粒子滤波 | |
| unscented / EKF | 无迹滤波 / 扩展卡尔曼滤波 | |

### 1.3 概率编程（15 章）

| English | 中文 | 备注 |
|---|---|---|
| relational probability model | 关系概率模型 | |
| open-universe probability model | 开宇宙概率模型 | 🚫 不译"开放世界" |
| number statement | 数量陈述 | 🚫 不译"编号变量" |
| existence (of objects) | （对象的）存在性 | |
| generative program | 生成程序 | |
| probabilistic programming | 概率编程 | |
| TrueSkill | TrueSkill | 算法名保留 |
| multitarget tracking | 多目标跟踪 | |
| skill rating | 技能评级 | |

### 1.4 决策与效用（16 章）

| English | 中文 | 备注 |
|---|---|---|
| utility | 效用 | |
| preference | 偏好 | |
| lottery | 彩票 | ✅（中译本确认） |
| rational preferences | 理性偏好 | |
| utility assessment | 效用评估 | |
| multiattribute utility | 多属性效用 | |
| dominance | 占优 | 全称 deterministic/stochastic dominance = 确定性/随机占优 |
| decision network / influence diagram | 决策网络 / 影响图 | |
| value of information (VPI) | 信息价值 | |
| preference elicitation | 偏好启发 | |
| deference to humans | 顺从人类 | |
| off-switch game | 关机博弈 | |
| myopic / nonmyopic | 短视 / 非短视 | |
| sensitivity analysis | 敏感性分析 | |

### 1.5 MDP 与 POMDP（17 章）

| English | 中文 | 备注 |
|---|---|---|
| MDP (Markov decision process) | 马尔可夫决策过程 | 缩写 MDP 可直接使用 |
| POMDP | 部分可观测 MDP | |
| policy | 策略 | |
| reward | 奖励 | |
| discount (factor) | 折扣（因子） | |
| value iteration | 价值迭代 | |
| policy iteration | 策略迭代 | |
| Bellman equation | 贝尔曼方程 | |
| bandit problem | 老虎机问题 | ✅ |
| Gittins index | Gittins 指数 | 人名保留 |
| Bernoulli bandit | 伯努利老虎机 | |
| exploration / exploitation | 探索 / 利用 | |
| belief state | 信念状态 | |
| alpha vector | α 向量 | |
| PWLC (piecewise linear convex) | 分段线性凸 | |
| QMDP | QMDP | 缩写保留，需加简短说明 |
| POMCP | POMCP | 同 |
| RTDP | RTDP | 同 |

### 1.6 博弈与多智能体（18 章）

| English | 中文 | 备注 |
|---|---|---|
| game theory | 博弈论 | |
| player / strategy / strategy profile | 玩家 / 策略 / 策略组合 | |
| normal-form game | 标准型博弈 | |
| extensive-form game | 扩展型博弈 | |
| Nash equilibrium | 纳什均衡 | |
| Pareto optimal | 帕累托最优 | |
| social welfare | 社会福利 | |
| price of anarchy | 无政府状态的代价 | |
| Braess's paradox | 布雷斯悖论 | |
| tit-for-tat | 以牙还牙 | |
| backward induction | 逆向归纳 | |
| subgame perfect | 子博弈完美 | |
| Bayesian game | 贝叶斯博弈 | |
| assistance game (CIRL) | 辅助博弈（合作逆强化学习） | |
| coalition / coalition structure | 联盟 / 联盟结构 | |
| characteristic function | 特征函数 | |
| core | 核 | ⚠️ 博弈论专属含义，🚫 不译"核心" |
| Shapley value | Shapley 值 | |
| marginal contribution net | 边际贡献网 | |
| social choice | 社会选择 | |
| Condorcet paradox | 孔多塞悖论 | |
| Arrow's impossibility theorem | 阿罗不可能定理 | |
| IIA | 无关备选独立性 | |
| mechanism design | 机制设计 | |
| contract net | 合同网 | |
| second-price (Vickrey) auction | 二价（Vickrey）拍卖 | |
| winner's curse | 赢家诅咒 | |
| VCG mechanism | VCG 机制 | |
| strategy-proof / truthful | 策略防御 / 真实报价 | |
| alternating offers protocol | 交替报价协议 | |
| monotonic concession protocol | 单调让步协议 | |
| Zeuthen strategy | Zeuthen 策略 | |
| Nash bargaining solution | 纳什议价解 | |

### 1.7 规划（11 章）

| English | 中文 | 备注 |
|---|---|---|
| planning | 规划 | |
| action schema | 动作模式 | |
| PDDL | PDDL | 保留 |
| STRIPS | STRIPS | 保留 |
| planning graph | 规划图 | |
| Graphplan | Graphplan | 算法名保留 |
| SATPLAN | SATPLAN | 保留 |
| relaxed plan | 松弛计划 | |
| h_FF / h_Add / h_Max | h_FF / h_Add / h_Max | 保留符号，🚫 不臆造 HSPr |
| HTN (hierarchical task network) | 分层任务网络 | |
| high-level action (HLA) | 高层动作 | |
| sensorless planning | 无传感规划 | |
| contingent planning | 应变规划 | ⚠️ 备选"条件规划"，本表取"应变" |
| online planning | 在线规划 | |
| scheduling | 调度 | |
| critical path | 关键路径 | |
| slack / float | 松弛量 / 浮动时间 | |
| ES / LS (earliest/latest start) | 最早 / 最晚开始时间 | |

### 1.8 通用 AI 词

| English | 中文 |
|---|---|
| agent | 智能体 |
| environment | 环境 |
| belief / desire | 信念 / 愿望 |
| nondeterministic | 非确定性 |
| partially observable | 部分可观测 |
| utility function | 效用函数 |
| rational | 理性的 |
| optimal | 最优的 |

### 1.9 同形异义必须分列

| English | 语境 A | 语境 B |
|---|---|---|
| **core** | 博弈论 → **核** | 通用 → 核心 |
| **factor** | 概率图 → **因子** | 通用 → 因素 |
| **inference** | 精确 → **推断** | 近似 / 章节名 → **推理** |
| **state** | 时序模型 → **状态** | 规划 → 状态（同，但注意 §12.7 的 Known/Frontier/**Other** 是**方格类别**不是状态） |
| **model** | 概率 → **模型** | 逻辑（第 8 章）→ 模型（指派） |

---

## 2. 第 11–18 章小节标题中英对照

> ✅ = 与中译本（二级）核对一致；未标注 = 三级，译名按 `book-translation` skill §3 判定流程自拟。

#### 第 11 章 自动规划（Automated Planning）

| 号 | English | 中文 |
|---|---|---|
| 11.1 ✅ | Definition of Classical Planning | 经典规划的定义 |
| 11.1.1 | Example domain: Air cargo transport | 示例域：航空货运 |
| 11.1.2 | Example domain: The spare tire problem | 示例域：备胎问题 |
| 11.1.3 | Example domain: The blocks world | 示例域：积木世界 |
| 11.2 ✅ | Algorithms for Classical Planning | 经典规划的算法 |
| 11.2.1 | Forward state-space search for planning | 规划的前向状态空间搜索 |
| 11.2.2 | Backward search for planning | 规划的反向搜索 |
| 11.2.3 | Planning as Boolean satisfiability | 规划即布尔可满足性 |
| 11.2.4 | Other classical planning approaches | 其他经典规划方法 |
| 11.3 ✅ | Heuristics for Planning | 规划的启发式方法 |
| 11.3.1 | Domain-independent pruning | 领域无关的剪枝 |
| 11.3.2 | State abstraction in planning | 规划中的状态抽象 |
| 11.4 ✅ | Hierarchical Planning | 分层规划 |
| 11.4.1 | High-level actions | 高层动作 |
| 11.4.2 | Searching for primitive solutions | 搜索基本解 |
| 11.4.3 | Searching for abstract solutions | 搜索抽象解 |
| 11.5 ✅ | Planning and Acting in Nondeterministic Domains | 非确定性域的规划和行动 |
| 11.5.1 | Sensorless planning | 无传感规划 |
| 11.5.2 | Contingent planning | 应变规划 |
| 11.5.3 | Online planning | 在线规划 |
| 11.6 ✅ | Time, Schedules, and Resources | 时间、调度和资源 |
| 11.6.1 | Representing temporal and resource constraints | 表示时间与资源约束 |
| 11.6.2 | Solving scheduling problems | 求解调度问题 |
| 11.7 ✅ | Analysis of Planning Approaches | 规划方法分析 |

#### 第 12 章 不确定性的量化（Quantifying Uncertainty）

| 号 | English | 中文 |
|---|---|---|
| 12.1 ✅ | Acting under Uncertainty | 不确定性下的动作 |
| 12.1.1 | Summarizing uncertainty | 概述不确定性 |
| 12.1.2 | Uncertainty and rational decisions | 不确定性与理性决策 |
| 12.2 ✅ | Basic Probability Notation | 基本概率记号 |
| 12.2.1 | What probabilities are about | 概率是关于什么的 |
| 12.2.2 | The language of propositions in probability assertions | 概率断言中的命题语言 |
| 12.2.3 | Probability axioms and their reasonableness | 概率公理及其合理性 |
| 12.3 ✅ | Inference Using Full Joint Distributions | 使用完全联合分布进行推断 |
| 12.4 ✅ | Independence | 独立性 |
| 12.5 ✅ | Bayes' Rule and Its Use | 贝叶斯法则及其应用 |
| 12.5.1 | Applying Bayes' rule: The simple case | 应用贝叶斯法则：简单情形 |
| 12.5.2 | Using Bayes' rule: Combining evidence | 使用贝叶斯法则：组合证据 |
| 12.6 ✅ | Naive Bayes Models | 朴素贝叶斯模型 |
| 12.6.1 | Text classification with naive Bayes | 朴素贝叶斯文本分类 |
| 12.7 ✅ | The Wumpus World Revisited | 重游 wumpus 世界 |

#### 第 13 章 概率推理（Probabilistic Reasoning）

| 号 | English | 中文 |
|---|---|---|
| 13.1 ✅ | Representing Knowledge in an Uncertain Domain | 不确定域的知识表示 |
| 13.2 ✅ | The Semantics of Bayesian Networks | 贝叶斯网络的语义 |
| 13.2.1 | Conditional independence relations in Bayesian networks | 贝叶斯网络中的条件独立性关系 |
| 13.2.2 | Efficient Representation of Conditional Distributions | 条件分布的高效表示 |
| 13.2.3 | Bayesian nets with continuous variables | 含连续变量的贝叶斯网络 |
| 13.2.4 | Case study: Car insurance | 案例研究：汽车保险 |
| 13.3 ✅ | Exact Inference in Bayesian Networks | 贝叶斯网络中的精确推断 |
| 13.3.1 | Inference by enumeration | 枚举推断 |
| 13.3.2 | The variable elimination algorithm | 变量消元算法 |
| 13.3.3 | The complexity of exact inference | 精确推断的复杂度 |
| 13.3.4 | Clustering algorithms | 聚类算法 |
| 13.4 ✅ | Approximate Inference for Bayesian Networks | 贝叶斯网络中的近似推理 |
| 13.4.1 | Direct sampling methods | 直接采样方法 |
| 13.4.2 | Inference by Markov chain simulation | 马尔可夫链模拟推断 |
| 13.4.3 | Compiling approximate inference | 编译近似推理 |
| 13.5 ✅ | Causal Networks | 因果网络 |
| 13.5.1 | Representing actions: do-operator | 表示动作：do 算子 |
| 13.5.2 | The back-door criterion | 后门准则 |

#### 第 14 章 时间上的概率推理（Probabilistic Reasoning over Time）

| 号 | English | 中文 |
|---|---|---|
| 14.1 ✅ | Time and Uncertainty | 时间与不确定性 |
| 14.1.1 | States and observations | 状态与观测 |
| 14.1.2 | Transition and sensor models | 转移模型与传感器模型 |
| 14.2 ✅ | Inference in Temporal Models | 时序模型中的推断 |
| 14.2.1 | Filtering and prediction | 滤波与预测 |
| 14.2.2 | Smoothing | 平滑 |
| 14.2.3 | Finding the most likely sequence | 寻找最可能序列 |
| 14.3 ✅ | Hidden Markov Models | 隐马尔可夫模型 |
| 14.3.1 | Simplified matrix algorithms | 简化的矩阵算法 |
| 14.3.2 | Hidden Markov model example: Localization | 隐马尔可夫模型示例：定位 |
| 14.4 ✅ | Kalman Filters | 卡尔曼滤波器 |
| 14.4.1 | Updating Gaussian distributions | 更新高斯分布 |
| 14.4.2 | A simple one-dimensional example | 简单的一维示例 |
| 14.4.3 | The general case | 一般情形 |
| 14.4.4 | Applicability of Kalman filtering | 卡尔曼滤波的适用性 |
| 14.5 ✅ | Dynamic Bayesian Networks | 动态贝叶斯网络 |
| 14.5.1 | Constructing DBNs | 构造 DBN |
| 14.5.2 | Exact inference in DBNs | DBN 中的精确推断 |
| 14.5.3 | Approximate inference in DBNs | DBN 中的近似推断 |

#### 第 15 章 概率编程（Probabilistic Programming）

| 号 | English | 中文 |
|---|---|---|
| 15.1 ✅ | Relational Probability Models | 关系概率模型 |
| 15.1.1 | Syntax and semantics | 语法与语义 |
| 15.1.2 | Example: Rating player skill levels | 示例：评估玩家技能水平 |
| 15.1.3 | Inference in relational probability models | 关系概率模型中的推断 |
| 15.2 ✅ | Open-Universe Probability Models | 开宇宙概率模型 |
| 15.2.1 | Syntax and semantics | 语法与语义 |
| 15.2.2 | Inference in open-universe probability models | 开宇宙概率模型中的推断 |
| 15.2.3 | Examples | 示例 |
| 15.3 ✅ | Keeping Track of a Complex World | 追踪复杂世界 |
| 15.3.1 | Example: Multitarget tracking | 示例：多目标跟踪 |
| 15.3.2 | Example: Traffic monitoring | 示例：交通监控 |
| 15.4 ✅ | Programs as Probability Models | 作为概率模型的程序 |
| 15.4.1 | Example: Reading text | 示例：文本阅读 |
| 15.4.2 | Syntax and semantics | 语法与语义 |
| 15.4.3 | Inference results | 推断结果 |
| 15.4.4 | Improving the generative program to incorporate a Markov model | 改进生成程序以纳入马尔可夫模型 |
| 15.4.5 | Inference in generative programs | 生成程序中的推断 |

#### 第 16 章 做简单决策（Making Simple Decisions）

| 号 | English | 中文 |
|---|---|---|
| 16.1 ✅ | Combining Beliefs and Desires under Uncertainty | 在不确定性下结合信念与愿望 |
| 16.2 ✅ | The Basis of Utility Theory | 效用理论基础 |
| 16.2.1 | Constraints on rational preferences | 理性偏好的约束 |
| 16.2.2 | Rational preferences lead to utility | 理性偏好导出效用 |
| 16.3 ✅ | Utility Functions | 效用函数 |
| 16.3.1 | Utility assessment and utility scales | 效用评估与效用尺度 |
| 16.3.2 | The utility of money | 金钱的效用 |
| 16.3.3 | Expected utility and post-decision disappointment | 期望效用与决策后失望 |
| 16.3.4 | Human judgment and irrationality | 人类判断与非理性 |
| 16.4 ✅ | Multiattribute Utility Functions | 多属性效用函数 |
| 16.4.1 | Dominance | 占优 |
| 16.4.2 | Preference structure and multiattribute utility | 偏好结构与多属性效用 |
| 16.5 ✅ | Decision Networks | 决策网络 |
| 16.5.1 | Representing a decision problem with a decision network | 用决策网络表示决策问题 |
| 16.5.2 | Evaluating decision networks | 评估决策网络 |
| 16.6 ✅ | The Value of Information | 信息价值 |
| 16.6.1 | A simple example | 简单示例 |
| 16.6.2 | A general formula for perfect information | 完美信息的一般公式 |
| 16.6.3 | Properties of the value of information | 信息价值的性质 |
| 16.6.4 | Implementation of an information-gathering agent | 信息收集智能体的实现 |
| 16.6.5 | Nonmyopic information gathering | 非短视的信息收集 |
| 16.6.6 | Sensitivity analysis and robust decisions | 敏感性分析与鲁棒决策 |
| 16.7 ✅ | Unknown Preferences | 未知偏好 |
| 16.7.1 | Uncertainty about one's own preferences | 关于自身偏好的不确定性 |
| 16.7.2 | Deference to humans | 顺从人类 |

#### 第 17 章 做复杂决策（Making Complex Decisions）

| 号 | English | 中文 |
|---|---|---|
| 17.1 ✅ | Sequential Decision Problems | 序贯决策问题 |
| 17.1.1 | Utilities over time | 时间上的效用 |
| 17.1.2 | Optimal policies and the utilities of states | 最优策略与状态的效用 |
| 17.1.3 | Reward scales | 奖励尺度 |
| 17.1.4 | Representing MDPs | 表示 MDP |
| 17.2 ✅ | Algorithms for MDPs | MDP 的算法 |
| 17.2.1 | Value Iteration | 价值迭代 |
| 17.2.2 | Policy iteration | 策略迭代 |
| 17.2.3 | Linear programming | 线性规划 |
| 17.2.4 | Online algorithms for MDPs | MDP 的在线算法 |
| 17.3 ✅ | Bandit Problems | 老虎机问题 |
| 17.3.1 | Calculating the Gittins index | 计算 Gittins 指数 |
| 17.3.2 | The Bernoulli bandit | 伯努利老虎机 |
| 17.3.3 | Approximately optimal bandit policies | 近似最优老虎机策略 |
| 17.3.4 | Non-indexable variants | 不可索引的变体 |
| 17.4 ✅ | Partially Observable MDPs | 部分可观测 MDP |
| 17.4.1 | Definition of POMDPs | POMDP 的定义 |
| 17.5 ✅ | Algorithms for Solving POMDPs | 求解 POMDP 的算法 |
| 17.5.1 | Value iteration for POMDPs | POMDP 的价值迭代 |
| 17.5.2 | Online algorithms for POMDPs | POMDP 的在线算法 |

#### 第 18 章 多智能体决策（Multiagent Decision Making）

| 号 | English | 中文 |
|---|---|---|
| 18.1 ✅ | Properties of Multiagent Environments | 多智能体环境的特性 |
| 18.1.1 | One decision maker | 单一决策者 |
| 18.1.2 | Multiple decision makers | 多个决策者 |
| 18.1.3 | Multiagent planning | 多智能体规划 |
| 18.1.4 | Planning with multiple agents: Cooperation and coordination | 多智能体规划：合作与协调 |
| 18.2 ✅ | Non-Cooperative Game Theory | 非合作博弈论 |
| 18.2.1 | Games with a single move: Normal form games | 单步博弈：标准型博弈 |
| 18.2.2 | Social welfare | 社会福利 |
| 18.2.3 | Repeated games | 重复博弈 |
| 18.2.4 | Sequential games: The extensive form | 序贯博弈：扩展型 |
| 18.2.5 | Uncertain payoffs and assistance games | 不确定收益与辅助博弈 |
| 18.3 ✅ | Cooperative Game Theory | 合作博弈论 |
| 18.3.1 | Coalition structures and outcomes | 联盟结构与结果 |
| 18.3.2 | Strategy in cooperative games | 合作博弈中的策略 |
| 18.3.3 | Computation in cooperative games | 合作博弈中的计算 |
| 18.4 ✅ | Making Collective Decisions | 做集体决策 |
| 18.4.1 | Allocating tasks with the contract net | 用合同网分配任务 |
| 18.4.2 | Allocating scarce resources with auctions | 用拍卖分配稀缺资源 |
| 18.4.3 | Voting | 投票 |
| 18.4.4 | Bargaining | 议价 |

---

---

---

## 3. 第 1–6 章（Part I & II）术语补充

> Part I = **Artificial Intelligence**（人工智能，第 1–2 章）；Part II = **Problem solving**（问题求解，第 3–6 章）。
> 由 6 个章节翻译 agent 按 `book-translation` skill §3 四步流程产出；本表 §1–§2 覆盖 11–18 章，§4 覆盖 7–11 章，故 Part I & II 术语单列于此。
> ⚠️ 这些译名**多数未与中译本正文核对**（信源 D 只能拿到章级目录），属自拟译法；对照纸书后请以中译本为准并回填。

### 3.1 第1章 绪论 Introduction

> **用途**：第 1 章「绪论」新增术语的待合并清单。
> **判定依据**：`book-translation` skill §3 四步流程——① 查 `AIMA-术语对照表.md`；② 查中译本；③ 查学界通行译法；④ 自拟并首现标注。
> **已有条目直接沿用、未改写**：agent=智能体、rational=理性的、rationality=理性、utility=效用、utility function=效用函数、game theory=博弈论、MDP=马尔可夫决策过程、HMM=隐马尔可夫模型、tractability=可处理性、inference=推断、model=模型、certainty factor（本章沿用第 13 章译法"确定性因子"）。
> **请勿修改 `AIMA-术语对照表.md`**（多个 agent 并发写），由项目所有者统一合并。
> **源文件**：`Artificial-Intelligence-A-Modern-Approach-4th.pdf`，第 1 章书页 1–36（PDF idx 13–48），信源 A。
> **合并方向**：建议在主表 §1 中新增「§1.0 导论与 AI 史（第 1 章）」分组；小节标题对照并入主表 §2。

---

#### 1. 新增术语条目

| English | 中文 | 备注 |
|---|---|---|
| artificial intelligence | 人工智能 | 通用词，全篇统一 |
| Turing test | 图灵测试 | ✅ 中译本 |
| total Turing test | 完全图灵测试 | 需与真实世界物体/人交互，另加视觉、语音与机器人学 |
| cognitive modeling | 认知建模 | 1.1.2 小节名 |
| cognitive science | 认知科学 | ✅ 通行译法 |
| introspection | 内省 | 与心理学"内省法"一致 |
| brain imaging | 脑成像 | |
| syllogism | 三段论 | ✅ 哲学通行译法 |
| logic / logicist | 逻辑 / 逻辑主义（者） | 后者指 AI 中的逻辑主义传统 |
| rational agent | 理性智能体 | 由已有条目 agent=智能体 + rational 复合 |
| standard model | 标准模型 | ⚠️ 本章特指"智能体追求我们给定的目标"这一 AI 范式，与物理学的"标准模型"同形异义，建议在主表 §1.9 登记 |
| limited rationality | 有限理性 | 与 Simon 的 bounded rationality 近义但本书用词为 limited rationality，照录 |
| beneficial machine | 有益机器 | 4e 新增 1.1.5 小节名 |
| provably beneficial | 可证明有益 | |
| value alignment problem | 价值对齐问题 | ✅ 学界通行 |
| dualism | 二元论 | ✅ 哲学通行 |
| materialism | 唯物主义 | ✅ |
| physicalism / naturalism | 物理主义 / 自然主义 | 均为与超自然相对立的立场 |
| empiricism | 经验主义 | ✅ |
| principle of induction | 归纳原则 | |
| logical positivism | 逻辑实证主义 | ✅ |
| observation sentence | 观察语句 | 逻辑实证主义术语 |
| confirmation theory | 确认理论 | Carnap–Hempel |
| utilitarianism | 功利主义 | ✅ |
| consequentialism | 后果主义 | ✅ |
| deontological ethics | 义务论伦理学 | ✅ |
| intractable | 难处理的 | 与已有 tractability=可处理性 配套 |
| NP-completeness | NP 完全性 | ✅ |
| decision theory | 决策理论 | ✅ |
| operations research | 运筹学 | ✅ |
| satisficing | 满意化 | ⚠️ 备选"满意原则""够用即可"；本书指"做足够好的决策而非求最优"，取"满意化" |
| neuron / synapse / axon / dendrite | 神经元 / 突触 / 轴突 / 树突 | ✅ |
| cerebral cortex | 大脑皮层 | ✅ |
| EEG (electroencephalograph) | 脑电图 | ✅ |
| fMRI | 功能性磁共振成像 | ✅ |
| optogenetics | 光遗传学 | ✅ |
| brain–machine interface | 脑机接口 | ✅ |
| singularity | 奇点 | 指计算机达到超人水平并自我改进的时刻 |
| behaviorism | 行为主义 | ✅ |
| cognitive psychology | 认知心理学 | ✅ |
| intelligence augmentation (IA) | 智能增强 | 与 AI 相对；缩写 IA 保留 |
| human–computer interaction (HCI) | 人机交互 | ✅ |
| Moore's law | 摩尔定律 | ✅ |
| bfloat16 | bfloat16 | 格式名保留原文 |
| GPU / TPU / WSE / FPGA | GPU / TPU / WSE / FPGA | 硬件名保留缩写，首现给全称：图形处理单元 / 张量处理单元 / 晶圆级引擎 / 现场可编程门阵列 |
| quantum computing | 量子计算 | ✅ |
| control theory | 控制理论 | ✅ |
| cybernetics | 控制论 | ✅ Wiener 书名 *Cybernetics* |
| homeostatic | 稳态的 | 指含反馈回路的稳态装置 |
| cost function | 代价函数 | ⚠️ 与"损失函数"（统计学）、"奖励之和"（运筹学）并列，勿混用 |
| computational linguistics | 计算语言学 | ✅ |
| physical symbol system hypothesis | 物理符号系统假说 | ✅ Newell & Simon 1976 |
| microworld | 微世界 | ✅ |
| blocks world | 积木世界 | ✅ |
| adaline | adaline | 系统名保留；可加注"自适应线性元件" |
| perceptron | 感知机 | ✅ |
| perceptron convergence theorem | 感知机收敛定理 | |
| Hebbian learning | 赫布学习 | ✅ |
| back-propagation | 反向传播 | ✅ |
| weak method | 弱方法 | 与领域特定的强知识相对 |
| expert system | 专家系统 | ✅ |
| knowledge-intensive system | 知识密集型系统 | |
| frames | 框架 | Minsky 1975；⚠️ 与"帧"（动画/视频）同形异义，建议在主表 §1.9 登记 |
| connectionist | 连接主义 | ✅ |
| neats / scruffies | 整洁派 / 邋遢派 | 原书脚注用词，中文无通行译法，首现附英文 |
| Bayesian network | 贝叶斯网络 | ✅ 主表已有相关条目 |
| big data | 大数据 | ✅ |
| deep learning | 深度学习 | ✅ |
| convolutional neural network | 卷积神经网络 | ✅ |
| word-sense disambiguation | 词义消歧 | ✅ |
| AI winter | AI 寒冬 | ✅ |
| state of the art | 最新进展 | 1.4 节名；⚠️ 备选"现状""技术现状"，本表取"最新进展" |
| AI Index / AI100 | AI Index / AI100 | 专名保留 |
| lethal autonomous weapons | 致命性自主武器 | ✅ |
| human-level AI (HLAI) | 人类水平人工智能 | 缩写 HLAI 保留 |
| artificial general intelligence (AGI) | 通用人工智能 | ✅ |
| artificial superintelligence (ASI) | 人工超级智能 | ✅ |
| gorilla problem | 大猩猩问题 | 本书自造比喻，直译 |
| King Midas problem | 弥达斯国王问题 | 本书自造比喻，直译 |
| assistance game | 辅助博弈 | 4e 新增（第 18 章） |
| inverse reinforcement learning | 逆向强化学习 | ✅ |
| recommender system | 推荐系统 | ✅ |

---

#### 2. 第 1 章小节标题中英对照

> 英文编号与标题取自原书（信源 A，官方 TOC 为三级起）；中文译名除标注 ✅ 外均为自拟。

#### 第 1 章 绪论（Introduction）

| 号 | English | 中文 |
|---|---|---|
| 1.1 | What Is AI? | 什么是人工智能？ |
| 1.1.1 | Acting humanly: The Turing test approach | 像人一样行动：图灵测试途径 |
| 1.1.2 | Thinking humanly: The cognitive modeling approach | 像人一样思考：认知建模途径 |
| 1.1.3 | Thinking rationally: The "laws of thought" approach | 像理性人一样思考："思维定律"途径 |
| 1.1.4 | Acting rationally: The rational agent approach | 理性地行动：理性智能体途径 |
| 1.1.5 | Beneficial machines | 有益机器（4e 新增） |
| 1.2 | The Foundations of Artificial Intelligence | 人工智能的基础 |
| 1.2.1 | Philosophy | 哲学 |
| 1.2.2 | Mathematics | 数学 |
| 1.2.3 | Economics | 经济学 |
| 1.2.4 | Neuroscience | 神经科学 |
| 1.2.5 | Psychology | 心理学 |
| 1.2.6 | Computer engineering | 计算机工程 |
| 1.2.7 | Control theory and cybernetics | 控制理论与控制论 |
| 1.2.8 | Linguistics | 语言学 |
| 1.3 | The History of Artificial Intelligence | 人工智能的历史 |
| 1.3.1 | The inception of artificial intelligence (1943–1956) | 人工智能的诞生（1943–1956） |
| 1.3.2 | Early enthusiasm, great expectations (1952–1969) | 早期的热情与厚望（1952–1969） |
| 1.3.3 | A dose of reality (1966–1973) | 现实的打击（1966–1973） |
| 1.3.4 | Expert systems (1969–1986) | 专家系统（1969–1986） |
| 1.3.5 | The return of neural networks (1986–present) | 神经网络的回归（1986 至今） |
| 1.3.6 | Probabilistic reasoning and machine learning (1987–present) | 概率推理与机器学习（1987 至今） |
| 1.3.7 | Big data (2001–present) | 大数据（2001 至今，4e 新增） |
| 1.3.8 | Deep learning (2011–present) | 深度学习（2011 至今，4e 新增） |
| 1.4 | The State of the Art | 最新进展 |
| 1.5 | Risks and Benefits of AI | 人工智能的风险与收益（4e 新增） |

---

#### 3. ⚠️ 待人工复核项

| # | 位置 | 问题 | 处理 |
|---|---|---|---|
| 1 | 1.2.1 义务论伦理学 | 原书作 "Immanuel Kant, in 1875 proposed…"；康德生卒 1724–1804，年份疑误（可能为 1785） | 笔记中照录原文并加 `⚠️ 待核` 标注 |
| 2 | 1.2.4 图 1.2 表格 | PDF 文本层把上标扁平化（`10 6`、`1015`），指数由列对齐关系还原 | 建议对照纸书核对三列数值 |
| 3 | 1.2.1 | Aristotle 引文"在一切动物中，人的脑按体型比例最大"原书注为约公元前 335 年 | 已照录 |
| 4 | 1.4 | "到 2019 年 AI 已达到或超过人类水平"的任务清单较长，逐条照录原文 | 建议抽查 2–3 条 |

---

#### 4. 维护约定

1. 本文件只收录第 1 章新增与主表未覆盖的条目，不重复主表已有条目。
2. 标记含义：✅ 与中译本或学界通行译法一致；⚠️ 有分歧或需复核。
3. 主表合并时：§1 进主表 §1 新增分组；§1.9 同形异义（standard model、frames）单列；§2 进主表 §2。

### 3.2 第2章 智能体 Intelligent Agents

> 来源：AIMA 4e Chapter 2 *Intelligent Agents*（pp. 36–62，PDF idx 48–74）
> 判定流程：`book-translation` skill §3 四步流程（术语表 → 中译本 → 学界通行 → 自拟）。
> **已有条目一律沿用、未改写**：agent=智能体、environment=环境、utility=效用、state=状态、transition model=转移模型、sensor model=传感器模型、percept=感知、reward=奖励、utility function=效用函数、expected utility=期望效用、partially observable=部分可观测、nondeterministic=非确定性、rational=理性的、policy=策略。
> ⚠️ **本文件未修改 `AIMA-术语对照表.md`**，请统一合并。
> ⚠️ 三级小节译名**均为自拟**：微信读书只能取到章级目录（信源 D 能力边界），无法核对三级标题。

---

#### 1. 智能体基础

| English | 中文 | 备注 |
|---|---|---|
| sensor | 传感器 | ✅ 学界通行 |
| actuator | 执行器 | ✅ 学界通行（" effector " 亦作效应器，本章无） |
| percept sequence | 感知序列 | 智能体有史以来感知到的一切的完整历史 |
| agent function | 智能体函数 | 感知序列 → 动作的**抽象数学描述** |
| agent program | 智能体程序 | 具体实现；⚠️ 与 agent function 必须区分（T5） |
| agent architecture | 智能体体系结构 | `agent = architecture + program` |
| table-driven agent | 表驱动智能体 | Figure 2.7 |
| software agent / software robot / softbot | 软件智能体 / 软件机器人 / 软体机器人 | ⚠️ softbot 备选"软 bot"；本表取"软体机器人" |
| environment class | 环境类 | 实验在该类上取平均性能 |

#### 2. 理性与性能度量

| English | 中文 | 备注 |
|---|---|---|
| performance measure | 性能度量 | ✅ 中译本通行译法 |
| rational agent | 理性智能体 | 章 1 已确立；本章给出正式定义 |
| consequentialism | 结果主义 | 道德哲学术语；按**后果**评价行为 |
| King Midas problem | 迈达斯国王问题 | p. 33 提出的"把错误目的放进机器"问题 |
| omniscience | 全知 | ⚠️ **理性 ≠ 全知 ≠ 完美**（T4/T5）；另见主表 logical omniscience=逻辑全知（第 7 章，不同语境） |
| perfection | 完美 | 原书对照：理性最大化**期望**性能，完美最大化**实际**性能 |
| information gathering | 信息收集 | ✅ 已见主表 16.6.4，本章沿用 |
| exploration | 探索 | 与 information gathering 相关但不等同（T5） |
| autonomy | 自主性 | 依赖设计者先验知识越少 → 自主性越高 |
| randomize / randomization | 随机化 | 单智能体环境中**通常非理性**；多智能体竞争环境中可理性 |

#### 3. 任务环境与 PEAS

| English | 中文 | 备注 |
|---|---|---|
| task environment | 任务环境 | "问题"；理性智能体是"解答" |
| PEAS (Performance, Environment, Actuators, Sensors) | PEAS | 缩写保留；四项分别译 性能度量/环境/执行器/传感器 |
| fully observable | 完全可观测 | |
| partially observable | 部分可观测 | ✅ 已入主表 |
| unobservable | 不可观测 | 无传感器；⚠️ 原书强调**并非无望**（第 4 章） |
| effectively fully observable | 有效完全可观测 | 检测到与动作选择**相关**的全部方面 |
| single-agent / multiagent | 单智能体 / 多智能体 | |
| competitive / cooperative | 竞争性 / 合作性 | 判别标准：B 的行为是否最大化**依赖于 A 行为**的性能度量 |
| deterministic | 确定性 | ✅ 已入主表 |
| nondeterministic | 非确定性 | ✅ 已入主表 |
| stochastic | 随机的 | ⚠️ **原书明确区分**：stochastic=显式处理概率；nondeterministic=列出但未量化（T5） |
| episodic | 片段式 | ⚠️ 备选"回合式""情节式"；本表取"片段式"（与 episode=片段 一致） |
| sequential | 序贯 | ✅ 与主表 17.1 "序贯决策问题"一致；⚠️ 原书脚注：与 CS 中"sequential vs parallel"无关 |
| static / dynamic | 静态 / 动态 | 判据：环境是否在智能体**思考期间**变化 |
| semidynamic | 半动态 | 环境不变但性能分数变（如带钟下棋） |
| discrete / continuous | 离散 / 连续 | 适用于**状态、时间处理、感知与动作**三方面 |
| known / unknown | 已知 / 未知 | ⚠️ **严格说不是环境的性质，而是知识状态**；与"完全/部分可观测"**不可混**（T4） |

#### 4. 智能体的四类结构

| English | 中文 | 备注 |
|---|---|---|
| simple reflex agent | 简单反射智能体 | ⚠️ 备选"简单反应式智能体"；本表取"反射"（与 reflex=反射、先天反射一致） |
| condition–action rule | 条件–动作规则 | 脚注 6：亦称 situation–action rules / productions / if–then rules |
| interpret input / rule match | 解释输入 / 规则匹配 | `INTERPRET-INPUT` / `RULE-MATCH`（伪代码标识符不译） |
| internal state | 内部状态 | ⚠️ 是"**最佳猜测**"，**不是确定的状态**（T4） |
| model-based reflex agent | 基于模型的反射智能体 | ⚠️ 选动作方式**与简单反射完全相同**，差别只在用什么匹配规则（T5） |
| model-based agent | 基于模型的智能体 | 上词的同义简称 |
| goal-based agent | 基于目标的智能体 | |
| goal | 目标 | 描述**合意的情形**；只给"高兴/不高兴"的**二元区分** |
| utility-based agent | 基于效用的智能体 | |
| utility function | 效用函数 | ✅ 已入主表；本章定义=**性能度量的内化** |
| model-free agent | 无模型智能体 | 第 22、26 章；⚠️ 基于效用**不一定**基于模型 |

#### 5. 学习智能体

| English | 中文 | 备注 |
|---|---|---|
| learning agent | 学习智能体 | |
| learning element | 学习元件 | ⚠️ 备选"学习部件""学习模块"；本表取"元件"（与 performance element 对称） |
| performance element | 性能元件 | 即此前认为的"整个智能体" |
| critic | 评价器 | ⚠️ 备选"评判器""批评者"；本表取"评价器" |
| problem generator | 问题生成器 | 建议**探索性动作** |
| performance standard | 性能标准 | ⚠️ 必须**固定**、概念上在智能体**之外** |
| penalty | 惩罚 | 与 reward=奖励 ✅（已入主表）配对 |

#### 6. 表示方式

| English | 中文 | 备注 |
|---|---|---|
| atomic representation | 原子表示 | 状态不可分割，黑箱 |
| factored representation | 因子化表示 | ⚠️ **主表内部冲突**：§3.1（第 7 章）作"因子化表示"，§3.4（第 11 章）作"**因袭**表示"并称"全书统一译法"。**建议统一为"因子化表示"**（"因袭"疑为笔误，且与 factor=因子 不合） |
| structured representation | 结构化表示 | ✅ 已入主表 |
| variable / attribute / value | 变量 / 属性 / 值 | 因子化表示的三件套 |
| expressiveness | 表达力 | ⚠️ 备选"表达性"；本表取"表达力" |
| localist representation | 局部化表示 | ⚠️ 备选"局部式表示"；概念↔存储位置**一对一** |
| distributed representation | 分布式表示 | 对噪声与信息丢失更鲁棒 |

#### 7. 专名与示例名

| English | 中文 | 备注 |
|---|---|---|
| vacuum-cleaner world | 真空吸尘器世界 | Figure 2.2；两方格 `A`/`B` |
| dung beetle | 蜣螂 | 内置假设被违反 → 行为失败 |
| sphex wasp | 泥蜂 | sphex 为泥蜂属；无法学到先天计划正在失败 |
| Champs Elysées | 香榭丽舍大街 | 全知 vs 理性 的例子 |
| Shakey the Robot | 机器人 Shakey | Fikes and Nilsson, 1971 |
| softbot | 软体机器人 | 见 §1 |

---

#### 待核清单（提交人工复核）

| # | 项 | 说明 |
|---|---|---|
| 1 | `factored representation` 译名冲突 | 主表 §3.1「因子化表示」vs §3.4「因袭表示」，需裁定并全书统一 |
| 2 | 全部三级小节中文译名 | 自拟，微信读书仅章级目录，**无法核对** |
| 3 | `episodic` 译"片段式" | 备选"回合式"；需对照中译本正文 |
| 4 | `critic` / `learning element` / `performance element` | 备选"评判器/学习部件/性能部件" |
| 5 | `localist representation` 译"局部化表示" | 备选"局部式表示" |
| 6 | `10^600,000,000,000` | PDF 文本层丢失上标，据 70 MB/s × 1 小时反推确认为 `10^600,000,000,000`（非 `10^600` 或 `10600…`），建议查勘误页 p.48 |
| 7 | `10^150`（国际象棋查找表）、`10^80`（可观测宇宙原子数）、`10^38`（原子语言写象棋规则的页数） | 同上，上标由 PDF 文本层丢失，依上下文确认为幂次 |

**合计新增：约 62 条**（其中 12 条为主表已有、本章仅补语境；实际新增约 50 条）。

### 3.3 第3章 通过搜索求解问题 Solving Problems by Searching

> **来源**：`第3章-通过搜索求解问题.md`（AIMA 4e 第 3 章，书页 64–111 / PDF idx 76–123）
> **说明**：本文件为**增量文件**，仅记录第 3 章新增（或术语表未收录）的条目。已有条目直接沿用，未改写。
> **不要修改** `AIMA-术语对照表.md`（多 agent 并发），由项目负责人统一合并。
> **判定流程**：按 `book-translation` skill §3 四步——① 查术语表（未命中）→ ② 查人邮 2022 中译本译法 → ③ 中文学界通行译法 → ④ 自拟（首现写「中文（English）」）。

---

#### 1. 新增术语总表

| English | 中文 | 备注 |
|---|---|---|
| problem-solving agent | 问题求解智能体 | 章首定义术语 |
| goal formulation | 目标形式化 | 四阶段之一；与 problem formulation 严格区分 |
| problem formulation | 问题形式化 | 四阶段之一 |
| search / execution | 搜索 / 执行 | 四阶段之三、四 |
| open-loop system / closed-loop | 开环系统 / 闭环 | 控制理论借词 |
| state space | 状态空间 | |
| initial state / goal state | 初始状态 / 目标状态 | |
| action / applicable | 动作 / 可用（的） | `ACTIONS(s)` 返回的动作在 `s` 中"可用" |
| transition model | 转移模型 | 与第 12 章同名术语一致；`RESULT(s, a)` |
| action cost function | 动作代价函数 | `ACTION-COST(s,a,s′)` / `c(s,a,s′)` |
| path / solution / optimal solution | 路径 / 解 / 最优解 | |
| abstraction | 抽象 | 有效抽象（valid）/ 有用抽象（useful）二分 |
| level of abstraction | 抽象层级 | |
| standardized problem / real-world problem | 标准化问题 / 真实世界问题 | |
| grid world | 网格世界 | |
| vacuum world | 吸尘器世界 | |
| sokoban puzzle | 推箱子 | 日文专名，用通行中文名 |
| sliding-tile puzzle | 滑块拼图 | |
| 8-puzzle / 15-puzzle | 八数码问题 / 十五数码问题 | 简称八数码、十五数码 |
| Rush Hour puzzle | Rush Hour 拼图 | 游戏名保留英文 |
| parity | 奇偶性 | 八数码状态空间二分为两半（习题 3.PART） |
| Knuth's "4" problem | Knuth 的「4」问题 | 人名保留英文 |
| route-finding problem | 寻路问题 | |
| touring problem | 巡游问题 | |
| traveling salesperson problem (TSP) | 旅行商问题 | 4e 用 salesperson；中文取通行译名"旅行商问题" |
| VLSI layout | VLSI 布局 | cell layout 单元布局 / channel routing 通道布线 |
| robot navigation | 机器人导航 | |
| automatic assembly sequencing | 自动装配排序 | |
| protein design | 蛋白质设计 | |
| search tree / state-space graph | 搜索树 / 状态空间图 | ⚠️ 二者不可混用（§3.3 明确区分） |
| node | 节点 | |
| expand / expansion | 扩展 | |
| child node / successor node / parent node | 子节点 / 后继节点 / 父节点 | |
| **frontier** | **边缘** | 🚫 不译"边界""前沿""开放列表"；原书脚注说明 open list 不恰当 |
| reached | 已到达 | 已为某状态生成过节点（无论是否已扩展） |
| interior / exterior | 内部 / 外部 | 由边缘分隔的两个区域 |
| separation property | 分隔性质 | |
| best-first search | 最佳优先搜索 | |
| evaluation function | 评价函数 | `f(n)` |
| priority queue / FIFO queue / LIFO queue | 优先队列 / FIFO 队列 / LIFO 队列 | LIFO 队列又称 stack 栈 |
| lookup table | 查找表 | 如哈希表 |
| repeated state | 重复状态 | |
| cycle / loopy path | 环 / 环路路径 | |
| redundant path | 冗余路径 | 环是冗余路径的特例 |
| graph search / tree-like search | 图搜索 / 树状搜索 | ⚠️ 按"是否检查冗余路径"区分，不按数据结构 |
| completeness | 完备性 | |
| cost optimality | 代价最优性 | ⚠️ 部分文献用 admissibility / optimality 指此性质，本书不采用 |
| time complexity / space complexity | 时间复杂性 / 空间复杂性 | |
| systematic | 系统性（的） | 完备算法在无穷空间上必须系统性 |
| branching factor | 分支因子 | `b` |
| depth / maximum depth | 深度 / 最大深度 | `d` / `m` |
| diameter | 直径 | 状态空间图上任意两点最短距离的最大值 |
| uninformed / informed search | 无信息 / 有信息搜索 | |
| breadth-first search | 广度优先搜索 | |
| early goal test / late goal test | 早期目标测试 / 晚期目标测试 | ⚠️ 影响一致代价搜索是否最优（Figure 3.10） |
| Dijkstra's algorithm / uniform-cost search | Dijkstra 算法 / 一致代价搜索 | 同一算法，两个学科的叫法 |
| depth-first search | 深度优先搜索 | |
| backtracking search | 回溯搜索 | |
| depth-limited search | 深度受限搜索 | 深度界限 `ℓ` |
| iterative deepening search | 迭代加深搜索 | |
| cutoff | （深度界限）截断值 | `DEPTH-LIMITED-SEARCH` 的第三种返回值 |
| bidirectional search | 双向搜索 | |
| heuristic function | 启发式函数 | `h(n)` |
| straight-line distance heuristic (`hSLD`) | 直线距离启发式 | |
| greedy best-first search | 贪婪最佳优先搜索 | |
| A* search | A\* 搜索 | 算法名保留 |
| **admissible heuristic** | **可采纳启发式** | 绝不高估到目标代价（= 乐观） |
| **consistent heuristic** | **一致性启发式** | `h(n) ≤ c(n,a,n′) + h(n′)`（三角形不等式） |
| monotonic heuristic | 单调启发式 | ⚠️ 与 consistent **等价**（Pearl, 1984），非另一个概念 |
| triangle inequality | 三角形不等式 | |
| contour | 等值线 | 地形图等高线类比 |
| surely expanded nodes | 必定被扩展的节点 | `f(n) < C*` |
| optimally efficient | 最优高效 | ⚠️ 不考虑 `f(n) = C*` 节点上的运气差别 |
| pruning | 剪枝 | |
| inadmissible heuristic | 不可采纳启发式 | |
| satisficing solution / satisficing search | 满意解 / 满意搜索 | 原书 4e §3.5.4 新增 |
| detour index | 绕行指数 | 多数地区 1.2–1.6 |
| weighted A* search | 加权 A\* 搜索 | `f = g + W×h`，`W > 1` |
| bounded suboptimal search | 有界次优搜索 | 保证在 `W×C*` 之内 |
| bounded-cost search | 有界代价搜索 | 代价 `< C` |
| unbounded-cost search | 无界代价搜索 | 只求快 |
| speedy search | 快速搜索 | 用"估计动作数"作启发式的贪婪变体 |
| reference count | 引用计数 | 用于从 `reached` 移除状态 |
| beam search | 束搜索 | 保留 `f` 最好的 `k` 个节点；变体用 `δ` 阈值 |
| iterative-deepening A* search (IDA*) | 迭代加深 A\* 搜索 | 算法名保留 |
| recursive best-first search (RBFS) | 递归最佳优先搜索 | 算法名保留 |
| backed-up value | 回传值 | RBFS / SMA\* 回卷时替换父节点 `f` 的值 |
| MA* / SMA* | 内存受限 A\* / 简化内存受限 A\* | 算法名保留 |
| thrashing | 颠簸 | 借自磁盘分页系统 |
| bidirectional heuristic search | 双向启发式搜索 | 4e §3.5.6 新增 |
| meet in the middle | 中间相遇 | |
| front-to-end / front-to-front | 前端到端 / 前端到前端 | ⚠️ 自拟译名，需与中译本核对 |
| bounding box | 包围盒 | 网格问题中概括边缘的方法 |
| misplaced tiles | 错位滑块数 | `h₁` |
| Manhattan distance / city-block distance | 曼哈顿距离 / 街区距离 | `h₂` |
| effective branching factor | 有效分支因子 | `b*` |
| effective depth | 有效深度 | `d − k_h` |
| domination / dominate | 占优 | `h₂ ≥ h₁` ⟹ `h₂` 占优 `h₁` |
| relaxed problem | 松弛问题 | 状态空间超图 |
| composite heuristic | 复合启发式 | `h = max{h₁,…,hₖ}` |
| subproblem | 子问题 | |
| pattern database | 模式数据库 | ✅ 术语表 §1.x 已有「pattern database = 模式数据库」，**沿用未改写** |
| disjoint pattern databases | 不相交模式数据库 | 只数涉及本子问题的移动 |
| precomputation | 预计算 | |
| landmark point | 地标（点） | 又称 pivots / anchors 枢点 / 锚点 |
| shortcuts | 捷径 | 人工边 |
| differential heuristic | 差分启发式 | `hDH(n) = max_L ｜C*(n,L) − C*(goal,L)｜` |
| metalevel state space | 元级状态空间 | |
| object-level state space | 对象级状态空间 | |
| metalevel learning | 元级学习 | |
| feature | 特征 | 机器学习语境，指状态的可计算属性 |
| coarse-to-fine search | 由粗到细搜索 | 出自文献注记 |
| iterative expansion (IE) | 迭代扩展 | 出自文献注记 |
| branch-and-bound | 分支限界 | 出自文献注记 |
| composite decision process (CDP) | 复合决策过程 | 出自文献注记 |

---

#### 2. 第 3 章小节标题中英对照

| 号 | English | 中文 | 核对状态 |
|---|---|---|---|
| 3 | Solving Problems by Searching | 通过搜索求解问题 | 自拟（与中译本章名待核） |
| 3.1 | Problem-Solving Agents | 问题求解智能体 | 自拟 |
| 3.1.1 | Search problems and solutions | 搜索问题与解 | 自拟 |
| 3.1.2 | Formulating problems | 问题形式化 | 自拟 |
| 3.2 | Example Problems | 示例问题 | 自拟 |
| 3.2.1 | Standardized problems | 标准化问题 | 自拟 |
| 3.2.2 | Real-world problems | 真实世界问题 | 自拟 |
| 3.3 | Search Algorithms | 搜索算法 | 自拟 |
| 3.3.1 | Best-first search | 最佳优先搜索 | 自拟 |
| 3.3.2 | Search data structures | 搜索数据结构 | 自拟 |
| 3.3.3 | Redundant paths | 冗余路径 | 自拟 |
| 3.3.4 | Measuring problem-solving performance | 问题求解性能的度量 | 自拟 |
| 3.4 | Uninformed Search Strategies | 无信息搜索策略 | 自拟 |
| 3.4.1 | Breadth-first search | 广度优先搜索 | 自拟 |
| 3.4.2 | Dijkstra's algorithm or uniform-cost search | Dijkstra 算法 / 一致代价搜索 | 自拟 |
| 3.4.3 | Depth-first search and the problem of memory | 深度优先搜索与内存问题 | 自拟 |
| 3.4.4 | Depth-limited and iterative deepening search | 深度受限搜索与迭代加深搜索 | 自拟 |
| 3.4.5 | Bidirectional search | 双向搜索 | 自拟 |
| 3.4.6 | Comparing uninformed search algorithms | 无信息搜索算法的比较 | 自拟 |
| 3.5 | Informed (Heuristic) Search Strategies | 有信息（启发式）搜索策略 | 自拟 |
| 3.5.1 | Greedy best-first search | 贪婪最佳优先搜索 | 自拟 |
| 3.5.2 | A\* search | A\* 搜索 | 自拟 |
| 3.5.3 | Search contours | 搜索等值线 | 自拟 |
| 3.5.4 | Satisficing search: Inadmissible heuristics and weighted A\* | 满意搜索：不可采纳启发式与加权 A\* | ⚠️ 4e 新增小节 |
| 3.5.5 | Memory-bounded search | 内存受限搜索 | 自拟 |
| 3.5.6 | Bidirectional heuristic search | 双向启发式搜索 | ⚠️ 4e 新增小节 |
| 3.6 | Heuristic Functions | 启发式函数 | 自拟 |
| 3.6.1 | The effect of heuristic accuracy on performance | 启发式精度对性能的影响 | 自拟 |
| 3.6.2 | Generating heuristics from relaxed problems | 由松弛问题生成启发式 | 自拟 |
| 3.6.3 | Generating heuristics from subproblems: Pattern databases | 由子问题生成启发式：模式数据库 | 自拟 |
| 3.6.4 | Generating heuristics with landmarks | 用地标生成启发式 | 自拟 |
| 3.6.5 | Learning to search better | 学习更好地搜索 | ⚠️ 4e 新增小节 |
| 3.6.6 | Learning heuristics from experience | 从经验中学习启发式 | ⚠️ 4e 新增小节 |

---

#### 3. 同形异义 / 易混对子（建议登记到术语表 §1.9）

| English | 含义 A | 含义 B | 备注 |
|---|---|---|---|
| **complete** | 搜索算法：保证找到解 | 逻辑系统：能推出所有被后承的句子（第 7 章） | 二者是**不同领域**的"完备"，不可互换定义 |
| **admissible** | 第 3 章：启发式不高估代价 | 部分文献：算法能找到最低代价解（本书不用此义，见 §3.3.4 脚注 7） | ⚠️ 必须按本书用法 |
| **consistent** | 第 3 章：启发式满足三角形不等式 | 第 7 章（逻辑）：知识库无模型 / 可满足 | ⚠️ 同形异义，须分列 |
| **monotonic** | 启发式：= consistent（等价） | 逻辑：加信息只增后承（第 7 章） | ⚠️ 同形异义，须分列 |
| **optimal** | 解：路径代价最低 | 算法：扩展节点数最少（optimally efficient） | 二者不等价 |
| **frontier** | 第 3 章：搜索树边缘 | 第 12 章 §12.7：方格类别 Known/**Frontier**/Other | ⚠️ 已在术语表登记，跨章复用时注意 |
| **state space** | 第 3 章：状态集合构成的图 | 第 4 章：state-space landscape 状态空间地形 | 相关但不同 |

---

#### 4. ⚠️ 待核项（需人工复核）

1. **`hSLD` 全部 20 个取值**：已用 PDF 坐标提取对 Figure 3.16 做了城市↔数值配对，并与 Figure 3.18 的 `g+h` 标注交叉验证了 10 个（Arad 366、Sibiu 253、Timisoara 329、Zerind 374、Fagaras 176、Rimnicu Vilcea 193、Pitesti 100、Craiova 160、Oradea 380、Bucharest 0）。其余 10 个（Giurgiu 77、Urziceni 80、Hirsova 151、Eforie 161、Iasi 226、Neamt 234、Drobeta 242、Mehadia 241、Lugoj 244、Vaslui 199）建议对照纸书 Figure 3.16 再确认一次。
2. **Figure 3.26 表格**：12 行 × 6 列数字来自归一化文本，顺序清晰（d 递增、BFS→A\*(h₁)→A\*(h₂)），但建议抽查 2–3 行对照原书。
3. **"31 次迭代"**：原文 "no more than 31 iterations on the hardest 8-puzzle problems" —— 与"最难的八数码问题需 31 步"这一常识一致（八数码最坏解长度 31），但原文表述是"不超过 `C*` 次迭代"，笔记按原文字面写。
4. **front-to-end / front-to-front** 中文译名为自拟，人邮中译本可能作"前端到端/前端到前端"或"面向终点/面向前沿"，待核。
5. **"satisficing"** 译"满意"——中文管理学/AI 文献亦作"满意化""次优满意"，需与中译本统一。
6. **"thrashing"** 在磁盘分页语境通行译"抖动"，本章取"颠簸"（更贴合"来回切换"的比喻）；如需全书统一可改。
7. Knuth 例子中的根号嵌套层数：PDF 文本层的根号符号提取为乱码（`/√adical…`），笔记中按原书公式写成 8 重根号，建议对照纸书核对层数。

---

#### 5. 本章重点自查的陷阱（对应 `pitfalls.md`）

| # | 类型 | 风险点 | 笔记中的处理 |
| - | ---- | ------ | ------------ |
| 1 | T5 近似概念混用 | complete vs optimal；admissible vs consistent/monotonic | 定义分开给；显式写"一致 ⟹ 可采纳，反之不然"；写"单调 = 一致的同义词" |
| 2 | T7 量化描述错 | Figure 3.15 复杂度表、Figure 3.26 数据表 | **逐字抄原文**表格，含 4 条上标脚注；Figure 3.26 全表抄录 |
| 3 | T2 缺步骤 | A\* 最优性反证、RBFS 回卷与回传、SMA\* 丢弃最差叶 | 反证法 5 行完整列出；RBFS 三步 (a)(b)(c) 与数值 417/450/447；SMA\* 微妙之处（扩展最新最佳叶、删除最旧最差叶）完整 |
| 4 | T1 方向颠倒 | 一致代价搜索必须**晚期**目标测试（早期则会返回次优解）；一致性不等号方向 `h(n) ≤ c + h(n′)` | 两处都按原文字面写并加"注意"提示 |
| 5 | T6 版本错 | 4e 新增 §3.5.4 weighted A\*、§3.5.6 双向启发式、§3.6.5–3.6.6 学习类内容 | 全部覆盖；未用 3e 结构 |
| 6 | T8 归属 | 文献内容混入正文 | 人物与成果全部放进「延伸阅读」，正文只保留原书论述；无作者发挥，故未使用 `【延伸·非原著】` 标记 |
| 7 | T3 性质误判 | 完备性在有限/无穷空间上的差别；"无解无穷空间下可靠算法必须永远搜索" | 按原文逐条列出（树形有限/无环/有环/无穷四种情形） |

### 3.4 第4章 复杂环境中的搜索 Search in Complex Environments

> 用途：本章新增术语的**暂存文件**，由负责人统一合并进 `AIMA-术语对照表.md`。
> **本人未修改 `AIMA-术语对照表.md`**（6 个 agent 并发，避免写坏）。
> 判定流程：`book-translation` skill §3（① 查术语表 → ② 查中译本 → ③ 查学界通行译法 → ④ 自拟并回填）。
> 标注说明：`【已有·沿用】`= 术语表中已有、直接沿用；`【通行】`= 中文学界强共识译法；`【自拟】`= 本项目自拟，建议合并前与中译本核对。

#### 4.1 局部搜索与最优化问题

| English | 中文 | 备注 |
|---|---|---|
| local search | 局部搜索 | 【通行】 |
| optimization problem | 最优化问题 | 【通行】 |
| objective function | 目标函数 | 【通行】 |
| state-space landscape | 状态空间地形 | 【自拟】3e 中译本亦作"状态空间地形图"；不译"景观"以免与计算机视觉 scene 混淆 |
| global maximum / global minimum | 全局极大值 / 全局极小值 | 【通行】 |
| hill climbing / gradient descent | 爬山 / 梯度下降 | 【通行】 |
| steepest ascent | 最陡上升 | 【通行】 |
| greedy local search | 贪婪局部搜索 | 【通行】 |
| complete-state formulation | 完整状态形式化 | 【自拟】 |
| local maximum | 局部极大值 | 【通行】⚠️ 与"局部最优解（local optimum）"区分：本章指地形上的峰 |
| ridge | 山脊 | 【通行】 |
| plateau | 高原 | 【通行】AIMA 中译本沿用 |
| shoulder | 山肩 | 【通行】 |
| "flat" local maximum | 平坦的局部极大值 | 【自拟】 |
| sideways move | 侧向移动 | 【通行】 |
| stochastic hill climbing | 随机爬山 | 【通行】 |
| first-choice hill climbing | 首选爬山 | 【通行】 |
| random-restart hill climbing | 随机重启爬山 | 【通行】 |
| simulated annealing | 模拟退火 | 【通行】 |
| schedule / cooling schedule | 调度 / 冷却调度 | 【通行】Figure 4.5 的 `schedule` 输入 |
| Boltzmann distribution | 玻尔兹曼分布 | 【通行】 |
| local beam search | 局部束搜索 | 【通行】 |
| stochastic beam search | 随机束搜索 | 【通行】 |
| evolutionary algorithms | 进化算法 | 【通行】 |
| genetic algorithm | 遗传算法 | 【通行】 |
| evolution strategies | 进化策略 | 【通行】 |
| genetic programming | 遗传编程 | 【通行】 |
| population / individual / offspring | 种群 / 个体 / 后代 | 【通行】 |
| fitness function | 适应度函数 | 【通行】 |
| fitness landscape | 适应度地形 | 【通行】仅出现在文献注释 |
| recombination | 重组 | 【通行】 |
| crossover / crossover point | 交叉 / 交叉点 | 【通行】 |
| mutation rate | 变异率 | 【通行】 |
| mixing number (ρ) | 混合数 ρ | 【自拟】ρ = 1 即随机束搜索（无性生殖） |
| elitism | 精英保留 | 【通行】亦译"精英主义"；本书语境取"保留上一代最优个体" |
| culling | 淘汰 | 【通行】 |
| schema / instance | 模式 / 实例 | 【通行】Holland 的 schema theorem 通译"模式定理" |
| Baldwin effect | 鲍德温效应 | 【通行】 |

#### 4.2 连续空间中的局部搜索

| English | 中文 | 备注 |
|---|---|---|
| discretization | 离散化 | 【通行】 |
| empirical gradient | 经验梯度 | 【自拟·直译】 |
| gradient | 梯度 | 【通行】 |
| step size (α) | 步长 α | 【通行】 |
| line search | 线搜索 | 【通行】 |
| Newton–Raphson method | 牛顿–拉弗森法 | 【通行】亦作"牛顿-拉夫逊法"；建议全书统一为"牛顿–拉弗森法" |
| Hessian (matrix) | 海塞矩阵 | 【通行】亦作"黑塞矩阵"；建议统一"海塞矩阵" |
| centroid | 质心 | 【通行】 |
| constrained optimization | 约束优化 | 【通行】 |
| linear programming | 线性规划 | 【通行】 |
| convex optimization | 凸优化 | 【通行】 |
| convex set / convex function | 凸集 / 凸函数 | 【通行】 |

#### 4.3 非确定性动作的搜索

| English | 中文 | 备注 |
|---|---|---|
| belief state | 信念状态 | 【已有·沿用】术语表 §1 / §3 均为"信念状态" |
| RESULTS function | RESULTS 函数 | 【沿用】ⓘ 与第 3 章返回单状态的 `RESULT` 对照，函数名保留英文 |
| conditional plan | 条件规划 | 【自拟】与术语表"online planning = 在线规划"体系一致 |
| contingency plan | 应变规划 | 【自拟】原书列为 conditional plan 的同义词 |
| strategy | 策略 | 【通行】原书亦列为 conditional plan 的同义词 |
| erratic vacuum world | 不稳定的真空吸尘器世界（erratic vacuum world） | 【自拟·待核】⚠️ 未与中译本核对；erratic 亦可读作"反复无常的"。首现已附英文 |
| slippery vacuum world | 打滑的真空吸尘器世界（slippery vacuum world） | 【自拟·待核】 |
| AND–OR tree / AND–OR graph | 与或树 / 与或图 | 【通行】 |
| OR node / AND node | 或节点 / 与节点 | 【通行】 |
| cyclic solution | 循环解 | 【通行】 |
| acyclic solution | 无环解 | 【自拟】与 cyclic solution 对举 |
| dead end | 死端 | 【自拟】⚠️ 4.5 亦用；亦译"死胡同"。建议统一"死端" |

#### 4.4 部分可观测环境中的搜索

| English | 中文 | 备注 |
|---|---|---|
| sensorless problem | 无传感问题 | 【已有·沿用】术语表"sensorless planning = 无传感规划"，同族一致 |
| conformant problem | conformant 问题 | 【已有·沿用】术语表"conformant planning = conformant 规划"保留英文 |
| coercion / coerce | 强制 | 【自拟】"coerce the world into state 7" 译"把世界强制到状态 7" |
| possibly achieve / necessarily achieve | 可能达成 / 必然达成 | 【自拟】⚠️ 二者是目标测试的两个不同强度，不可混用（T5） |
| incremental belief-state search | 增量式信念状态搜索 | 【自拟】 |
| local-sensing vacuum world | 局部感知真空吸尘器世界 | 【自拟·待核】 |
| kindergarten vacuum world | 幼儿园真空吸尘器世界 | 【自拟·待核】原书自造示例名 |
| prediction stage / possible percepts stage / update stage | 预测阶段 / 可能感知阶段 / 更新阶段 | 【自拟】与术语表"filtering / prediction / smoothing = 滤波 / 预测 / 平滑"一致 |
| PREDICT / POSSIBLE-PERCEPTS / UPDATE | PREDICT / POSSIBLE-PERCEPTS / UPDATE | 【沿用】函数名保留英文 |
| recursive state estimator | 递归状态估计器 | 【自拟】 |
| monitoring / filtering / state estimation | 监视 / 滤波 / 状态估计 | 【已有·沿用】"filtering = 滤波"已在术语表 |
| localization | 定位 | 【通行】 |

#### 4.5 在线搜索智能体与未知环境

| English | 中文 | 备注 |
|---|---|---|
| offline search / online search | 离线搜索 / 在线搜索 | 【已有·沿用】术语表"online planning = 在线规划" |
| mapping problem | 建图问题 | 【自拟】 |
| competitive ratio | 竞争比 | 【通行】在线算法理论标准术语 |
| adversary argument | 对手论证 | 【通行】 |
| irreversible action | 不可逆动作 | 【自拟·直译】 |
| safely explorable | 安全可探索（的） | 【自拟】"some goal state is reachable from every reachable state" |
| random walk | 随机游走 | 【通行】 |
| learning real-time A* (LRTA*) | 学习实时 A*（LRTA*） | 【自拟】算法名保留 LRTA* |
| optimism under uncertainty | 不确定性下的乐观 | 【自拟】ⓘ 第 17/22 章强化学习的同名策略请沿用此译法 |
| incremental search | 增量搜索 | 【自拟】与"增量式信念状态搜索"保持"增量"词根 |
| tabu search | 禁忌搜索 | 【通行】仅出现在文献注释 |
| heavy-tailed distribution | 重尾分布 | 【通行】仅出现在文献注释 |
| Eulerian graph | 欧拉图 | 【通行】仅出现在文献注释 |

#### 建议登记到「同形异义」节

| English | 语境 A | 语境 B |
|---|---|---|
| hill climbing | 4.1 目标函数为"值"，爬向极大 → **爬山** | 目标函数为"代价"时改称 **梯度下降**（同一算法家族的两种说法） |
| local maximum | 4.1 地形上的峰 → **局部极大值** | 泛称"局部最优"，⚠️ 不要写成"局部最优解"而丢失"极大/极小"方向 |
| online | 4.5 = 必须随输入到达就处理 → **在线** | ⚠️ **与"有互联网连接"无关**（原书脚注 8 特别声明） |
| strategy | 4.3 = conditional plan 的同义词 → **策略** | 第 5/17 章博弈与决策论中的"策略"是另一个技术含义 |

#### 建议登记到「禁用译法」节

| 禁用 | 用 | 理由 |
|---|---|---|
| 一致性规划 | conformant 规划 / 无传感规划 | 术语表已定 conformant 保留英文；"一致性"易与逻辑 consistency 混淆 |
| 局部最优（泛指） | 局部极大值 / 局部极小值 | 需保留方向 |
| 束搜索（不加限定） | 局部束搜索 | 与第 3 章的 beam search 区分 |
| 实时 A* | 学习实时 A*（LRTA*） | LRTA* 的 L 是 learning，不能丢 |

### 3.5 第5章 对抗搜索和博弈 Adversarial Search and Games

> **用途**：本章（AIMA 4e Chapter 5）新增术语的**增量文件**，供统一合并进 `AIMA-术语对照表.md`。
> **不得由本文件直接改写主术语表**——多人并发会写坏文件。
> **方法论**：`book-translation` skill §3 四步判定流程（主表 → 中译本 → 学界通行 → 自拟）。
> 标注：✅ = 已与中译本/权威源核对；⚠️ = 学界有分歧或本章自拟；🚫 = 禁用译法。

- **源**：`Artificial-Intelligence-A-Modern-Approach-4th.pdf`，Chapter 5，书页 146–179（PDF idx 158–191）
- **权威目录**：`https://aima.cs.berkeley.edu/contents.html`（小节编号已核对，与本文档一致）
- **章名**：第 5 章 对抗搜索和博弈 ✅（微信读书官方章名）
- **版本**：v1.0 / 2026-10-07

---

#### 1. 新术语总表

| English | 中文 | 备注 |
|---|---|---|
| adversarial search | 对抗搜索 | 章名术语 ✅ |
| game (formal) | 博弈 | 与第 18 章 game theory（博弈论）同源 |
| economy (stance) | 经济（立场） | 指"把大量智能体聚合成经济体"的立场 |
| deterministic, two-player, turn-taking, perfect information, zero-sum game | 确定性、双人、轮流、完美信息、零和博弈 | 5.1.1 的核心限定语 |
| perfect information | 完美信息 | ⚠️ 原书：是 fully observable 的**同义词**；🚫 不与 imperfect information 混用 |
| imperfect information | 不完全信息 | ⚠️ 部分作者用它专指"私有信息"（扑克） |
| partially observable game | 部分可观测博弈 | ⚠️ 部分作者用它专指"看得见近处、看不见远处"（《星际争霸 II》）；与上行**分列** |
| zero-sum | 零和 | 原书脚注：严格说是"常和"，零和为传统说法 |
| move / position / ply | 走法 / 局面 / ply（层） | ⚠️ move = action 同义、position = state 同义；ply = "**一方**走一步"（部分博弈里 move 指双方各一步） |
| initial state `S0` | 初始状态 | |
| `TO-MOVE(s)` | 轮到谁走 | |
| terminal test / terminal state | 终止测试 / 终止状态 | |
| utility function / objective function / payoff function | 效用函数 / 目标函数 / 收益函数 | utility/payoff 已入主表 |
| state space graph / search tree / game tree | 状态空间图 / 搜索树 / 博弈树 | |
| contingent strategy | 应变策略 | ⚠️ 与第 11 章 contingent planning（应变规划）保持一致 |
| minimax search / minimax value / minimax decision | minimax 搜索 / minimax 值 / minimax 决策 | 算法名 minimax 保留英文（主表规则：算法名不译） |
| backed-up value | 回传值 | |
| branching factor | 分支因子 | |
| utility vector | 效用向量 | |
| alliance | 联盟 | |
| pruning | 剪枝 | 主表 §11.3.1 已有"领域无关的剪枝"，本章同一译法 |
| alpha–beta pruning | alpha–beta 剪枝 / α–β 剪枝 | ✅ |
| alpha cutoff / beta cutoff | α 剪枝 / β 剪枝 | ⚠️ **T1 高危**：MAX 层 `v ≥ β` 是 **β 剪枝**；MIN 层 `v ≤ α` 是 **α 剪枝** |
| move ordering | 走法排序 | ⚠️ 自拟（备选"动作排序"）；本章 move 统一译"走法"，故取"走法排序" |
| killer move / killer move heuristic | 杀手走法 / 杀手走法启发式 | ⚠️ 自拟（备选"关键走法"） |
| transposition / transposition table | 变位 / 变位表 | ⚠️ 棋界常译"置换表"；本项目取直译"变位表" |
| Type A strategy / Type B strategy | A 型策略 / B 型策略 | Shannon (1950)：A = 宽而浅、B = 深而窄 |
| heuristic alpha–beta tree search | 启发式 alpha–beta 树搜索 | |
| evaluation function `EVAL` | 评估函数 | ⚠️ 与第 3 章 heuristic function（启发式函数）区分 |
| cutoff test | 截断测试 | |
| H-MINIMAX | 启发式 minimax 值 | 符号保留 |
| feature / equivalence class | 特征 / 等价类（类别） | |
| expected value | 期望值 | 已入主表（第 16 章），本章同一译法 |
| material value | 子力价值 | |
| weighted linear function | 加权线性函数 | |
| quiescence / quiescent / quiescence search | 静态性 / 静态局面 / 静态搜索 | ⚠️ 备选"平静搜索"；计算机象棋中文文献通行"静态搜索" |
| horizon effect | 地平线效应 | |
| singular extension | 奇异延伸 | ⚠️ 自拟直译（备选"单步延伸"） |
| forward pruning | 前向剪枝 | 主表 §3 p.355 已收录（第 11 章），本章同一译法 |
| beam search | 集束搜索 | |
| PROBCUT / probabilistic cut | PROBCUT / 概率剪枝 | 算法名保留 |
| late move reduction | 后手走法缩减 | ⚠️ 自拟直译 |
| retrograde minimax search | 逆向 minimax 搜索 | |
| reverse move | 逆着 | |
| policy (endgame) | 策略（残局语境：状态 → 最佳走法的映射） | 主表 policy=策略；本章为映射义，需注明 |
| Monte Carlo tree search (MCTS) | 蒙特卡洛树搜索 | 缩写 MCTS 可直接使用 |
| simulation / playout / rollout | 模拟（playout / rollout） | ⚠️ 三者同义，均指"从某状态走到终局的一次完整对局"；playout/rollout 建议行文保留英文 |
| playout policy | 模拟策略 | |
| selection policy | 选择策略 | |
| pure Monte Carlo search | 纯蒙特卡洛搜索 | |
| selection / expansion / simulation / back-propagation | 选择 / 扩展 / 模拟 / 回传 | MCTS 四阶段 |
| UCT (upper confidence bounds applied to trees) | UCT | 缩写保留 |
| UCB1 | UCB1 | 公式名保留 |
| early playout termination | 早期模拟终止 | |
| stochastic game | 随机博弈 | |
| chance node | 机会节点 | |
| expectiminimax (value) | expectiminimax（值）/ 期望 minimax | ⚠️ 学界常译"期望最小最大"；本项目建议保留 expectiminimax 并括注"期望 minimax" |
| positive linear transformation | 正线性变换 | |
| bluff | 诈唬 | |
| guaranteed checkmate | 保证将死 | |
| probabilistic checkmate | 概率将死 | |
| accidental checkmate | 偶然将死 | |
| equilibrium (solution) | 均衡（解） | 主表已有 Nash equilibrium（纳什均衡） |
| averaging over clairvoyance | 对超视者取平均 | ⚠️ 自拟直译 |
| abstraction | 抽象 | |
| utility of a node expansion | 节点扩展的效用 | |
| metareasoning | 元推理 | |

---

#### 2. 第 5 章小节标题中英对照

> 英文编号来自官方 TOC（信源 B，权威）；中文译名为**自拟**，除章名外未与中译本正文核对。

| 号 | English | 中文 |
|---|---|---|
| 5 ✅ | Adversarial Search and Games | 对抗搜索和博弈 |
| 5.1 | Game Theory | 博弈论 |
| 5.1.1 | Two-player zero-sum games | 双人零和博弈 |
| 5.2 | Optimal Decisions in Games | 博弈中的最优决策 |
| 5.2.1 | The minimax search algorithm | minimax 搜索算法 |
| 5.2.2 | Optimal decisions in multiplayer games | 多人博弈中的最优决策 |
| 5.2.3 | Alpha–Beta Pruning | Alpha–Beta 剪枝 |
| 5.2.4 | Move ordering | 走法排序 |
| 5.3 | Heuristic Alpha–Beta Tree Search | 启发式 Alpha–Beta 树搜索 |
| 5.3.1 | Evaluation functions | 评估函数 |
| 5.3.2 | Cutting off search | 截断搜索 |
| 5.3.3 | Forward pruning | 前向剪枝 |
| 5.3.4 | Search versus lookup | 搜索 vs 查表 |
| 5.4 | Monte Carlo Tree Search | 蒙特卡洛树搜索 |
| 5.5 | Stochastic Games | 随机博弈 |
| 5.5.1 | Evaluation functions for games of chance | 机会博弈的评估函数 |
| 5.6 | Partially Observable Games | 部分可观测博弈 |
| 5.6.1 | Kriegspiel: Partially observable chess | Kriegspiel：部分可观测的国际象棋 |
| 5.6.2 | Card games | 纸牌博弈 |
| 5.7 | Limitations of Game Search Algorithms | 博弈搜索算法的局限 |

---

#### 3. 建议登记的同形异义 / 易混对子（T5）

| English | 语境 A | 语境 B |
|---|---|---|
| **pruning** | α–β 剪枝：剪掉**可证明无影响**的分支（结果不变） | 前向剪枝：剪掉**可能好**的走法（结果可能错） |
| **strategy** | 博弈树语境：条件计划 / 应变策略 | 残局表语境：状态 → 最佳走法的**映射**（policy） |
| **imperfect information** | 私有信息（扑克） | —（部分作者与 partially observable 对调） |
| **utility** | 博弈终局给玩家的数值（第 5 章） | 决策论中的偏好度量（第 16 章）——同一译法"效用" |

---

#### 4. 待人工复核项

1. **Figure 5.16**（p.173）的树形数值：PDF 文本层无数值，正文只给出"右分支 `100`、左分支 `99`、右分支有四个叶"。需查中译本或勘误页补全叶子布局。
2. **Figure 5.12 双陆**（p.164）：正文说 "White has rolled a 6–5"，图注说 "Black has rolled 6–5"。疑原书不一致。
3. **p.162 MCTS 回传**：原书正文写 `27/35 becomes 28/26`，应为 `28/36`（印刷笔误）。
4. 三级小节中文译名（§2 全部）：未与中译本正文核对。

### 3.6 第6章 约束满足问题 Constraint Satisfaction Problems

> **用途**：第 6 章（约束满足问题）新增术语的待合并清单。
> **不得直接修改 `AIMA-术语对照表.md`**（6 个 agent 并发写该文件），由项目所有者统一合并。
> **判定流程**：`book-translation` skill §3 四步（查表 → 查中译本 → 查学界通行译法 → 自拟）。已有条目（agent=智能体、inference=推断、backtracking=回溯、treewidth=树宽、job-shop scheduling problem=作业车间调度问题）**直接沿用，未改写**。
> **来源**：`Artificial-Intelligence-A-Modern-Approach-4th.pdf`，书页 **180–207**（PDF idx 192–219）
> **章名定译**：第 6 章 约束满足问题（Constraint Satisfaction Problems）✅ 微信读书官方章名，已核实
> **版本**：v1.0 / 2026-10-07 ｜ 新增术语 **63 条**

---

#### 1. 新增术语总表

##### 1.1 CSP 形式体系（§6.1）

| English | 中文 | 备注 |
|---|---|---|
| constraint satisfaction problem (CSP) | 约束满足问题 | 章名 ✅ 权威 |
| factored representation | 因子化表示 | ⚠️ 沿用第 8 章增量表译法；第 11 章增量表作「因袭表示」，疑为笔误，建议统一为**因子化表示** |
| variable / domain / constraint | 变量 / 域 / 约束 | |
| scope / relation | 作用域 / 关系 | 约束 `Cⱼ = ⟨scope, rel⟩`；⚠️ scope 备选「论域」「范围」，本表取「作用域」 |
| assignment | 赋值 | |
| consistent (legal) assignment | 相容（合法）赋值 | |
| complete assignment | 完整赋值 | |
| partial assignment | 部分赋值 | |
| solution | 解 | 相容且完整的赋值 |
| partial solution | 部分解 | 相容的部分赋值 |
| constraint graph | 约束图 | |
| constraint hypergraph | 约束超图 | 普通节点 + 超节点（hypernode，代表 n 元约束） |
| hypernode | 超节点 | |
| job-shop scheduling | 作业车间调度 | ✅ 主表 §3.5 已有「作业车间调度问题」 |
| precedence constraint | 优先约束 | ⚠️ 备选「前驱约束」「时序优先约束」；本表取运筹学通行「优先约束」 |
| disjunctive constraint | 析取约束 | `T₁+d₁≤T₂ 或 T₂+d₂≤T₁` |
| discrete / finite / infinite domain | 离散 / 有限 / 无限域 | |
| continuous domain | 连续域 | |
| linear constraint | 线性约束 | |
| nonlinear constraint | 非线性约束 | ⚠️ T7：整数变量上一般非线性约束**不可判定**（原书明言，非"难解"） |
| linear programming | 线性规划 | 可在关于变量数**多项式**时间内求解 |
| unary / binary / ternary constraint | 一元 / 二元 / 三元约束 | |
| higher-order constraint | 高阶约束 | 三个及以上变量 |
| global constraint | 全局约束 | ⚠️ 原书自注：名字易误解——**不必**涉及全部变量 |
| binary CSP | 二元 CSP | 只含一元与二元约束 |
| Alldiff | Alldiff | 约束名保留不译 |
| Atmost | Atmost | 同上 |
| cryptarithmetic | 密码算术 | ⚠️ 备选「算式字谜」「竖式谜」；本表取「密码算术」 |
| dual graph transformation | 对偶图变换 | |
| preference constraint | 偏好约束 | 与 absolute constraint（绝对约束）对举 |
| absolute constraint | 绝对约束 | 违反即排除候选解 |
| constrained optimization problem (COP) | 约束优化问题 | |

##### 1.2 约束传播与一致性（§6.2）

| English | 中文 | 备注 |
|---|---|---|
| constraint propagation | 约束传播 | |
| local consistency | 局部一致性 | |
| node consistency | 节点一致性 | = 1-一致性 |
| arc consistency | 弧一致性 | = 2-一致性；⚠️ T1：**有方向**——`REVISE(Xᵢ,Xⱼ)` 只删减 `Dᵢ`，不动 `Dⱼ`；每条二元约束对应**两条**弧 |
| path consistency | 路径一致性 | 对二元约束图 = 3-一致性 |
| k-consistency | k-一致性 | |
| strongly k-consistent | 强 k-一致 | 需同时 k-, (k−1)-, …, 1-一致 |
| AC-3 / REVISE | AC-3 / REVISE | 算法/函数名保留；AC-3 得名于 Mackworth (1977) 论文中的第三个版本 |
| PC-2 | PC-2 | 算法名保留 |
| resource constraint | 资源约束 | 即 Atmost 约束 |
| bounds propagation | 界传播 | |
| bounds-consistent | 界一致 | |
| Sudoku | 数独 | |
| unit | 单元 | 数独中的行、列或宫；⚠️ 与通用「单位」区分 |
| naked triples | 显性三元组 | ⚠️ 数独术语，备选「裸三元组」「显性三数组」；本质是强制 Alldiff 一致性的策略，**非数独专属** |

##### 1.3 回溯搜索（§6.3）

| English | 中文 | 备注 |
|---|---|---|
| backtracking search | 回溯搜索 | ✅ backtracking=回溯（主表沿用） |
| commutativity | 可交换性 | 动作顺序不影响结果；使叶子数从 `n!·dⁿ` 降回 `dⁿ` |
| minimum-remaining-values (MRV) | 最小剩余值 | 别名 most constrained variable=**最受约束变量**、fail-first=**失败优先** |
| degree heuristic | 度启发式 | 选与最多未赋值变量有约束者；常作 MRV 的**平局打破**手段 |
| least-constraining-value | 最小约束值 | 选给邻居排除最少选择的值 |
| forward checking | 向前检查 | ⚠️ T1：赋值 `X` 后删减的是**未赋值邻居 `Y` 的域** |
| Maintaining Arc Consistency (MAC) | MAC（维持弧一致性） | ⚠️ T1：队列初始只含弧 `(Xⱼ,Xᵢ)`（**从邻居指向 `Xᵢ`**）；严格强于向前检查 |
| chronological backtracking | 时序回溯 | 重访最近的决策点 |
| conflict set | 冲突集 | |
| backjumping | 回跳 | ⚠️ T2：在用了向前检查/MAC 的搜索中**是冗余的**（被剪掉的分支也被向前检查剪掉） |
| conflict-directed backjumping | 冲突导向回跳 | `conf(Xᵢ) ← conf(Xᵢ) ∪ conf(Xⱼ) − {Xᵢ}` |
| constraint learning | 约束学习 | |
| no-good | no-good | 保留英文（主表 §3.1 已有「no-good 学习」） |

##### 1.4 局部搜索与结构（§6.4–6.5）

| English | 中文 | 备注 |
|---|---|---|
| min-conflicts | 最小冲突 | 启发式名 |
| plateau / sideways move | 高原 / 侧向移动 | |
| tabu search | 禁忌搜索 | ⚠️ 备选「tabu 搜索」，本表取通行「禁忌搜索」 |
| constraint weighting | 约束加权 | |
| independent subproblem | 独立子问题 | |
| connected component | 连通分量 | |
| directional arc consistency (DAC) | 有向弧一致性 | Dechter & Dechter (1987) |
| topological sort | 拓扑排序 | |
| cycle cutset | 环割集 | ⚠️ 与主表 §1.1 的 treewidth=树宽配套；割集大小 `c`，最坏可达 `n−2` |
| cutset conditioning | 割集条件化 | 第 13 章概率推理中再次出现 |
| tree decomposition | 树分解 | |
| tree width | 树宽 | ✅ 主表 §1.1 已有；原书补：= 最大节点大小 **减一**，图的树宽 = 所有分解中的最小宽度 |
| value symmetry | 值对称 | |
| symmetry-breaking constraint | 对称破缺约束 | |
| dependency-directed backtracking | 依赖导向回溯 | Stallman & Sussman (1977) |
| backmarking | 回标记 | Gaschnig (1979) |
| dynamic backtracking | 动态回溯 | Ginsberg (1993) |
| hypertree width | 超树宽 | Gottlob et al. (1999a,b)；原书：`O(nʷ⁺¹ log n)` |

---

#### 2. 同形异义必须分列（第 6 章新增）

| English | 语境 A | 语境 B |
|---|---|---|
| **consistency** | CSP → **一致性**（node/arc/path/k-，是**必要非充分**条件，弧一致仍可能无解） | 逻辑 → 一致性（可满足性） |
| **unit** | 数独 → **单元**（行/列/宫） | 通用 → 单位 |
| **scope** | CSP 约束 → **作用域**（参与约束的变量元组） | 逻辑量词 → 辖域 |
| **degree** | 度启发式 → **度**（约束图中变量的邻居数） | 通用 → 程度/次数 |
| **complete** | CSP → **完整赋值**（每个变量都已赋值） | 逻辑 → **完备**（completeness） |
| **solution** | CSP → **解**（相容且完整的赋值） | 通用 → 解决方案 |
| **conflict** | 冲突集 → **冲突**（被违反的约束关系） | 最小冲突 → **冲突数**（违反的约束条数） |

---

#### 3. 第 6 章小节标题中英对照

> 英文编号来自原书（权威，与官方 TOC 一致）。二级章名 ✅ 已核实（微信读书官方章名）；三级中文译名**为自拟**，未与中译本正文核对（信源 D 仅目录可用）。

##### 第 6 章 约束满足问题（Constraint Satisfaction Problems）✅

| 号 | English | 中文 |
|---|---|---|
| 6.1 | Defining Constraint Satisfaction Problems | 定义约束满足问题 |
| 6.1.1 | Example problem: Map coloring | 示例问题：地图着色 |
| 6.1.2 | Example problem: Job-shop scheduling | 示例问题：作业车间调度 |
| 6.1.3 | Variations on the CSP formalism | CSP 形式体系的变体 |
| 6.2 | Constraint Propagation: Inference in CSPs | 约束传播：CSP 中的推断 |
| 6.2.1 | Node consistency | 节点一致性 |
| 6.2.2 | Arc consistency | 弧一致性 |
| 6.2.3 | Path consistency | 路径一致性 |
| 6.2.4 | K-consistency | k-一致性 |
| 6.2.5 | Global constraints | 全局约束 |
| 6.2.6 | Sudoku | 数独 |
| 6.3 | Backtracking Search for CSPs | CSP 的回溯搜索 |
| 6.3.1 | Variable and value ordering | 变量与值排序 |
| 6.3.2 | Interleaving search and inference | 搜索与推断交错进行 |
| 6.3.3 | Intelligent backtracking: Looking backward | 智能回溯：向后看 |
| 6.3.4 | Constraint learning | 约束学习 |
| 6.4 | Local Search for CSPs | CSP 的局部搜索 |
| 6.5 | The Structure of Problems | 问题的结构 |
| 6.5.1 | Cutset conditioning | 割集条件化 |
| 6.5.2 | Tree decomposition | 树分解 |
| 6.5.3 | Value symmetry | 值对称 |

---

#### 4. ⚠️ 待核项（需人工复核）

| # | 位置 | 问题 | 笔记中的处理 |
|---|---|---|---|
| 1 | §6.2.2（书 p.187，Figure 6.3） | `REVISE` 中 `revised ← true` 写在 `for` 循环**之外**，按字面函数恒返回 true（与第 3 版同） | 伪代码**逐字照录**未改，另在正文中以 ⚠️ 标出，并注明"实际实现通常置于 delete 分支内" |
| 2 | §6.5（书 p.199） | PDF 文本层丢失上标：`O(dcn/c)`、`O(dn)`、`n!·dn` | 据上下文还原为 `O(dᶜ·n/c)`、`O(dⁿ)`、`n!·dⁿ` |
| 3 | §6.1.1（书 p.181） | 同上：`35 = 243`、`25 = 32` | 还原为 `3⁵ = 243`、`2⁵ = 32`；32/243 ≈ 13.2%，与"减少 87%"一致 ✅ |
| 4 | §6.2.4（书 p.188） | `O(n2d)` | 还原为 `O(n²d)`（PDF 丢上标） |
| 5 | §6.5.2（书 p.202） | `d = 210`（10 个布尔变量） | 还原为 `d = 2¹⁰` |
| 6 | §6.4（书 p.197） vs 历史注释（书 p.206） | 正文说"百万皇后平均 50 步"，历史注释说 Sosic & Gu (1994) 解 **3,000,000 皇后**不到一分钟 | 两处**各自照录**，未统一（原书两处数字本来就不同） |
| 7 | 全部三级标题 | 中文译名均为自拟，未与中译本核对 | 已在 §3 表头声明 |
| 8 | 章节页码边界 | 任务描述为书页 182–209；按页眉核对，第 6 章正文实际为 **180–207**（PDF idx 192–219，idx 220 为 CHAPTER 7 起始） | 已按页眉实际边界提取，未遗漏章首（§6.1 定义在 p.180–181） |

---

#### 5. 本章重点自查的陷阱（对应 `references/pitfalls.md`）

| # | 类型 | 检查点 | 结果 |
|---|---|---|---|
| 1 | T1 方向颠倒 | 弧一致性 `Xᵢ → Xⱼ` 的方向：`REVISE(Xᵢ,Xⱼ)` 只删 `Dᵢ`；每条二元约束 = 两条弧 | ✅ 已在 6.2.2 加"注意方向"提示 |
| 2 | T1 方向颠倒 | AC-3 缩减 `Dᵢ` 后入队的是 `(Xₖ,Xᵢ)`（邻居 → `Xᵢ`），**排除 `Xⱼ`** | ✅ 逐步说明第 4 点已明确 |
| 3 | T1 方向颠倒 | MAC 初始队列是弧 `(Xⱼ,Xᵢ)`（邻居 → 已赋值变量），使 `REVISE` 缩减**邻居**的域 | ✅ 已注明方向 |
| 4 | T1 方向颠倒 | 向前检查：赋值 `X` 后删的是**未赋值邻居 `Y`** 的域 | ✅ 已注明 |
| 5 | T1 方向颠倒 | 冲突导向回跳 `conf(Xᵢ) ← conf(Xᵢ) ∪ conf(Xⱼ) − {Xᵢ}` 的吸收方向 | ✅ 公式与四步示例均照录 |
| 6 | T2 缺步骤 | AC-3 的入队条件（仅 `Dᵢ` 变化时）与终止条件（队列空 / `Dᵢ` 为空） | ✅ 七步逐步说明 |
| 7 | T2 缺步骤 | 回跳 vs 冲突导向回跳的判定（后者用于"域未空但分支已注定失败"） | ✅ 已用 `{WA=red,NSW=red}` 示例区分 |
| 8 | T5 近似概念混用 | node / arc / path / k-一致性的严格层级（1=node, 2=arc, 3=path 仅对**二元约束图**成立） | ✅ 已列表并注明"对二元约束图"这一限定 |
| 9 | T3 性质误判 | 弧一致 ≠ 可满足（两色弧一致仍无解） | ✅ 已加 ⚠️ 提示 + 6.2.3 反例 |
| 10 | T7 量化描述错 | `O(cd³)`、`O(n²d)`、`O(nd²)`、`O(dᶜ·(n−c)d²)`、`O(ndʷ⁺¹)`、"树状 CSP 可线性求解" | ✅ 逐字照录，未改写措辞 |
| 11 | T7 量化描述错 | 非线性整数约束是**不可判定**（不是 NP-hard / 指数时间） | ✅ 逐字照录 |
| 12 | T8 归属 | 作者发挥一律标 `【延伸·非原著】` | ✅ 本章**未添加**任何原著外内容，无需标注 |

---

#### 7. 变更记录

| 版本 | 日期 | 变更 |
|---|---|---|
| v1.0 | 2026-10-07 | 初版。63 条新术语 + 7 组同形异义 + 第 6 章 21 条小节标题对照 + 8 项待核 + 12 条陷阱自查记录。 |


---

## 4. 第 7–11 章（Part III）术语补充

> Part III = **Knowledge, reasoning, and planning**（知识、推理与规划）。
> 由 5 个章节翻译 agent 按 `book-translation` skill §3 四步流程产出，本表 §1 覆盖 11–18 章，故 Part III 术语单列于此。
> ⚠️ 这些译名**多数未与中译本正文核对**（信源 D 只能拿到章级目录），属自拟译法；对照纸书后请以中译本为准并回填。

### 4.1 第7章 逻辑智能体

> 本章新增术语，待统一合并入 `AIMA-术语对照表.md`。
> 格式：`| English | 中文 | 备注 |`
> 判定流程：`book-translation` skill §3。已有条目直接沿用（agent=智能体、inference 精确语境=推断、model 逻辑语境=模型、wumpus 不译保留小写）。
> ⚠️ = 中译本未逐条核对（信源 D 仅目录可用），译名为自拟，需对照中译本正文确认。

### 1. 知识库与推断

| English | 中文 | 备注 |
|---|---|---|
| knowledge-based agent | 基于知识的智能体 | 章名"逻辑智能体"为中译本权威译法 |
| knowledge base (KB) | 知识库 | |
| sentence | 句子 | 技术术语，与英语句子相关但不等同 |
| axiom | 公理 | |
| knowledge representation language | 知识表示语言 | |
| assertion | 断言 | |
| inference | 推断 | ✅ 已入总表（精确语境） |
| entailment | 后承 | ⚠️ 中译本译法待核（另有"蕴含"通行译法）；符号 `\|=` 读作"后承" |
| model | 模型 | ✅ 已入总表 §1.9（逻辑语境=模型，数学抽象、指派） |
| possible world | 可能世界 | |
| satisfaction | 满足 | |
| sound / truth-preserving | 可靠 / 保真 | |
| complete / completeness | 完备 / 完备性 | |
| proof | 证明 | |
| inference rule | 推断规则 | |
| monotonicity | 单调性 | |

### 2. 命题逻辑

| English | 中文 | 备注 |
|---|---|---|
| propositional logic | 命题逻辑 | |
| proposition symbol | 命题符号 | |
| atomic sentence / complex sentence | 原子句子 / 复合句子 | |
| logical connective | 连接词 | ⚠️ 中译本译法待核 |
| truth table | 真值表 | |
| exclusive or (xor) | 异或 | |
| logical equivalence | 逻辑等价 | 符号 `≡`；与 `⇔` 区分（`⇔` 是句子内部的一部分） |
| reductio ad absurdum | 归谬法 | 即反证法（proof by refutation / proof by contradiction） |
| contrapositive | 逆否 | |

### 3. 归结与范式

| English | 中文 | 备注 |
|---|---|---|
| resolution | 归结 | |
| clause | 子句 | 文字的析取 |
| literal | 文字 | |
| complementary literals | 互补文字 | 一个是另一个的否定 |
| unit clause | 单元子句 | |
| factoring | 因子提取 | ⚠️ 中译本译法待核 |
| conjunctive normal form (CNF) | 合取范式 | |
| k-CNF | k-CNF | 每子句至多 k 个文字的 CNF |
| empty clause | 空子句 | 等价于 False |

### 4. 霍恩子句与链式推断

| English | 中文 | 备注 |
|---|---|---|
| Horn clause | 霍恩子句 | 至多一个正文字 |
| definite clause | 确定子句 | 恰一个正文字 |
| goal clause | 目标子句 | 无正文字 |
| body / head | 体 / 头 | 蕴含形式中前提=体、结论=头 |
| fact | 事实 | 单个正文字的句子 |
| forward-chaining | 前向链 | |
| backward-chaining | 后向链 | |
| goal-directed reasoning | 目标导向推理 | |
| agenda | 议程 | 前向链中的待处理符号队列 |

### 5. 有效模型检查

| English | 中文 | 备注 |
|---|---|---|
| Davis–Putnam algorithm | Davis–Putnam 算法 | 人名保留 |
| DPLL | DPLL | 算法名保留，四人首字母 |
| early termination | 提前终止 | |
| pure symbol | 纯符号 | |
| unit clause heuristic | 单元子句启发式 | |
| component analysis | 分量分析 | |
| intelligent backtracking | 智能回溯 | |
| no-good learning | no-good 学习 | |
| WALKSAT | WALKSAT | 算法名保留 |
| random walk | 随机游走 | |
| underconstrained | 约束不足 | |
| overconstrained | 过约束 | |
| thresholding effect | 阈值效应 | |
| clause/symbol ratio | 子句/符号比 | |
| survey propagation | 传播调查 | ⚠️ 中译本译法待核；文献中常保留英文 |

### 6. 逻辑智能体实现

| English | 中文 | 备注 |
|---|---|---|
| fluent | 流 | 源自拉丁语 *fluens*（流动）；"状态变量"的同义词，强调时间维度 |
| effect axiom | 效果公理 | |
| frame problem | 帧问题 | |
| frame axiom | 帧公理 | |
| successor-state axiom | 后继状态公理 | |
| qualification problem | 资格问题 | ✅ 已入总表（第 12 章） |
| hybrid agent | 混合智能体 | |
| belief state | 信念状态 | ✅ 已入总表（第 17 章 POMDP 语境）；本章为逻辑语境，同一译法 |
| conservative approximation | 保守近似 | |
| SATPLAN | SATPLAN | 算法名保留 |
| precondition axiom | 前提公理 | |
| action exclusion axiom | 动作互斥公理 | |
| atemporal | 不含时间的 / 非时间的 | ⚠️ 中译本译法待核 |
| percept | 感知 | ⚠️ 中译本译法待核 |

### 7. 人名（保留英文）

| English | 备注 |
|---|---|
| John McCarthy | "常识程序"（Programs with Common Sense） |
| Allen Newell | "知识级"（The Knowledge Level） |
| Gottlob Frege | 《概念文字》(Begriffschrift, 1879) |
| Alfred Horn | 霍恩子句 (1951) |
| J. A. Robinson | 一阶逻辑归结的完备性 (1965) |
| Stephen Cook | SAT 是 NP-complete (1971) |
| Selman | GSAT / WALKSAT |
| Ray Reiter | 后继状态公理解帧问题 (1991) |
| Stan Rosenschein | 电路智能体 / 后继状态公理 |
| Gregory Yob | wumpus 世界的发明者 (1975) |
| Michael Genesereth | 建议把 wumpus 世界用作智能体测试平台 |

### 8. 同形异义登记（并入总表 §1.9）

| English | 语境 A | 语境 B |
|---|---|---|
| **entailment** | 逻辑（本章）→ **后承** | 日常 → 蕴含 |
| **model** | 逻辑（第 7–8 章）→ **模型**（指派） | 概率 → 模型 |
| **inference** | 精确 → **推断** | 近似/章节名 → **推理** |
| **clause** | 逻辑 → **子句** | 通用 → 条款/从句 |
| **fact** | 逻辑（霍恩子句）→ **事实** | 通用 → 事实 |
| **resolution** | 逻辑 → **归结** | 通用 → 解决/分辨率 |

### 4.2 第8章 一阶逻辑

> **用途**：本章新增术语的待合并清单。**请勿修改 `AIMA-术语对照表.md`**（多 agent 并发），由项目所有者统一合并。
> **来源**：`Artificial-Intelligence-A-Modern-Approach-4th.pdf`，书页 251–279（PDF idx 263–291）
> **判定依据**：`book-translation` skill §3 四步流程。已有条目（agent=智能体、inference=推断 等）直接沿用，未改写。
> **版本**：v1.0 / 2026-10-07 ｜ 新术语 **76 条**（§1.1 表示语言 21 + §1.2 语法与语义 31 + §1.3 使用与知识工程 24），另登记同形异义 6 组、小节标题对照 27 条

---

### 1. 术语总表

#### 1.1 表示语言（§8.1）

| English | 中文 | 备注 |
|---|---|---|
| representation | 表示 | 沿用 |
| declarative | 声明式 | 与 procedural（过程式）对举 |
| procedural | 过程式 | |
| compositionality | 组合性 | |
| factored representation | 因子化表示 | 指命题逻辑 |
| structured representation | 结构化表示 | 指一阶逻辑、自然英语 |
| language of thought | 思想的语言 | ⚠️ 待核：中文哲学界也作"思想语言""思维语言"，需与中译本核对 |
| Sapir–Whorf hypothesis | 萨丕尔–沃尔夫假说 | 人名音译 + 保留英文 |
| Guugu Yimithirr | Guugu Yimithirr | 语言名保留原文 |
| object | 对象 | |
| relation | 关系 | |
| function | 函数 | |
| property | 性质 | 即一元关系（unary relation） |
| n-ary relation | n 元关系 | |
| ontological commitment | 本体论承诺 | ⚠️ 与下面的 ontology（本体）形近而义不同，不可合并 |
| epistemological commitment | 认识论承诺 | |
| degree of truth | 真值度 | ⚠️ **真值度 ≠ 信念度**（degree of belief）；前者属模糊逻辑，后者属概率论 |
| fuzzy logic | 模糊逻辑 | |
| temporal logic | 时序逻辑 | |
| higher-order logic | 高阶逻辑 | 严格强于一阶逻辑 |
| universe (of objects) | （对象的）宇宙 | 用于"关于宇宙中某些或全部对象" |

#### 1.2 语法与语义（§8.2）

| English | 中文 | 备注 |
|---|---|---|
| model | 模型 | 一阶逻辑中 = 一组对象 + 一个解释；⚠️ 与"概率模型"分列（见 §1.9） |
| domain | 域 | |
| domain element | 域元素 | |
| tuple | 元组 | |
| total function | 全函数 | |
| constant symbol | 常量符号 | |
| predicate symbol | 谓词符号 | |
| function symbol | 函数符号 | |
| arity | 元数 | |
| interpretation | 解释 | 模型的一部分，把符号映射到对象/关系/函数 |
| intended interpretation | 预期解释 | |
| extended interpretation | 扩展解释 | 给量词变量指定域元素 |
| term | 项 | |
| ground term | 基项 | 不含变量的项 |
| complex term | 复合项 | ⚠️ 是"复杂的名字"，**不是**返回值的子程序调用 |
| atomic sentence / atom | 原子句子 / 原子 | |
| complex sentence | 复合句子 | |
| quantifier | 量词 | |
| universal quantifier | 全称量词 | ∀ |
| existential quantifier | 存在量词 | ∃（变体 ∃¹ / ∃! = 恰好存在一个） |
| variable | 变量 | |
| equality symbol | 相等符号 | `=`，缩写 `≠` 表示 `¬(x = y)` |
| unique-names assumption | 唯一名称假设 | |
| closed-world assumption | 封闭世界假设 | |
| domain closure | 域闭包 | |
| database semantics | 数据库语义 | 与标准一阶语义相对 |
| entailment | 蕴涵（逻辑蕴涵） | ⚠️ 与联结词 `⇒`（蕴含）区分，见 §1.9 |
| sound | 可靠的 | soundness = 可靠性 |
| valid | 有效的 | validity = 有效性 |
| Backus–Naur form | Backus–Naur 范式 | 沿用 |
| λ-expression | λ 表达式 | 不增加一阶逻辑的形式表达力 |

#### 1.3 使用与知识工程（§8.3–8.4）

| English | 中文 | 备注 |
|---|---|---|
| assertion | 断言 | 用 TELL 加入的句子 |
| query / goal | 查询 / 目标 | |
| substitution / binding list | 代入 / 绑定列表 | |
| axiom | 公理 | |
| theorem | 定理 | |
| definition | 定义 | |
| domain（知识表示语境） | 域 | 世界中我们想表达知识的某个部分 |
| natural numbers | 自然数 | 即非负整数 |
| Peano axioms | 皮亚诺公理 | |
| successor | 后继 | 函数符号 S |
| prefix / infix | 前缀 / 中缀 | |
| syntactic sugar | 语法糖 | 不改变语义的语法扩展 |
| set | 集合 | |
| list | 列表 | |
| successor-state axiom | 后继状态公理 | |
| percept / perception | 感知 | 沿用第 7 章 |
| percept vector | 感知向量 | |
| knowledge engineering | 知识工程 | |
| knowledge engineer | 知识工程师 | |
| knowledge acquisition | 知识获取 | |
| ontology | 本体 | ⚠️ 指某域的"存在哪类事物"的理论；与 ontological commitment（本体论承诺）不同层 |
| circuit verification | 电路验证 | |
| Horn clause | Horn 子句 | 沿用 |
| TELL / ASK / ASKVARS | TELL / ASK / ASKVARS | 接口名保留原样 |

#### 1.9 本章新登记的同形异义

| English | 语境 A | 语境 B |
|---|---|---|
| **model** | 逻辑（第 8 章）→ **模型**（对象集 + 解释） | 概率（12–15 章）→ **模型**（概率模型） |
| **domain** | 逻辑 → **域**（模型中的对象集合） | 知识表示 → **域**（世界的某个部分） |
| **ontology** | 知识工程 → **本体**（域的词汇/存在理论） | ontological commitment → **本体论承诺**（语言关于现实的假设） |
| **inference** | 名词 → **推断**（推断过程、逻辑推断） | 固定复合术语 rules of inference → **推理规则** |
| **entailment / implies** | entailment → **蕴涵** | 联结词 `⇒` → **蕴含** |
| **degree of truth / degree of belief** | 模糊逻辑 → **真值度** | 概率论 → **信念度** |

---

### 2. 第 8 章小节标题中英对照

> 英文编号来自原书（权威）。二级中文译名按用户指定"第 8 章 一阶逻辑"体系；三级中文译名**为自拟**，未与中译本核对（微信读书仅能取到章级目录，见项目配置 §6 能力边界）。

##### 第 8 章 一阶逻辑（First-Order Logic）

| 号 | English | 中文 |
|---|---|---|
| 8.1 | Representation Revisited | 重新审视表示 |
| 8.1.1 | The language of thought | 思想的语言（⚠️ 待核） |
| 8.1.2 | Combining the best of formal and natural languages | 结合形式语言与自然语言之长 |
| 8.2 | Syntax and Semantics of First-Order Logic | 一阶逻辑的语法与语义 |
| 8.2.1 | Models for first-order logic | 一阶逻辑的模型 |
| 8.2.2 | Symbols and interpretations | 符号与解释 |
| 8.2.3 | Terms | 项 |
| 8.2.4 | Atomic sentences | 原子句子 |
| 8.2.5 | Complex sentences | 复合句子 |
| 8.2.6 | Quantifiers | 量词 |
| — | Universal quantification (∀) | 全称量化（∀）｜**原书无编号**，笔记用 `####` 呈现 |
| — | Existential quantification (∃) | 存在量化（∃）｜**原书无编号** |
| — | Nested quantifiers | 嵌套量词｜**原书无编号** |
| — | Connections between ∀ and ∃ | `∀` 与 `∃` 的联系｜**原书无编号** |
| 8.2.7 | Equality | 相等 |
| 8.2.8 | Database semantics | 数据库语义 |
| 8.3 | Using First-Order Logic | 使用一阶逻辑 |
| 8.3.1 | Assertions and queries in first-order logic | 一阶逻辑中的断言与查询 |
| 8.3.2 | The kinship domain | 亲属关系域 |
| 8.3.3 | Numbers, sets, and lists | 数、集合与列表 |
| 8.3.4 | The wumpus world | wumpus 世界 |
| 8.4 | Knowledge Engineering in First-Order Logic | 一阶逻辑中的知识工程 |
| 8.4.1 | The knowledge engineering process | 知识工程过程 |
| 8.4.2 | The electronic circuits domain | 电子电路域 |

---

### 3. ⚠️ 待核项（需人工复核）

| # | 位置 | 问题 | 笔记中的处理 |
|---|---|---|---|
| 1 | §8.3.3（书 p.268） | 原书正文说"二元函数符号 `+` **在项 `+(m,0)` 中的使用**"，但紧邻的公理写的是 `+(0,m) = m`。疑为原书笔误 | 按**公理正文**录为 `+(0,m) = m`，并在正文中以 `⚠️ 待核` 标出该不一致 |
| 2 | §8.4.2 调试（书 p.277） | 原书说"忘了断言 `1 ≠ 0` 后，系统除输入情形 **000 和 110** 之外证明不出任何输出"。该组合的合理性未独立验算 | 逐字照录，未做"修正" |
| 3 | §8.2.1 / §8.2.2（书 p.258） | "There are **25** possible interpretations"——PDF 版式丢失上标，实为 5² | 还原为 `5² = 25`，未改动数值 |
| 4 | §8.2.2（书 p.259） | "there are **137,506,194,466** models with six or fewer objects" | 逐字照录，建议对照纸书复核位数 |
| 5 | §8.1.1 译名 | "The language of thought" 有三种通行中译 | 取"思想的语言"，在表中标 ⚠️ |
| 6 | 全部三级标题 | 中文译名均为自拟，未与中译本核对 | 已在 §2 表头声明 |
| 7 | §8.2.6 四个子标题 | 原书该四处**无小节编号** | 用 `####`（四级、无编号）呈现，未自造编号 |

---

### 4. 本章翻译时重点自查的陷阱（对应 pitfalls.md）

| # | 类型 | 检查点 | 结果 |
|---|---|---|---|
| 1 | T1 方向颠倒 | `∀ x King(x) ⇒ Person(x)` 的蕴含方向；常见错误 `∀ x King(x) ∧ Person(x)` | ✅ 已保留并保留原书"最常见错误"提示 |
| 2 | T1 方向颠倒 | `∃ x Crown(x) ∧ OnHead(x,John)`；反过来用 `⇒` 得到过弱句子 | ✅ 已保留 |
| 3 | T1 方向颠倒 | `∀ x ∃ y Loves(x,y)` vs `∃ y ∀ x Loves(x,y)` | ✅ 已保留并加括号说明 |
| 4 | T1 方向颠倒 | 式 (8.4) `∀ s Breezy(s) ⇔ ∃ r Adjacent(r,s) ∧ Pit(r)` 的参数顺序 | ✅ `r` 为第一参数 |
| 5 | T1 方向颠倒 | 诊断规则写成 `⇒` 而非 `⇔` 导致"永远无法证明没有 wumpus" | ✅ 已保留 |
| 6 | T1 方向颠倒 | `∀ x NumOfLegs(x,4) ⇒ Mammal(x)` 对爬行动物/两栖动物/桌子为假 | ✅ 方向照录 |
| 7 | T5 近似概念混用 | syntax（语法）vs semantics（语义）；model vs interpretation | ✅ 分列，见 §1.9 |
| 8 | T5 近似概念混用 | degree of truth（真值度）vs degree of belief（信念度） | ✅ 已在正文与表中双重标注 |
| 9 | T3 性质误判 | 复合项是"名字"而非"子程序调用"；量词语义是"合取/析取"而非数值 | ✅ 已保留原书强调 |
| 10 | T8 归属 | 作者发挥一律标 `【延伸·非原著】` | ✅ 本章**未添加**任何原著外内容，无需标注 |

---

### 7. 变更记录

| 版本 | 日期 | 变更 |
|---|---|---|
| v1.0 | 2026-10-07 | 初版。76 条新术语 + 6 组同形异义 + 第 8 章 27 条小节标题对照 + 7 项待核 + 10 条陷阱自查记录。 |

### 4.3 第9章 一阶逻辑中的推断

> **说明**：本章（一阶逻辑中的推断）术语基本不在现有 `AIMA-术语对照表.md` 覆盖范围内（现有条目主要覆盖 11–18 章）。
> 本文件为**增量**，待人工合并进总表后方可视为生效。判定流程依 `book-translation` skill §3。
> **来源**：`Artificial-Intelligence-A-Modern-Approach-4th.pdf` pp.280–313（PDF idx 292–325）。
> **章节中译名**：第 9 章 一阶逻辑中的推断（用户提供，权威）。小节英文编号来自官方 TOC（信源 B）。

---

### 1. 推断与量词（9.1）

| English | 中文 | 备注 |
|---|---|---|
| inference | 推断 | 沿用总表 §1.1/§1.9：精确语境用「推断」。本章全篇统一用**推断**（推断规则 / 推断过程 / 推断算法） |
| entailment | 蕴含 | 不写「蕴涵」；本章统一 |
| Universal Instantiation (UI) | 全称实例化 | |
| Existential Instantiation | 存在实例化 | |
| ground term | 基项 | 即不含变量的项；同族：ground clause 基子句 / ground instance 基实例 |
| substitution | 置换 | `SUBST(θ, α)` 保留原样不译 |
| Skolem constant | Skolem 常量 | ⚠️ 待核：备选「Skolem 常元」「斯科伦常量」。人名 Skolem 保留英文（skill §4） |
| propositionalization | 命题化 | |
| semidecidable | 半可判定的 | T5 易混：半可判定 ≠ 不可判定（不可判定是更强的否定）；原书只说 semidecidable |
| complete / sound | 完备 / 可靠 | T5 必分：completeness=完备性，soundness=可靠性，🚫 不互换 |
| decidable | 可判定的 | Datalog 知识库的蕴含是**可判定的**（与一般一阶逻辑半可判定对照） |

### 2. 合一与提升（9.2）

| English | 中文 | 备注 |
|---|---|---|
| Generalized Modus Ponens | 广义假言推理 | Modus Ponens 沿用「假言推理」 |
| lifting / lifted | 提升（的） | lifted version = 提升版本 |
| unification | 合一 | |
| unifier | 合一子 | |
| most general unifier (MGU) | 最一般合一子 | ⚠️ T3：**唯一性是「在变量改名与置换意义下」的**，不可写成绝对唯一 |
| standardizing apart | 标准化分离 | ⚠️ 待核：备选「变量分离」「改名分离」 |
| occur check | 出现检查 | T7：使合一算法复杂度**关于表达式大小为二次的**；部分系统有线性时间算法 |
| STORE / FETCH | 存储 / 检索 | 函数名保留英文 |
| indexing / predicate indexing | 索引 / 谓词索引 | |
| subsumption lattice | 包容格 | ⚠️ 待核：备选「包含格」「归类格」。T7：n 元谓词的格有 **O(2ⁿ)** 个节点 |
| subsumption | 包容 | ⚠️ T1：**X 被 Y 包容 ⇔ X 比 Y 更具体**（如 `P(A)` 被 `P(x)` 包容） |

### 3. 前向链接（9.3）

| English | 中文 | 备注 |
|---|---|---|
| definite clause | 确定子句 | |
| Datalog | Datalog | 保留原文；= 无函数符号的一阶确定子句 |
| fixed point | 不动点 | |
| renaming | 重命名 | ``Likes(x, IceCream)`` 与 ``Likes(y, IceCream)`` 互为重命名 |
| forward chaining | 前向链接 | ⚠️ 待核：备选「前向链」 |
| conjunct ordering | 合取项排序 | T7：求最优排序 **NP-hard** |
| data complexity | 数据复杂度 | T7：前向链接的数据复杂度是**多项式**的 |
| pattern matching（规则匹配） | 模式匹配 | T7：把确定子句与一组事实相匹配是 **NP-hard** |
| incremental forward chaining | 增量式前向链接 | |
| Rete algorithm | Rete 算法 | 算法名保留；Rete 为拉丁语「网」 |
| production system | 产生式系统 | T8：此处 production 指条件–动作规则，🚫 不译「生产系统」 |
| cognitive architecture | 认知架构 | |
| XCON / OPS-5 / ACT / SOAR | XCON / OPS-5 / ACT / SOAR | 系统名保留原样 |
| deductive database | 演绎数据库 | |
| magic set | 魔集 | ⚠️ 待核：备选「魔法集」 |

### 4. 后向链接与逻辑编程（9.4）

| English | 中文 | 备注 |
|---|---|---|
| backward chaining | 后向链接 | ⚠️ 待核：备选「后向链」「反向链接」 |
| AND/OR search | AND/OR 搜索 | 保留符号 |
| generator | 生成器 | 指返回多次的函数 |
| logic programming | 逻辑编程 | ⚠️ 待核：备选「逻辑程序设计」 |
| Prolog | Prolog | 保留 |
| dynamic programming | 动态规划 | |
| tabled logic programming | 制表逻辑编程 | ⚠️ 待核：备选「表逻辑编程」「列表逻辑编程」 |
| memoization | 记忆化 | 小结原文用 memoization |
| unique names assumption | 唯一名称假设 | |
| closed world assumption | 封闭世界假设 | |
| negation as failure | 失败即否定 | 仅见于 Summary；⚠️ 待核：备选「否定即失败」 |
| completion | 完备化 | ⚠️ 待核：备选「补全」；指数据库语义的 FOL 翻译 |
| constraint logic programming (CLP) | 约束逻辑编程 | 缩写 CLP 保留 |
| metarule | 元规则 | MRS 语言用语 |
| MRS | MRS | 保留 |

### 5. 归结（9.5）

| English | 中文 | 备注 |
|---|---|---|
| resolution | 归结 | |
| conjunctive normal form (CNF) | 合取范式 | 缩写 CNF 保留 |
| Skolemization | Skolem 化 | |
| Skolem function | Skolem 函数 | 参数为该存在量词作用域内的**全部全称量化变量** |
| binary resolution | 二元归结 | T5：**单独使用不完备** |
| factoring | 因子化 | ⚠️ 待核：备选「归并」「合并」。二元归结 + 因子化 = 完备 |
| refutation-complete | 反驳完备的 | |
| Herbrand universe | Herbrand 域 | ⚠️ 待核：备选「Herbrand 全域」 |
| saturation | 饱和 | |
| Herbrand base | Herbrand 基 | |
| Herbrand's theorem | Herbrand 定理 | |
| ground resolution theorem | 基归结定理 | |
| lifting lemma | 提升引理 | |
| resolution closure | 归结闭包 | 记号 `RC(S)` 保留 |
| nonconstructive proof | 非构造性证明 | |
| demodulation | 解调 | ⚠️ T1：**有方向**——给定 `x = y` 总是把 x 替换为 y，绝不反向 |
| paramodulation | 调解 | 对含相等的一阶逻辑**完备** |
| equational unification | 等式合一 | |
| unit preference | 单元优先 | |
| unit resolution | 单元归结 | 一般**不完备**，对 Horn 子句完备 |
| set of support | 支持集 | |
| input resolution | 输入归结 | 对 Horn 形式**完备**，一般**不完备** |
| linear resolution | 线性归结 | **完备** |
| unit clause | 单元子句 | |
| Horn clause | Horn 子句 | |
| OTTER / DEEPHOL / SPIN / AURA | OTTER / DEEPHOL / SPIN / AURA | 系统名保留原样 |
| embedding | 嵌入 | DEEPHOL 用神经网络构造的表示 |
| synthesis / verification | 综合 / 验证 | |

### 6. 第 9 章小节标题中英对照

> 英文编号来自官方 TOC（`aima.cs.berkeley.edu/contents.html`，信源 B）。中文译名未标 ✅ 者为自拟。

| 号 | English | 中文 |
|---|---|---|
| 9.1 | Propositional vs. First-Order Inference | 命题推断与一阶推断 |
| 9.1.1 | Reduction to propositional inference | 归约到命题推断 |
| 9.2 | Unification and First-Order Inference | 合一与一阶推断 |
| 9.2.1 | Unification | 合一 |
| 9.2.2 | Storage and retrieval | 存储与检索 |
| 9.3 | Forward Chaining | 前向链接 |
| 9.3.1 | First-order definite clauses | 一阶确定子句 |
| 9.3.2 | A simple forward-chaining algorithm | 一个简单的前向链接算法 |
| 9.3.3 | Efficient forward chaining | 高效的前向链接 |
| — | Matching rules against known facts（9.3.3 下无编号） | 规则与已知事实的匹配 |
| — | Incremental forward chaining（9.3.3 下无编号） | 增量式前向链接 |
| — | Irrelevant facts（9.3.3 下无编号） | 无关事实 |
| 9.4 | Backward Chaining | 后向链接 |
| 9.4.1 | A backward-chaining algorithm | 一个后向链接算法 |
| 9.4.2 | Logic programming | 逻辑编程 |
| 9.4.3 | Redundant inference and infinite loops | 冗余推断与无限循环 |
| 9.4.4 | Database semantics of Prolog | Prolog 的数据库语义 |
| 9.4.5 | Constraint logic programming | 约束逻辑编程 |
| 9.5 | Resolution | 归结 |
| 9.5.1 | Conjunctive normal form for first-order logic | 一阶逻辑的合取范式 |
| 9.5.2 | The resolution inference rule | 归结推断规则 |
| 9.5.3 | Example proofs | 示例证明 |
| 9.5.4 | Completeness of resolution | 归结的完备性 |
| 9.5.5 | Equality | 相等性 |
| 9.5.6 | Resolution strategies | 归结策略 |
| — | Practical uses of resolution theorem provers（9.5.6 下无编号） | 归结定理证明器的实际用途 |

### 7. 需要人工复核的点

| # | 事项 | 说明 |
|---|---|---|
| 1 | 中文二级/三级小节译名 | 英文编号来自官方 TOC（权威）；中文译名**未与中译本核对**（信源 D 仅目录可用），建议对照人民邮电 2022 中译本正文 |
| 2 | `z·1 = z` | PDF 文本层丢失乘号，原样为 `z1 = z`；笔记中已加 ⚠️ 待核 |
| 3 | Figure 9.10 / 9.11 的归结链 | 两图是**图形**，PDF 文本层无内容。笔记中的归结链是依正文描述与 CNF 子句**重建**的，步骤与合一子已逐条验算，但**图示的分枝顺序/加粗位置无法核对** |
| 4 | Figure 9.8(b) 的 877 / 62 次推断 | 数值取自正文（p.296、p.297），✅ 已核对 |
| 5 | Gödel 侧栏 | 位于 p.305（9.5.4 中间），笔记中已标【原书侧栏】；其中"barring 29½ pages"未逐字译出，改写为"至少占 30 页" |

### 4.4 第10章 知识表示

> **说明**：本文件只收录**第 10 章新增**术语（AIMA-术语对照表.md 中未出现的）。
> **不得直接改 `AIMA-术语对照表.md`**（5 个 agent 并发），由项目负责人统一合并。
> **判定流程**：`book-translation` skill §3 四步（查表 → 查中译本 → 查学界通行 → 自拟）。
> **源**：原书 PDF idx 326–355（书页 314–343）。

- **版本**：v1.0 / 2026-10-07
- **章名定译**：第 10 章 知识表示（Knowledge Representation）✅ 与中译本一致

---

### 1. 新增术语总表

> 标注：✅ = 已与中译本核对；⚠️ = 学界有分歧，本表取某译法并注备选；🚫 = 禁用译法。

#### 1.1 本体与类别

| English | 中文 | 备注 |
|---|---|---|
| ontology | 本体 | ✅ 哲学/逻辑/知识工程通用 |
| upper ontology | 顶层本体 | ✅ 原书图 10.1 语境 |
| general-purpose ontology | 通用本体 | 🚫 不译"通用本体论" |
| special-purpose ontology | 专用本体 | |
| category | 类别 | ✅ 本章首选；🚫 不译"范畴"（范畴论另有含义） |
| subcategory / subclass / subset | 子类别 / 子类 / 子集 | 三者 interchangeable（原书明言） |
| reification | 对象化 | ⚠️ 别名"物化"；本表取"对象化"，与"把命题变成对象"的动作一致 |
| reiﬁcation（thingiﬁcation） | 对象化 | John McCarthy 提过 thingiﬁcation，未通行 |
| inheritance | 继承 | ✅ 与 OOP 一致 |
| taxonomic hierarchy / taxonomy | 分类层次 / 分类法 | |
| member / membership | 成员 / 成员资格 | |
| disjoint | 不相交 | |
| exhaustive decomposition | 穷尽分解 | |
| partition | 划分 | ⚠️ 数学术语"划分"；注意与"分区"区分 |
| intersection | 交集 | |
| necessary and sufficient conditions | 必要条件与充分条件 | |
| natural kind | 自然种类 | ✅ 哲学/语言学术语（Wittgenstein、Quine） |
| typical (category) | 典型的（类别） | `Typical(c) ⊆ c` |
| family resemblance | 家族相似 | ✅ Wittgenstein 术语 |

#### 1.2 对象与构成

| English | 中文 | 备注 |
|---|---|---|
| PartOf | 部分关系（PartOf） | 传递且自反 |
| composite object | 复合对象 | |
| PartPartition | 部分划分 | 类比类别的 Partition |
| bunch | 束 | ⚠️ 原书自造概念；🚫 不译"串/捆/把" |
| BunchOf | BunchOf | 函数符号保留 |
| logical minimization | 逻辑最小化 | |
| intrinsic property | 内在性质 | |
| extrinsic property | 外在性质 | |
| substance | 物质 | ⚠️ 哲学语境；🚫 不译"实体"（entity 另译） |
| stuff | 物质 / 物 | ⚠️ 原书自造用法；与"东西"区分 |
| thing | 物 / 对象 | 与 stuff 对举 |
| count noun | 可数名词 | ✅ 语言学 |
| mass noun | 物质名词 / 不可数名词 | ✅ 语言学 |

#### 1.3 度量

| English | 中文 | 备注 |
|---|---|---|
| measure | 度量 | ⚠️ 本章专属；🚫 不译"测量/措施" |
| units function | 单位函数 | |
| quantitative measure | 定量度量 | |
| qualitative physics | 定性物理 | ✅ 物理系统不陷入数值方程的推理 |

#### 1.4 事件与时间

| English | 中文 | 备注 |
|---|---|---|
| event | 事件 | 与 action 可互换（原书脚注） |
| event calculus | 事件演算 | ✅ Kowalski & Sergot 1986 |
| fluent | 流变 | ✅ AIMA 通用译法（第 7 章起）；🚫 不译"流子/流体" |
| time point | 时间点 | |
| moment | 时刻 | 持续时间为零的区间 |
| extended interval | 延长时间区间 | |
| absolute time | 绝对时间 | |
| time scale | 时间尺度 | |
| interval relation | 区间关系 | Allen 1983 的 8 种 |
| Meet / Before / During / Overlap / Starts / Finishes / Equals / After | 紧接 / 之前 / 期间 / 重叠 / 起点同 / 终点同 / 相等 / 之后 | 保留英文以便对照 |
| generalized event | 广义事件 | 物理对象即"一团时空" |
| simultaneous event | 同时事件 | |
| exogenous event | 外生事件 | |
| continuous event | 连续事件 | |
| nondeterministic event | 非确定性事件 | |

#### 1.5 心理对象与模态逻辑

| English | 中文 | 备注 |
|---|---|---|
| mental object | 心理对象 | |
| propositional attitude | 命题态度 | ✅ 哲学/逻辑术语（Believes/Knows/Wants/Informs） |
| referential transparency | 指称透明性 | |
| referential opacity | 指称不透明性 | |
| co-referential | 共指 | |
| modal logic | 模态逻辑 | |
| modal operator | 模态算子 | `K_A`、`B_A` 等 |
| possible world | 可能世界 | ✅ 模态逻辑/哲学 |
| accessibility relation | 可达关系 | |
| knowledge atom | 知识原子 | `K_A P` |
| nested knowledge | 嵌套知识 | |
| logical omniscience | 逻辑全知 | ⚠️ 模态逻辑的麻烦假设 |
| justified true belief | 得到辩护的真信念 | ✅ 柏拉图传统 |
| introspect | 内省 | |
| linear temporal logic | 线性时序逻辑 | |
| next / finally / globally / until | 下一时间步 / 最终 / 始终 / 直到 | 算子 `X`、`F`、`G`、`U` |

#### 1.6 推理系统

| English | 中文 | 备注 |
|---|---|---|
| semantic network | 语义网络 | ✅ |
| existential graph | 存在图 | ✅ Peirce 1909 |
| single-boxed link | 单框链接 | 断言每个成员的性质 |
| double-boxed link | 双框链接 | 断言成员之间的关系 |
| multiple inheritance | 多重继承 | |
| procedural attachment | 过程附着 | |
| default value | 默认值 | |
| override (a default) | 压倒（默认） | ⚠️ 备选"覆盖"；本表取"压倒"，与"默认被更具体值取代"语义一致 |
| description logic | 描述逻辑 | |
| subsumption | 包含判定 | ⚠️ 备选"包含/归摄"；本表取"包含判定" |
| classification | 分类 | |
| consistency (of a category) | 一致性（类别的） | |
| CLASSIC | CLASSIC | 算法/系统名保留（Borgida et al. 1989） |
| tractability | 可处理性 | |

#### 1.7 默认推理与真值维护

| English | 中文 | 备注 |
|---|---|---|
| monotonicity | 单调性 | ✅ 第 7 章已用 |
| nonmonotonicity | 非单调性 | |
| nonmonotonic logic | 非单调逻辑 | |
| circumscription | 限定 | ✅ McCarthy 1980；🚫 不译"环绕/划界" |
| model preference logic | 模型偏好逻辑 | |
| preferred model | 优先模型 | |
| abnormal (object) | 异常（对象） | |
| prioritized circumscription | 优先限定 | |
| default logic | 默认逻辑 | |
| default rule | 默认规则 | 形式 `P : J1,...,Jn / C` |
| prerequisite | 前提 | 默认规则的 P |
| conclusion | 结论 | 默认规则的 C |
| justification | 辩护 | ⚠️ TMS/默认逻辑专属；🚫 不译"理由/正当化" |
| extension (of a default theory) | 扩展（默认理论的） | ⚠️ 默认理论后果的极大集合 |
| Nixon diamond | Nixon 菱形 | 多重继承标准反例 |
| belief revision | 信念修正 | 与 belief update 对照 |
| belief update | 信念更新 | 反映世界变化，非新信息 |
| truth maintenance system (TMS) | 真值维护系统 | |
| JTMS | JTMS | 基于辩护的 TMS |
| ATMS | ATMS | 基于假设的 TMS |
| assumption | 假设 | ATMS 中的标签成分 |
| explanation | 解释 | `E ⊨ P` 的 E |
| minimal explanation | 极小解释 | 没有真子集也是解释 |
| threshold probability | 阈值概率 | 默认规则的概率解释 |
| nonmodularity | 非模块化 | 默认规则集选择的难题 |

---

### 2. 同形异义必须分列（第 10 章新增）

| English | 语境 A | 语境 B |
|---|---|---|
| **model** | 逻辑（本章 §10.4）→ **模型（指派）** | 概率（12–15 章）→ **模型**（同） |
| **extension** | 默认逻辑 → **（默认理论的）扩展**（后果的极大集合） | 通用 → 扩展/延伸/外延 |
| **justification** | TMS/默认逻辑 → **辩护** | 通用 → 理由/正当化 |
| **default** | 知识表示 → **默认**（缺省值/默认规则） | 金融 → 违约/拖欠 |
| **fluent** | AI 逻辑 → **流变**（随时间变化的方面） | 通用英语 → 流畅的（形容词） |
| **measure** | 知识表示 → **度量**（长度/质量/价格等） | 通用 → 措施/衡量/度量（动词） |
| **stuff** | 本体论 → **物质**（无明确个体化的部分） | 通用 → 东西/物品 |
| **bunch** | 本体论 → **束**（无结构复合对象） | 通用 → 束/串/捆 |
| **override** | 默认推理 → **压倒**（默认被更具体值取代） | 通用 → 推翻/优先于 |
| **subsumption** | 描述逻辑 → **包含判定** | 通用 → 归入/吸收 |
| **category** | 知识表示 → **类别** | 数学（范畴论）→ 范畴 |
| **object** | 一阶逻辑 → **对象**（项所指） | 通用 → 物体/目标/宾语 |
| **event** | 事件演算 → **事件**（可附加信息的对象） | 通用 → 事件/事情 |
| **process** | 心理过程 → **过程** | 业务流程 → 流程/工序 |

---

### 3. 小节标题中英对照（第 10 章）

> 二级章名 ✅ = 任务配置给定权威译法（"第 10 章 知识表示"）；三级/二级小节中文译名未与中译本核对，按 skill §3 判定流程自拟（多为哲学/逻辑学通行译法），需对照中译本正文确认。

##### 第 10 章 知识表示（Knowledge Representation）✅

| 号 | English | 中文 |
|---|---|---|
| 10.1 | Ontological Engineering | 本体工程 |
| 10.2 | Categories and Objects | 类别与对象 |
| 10.2.1 | Physical composition | 物理构成 |
| 10.2.2 | Measurements | 度量 |
| 10.2.3 | Objects: Things and stuff | 对象：物与物质 |
| 10.3 | Events | 事件 |
| 10.3.1 | Time | 时间 |
| 10.3.2 | Fluents and objects | 流变与对象 |
| 10.4 | Mental Objects and Modal Logic | 心理对象与模态逻辑 |
| 10.4.1 | Other modal logics | 其他模态逻辑 |
| 10.5 | Reasoning Systems for Categories | 面向类别的推理系统 |
| 10.5.1 | Semantic networks | 语义网络 |
| 10.5.2 | Description logics | 描述逻辑 |
| 10.6 | Reasoning with Default Information | 默认信息推理 |
| 10.6.1 | Circumscription and default logic | 限定与默认逻辑 |
| 10.6.2 | Truth maintenance systems | 真值维护系统 |

---

### 增量原稿的维护说明

1. 本文件由第 10 章翻译 agent 维护，只收录本章新增；不重复主表已有条目。
2. 主表合并时：§1 进主表 §1（按主题分组）；§2 进主表 §1.9（同形异义）；§3 进主表 §2。
3. 标记含义：✅ 已与中译本核对；⚠️ 学界有分歧，本表为准；🚫 禁用译法。
4. 二级标题英文编号来自原书目录（权威）；三级中文译名未标 ✅ 者为自拟。

### 4.5 第11章 自动规划

> **用途**：第 11 章精校（对照原书 4e p.344–385，PDF idx 356–397）时新增/调整的术语。
> **为什么不直接改 `AIMA-术语对照表.md`**：有 5 个 agent 并发写该文件，为避免写冲突，本章增量先落在本文件，待并发结束后由维护者合并。
> **合并方向**：以下条目建议并入 `AIMA-术语对照表.md` 的 §1.7「规划（11 章）」，个别跨章条目按主题归位。

- 书：Russell & Norvig, *AIMA* 4th US Edition, Pearson 2020
- 精校日期：2026-10-07
- 依据：原书 PDF 第 11 章全文（信源 A）

---

### 1. 新增条目（拟并入 §1.7）

| English | 中文 | 备注 / 出处 |
|---|---|---|
| factored representation | 因袭表示 | 全书统一译法；p.344 |
| fluent | 流 | p.344；ground atomic fluent = 基原子流 |
| ground atomic fluent | 基原子流 | p.345 |
| database semantics | 数据库语义 | p.345（含封闭世界 + 唯一名两个假设） |
| closed-world assumption | 封闭世界假设 | p.345 |
| unique names assumption | 唯一名假设 | p.345 |
| ground action | 基动作 | p.345；⚠️ 与 primitive action 区分，见 §3 |
| precondition / effect | 前提 / 效果 | p.345 |
| delete list / add list (DEL / ADD) | 删除表 / 添加表 | p.345，式 (11.1) |
| primitive action | 基元动作 | p.357（与 HLA 相对的最低层动作） |
| forward (progression) state-space search | 前向（进展）状态空间搜索 | §11.2.1 |
| backward (regression) state-space search | 反向（回归）状态空间搜索 | §11.2.2 |
| relevant action | 相关动作 | p.350；⚠️ 定义含"无任何效果否定目标任一部分" |
| standardizing apart | 变量标准化分离 | p.350，另见 p.284 |
| successor-state axiom | 后继状态公理 | p.352（SATPLAN 编码第 6 步） |
| action exclusion axiom | 动作排除公理 | p.351 |
| precondition axiom | 前提公理 | p.351 |
| bounded planning problem | 有界规划问题 | p.352；对应 Bounded PlanSAT（p.384） |
| planning graph | 规划图 | p.352（主表已有，此处补出处） |
| situation calculus | 情境演算 | p.352；McCarthy (1963) / Reiter (2001) |
| partial-order planning | 偏序规划 | p.352 |
| ignore-preconditions heuristic | 忽略前提启发式 | p.353 |
| set-cover problem | 集合覆盖问题 | p.353 |
| ignore-delete-lists heuristic | 忽略删除表启发式 | p.354；**4e 用此术语，不用 h_FF** |
| domain-independent heuristic | 领域无关启发式 | p.353 |
| symmetry reduction | 对称性消减 | p.354 |
| forward pruning | 前向剪枝 | p.355 |
| preferred action | 偏好动作 | p.355 |
| serializable subgoals | 可串行化子目标 | p.355 |
| state abstraction | 状态抽象 | p.355 |
| decomposition | 分解 | p.356 |
| subgoal independence | 子目标独立性（假设） | p.356 |
| pattern database | 模式数据库 | p.356（另见 §3.6.3） |
| FF / FAST FORWARD | FF / FAST FORWARD | 规划器名保留不译；p.356，Hoffmann (2005) |
| refinement | 细化 | p.357 |
| implementation | 实现 | p.357（只含基元动作的细化） |
| downward refinement property | 向下细化性质 | p.360；⚠️ 方向易错，见 §3 |
| reachable set | 可达集 | p.361，`REACH(s, h)` |
| angelic nondeterminism / semantics | 天使（式）非确定性 / 天使语义 | p.361 |
| demonic nondeterminism | 恶魔（式）非确定性 | p.361 |
| optimistic / pessimistic description | 乐观 / 悲观描述 | p.362，`REACH⁺` / `REACH⁻` |
| percept schema | 感知模式 | p.366 |
| open-world assumption | 开世界假设 | p.367；⚠️ 与经典规划的封闭世界假设相对 |
| 1-CNF belief state | 1-CNF 信念状态 | p.368；closed under PDDL updates |
| conditional effect | 条件效果 | p.368–369；⚠️ 与 precondition 区分，见 §3 |
| conformant planning | conformant 规划 | p.365；= sensorless planning |
| AND–OR search | 与或搜索 | p.371（另见 §4.4） |
| replanning | 重规划 | p.372 |
| execution monitoring | 执行监控 | p.372 |
| action / plan / goal monitoring | 动作 / 计划 / 目标监控 | p.372 |
| plan repair | 计划修复 | p.373，Figure 11.12 |
| resource constraint | 资源约束 | p.374 |
| job-shop scheduling problem | 作业车间调度问题 | p.375（另见 §6.1.2） |
| consumable / reusable resource | 可消耗 / 可复用资源 | p.375 |
| aggregation | 聚合 | p.376（把不可区分个体归为数量） |
| duration | 持续时间 | p.375 |
| makespan | 总工期 | p.375 |
| critical path method (CPM) | 关键路径法 | p.376 |
| critical path | 关键路径 | p.376（主表已有，此处补出处） |
| schedule | 调度（方案） | p.376，指 ES/LS 的集合 |
| minimum slack heuristic | 最小松弛量启发式 | p.378；⚠️ 不是"最小冲突" |
| PlanSAT / Bounded PlanSAT | PlanSAT / Bounded PlanSAT | p.384，保留英文 |
| portfolio (planning) system | 组合（规划）系统 | p.379 |

**合计新增：54 条**（其中 `planning graph`、`critical path` 两条主表已收，实际新增 52 条）。

---

### 2. 建议在主表标注的修订

| 现有条目 | 建议 | 依据 |
|---|---|---|
| `h_FF / h_Add / h_Max` | 加注「⚠️ 4e 第 11 章**未出现**（全文检索 0 次），属第 3 版术语；4e 对应术语是 **ignore-delete-lists heuristic**。保留符号条目以防他章引用，但第 11 章笔记不采用」 | 原书 p.344–385 全文 |
| `sensorless planning \| 无传感规划` | 建议补 `conformant planning \| conformant 规划`（两者同义，原书并用） | p.365 |
| `relaxed plan \| 松弛计划` | 保留；4e 仅出现在「偏好动作」定义中（p.355），**不用于指代 h_FF 的松弛计划解** | p.355 |
| `ES / LS` | 建议补 `slack` 的定义：松弛量 = `LS − ES` | p.376 |
| — | 新增「同形异义」行：`ground action` ≠ `primitive action`，见 §3 | — |

---

### 3. 同形异义必须分列

| English | 语境 A | 语境 B |
|---|---|---|
| **基元动作** | `ground action` → 建议译**基动作**（动作模式实例化后无变量的动作），与「基原子 ground atom」的"基"一致 | `primitive action` → **基元动作**（分层规划中与 HLA 相对的最低层动作） |
| **效果条件** | `precondition` → **前提**：不满足则动作**不适用**、结果状态**未定义** | `conditional effect` 的 condition → **条件**：不满足则该条件效果**不施加**，结果状态**不变** |
| **世界假设** | 经典规划 → **封闭世界假设**（未提及的流为假） | 无传感 / 部分可观测规划 → **开世界假设**（未出现的流取值**未知**） |
| **可达集** | `REACH⁺` → **乐观描述**，可能**夸大**可达集 | `REACH⁻` → **悲观描述**，可能**缩小**可达集 |

---

### 4. 本章专有名词（保留不译）

| 类别 | 条目 |
|---|---|
| 语言 / 系统名 | PDDL、STRIPS、ADL、Graphplan、SATPLAN、FF / FAST FORWARD、Fast Downward、O-PLAN、Remote Agent、PLANEX、SIPE、WARPLAN、NOAH、NONLIN、UCPOP、UNPOP、HSP、HSCP、CGP、T0、MBP、SGP、CPLAN、GP-CSP、FDSS、SYMBA*、LAO* |
| 缩写 | HTN、HLA、CPM、ES、LS、MRV、BDD、QBF、PSPACE、PlanSAT |
| 变量名 / 记号 | `REACH(s,h)`、`REACH⁺`、`REACH⁻`、`~+A`、`~−A`、`~±A`、`Actionₜ`、`Fᵗ`、`DEL(a)`、`ADD(a)` |
| 练习号 | 11.HLAU、11.HLAP、11.PART、11.SUSS |

---

### 5. 本章踩到的陷阱（建议并入 `AIMA-翻译项目配置.md` §5）

| # | 类型 | 错误写法 | 正确写法 | 出处 |
|---|---|---|---|---|
| 1 | T6 版本错（🔴） | 第 11 章讲 `hMax` / `hAdd` / `h_FF` / 松弛规划图启发式 / 地标 landmark | **4e 全无**（检索 0 次）。4e §11.3 讲：忽略前提启发式 + 集合覆盖、忽略删除表启发式、对称性消减、偏好动作、可串行化子目标、状态抽象、子目标独立性、模式数据库、FF | p.353–356 |
| 2 | T1 方向颠倒（🔴） | 「无回路细化性质：若高层计划能达成目标，则它的**任意细化**也能达成目标」 | **向下细化性质**：每个"**声称**"达成目标的高层计划（依其步骤描述）都**事实上**达成目标——即**至少存在一个**实现达成目标 | p.360 |
| 3 | T3/T4 类别混淆（🔴） | 无传感规划沿用封闭世界假设 | 必须改用**开世界假设**：未出现的流取值**未知**（不是"为假"） | p.367 |
| 4 | T7 量化错（🟡） | 「一般情形 PSPACE-完全（长度有界时 NP-完全）」 | 原文：「For propositionalized problems **both are in the complexity class PSPACE**」——**只说在 PSPACE 内**，未说 -完全；Bounded PlanSAT 也未说 NP-完全 | p.384 |
| 5 | T6 示例归属错（🟡） | 备胎问题含 `Inflate`（打气）动作 | 4e 只有 `Remove` / `PutOn` / `LeaveOvernight` 三个模式（对应四个动作描述） | p.346–347 |
| 6 | T2 缺步骤（🟡） | 求解调度用「最小冲突局部搜索」 | 原书讲的是**最小松弛量启发式**（选松弛量最小的未调度动作安排在其最早开始时间，更新 ES/LS 后重复） | p.378 |
| 7 | T1 方向（🟡） | 反向搜索"不能处理量词与函数符号" | 原书写的缺点是：反向搜索用**含变量的状态**而非基状态，**难以设计好的启发式**——这是多数系统偏爱前向搜索的主要原因 | p.351 |
| 8 | T8 归属（🟢） | 「分层规划…可与 HTN 规划器（如 SHOP2）配合」 | SHOP2 不在 4e 第 11 章；本书 HLA 与天使语义的陈述出自 **Marthi et al. (2007, 2008)** | p.381 / p.358–364 |
| 9 | T2 缺步骤（🟡） | 相关动作 = "效果能达成目标中某个文字的动作" | 完整定义：效果与某目标文字合一，**且没有任何效果否定目标的任一部分** | p.350 |
| 10 | T2 缺步骤（🟡） | 积木世界 `Move` 含 `ArmEmpty`、无 `Block`/不等约束 | Figure 11.4：`On(b,x) ∧ Clear(b) ∧ Clear(y) ∧ Block(b) ∧ Block(y) ∧ (b≠x) ∧ (b≠y) ∧ (x≠y)`；4e 无 `ArmEmpty` | p.347 |

---

### 6. 遗留待核

| 项 | 说明 |
|---|---|
| ISBN 数量不一致 | 原文同一段先说 "a trillion 13-digit ISBNs"，后说 "10 billion ground Buy actions"（p.351），疑为原书笔误；笔记照抄两个数未统一 |
| 46 页边界 | 原书第 11 章正文为 p.344–385（PDF idx 356–397）；任务描述给的是 346–385，**章首实际从 p.344 开始**（idx 356 页眉为 `CHAPTER 11 AUTOMATED PLANNING`） |


---

## 5. 第 19–28 章（Part V–VII）术语补充

> 2026-10-07 由各章「术语增量」并入。三级中文标题为自拟，未核对中译本。已有译法未改。

### 5.1 第19章 从样例中学习

> 只收录本章新出现、且 `AIMA-术语对照表.md` 中尚无同条的译法。已有译法不改。
> 小节中文为自拟，**未核对中译本**。🚫 沿用总表：绝对独立、单连通、开放世界、编号变量；`cost function` 仍是「代价函数」，本章 `loss function` 另译「损失函数」。

### 小节标题

| English | 中文 | 备注 |
|---|---|---|
| Forms of Learning | 学习的形式 | 19.1；自拟·未核对 |
| Supervised Learning | 监督学习 | 19.2；自拟·未核对 |
| Example problem: Restaurant waiting | 示例问题：餐馆等候 | 19.2.1；自拟·未核对 |
| Learning Decision Trees | 学习决策树 | 19.3；自拟·未核对 |
| Expressiveness of decision trees | 决策树的表达能力 | 19.3.1；自拟·未核对 |
| Learning decision trees from examples | 从样例中学习决策树 | 19.3.2；自拟·未核对 |
| Choosing attribute tests | 选择属性测试 | 19.3.3；自拟·未核对 |
| Generalization and overfitting | 泛化与过拟合 | 19.3.4；自拟·未核对 |
| Broadening the applicability of decision trees | 拓宽决策树的适用范围 | 19.3.5；自拟·未核对 |
| Model Selection and Optimization | 模型选择与优化 | 19.4；自拟·未核对 |
| Model selection | 模型选择 | 19.4.1；自拟·未核对 |
| From error rates to loss | 从错误率到损失 | 19.4.2；自拟·未核对 |
| Regularization | 正则化 | 19.4.3；自拟·未核对 |
| Hyperparameter tuning | 超参数调优 | 19.4.4；自拟·未核对 |
| The Theory of Learning | 学习理论 | 19.5；自拟·未核对 |
| PAC learning example: Learning decision lists | PAC 学习示例：学习决策列表 | 19.5.1；自拟·未核对 |
| Linear Regression and Classification | 线性回归与分类 | 19.6；自拟·未核对 |
| Univariate linear regression | 单变量线性回归 | 19.6.1；自拟·未核对 |
| Gradient descent | 梯度下降 | 19.6.2；总表已有「梯度下降」，标题沿用 |
| Multivariable linear regression | 多变量线性回归 | 19.6.3；自拟·未核对。输入为向量、输出为标量 |
| Linear classifiers with a hard threshold | 带硬阈值的线性分类器 | 19.6.4；自拟·未核对 |
| Linear classification with logistic regression | 用逻辑回归做线性分类 | 19.6.5；自拟·未核对 |
| Nonparametric Models | 非参数模型 | 19.7；自拟·未核对 |
| Nearest-neighbor models | 最近邻模型 | 19.7.1；自拟·未核对 |
| Finding nearest neighbors with k-d trees | 用 k-d 树找最近邻 | 19.7.2；自拟·未核对 |
| Locality-sensitive hashing | 局部敏感哈希 | 19.7.3；自拟·未核对 |
| Nonparametric regression | 非参数回归 | 19.7.4；自拟·未核对 |
| Support vector machines | 支持向量机 | 19.7.5；自拟·未核对 |
| The kernel trick | 核技巧 | 19.7.6；自拟·未核对 |
| Ensemble Learning | 集成学习 | 19.8；自拟·未核对 |
| Bagging | 装袋 | 19.8.1；自拟·未核对。bootstrap aggregating |
| Random forests | 随机森林 | 19.8.2；自拟·未核对 |
| Stacking | 堆叠 | 19.8.3；自拟·未核对 |
| Boosting | 提升 | 19.8.4；自拟·未核对。⚠️ 与第 9 章 lifting「提升」同形异义 |
| Gradient boosting | 梯度提升 | 19.8.5；自拟·未核对 |
| Online learning | 在线学习 | 19.8.6；自拟·未核对 |
| Developing Machine Learning Systems | 开发机器学习系统 | 19.9；自拟·未核对 |
| Problem formulation | 问题表述 | 19.9.1；自拟·未核对 |
| Data collection, assessment, and management | 数据的收集、评估与管理 | 19.9.2；自拟·未核对 |
| Feature engineering | 特征工程 | 19.9.2 下无编号小标题；自拟·未核对 |
| Exploratory data analysis and visualization | 探索性数据分析与可视化 | 19.9.2 下无编号小标题；自拟·未核对 |
| Model selection and training | 模型选择与训练 | 19.9.3；自拟·未核对 |
| Trust, interpretability, and explainability | 信任、可解释性与可说明性 | 19.9.4；自拟·未核对。两词在本书中分开 |
| Operation, monitoring, and maintenance | 运行、监控与维护 | 19.9.5；自拟·未核对 |

### 学习问题

| English | 中文 | 备注 |
|---|---|---|
| machine learning | 机器学习 | |
| supervised learning | 监督学习 | |
| unsupervised learning | 无监督学习 | |
| reinforcement learning | 强化学习 | 总表已有 inverse reinforcement learning「逆向强化学习」 |
| semisupervised learning | 半监督学习 | |
| weakly supervised learning | 弱监督学习 | |
| label | 标签 | |
| training set | 训练集 | |
| validation set / development set / dev set | 验证集 / 开发集 | |
| test set | 测试集 | |
| hypothesis | 假设 | ⚠️ 第 1 章 physical symbol system hypothesis 译「假说」；第 10 章 assumption 译「假设」。本章 hypothesis 译「假设」 |
| hypothesis space | 假设空间 | |
| consistent hypothesis | 一致假设 | `h(x_i) = y_i` 对每个训练样例成立 |
| ground truth | 真实答案 | |
| model class | 模型类 | |
| induction | 归纳 | 总表 principle of induction 为「归纳原则」。与 backward induction「逆向归纳」不同 |
| classification | 分类 | 总表已有，沿用 |
| regression | 回归 | ⚠️ 统计意义的函数逼近。第 11 章 backward (regression) 是「反向（回归）搜索」，不是本词 |
| clustering | 聚类 | 总表已有，沿用 |
| generalization | 泛化 | |
| overfitting | 过拟合 | |
| underfitting | 欠拟合 | |
| bias | 偏差 | 本章：对不同训练集平均后偏离期望值的倾向。不是「归纳偏置」这条专名的译法 |
| variance | 方差 | 假设因训练集起伏而改变的多少 |
| bias–variance tradeoff | 偏差–方差权衡 | |
| Ockham's razor | 奥卡姆剃刀 | 原文拼 Ockham；脚注写 Occam 是误拼 |
| positive example / negative example | 正例 / 负例 | |
| Boolean classification | 布尔分类 | |
| noise | 噪声 | |
| learning curve | 学习曲线 | 测试准确率对训练集大小。⚠️ 不是 training curve |
| training curve | 训练曲线 | 固定训练集上，准确率对权重更新次数 |
| happy graph | happy graph | 原书对学习曲线的别称，保留 |

### 决策树与模型选择

| English | 中文 | 备注 |
|---|---|---|
| decision tree | 决策树 | |
| information gain | 信息增益 | `Gain(A) = B(p/(p+n)) − Remainder(A)` |
| entropy | 熵 | |
| remainder | 剩余熵 | `Remainder(A)` |
| significance test | 显著性检验 | |
| null hypothesis | 原假设 | |
| decision tree pruning | 决策树剪枝 | pruning 总表已作「剪枝」 |
| χ² pruning | χ² 剪枝 | |
| early stopping | 早停 | 先生成再剪枝才能处理 XOR；早停会错过 |
| split point | 分裂点 | 连续属性上的不等式测试 |
| information gain ratio | 信息增益比 | 正文指向习题 19.GAIN，未给公式 |
| regression tree | 回归树 | 叶上是线性函数，不是单个类别 |
| CART | CART | Classification And Regression Trees，保留 |
| unstable | 不稳定 | 决策树：一个新样例可能换掉根测试 |
| stationarity | 平稳性 | 同分布，并且与此前样例独立 |
| i.i.d. | 独立同分布 | |
| error rate | 错误率 | `h(x) ≠ y` 的比例。⚠️ 不等于损失 |
| hyperparameter | 超参数 | 模型类的旋钮，不是单个模型的参数 |
| k-fold cross-validation | k 折交叉验证 | 常用 k = 5 或 10 |
| leave-one-out cross-validation (LOOCV) | 留一交叉验证 | k = n。仍需单独测试集 |
| model selection | 模型选择 | 选假设空间。脚注认为更好的名字是模型类选择 |
| optimization | 优化 | 也称训练；在空间内找最佳假设 |
| loss function | 损失函数 | ⚠️ 总表 cost function = 代价函数，勿混 |
| L1 loss / L2 loss / L0/1 loss | L1 损失 / L2 损失 / L0/1 损失 | 与同名正则化不必配对。逻辑回归本节用的是 L2 |
| generalization loss | 泛化损失 | 对全部可能样例的期望 |
| empirical loss | 经验损失 | 样本上的平均 |
| realizable | 可实现 | 真函数在假设空间内 |
| approximation error | 逼近误差 | 空间里没有真函数 |
| estimation error | 估计误差 | 样例不够、方差没压住 |
| small-scale learning | 小规模学习 | 几十到低几千个样例 |
| large-scale learning | 大规模学习 | 百万级样例；损失可能由计算限度主导 |
| regularization | 正则化 | |
| regularization function | 正则化函数 | |
| feature selection | 特征选择 | χ² 剪枝是其中一种。feature 总表已作「特征」 |
| minimum description length (MDL) | 最小描述长度 | |
| interpolated | 插值 | 精确拟合全部训练数据。有的作者说「记住」 |
| hand-tuning | 手工调 | |
| grid search | 网格搜索 | |
| random search | 随机搜索 | |
| Bayesian optimization | 贝叶斯优化 | |
| population-based training (PBT) | 基于种群的训练 | |

### 学习理论与线性模型

| English | 中文 | 备注 |
|---|---|---|
| computational learning theory | 计算学习理论 | |
| probably approximately correct (PAC) | 可能近似正确 | |
| sample complexity | 样本复杂度 | |
| ε-ball | ε-球 | `error(h) ≤ ε` |
| decision list | 决策列表 | |
| k-DL | k-DL | 每个测试至多 k 个文字 |
| k-DT | k-DT | 深度至多 k 的决策树。k-DT ⊆ k-DL |
| linear function | 线性函数 | |
| weight | 权重 | |
| linear regression | 线性回归 | 见上「回归」的同形异义 |
| weight space | 权重空间 | |
| learning rate | 学习率 | 即第 4 章的步长 |
| batch gradient descent | 批量梯度下降 | 也称确定性梯度下降。gradient descent 总表已有 |
| stochastic gradient descent (SGD) | 随机梯度下降 | |
| minibatch | 小批量 | |
| epoch | 轮 | 覆盖全部训练样例的一步 |
| online gradient descent | 在线梯度下降 | SGD 的另一名称 |
| multivariable regression | 多变量回归 | 输入向量、输出标量 |
| multivariate regression | 多元回归 | 输出也是向量。⚠️ 勿与 multivariable 互换 |
| data matrix | 数据矩阵 | |
| pseudoinverse | 伪逆 | `(X⊤X)^{-1} X⊤` |
| normal equation | 正规方程 | (19.7) |
| sparse model | 稀疏模型 | L1 正则化倾向于把权重打成 0 |
| decision boundary | 决策边界 | |
| linear separator | 线性分离器 | |
| linearly separable | 线性可分 | |
| threshold function | 阈值函数 | 硬阈值只输出 0 或 1 |
| perceptron learning rule | 感知机学习规则 | perceptron 总表已作「感知机」 |
| logistic function | 逻辑函数 | 也称 sigmoid |
| logistic regression | 逻辑回归 | 本节用 L2 损失，不是对数损失 |
| parametric model | 参数模型 | 参数个数不随样例数增长 |
| nonparametric model | 非参数模型 | |

### 非参数、核与集成

| English | 中文 | 备注 |
|---|---|---|
| instance-based learning | 基于实例的学习 | |
| memory-based learning | 基于记忆的学习 | |
| nearest neighbors | 最近邻 | |
| Minkowski distance / L_p norm | Minkowski 距离 / L_p 范数 | p=2 欧氏，p=1 曼哈顿 |
| Hamming distance | 汉明距离 | |
| Mahalanobis distance | Mahalanobis 距离 | 人名保留 |
| curse of dimensionality | 维数灾难 | Bellman (1961) |
| k-d tree | k-d 树 | k-dimensional tree |
| locality-sensitive hash (LSH) | 局部敏感哈希 | |
| approximate near-neighbors | 近似近邻 | 半径 r 内有点，则高概率找到 cr 内的点 |
| locally weighted regression | 局部加权回归 | |
| kernel | 核 | ⚠️ 局部加权回归的核与 SVM 的核用法略有不同 |
| support vector machine (SVM) | 支持向量机 | |
| maximum margin separator | 最大间隔分离器 | |
| margin | 间隔 | 到最近样例距离的两倍 |
| support vector | 支持向量 | |
| quadratic programming | 二次规划 | |
| kernel trick | 核技巧 | |
| Mercer's theorem | Mercer 定理 | 合理 = 核矩阵正定 |
| polynomial kernel | 多项式核 | `(1 + x_j·x_k)^d`，维数对 d 指数 |
| soft margin | 软间隔 | 罚与移回正确一侧的距离成比例 |
| kernelization | 核化 | |
| ensemble learning | 集成学习 | |
| base model | 基模型 | |
| ensemble model | 集成模型 | |
| bagging | 装袋 | bootstrap aggregating |
| bootstrap | 自助法 | 有放回抽样 |
| random forest | 随机森林 | 分类默认 √n 个属性，回归默认 n/3 |
| extremely randomized trees (ExtraTrees) | 极端随机树 | |
| out-of-bag error | 袋外误差 | 只用未抽到该样例的那些树 |
| stacked generalization / stacking | 堆叠泛化 / 堆叠 | 降低偏差 |
| boosting | 提升 | ⚠️ 与第 9 章 lifting「提升」同形异义，不可互换 |
| weighted training set | 加权训练集 | |
| weak learning | 弱学习 | 训练集上略好于 50%+ε |
| decision stump | 决策树桩 | 只有根上一个测试 |
| gradient boosting | 梯度提升 | 分类可以用对数损失；这与 19.6.5 的 L2 不是同一处 |
| XGBOOST | XGBOOST | 算法名保留 |
| online learning | 在线学习 | |
| randomized weighted majority algorithm | 随机加权多数算法 | |
| regret | 遗憾 | 比事后最佳专家多犯的错误数 |
| no-regret learning | 无遗憾学习 | 每试平均遗憾趋于 0 |

### 系统开发

| English | 中文 | 备注 |
|---|---|---|
| federated learning | 联邦学习 | |
| data provenance | 数据溯源 | |
| data augmentation | 数据增强 | |
| unbalanced classes | 不平衡类别 | |
| undersampling | 欠采样 | |
| over-sample | 过采样 | 原文 over-sample |
| outlier | 离群点 | |
| one-hot encoding | 独热编码 | |
| quantization | 量化 | 连续值压进固定箱子 |
| exploratory data analysis (EDA) | 探索性数据分析 | |
| t-distributed stochastic neighbor embedding (t-SNE) | t 分布随机近邻嵌入 | 缩写 t-SNE 保留 |
| false positive | 假正例 | 本章例：合法邮件标成垃圾 |
| false negative | 假负例 | 本章例：垃圾标成合法 |
| receiver operating characteristic (ROC) curve | 受试者工作特征曲线 | |
| AUC | AUC | ROC 曲线下面积 |
| confusion matrix | 混淆矩阵 | |
| interpretability | 可解释性 | 检查模型本身 |
| explainability | 可说明性 | ⚠️ 可来自单独过程。勿与 interpretability 互换；有的作者把二者当同义词，本书正文分开 |
| LIME | LIME | local interpretable model-agnostic explanations |
| long tail | 长尾 | |
| nonstationarity | 非平稳 | |
| monitoring | 监控 | |
| transfer learning | 迁移学习 | 正文指向 21.7.2 |
| automated machine learning (AutoML) | 自动机器学习 | 只在文献注记 |
| metalearning | 元学习 | 文献注记；MAML 保留英文 |

### 5.2 第20章 学习概率模型

> 只收录 `AIMA-术语对照表.md` 中尚未出现的条目。已有译名沿用不重复：似然、贝叶斯法则、朴素贝叶斯、隐变量、先验/后验、证据、条件独立、无条件独立、相互独立、两两独立、高斯、平滑/滤波、贝叶斯网络、MCMC、HMM、牛顿–拉弗森法。
> 🚫 不译「绝对独立」。相互独立 ≠ 两两独立。本章 MAP 是最大后验假设，🚫 不把「最可能序列」译成 MAP。

### 术语

| English | 中文 | 备注 |
|---|---|---|
| statistical learning | 统计学习 | §20.1 标题 |
| Bayesian learning | 贝叶斯学习 | 用全部假设的后验加权预测 |
| hypothesis prior | 假设先验 | |
| maximum a posteriori (MAP) | 最大后验 | 读作 “em-ay-pee”。与总表「最可能序列」严格区分 |
| maximum-likelihood hypothesis | 最大似然假设 | h_ML |
| maximum-likelihood learning | 最大似然学习 | 均匀先验下的 MAP |
| Ockham's razor | 奥卡姆剃刀 | 原书拼作 Ockham，不作 Occam |
| minimum description length (MDL) | 最小描述长度 | |
| i.i.d. | 独立同分布 | 见书 p.665；袋子不够大则该假定失败 |
| density estimation | 密度估计 | 原指连续密度，现也用于离散分布；无监督 |
| complete data | 完整数据 | 每个数据点含模型中每一个变量的值 |
| parameter learning | 参数学习 | 结构固定，只求数值参数 |
| log likelihood | 对数似然 | 信息论压缩那一段用 log₂；最大化似然时底任意 |
| generative model | 生成模型 | 与总表 generative program「生成程序」不同 |
| discriminative model | 判别模型 | 学 P(类别 \| 输入)，不生成该类样本 |
| learning curve | 学习曲线 | |
| overfitting | 过拟合 | |
| beta distribution | 贝塔分布 | 布尔变量的共轭先验；均值 a/(a+b) |
| hyperparameter | 超参数 | 参数化「参数上的分布」 |
| conjugate prior | 共轭先验 | Beta 对更新封闭 |
| virtual count | 虚拟计数 | Beta(a,b) 相当于从 Beta(1,1) 出发已看过 a−1 颗 cherry、b−1 颗 lime |
| parameter independence | 参数独立 | P(Θ,Θ₁,Θ₂)=P(Θ)P(Θ₁)P(Θ₂)：无条件**相互**独立，不是两两独立 |
| uninformative prior | 无信息先验 | 例：θ₀=0 且 σ₀² 很大 |
| Bayesian linear regression | 贝叶斯线性回归 | |
| linear–Gaussian model | 线性–高斯模型 | 书 p.422；固定方差高斯噪声下等价于 L2 |
| L2 loss | L2 损失 | (y−(θ₁x+θ₂))² |
| nonparametric density estimation | 非参数密度估计 | |
| k-nearest-neighbors | k 近邻 | 本章用于密度估计；k=3 太尖，10 差不多，40 太滑 |
| kernel function | 核函数 | |
| kernel width | 核宽 | w；0.02 / 0.07 / 0.20 |
| cross-validation | 交叉验证 | 用来选 k 与 w |
| latent variable | 隐变量 | 与 hidden variable 同义；中文沿用总表「隐变量」，不另造「潜变量」 |
| expectation–maximization (EM) | 期望最大化 | E 步在前、M 步在后，不可写反 |
| E-step | E 步 | 期望步：算隐变量后验 / 指示变量期望 |
| M-step | M 步 | 最大化步：在该期望下最大化对数似然 |
| unsupervised clustering | 无监督聚类 | 类别标签不给出 |
| mixture distribution | 混合分布 | 先选分量再从该分量抽样 |
| component (of a mixture) | 分量 | 与总表 connected component「连通分量」不同 |
| mixture of Gaussians | 高斯混合 | 图 20.12(a) 权重从左到右 0.2、0.3、0.5 |
| indicator variable | 指示变量 | Zᵢⱼ ∈ {0,1}；E 步算的是它的期望 |
| identifiability | 可辨识性 | 两属性糖果混合不可辨识；Bag 对调也观测等价 |
| structural EM | 结构 EM | 用当前结构的期望计数评估新结构，不必为每个候选结构重算计数 |
| model selection | 模型选择 | 小结：结构学习是其一例 |
| Dirichlet family | 狄利克雷族 | 脚注：多值离散分布参数的共轭先验 |
| Normal–Wishart family | 正态–威沙特族 | 脚注：高斯参数的共轭先验。Wishart 取通行音译「威沙特」，未核对中译本 |
| Dirichlet process | 狄利克雷过程 | 注释：狄利克雷分布上的分布；Ferguson (1973) |
| Gaussian process | 高斯过程 | 注释：连续函数空间上的先验；Rasmussen and Williams (2006) |
| Parzen window | Parzen 窗 | 非参数密度估计的别名；人名保留英文 |

### 小节标题

二级据官方英文目录译出，三级据 PDF 正文标题自拟。均未核对人民邮电中译本目录。

| English | 中文 | 备注 |
|---|---|---|
| 20.1 Statistical Learning | 统计学习 | 无三级编号 |
| 20.2 Learning with Complete Data | 完整数据下的学习 | |
| 20.2.1 Maximum-likelihood parameter learning: Discrete models | 离散模型的最大似然参数学习 | 自拟·未核对 |
| 20.2.2 Naive Bayes models | 朴素贝叶斯模型 | 自拟·未核对；naive Bayes 总表已作「朴素贝叶斯」 |
| 20.2.3 Generative and discriminative models | 生成模型与判别模型 | 自拟·未核对 |
| 20.2.4 Maximum-likelihood parameter learning: Continuous models | 连续模型的最大似然参数学习 | 自拟·未核对 |
| 20.2.5 Bayesian parameter learning | 贝叶斯参数学习 | 自拟·未核对 |
| 20.2.6 Bayesian linear regression | 贝叶斯线性回归 | 自拟·未核对 |
| 20.2.7 Learning Bayes net structures | 学习贝叶斯网络结构 | 自拟·未核对 |
| 20.2.8 Density estimation with nonparametric models | 用非参数模型做密度估计 | 自拟·未核对 |
| 20.3 Learning with Hidden Variables: The EM Algorithm | 隐变量学习：EM 算法 | |
| 20.3.1 Unsupervised clustering: Learning mixtures of Gaussians | 无监督聚类：学习高斯混合 | 自拟·未核对 |
| 20.3.2 Learning Bayes net parameter values for hidden variables | 为隐变量学习贝叶斯网络的参数值 | 自拟·未核对 |
| 20.3.3 Learning hidden Markov models | 学习隐马尔可夫模型 | 自拟·未核对 |
| 20.3.4 The general form of the EM algorithm | EM 算法的一般形式 | 自拟·未核对 |
| 20.3.5 Learning Bayes net structures with hidden variables | 含隐变量的贝叶斯网络结构学习 | 自拟·未核对 |

### 5.3 第21章 深度学习

> 只收主表 `AIMA-术语对照表.md` **尚未单列**的条目。主表已有且本章沿用、不重复造译的包括：deep learning=深度学习、convolutional neural network=卷积神经网络、back-propagation=反向传播、perceptron=感知机、gradient=梯度、gradient descent=梯度下降、feature=特征、embedding=嵌入、normalization=归一化、Gaussian=高斯、likelihood=似然、prior/posterior=先验/后验、hidden variable=隐变量、stochastic=随机的、policy=策略、reward=奖励、GPU/TPU、neuron=神经元、connectionist=连接主义。
> 算法名、系统名保留英文。拿不准的在备注标待核。小节中文标题为自拟，未核对中译本正文。

### 1. 新术语

| English | 中文 | 备注 |
|---|---|---|
| feedforward network | 前馈网络 | 有向无环；与 recurrent network 对举 |
| recurrent neural network (RNN) | 循环神经网络 | 算法名 RNN 保留 |
| layer | 层 | “deep” 指多层 |
| neural network | 神经网络 | 主表只有历史小节标题，无本条 |
| unit | 单元 | ⚠️ 同形：主表 unit 指数独的行/列/宫。本章是网络中的计算节点 |
| activation function | 激活函数 | |
| logistic / sigmoid function | 逻辑斯谛函数 / sigmoid 函数 | 通行；备选“逻辑回归”里的“逻辑”。本章与 logistic regression 同一函数 |
| logistic regression | 逻辑斯谛回归 | 书页 684–685；备选“逻辑回归” |
| ReLU (rectified linear unit) | ReLU（整流线性单元） | 名称保留 ReLU |
| softplus | softplus | 平滑版 ReLU；名称保留 |
| tanh | tanh（双曲正切） | 名称保留 |
| weight | 权重 | |
| bias weight / dummy unit | 偏置权重 / 虚单元 | 虚单元 0 固定为 +1 |
| hidden layer | 隐藏层 | ⚠️ 不要与主表 hidden variable=隐变量 混用 |
| output layer | 输出层 | |
| input layer | 输入层 | |
| fully connected | 全连接 | |
| computation graph | 计算图 | |
| dataflow graph | 数据流图 | 与 computation graph 并称 |
| universal approximation theorem | 万能逼近定理 | 两层：先非线性、后线性 |
| loss function | 损失函数 | 与主表 cost function=代价函数分列。本章 loss 用损失函数 |
| squared loss / squared-error loss | 平方损失 / 平方误差损失 | `L₂`；标量时为 `(y−ŷ)²`，不是 `½` |
| negative log likelihood | 负对数似然 | likelihood=似然已入主表 |
| cross-entropy | 交叉熵 | ⚠️ 式 (21.7) 印刷号见笔记待核，不影响译名 |
| Kullback–Leibler divergence | KL 散度 | `D_KL(P∥Q)`；方向不可写反 |
| entropy | 熵 | (21.17) 推导中 `H(Q)=−∫Q log Q` |
| one-hot encoding | 独热编码 | 对应位为 1，其余为 0；是类别编码，不是概率 |
| softmax | softmax | 名称保留。`d=2` 时即 sigmoid |
| categorical distribution | 范畴分布 | |
| mixture density layer | 混合密度层 | 高斯混合的频率、均值、方差 |
| linear output layer | 线性输出层 | 回归：`ŷⱼ=inⱼ`，固定方差高斯的均值 |
| kernel | 核 | 在多个局部区域复制的权重模式。⚠️ 与核机器的 kernel 同词，本章是卷积核 |
| convolution | 卷积 | 脚注：信号处理里该运算叫 cross-correlation |
| cross-correlation | 互相关 | 脚注用语；神经网络领域仍叫卷积 |
| stride | 步幅 | `s`；二维为 `s_x, s_y` |
| padding | 填充 | 零或复制外层像素 |
| spatial invariance | 空间不变性 | 小到中等尺度；整幅图上下半不要求相同 |
| temporal invariance | 时间不变性 | 脚注；RNN 自动具有 |
| feature detector | 特征检测器 | feature=特征已入主表 |
| receptive field | 感受野 | 步幅 1 时第 `m` 层大小 `(l−1)m+1` |
| pooling | 池化 | 运算固定，不学习；通常无激活 |
| average-pooling | 平均池化 | 均匀核 `[1/l,…,1/l]` |
| max-pooling | 最大池化 | 书中比作逻辑析取 |
| downsampling | 下采样 | `l=s` 时分辨率按 `s` 变粗 |
| tensor | 张量 | 本章深度学习用法=多维数组；脚注指出严格数学定义还要求换基不变性 |
| feature map | 特征图 | |
| channel | 通道 | ⚠️ 同形：主表 channel routing=通道布线。本章是特征通道 / 颜色通道 |
| residual network | 残差网络 | |
| residual | 残差 | `f`，扰动默认的恒等传递 |
| minibatch | 小批量 | 大小 `m` |
| stochastic gradient descent (SGD) | 随机梯度下降 | stochastic=随机的已入主表；算法名 SGD 保留 |
| learning rate | 学习率 | `α`；`w ← w − α ∇_w L(w)` |
| momentum | 动量 | 过去小批量梯度的滑动平均 |
| vanishing gradient | 梯度消失 | |
| exploding gradient | 梯度爆炸 | RNN：`w_{z,z}>1`；一般看 `W_{z,z}` 第一特征值 |
| exploding / vanishing activations | 激活爆炸 / 激活消失 | 与梯度的消失、爆炸并列，21.4 数值稳定性 |
| automatic differentiation | 自动微分 | |
| reverse mode differentiation | 反向模式微分 | 反向传播是其应用 |
| end-to-end learning | 端到端学习 | |
| weight sharing | 权重共享 | 共享权重的梯度是各处贡献之和 |
| back-propagation through time | 沿时间反向传播 | 对网络大小线性 |
| batch normalization | 批归一化 | normalization=归一化已入主表；β、γ 可学习 |
| generalization | 泛化 | 以测试集衡量 |
| overfitting | 过拟合 | 本章无单独公式；与“再训练只降低不了测试误差”一起出现 |
| regularization | 正则化 | 19.4.3；神经网络里常实现为权重衰减 |
| weight decay | 权重衰减 | 惩罚 `λ Σ Wᵢ,ⱼ²`，`λ` 常在 `10⁻⁴` 附近 |
| maximum a posteriori (MAP) | 最大后验 | prior/posterior 已入主表 |
| dropout | dropout | 名称保留。以概率 `p` 乘 `1/p`，否则置 0；测试时关闭。备选“随机失活”不作为正文译名 |
| adversarial example | 对抗样本 | ⚠️ 同形：主表 adversarial search=对抗搜索。本章是输入上的对抗样本 |
| neural architecture search (NAS) | 神经架构搜索 | |
| graduate student descent (GSD) | graduate student descent | 脚注玩笑，保留英文 |
| recurrent neural network memory | 记忆 | 图 21.8 旁注 Memory；与 LSTM memory cell 相关但更泛 |
| long short-term memory (LSTM) | 长短期记忆 | 名称 LSTM 保留 |
| memory cell | 记忆细胞 | `c`；跨时间步复制，更新用加法 |
| gating unit | 门控单元 | 值在 `[0, 1]`，软门，不是布尔门 |
| forget gate | 遗忘门 | `f` |
| input gate | 输入门 | `i` |
| output gate | 输出门 | `o` |
| elementwise multiplication | 逐元素乘法 | `⊙` |
| unsupervised learning | 无监督学习 | |
| transfer learning | 迁移学习 | |
| semisupervised learning | 半监督学习 | 本章只给定义，不展开技术 |
| generative model | 生成模型 | |
| latent variable | 隐变量 | 与主表 hidden variable=隐变量 同译；本章符号 `z` |
| representation learning | 表示学习 | |
| probabilistic PCA (PPCA) | 概率主成分分析 | 算法名 PPCA 保留 |
| principal component | 主成分 | |
| autoencoder | 自编码器 | |
| encoder | 编码器 | |
| decoder | 解码器 | |
| linear autoencoder | 线性自编码器 | 与 PCA 的主成分对应；共享 `W` 与 `W⊤` |
| variational autoencoder (VAE) | 变分自编码器 | 名称 VAE 保留 |
| variational posterior | 变分后验 | `Q(z)`，用来近似 `P(z\|x)` |
| variational lower bound / ELBO | 变分下界 / 证据下界 | `L(x,Q)=log P(x)−D_KL(Q∥P(z\|x))` |
| autoregressive model (AR model) | 自回归模型 | `n` 元模型是 `n−1` 阶 AR |
| deep autoregressive model | 深度自回归模型 | |
| Yule–Walker equations | Yule–Walker 方程 | 人名保留；与正规方程相关 |
| generative adversarial network (GAN) | 生成对抗网络 | 名称 GAN 保留 |
| generator | 生成器 | ⚠️ 同形：主表 generator=多次返回的函数。本章是 GAN 的生成网络 |
| discriminator | 判别器 | |
| implicit model | 隐式模型 | 能采样，概率不易得到 |
| unsupervised translation | 无监督翻译 | 有 `x` 的样本和 `y` 的样本，没有配对 |
| multitask learning | 多任务学习 | |
| fine-tune | 微调 | |
| pretrained model | 预训练模型 | |
| freeze (layers) | 冻结（层） | 前几层当特征检测器时不更新 |
| word embedding | 词嵌入 | embedding=嵌入已入主表 |
| top-5 score | top-5 分数 | ImageNet 评价：正确类是否在前五个预测中 |
| deep reinforcement learning | 深度强化学习 | 主表只有 inverse reinforcement learning=逆向强化学习 |
| Q-function | Q 函数 | |
| value function | 价值函数 | 第 17 章用语；本章未单列进主表则在此补 |
| Hopfield network | Hopfield 网络 | 人名保留；对称连接、联想记忆、确定性 |
| Boltzmann machine | 玻尔兹曼机 | ⚠️ 主表已有 Boltzmann distribution=玻尔兹曼分布，不是同一条 |
| associative memory | 联想记忆 | |
| computational neuroscience | 计算神经科学 | |
| simple cell / complex cell | 简单细胞 / 复杂细胞 | Hubel & Wiesel；卷积≈简单细胞，池化≈复杂细胞 |
| neocognitron | neocognitron | 系统名保留 |
| madaline | madaline | 系统名保留；主表已有 adaline |
| B-type unorganized machine | B 型无组织机器 | Turing 1948 的叫法，保留英文并直译 |
| Kelley–Bryson gradient procedure | Kelley–Bryson 梯度程序 | Dreyfus (1990) 对反向传播的称呼 |

### 2. 小节标题（自拟，未核对中译本）

| 号 | English | 中文 |
|---|---|---|
| 21 | Deep Learning | 深度学习 |
| 21.1 | Simple Feedforward Networks | 简单前馈网络 |
| 21.1.1 | Networks as complex functions | 作为复杂函数的网络 |
| 21.1.2 | Gradients and learning | 梯度与学习 |
| 21.2 | Computation Graphs for Deep Learning | 深度学习的计算图 |
| 21.2.1 | Input encoding | 输入编码 |
| 21.2.2 | Output layers and loss functions | 输出层与损失函数 |
| 21.2.3 | Hidden layers | 隐藏层 |
| 21.3 | Convolutional Networks | 卷积网络 |
| 21.3.1 | Pooling and downsampling | 池化与下采样 |
| 21.3.2 | Tensor operations in CNNs | CNN 中的张量运算 |
| 21.3.3 | Residual networks | 残差网络 |
| 21.4 | Learning Algorithms | 学习算法 |
| 21.4.1 | Computing gradients in computation graphs | 在计算图中计算梯度 |
| 21.4.2 | Batch normalization | 批归一化 |
| 21.5 | Generalization | 泛化 |
| 21.5.1 | Choosing a network architecture | 选择网络架构 |
| 21.5.2 | Neural architecture search | 神经架构搜索 |
| 21.5.3 | Weight decay | 权重衰减 |
| 21.5.4 | Dropout | Dropout |
| 21.6 | Recurrent Neural Networks | 循环神经网络 |
| 21.6.1 | Training a basic RNN | 训练基本 RNN |
| 21.6.2 | Long short-term memory RNNs | 长短期记忆 RNN |
| 21.7 | Unsupervised Learning and Transfer Learning | 无监督学习与迁移学习 |
| 21.7.1 | Unsupervised learning | 无监督学习 |
| 21.7.2 | Transfer learning and multitask learning | 迁移学习与多任务学习 |
| 21.8 | Applications | 应用 |
| 21.8.1 | Vision | 视觉 |
| 21.8.2 | Natural language processing | 自然语言处理 |
| 21.8.3 | Reinforcement learning | 强化学习 |
| — | Summary | 小结 |
| — | Bibliographical and Historical Notes | 文献与历史注释 |

正文里无编号、笔记中用作小标题的原书旁注：Probabilistic PCA、Autoencoders、Deep autoregressive models、Generative adversarial networks、Unsupervised translation。译为：概率主成分分析、自编码器、深度自回归模型、生成对抗网络、无监督翻译。

### 3. 同形异义（合并进主表 §1.9 时单列）

| English | 本章 | 主表已有的另一义 |
|---|---|---|
| unit | 网络计算节点（单元） | 数独的行、列或宫 |
| generator | GAN 的生成网络 | 多次返回的函数 |
| channel | 特征通道 / 颜色通道 | channel routing 通道布线 |
| kernel | 卷积核 | 核方法里的核（本章脚注未展开，但用词会撞） |
| adversarial | adversarial example 对抗样本 | adversarial search 对抗搜索 |
| hidden | hidden layer 隐藏层 | hidden variable 隐变量 |
| normalization | batch normalization 批归一化 | 概率向量的归一化 |
| embedding | word embedding 词嵌入 | 主表 embedding 注的是 DEEPHOL 的表示；译名同为嵌入 |

### 5.4 第22章 强化学习

> 写前已 Grep `AIMA-术语对照表.md`。下表只收**主表未收录**的条目。
> 主表已有、本章沿用、不改写：reward=奖励，policy=策略，utility=效用，utility function=效用函数，discount factor=折扣因子，Bellman equation=贝尔曼方程，value iteration=价值迭代，policy iteration=策略迭代，MDP=马尔可夫决策过程，POMDP=部分可观测 MDP，exploration/exploitation=探索/利用，belief state=信念状态，transition model=转移模型，terminal state=终止状态，inverse reinforcement learning=逆向强化学习，model-free agent=无模型智能体，feature=特征，gradient=梯度，empirical gradient=经验梯度，back-propagation=反向传播，deep learning=深度学习，convolutional neural network=卷积神经网络，HTN=分层任务网络，assistance game=辅助博弈，Boltzmann distribution=玻尔兹曼分布，episodic=片段式，bandit problem=老虎机问题，penalty=惩罚，agent=智能体，environment=环境。
> 三级小节中文为自拟，**未与中译本核对**。
> 🚫 = 本章禁用译法。

### 1. 新增术语

### 1.1 问题与智能体

| English | 中文 | 备注 |
|---|---|---|
| reinforcement learning (RL) | 强化学习 | 缩写 RL 可直接使用 |
| sparse reward | 稀疏奖励 | |
| model-based reinforcement learning | 基于模型的强化学习 | ⚠️ 与第 2 章 model-based agent（智能体结构）分列 |
| model-free reinforcement learning | 无模型强化学习 | 主表已有 model-free agent=无模型智能体；此处是学习算法 |
| passive reinforcement learning | 被动强化学习 | 策略固定，学 `U^π` |
| active reinforcement learning | 主动强化学习 | 自己选动作；⚠️ 与被动不可互换 |
| passive learning agent | 被动学习智能体 | |
| active learning agent | 主动学习智能体 | |
| trial | 试验 | 从 (1,1) 到终止格的一条轨迹 |
| value function | 价值函数 | 脚注：RL 文献对效用函数的叫法，记 `V(s)`。主表 utility=效用，不改 |

### 1.2 被动学习

| English | 中文 | 备注 |
|---|---|---|
| direct utility estimation | 直接效用估计 | |
| reward-to-go | 此后奖励 | 从该状态起到终止的奖励之和；🚫 不要改叫第 17 章未使用的 “return/回报” 来替换本书用词 |
| adaptive dynamic programming (ADP) | 自适应动态规划 | |
| temporal-difference (TD) learning | 时序差分学习 | |
| temporal-difference equation | 时序差分方程 | 式 (22.3) |
| learning rate | 学习率 | `α` |
| step-size function | 步长函数 | `α(n)`；图 22.5 为 `60/(59+n)` |
| pseudoexperience | 伪经验 | 用当前模型模拟出来的转移 |
| prioritized sweeping | 优先扫描 | |

### 1.3 主动学习、探索与安全

| English | 中文 | 备注 |
|---|---|---|
| greedy agent | 贪心智能体 | 每步执行当前模型下的最优动作 |
| policy loss | 策略损失 | 图 22.6 在 (1,1) 上为 0.235；原文未给独立公式 |
| GLIE | 无限探索极限下的贪心 | greedy in the limit of infinite exploration；缩写保留 |
| exploration function | 探索函数 | `f(u,n)` |
| optimistic estimate | 乐观估计 | `U⁺`；`R⁺` 是最佳奖励的乐观估计 |
| absorbing state | 吸收状态 | 动作无效果、也无奖励 |
| safe exploration | 安全探索 | |
| Bayesian reinforcement learning | 贝叶斯强化学习 | |
| exploration POMDP | 探索 POMDP | 信念状态是模型上的分布；不是第 17 章的主例 |
| robust control theory | 鲁棒控制理论 | |
| robust policy | 鲁棒策略 | `argmax_π min_h U^π_h` |

### 1.4 动作效用与 Q 学习

| English | 中文 | 备注 |
|---|---|---|
| action-utility learning | 动作效用学习 | |
| action-utility function | 动作效用函数 | |
| Q-learning | Q-learning | 可辅以“Q 学习”；算法名保留英文 |
| Q-function | Q 函数 | `Q(s,a)` |
| quality-function | 品质函数 | 书中 Q-function 的同位语；🚫 质量函数 |
| SARSA | SARSA | state, action, reward, state, action；保留 |
| off-policy | 离策略 | Q-learning |
| on-policy | 在策略 | SARSA |

### 1.5 泛化、整形与分层

| English | 中文 | 备注 |
|---|---|---|
| function approximation | 函数近似 | |
| Widrow–Hoff rule | Widrow–Hoff 规则 | 人名保留 |
| delta rule | delta 规则 | 与上一行同一更新 |
| catastrophic forgetting | 灾难性遗忘 | |
| experience replay | 经验回放 | |
| deep reinforcement learning | 深度强化学习 | |
| credit assignment problem | 信用分配问题 | |
| reward shaping | 奖励整形 | 与第 17 章势函数整形同一公式；备选“奖励塑造” |
| pseudoreward | 伪奖励 | |
| hierarchical reinforcement learning (HRL) | 分层强化学习 | |
| partial program | 部分程序 | |
| joint state space | 联合状态空间 | `(s, m)` |
| machine state | 机器状态 | 程序计数器、参数与变量；指智能体程序内部状态 |
| choice state | 选择状态 | `σ = (s, m)` |
| additive decomposition | 加性分解 | |
| semi-Markov decision process | 半马尔可夫决策过程 | 脚注：动作时长可以不同 |

### 1.6 策略搜索与逆向强化学习

| English | 中文 | 备注 |
|---|---|---|
| policy search | 策略搜索 | 直接改进策略表示；与 Q-learning 的目标不同 |
| stochastic policy | 随机策略 | `π_θ(s,a)` |
| softmax function | softmax 函数 | 式 (22.14)，`β > 0` |
| policy value | 策略价值 | `ρ(θ)`，期望此后奖励 |
| policy gradient | 策略梯度 | `∇_θ ρ(θ)` |
| REINFORCE | REINFORCE | Williams 1992；算法名保留 |
| correlated sampling | 相关抽样 | |
| apprenticeship learning | 学徒学习 | |
| imitation learning | 模仿学习 | 对状态–动作对做监督学习 |
| feature matching | 特征匹配 | |
| feature expectation | 特征期望 | `μ_i(π)` |
| Boltzmann rationality | 玻尔兹曼理性 | 主表已有 Boltzmann distribution=玻尔兹曼分布；此处是 softmax 策略假设 |
| behavioral cloning | 行为克隆 | Sammut 等，1992；书末注 |

### 1.7 应用中的问题名

| English | 中文 | 备注 |
|---|---|---|
| deep Q-network (DQN) | 深度 Q 网络 | 缩写 DQN 保留 |
| cart–pole balancing | 车杆平衡 | |
| inverted pendulum | 倒立摆 | 与车杆平衡同一问题 |
| bang-bang control | bang-bang 控制 | 离散的左右猛推 |
| keepaway | keepaway | 游戏专名保留；三对二控球 |

**新增术语 72 条**（§1.1–§1.7 表行合计）。专名 NEUROGAMMON、TD-GAMMON、BOXES、PEGASUS、DYNA、ALPHAGO、ALPHAZERO、ALE 等算法/系统名保留英文，不单列译名。

### 2. 同形异义（建议并入主表 §1.9）

| English | 语境 A | 语境 B |
|---|---|---|
| model-based | 第 2 章：智能体**结构**（基于模型的反射智能体） | 本章：学习算法**使用转移模型** |
| utility / value function | 本书正文：效用 `U` | RL 文献脚注：价值函数 `V(s)`，同一量 |
| Q-learning 学到的 `θ` | 使 `Q̂` 接近 `Q*` | 策略搜索学到的 `θ`：使性能好；`Q*/100` 仍可最优 |
| feature | 主表：状态的可计算属性 | 本章 feature expectation / feature matching：奖励的线性特征及其折扣期望 |
| Boltzmann | 主表：玻尔兹曼分布 | 本章 Boltzmann rationality：用 softmax 描述专家的偶然失误 |

### 3. 小节标题中英对照

二级标题中文为自拟，未与人民邮电出版社中译本核对。三级标题自拟，编号来自 PDF 正文，无跳号。

| 号 | English | 中文 |
|---|---|---|
| 22.1 | Learning from Rewards | 从奖励中学习 |
| 22.2 | Passive Reinforcement Learning | 被动强化学习 |
| 22.2.1 | Direct utility estimation | 直接效用估计 |
| 22.2.2 | Adaptive dynamic programming | 自适应动态规划 |
| 22.2.3 | Temporal-difference learning | 时序差分学习 |
| 22.3 | Active Reinforcement Learning | 主动强化学习 |
| 22.3.1 | Exploration | 探索 |
| 22.3.2 | Safe exploration | 安全探索 |
| 22.3.3 | Temporal-difference Q-learning | 时序差分 Q 学习 |
| 22.4 | Generalization in Reinforcement Learning | 强化学习中的泛化 |
| 22.4.1 | Approximating direct utility estimation | 近似直接效用估计 |
| 22.4.2 | Approximating temporal-difference learning | 近似时序差分学习 |
| 22.4.3 | Deep reinforcement learning | 深度强化学习 |
| 22.4.4 | Reward shaping | 奖励整形 |
| 22.4.5 | Hierarchical reinforcement learning | 分层强化学习 |
| 22.5 | Policy Search | 策略搜索 |
| 22.6 | Apprenticeship and Inverse Reinforcement Learning | 学徒学习与逆向强化学习 |
| 22.7 | Applications of Reinforcement Learning | 强化学习的应用 |
| 22.7.1 | Applications in game playing | 博弈中的应用 |
| 22.7.2 | Application to robot control | 机器人控制中的应用 |

Summary、Bibliographical and Historical Notes 分别写为「小结」「延伸阅读」，不单列编号。

### 4. 本章待核（不改原书）

| # | 类型 | 现象 | 处理 |
|---|---|---|---|
| 1 | T6/T7 | p.794：第一次试验后写 `U^π(1,3)=0.88`、`U^π(2,3)=0.96`，若转移总发生则应为 0.92；下一句又说“当前估计 **0.84** 偏低”。0.84 与 0.92 是 (1,3) 的两个样本，0.88 才是它们的平均 | 笔记两数照录，标 ⚠️ 待核 |
| 2 | T2/T8 | p.800：写有三种数学途径，正文只展开贝叶斯强化学习与鲁棒控制，随后是人类知识（示教与外部约束） | 不补写第三条 |
| 3 | T7 | 图 22.1(b) 的四位小数在 PDF 文本层是三行，未带格子坐标；+1/−1 不在小数文本层 | 按 4×3 坐标从左到右、自上而下安放，并在笔记中说明来源 |

### 5.5 第23章 自然语言处理

> 待合并进 `AIMA-术语对照表.md`，合并前**不**视为总表已生效。
> 判定：`book-translation` skill §3。① 总表已有则沿用，不改写；② 人邮 4e 目录（天珑书店转载，ISBN 9787115598103）核对二级与已列出的三级；③ 通行译法；④ 自拟则在备注标明。
> 格式：`| English | 中文 | 备注 |`。已有条目见文末「沿用」，**不计入**新术语条数。

### 1. 新术语

### 1.1 语言模型与 n 元

| English | 中文 | 备注 |
|---|---|---|
| natural language processing (NLP) | 自然语言处理 | 缩写 NLP |
| language model | 语言模型 | |
| bag-of-words model | 词袋模型 | ✅ 人邮 23.1.1；生成模型，词条件独立 |
| corpus | 语料库 | |
| tokenization | 词元切分 | “aren’t” 可切成 aren/’/t 或 are/n’t |
| n-gram | n 元语法 | 长度为 n 的符号串。⚠️「语法」译 *gram*，不是 grammar，也不是逻辑章的 syntax |
| n-gram model | n 元模型 | ✅ 人邮「n 元单词模型 / n 元模型的平滑」 |
| unigram / bigram / trigram | 一元语法 / 二元语法 / 三元语法 | 即 1-gram / 2-gram / 3-gram |
| character-level model | 字符级模型 | |
| language identification | 语种识别 | 短文本通常 >99%；瑞典语/挪威语约 95% |
| skip-gram | 跳词模型 | ⚠️ 本章 = 跳过词的 n 元计数（“je ne comprends pas”）。不是第 24 章词向量的 skip-gram |
| out-of-vocabulary word | 词表外词 | 概率不可写成 0，否则整句为 0。符号 `<UNK>` 不译 |
| smoothing (n-gram) | 平滑 | ⚠️ 与第 14 章「平滑」同形异义，见 §2 |
| Laplace smoothing / add-one smoothing | 拉普拉斯平滑 / 加一平滑 | 估计形如 1/(N+2)。许多 NLP 任务上效果差 |
| backoff model | 回退模型 | 低计数或零计数时退到 (n−1) 元 |
| linear interpolation smoothing | 线性插值平滑 | `λ₃+λ₂+λ₁=1`；变量是 `cᵢ` 不是 `wᵢ` |
| stupid backoff | stupid backoff | 算法名保留；靠更大语料让简单平滑够用 |
| dictionary | 词典 | 与 lexicon（词库）分列 |
| WordNet | WordNet | 系统名不译 |
| part of speech (POS) | 词性 | 亦称 lexical category 或 tag |
| lexical category | 词汇类别 | 沿用 category→类别；🚫 不译「范畴」 |
| part-of-speech tagging | 词性标注 | ✅ 人邮 23.1.6 |
| Penn Treebank | 宾州树库（Penn Treebank） | 45 个标记；三百多万词 |
| logistic regression | 逻辑斯谛回归 | 第 19.6.5 节；判别模型。中译本用词未逐条核对 |
| support vector machine | 支持向量机 | 词袋分类的备选，本章未展开 |
| feature selection | 特征选择 | |
| gradient descent | 梯度下降 | 逻辑斯谛回归的权重学习 |
| greedy search | 贪婪搜索 | 沿用总表 greedy→贪婪。每步选定后不回溯 |
| generative model | 生成模型 | 学习联合 `P(W, C)`，能抽样出句子 |
| discriminative model | 判别模型 | 学习条件 `P(C\|W)`，不能生成随机句子。⚠️ 方向不可对调 |

### 1.2 文法与句法分析

| English | 中文 | 备注 |
|---|---|---|
| grammar | 文法 | ✅ 人邮 23.2。🚫 不与 syntax（语法，逻辑章）合并 |
| language (of a grammar) | 语言 | 遵循文法规则的句子集合 |
| syntactic category | 句法类别 | 如 NP、VP。🚫 不译「句法范畴」 |
| phrase structure | 短语结构 | |
| probabilistic context-free grammar (PCFG) | 概率上下文无关文法 | |
| context-free | 上下文无关 | 任何规则可用于任何上下文；同一短语两处概率相同 |
| probabilistic grammar | 概率文法 | 给每个字符串一个概率 |
| overgeneration | 过生成 | 例：“Me go I.” |
| undergeneration | 欠生成 | 例：“I think the wumpus is smelly.” |
| lexicon | 词库 | 图 23.3。与 dictionary 分列 |
| open class | 开放类 | 名词、名字、动词、形容词、副词；不断有新词 |
| closed class | 封闭类 | 代词、关系代词、冠词、介词、连词；大约十来个，以世纪计变化 |
| parsing | 句法分析 | ✅ 人邮 23.3 |
| parse tree | 分析树 | |
| top-down / bottom-up parsing | 自顶向下 / 自底向上句法分析 | |
| chart | 线图 | |
| chart parser | 线图分析器 | |
| CYK algorithm | CYK 算法 | 人名照录 Ali Cocke, Daniel Younger, Tadeo Kasami。⚠️ 待核，见章末 |
| Chomsky Normal Form | 乔姆斯基范式（Chomsky Normal Form） | 词汇规则 `X → word [p]`；句法规则 `X → Y Z [p]` |
| shift-reduce parsing | 移进–归约分析 | `b=1` 的束搜索即确定性分析器的一种做法 |
| deterministic parser | 确定性分析器 | 束宽 `b = 1` |
| dependency grammar | 依存文法 | |
| dependency parsing | 依存分析 | ✅ 人邮 23.3.1 |
| head | 中心词 | 短语中最重要的词。⚠️ 与第 7–9 章子句的「头」分列，见 §2 |
| treebank | 树库 | Penn Treebank 超过 10 万句 |
| data-oriented parsing | 数据导向句法分析 | Bod et al. 2003；Bod 2008 |
| unsupervised parsing | 无监督句法分析 | 句子没有树 |
| semisupervised parsing | 半监督句法分析 | 少量树 + 大量未分析句子 |
| inside–outside algorithm | 内外算法 | 正文引 Dodd, 1988；注记归 Baker, 1979。⚠️ |
| curriculum learning | 课程学习 | 从两词句到 40 词句 |
| partial bracketing | 部分括号 | HTML 等作者标记，不是专家树库 |
| augmented grammar | 扩展文法 | ✅ 人邮 23.4。不用「增强文法」 |
| lexicalized PCFG | 词汇化 PCFG | 概率依赖中心词，不只依赖句法类别 |
| subjective case | 主语格 | 脚注亦称 nominative 主格。例：I |
| objective case | 宾语格 | 脚注亦称 accusative 宾格。例：me |
| nominative / accusative / dative case | 主格 / 宾格 / 与格 | 仅脚注。与 subjective / objective 分列，不互相替换 |
| agreement | 一致 | 主谓的人称与数相同，且 NP 为主语格，才能构成 S |
| compositional semantics | 组合语义 | 短语语义是子短语语义的函数。总表 compositionality=组合性 |
| semantic interpretation | 语义解释 | ✅ 人邮 23.4.1 |
| β-reduction | β 归约 | `(λx Loves(x, Bo))(Ali)` 得到 `Loves(Ali, Bo)` |
| semantic grammar | 语义文法 | ✅ 人邮 23.4.2 |

### 1.3 真实语言与任务

| English | 中文 | 备注 |
|---|---|---|
| quantification | 量化 | 与总表 quantifier=量词相关。句法一种分析，语义可有两种辖域 |
| quasi-logical form | 准逻辑形式 | 辖域由分析过程之外的算法决定 |
| pragmatics | 语用 | |
| indexical | 指示语 | 例：“I am in Boston today” 中的 I、today |
| speech act | 言语行为 | 疑问、陈述、承诺、警告、命令等 |
| long-distance dependency | 长距离依存 | 空位与其所指 NP 可隔任意远；书中一例为 11 个词 |
| gap | 空位 | 缺失的 NP。不能只出现在 NP 并列的一个分支 |
| ambiguity | 歧义 | |
| lexical ambiguity | 词汇歧义 | ⚠️ 不是总表的 word-sense disambiguation 一词的同义替换；后者是任务名 |
| syntactic ambiguity | 句法歧义 | 例：“in 2,2” 修饰名词或动词 |
| semantic ambiguity | 语义歧义 | 可由句法歧义引起。修饰名词→wumpus 在 2,2；修饰动词→臭气在 2,2 |
| metonymy | 转喻 | `Metonymy(m, x)`：`m` 为转喻对象（发言人），`x` 为字面对象（Chrysler） |
| metaphor | 隐喻 | 原书：可看成关系为相似的转喻 |
| disambiguation | 消歧 | 解释概率 = 所用规则概率之积；反映语料一般知识，不是当前情境 |
| world model | 世界模型 | 消歧四模型之 1 |
| mental model | 心理模型 | 消歧四模型之 2。政客例：不是罪犯 50%，不是牧杖 99.999%，仍选前者 |
| acoustic model | 声学模型 | 消歧四模型之 4。手写/打字则是 OCR |
| speech recognition | 语音识别 | 词错误率约 3%–5% |
| word error rate | 词错误率 | |
| text-to-speech synthesis | 文语转换 | 亦称语音合成。WaveNet：约 2/3 听者认为更自然 |
| machine translation | 机器翻译 | |
| bilingual corpus | 双语语料库 | 不必标注 |
| information extraction | 信息抽取 | |
| information retrieval | 信息检索 | |
| question answering | 问答 | 响应是答案，不是排序的文档列表 |
| spam detection | 垃圾邮件检测 | |
| sentiment analysis | 情感分析 | 正/负，不是分数 |
| author attribution | 作者归属 | |
| named-entity recognition | 命名实体识别 | 出现在小结的任务列举 |
| genre classification | 体裁分类 | 出现在小结 |
| spelling correction | 拼写更正 | 语言模型的用途之一 |
| optical character recognition (OCR) | 光学字符识别 | 书面通信上与声学模型对举 |
| regular expression | 正则表达式 | 结构化文本上的信息抽取 |

### 1.4 文献注记中首次需要固定的译名

| English | 中文 | 备注 |
|---|---|---|
| optimality theory | 优选论 | Smolensky and Prince, 1993。注记，非正文模型 |
| universal grammar | 普遍文法 | Gold 1967 之后 Chomsky/Pinker 的论证 |
| poverty of the stimulus | 刺激贫乏 | 儿童输入不足以学 CFG，故假定生来已知文法。多数计算机科学家不接受 |
| maximum entropy Markov model (MEMM) | 最大熵马尔可夫模型 | 逻辑斯谛回归词性标注的历史别名 |
| PAC learning | PAC 学习 | Horning 1969：概率上下文无关文法在 PAC 意义上可学习。与 Gold 的否定结果不是同一标准 |

### 2. 同形异义（不合并）

| English | 语境 A | 语境 B |
|---|---|---|
| smoothing | 第 14 章：给定更晚证据后，对**过去状态**的后验（滤波/预测/平滑） | 本章：n 元**计数**的平滑（加一、回退、插值），给未见 n 元留概率质量 |
| grammar / syntax / n-gram | grammar → **文法**（规则系统） | syntax → **语法**（总表，逻辑章）；n-gram 的「语法」只译 *gram* |
| skip-gram | 本章：跳过中间词的搭配计数 | 第 24 章：词向量训练里的 skip-gram。本章禁止混用 |
| model | 语言模型：字符串上的概率分布 | 总表：逻辑模型 / 概率模型。不要写成「一种解释」 |
| sentence | 本章：自然语言词串 | 第 7 章：逻辑句子。本章仍用「句子」，不另造译名 |
| category | 总表：类别；🚫 范畴 | 本章句法类别、词汇类别、子类别都用「类别」 |
| disambiguation / word-sense disambiguation | 本章消歧：恢复整句最可能的意图意义，四模型 | 总表词义消歧：多义词选义。前者不蕴含后者已在本章定义 |
| beam search | 第 3 章译「束搜索」。本章 POS 与句法分析沿用此译 | 第 5 章另有「集束搜索」。本章不改用第 5 章译名 |
| generative | 本章生成模型：联合分布 `P(W,C)` | 第 15 章生成程序。相关但不是同一个术语 |
| head | 本章：短语中心词 | 第 7–9 章：子句的头。不要互译 |

### 3. 小节标题

> ✅ = 与人邮 4e 目录一致（繁体转简体）。未标 ✅ 的三级为英文 PDF 有、人邮目录未列。

| 号 | English | 中文 | 备注 |
|---|---|---|---|
| 23 | Natural Language Processing | 自然语言处理 | ✅ |
| 23.1 | Language Models | 语言模型 | ✅ |
| 23.1.1 | The bag-of-words model | 词袋模型 | ✅ |
| 23.1.2 | N-gram word models | n 元单词模型 | ✅ |
| 23.1.3 | Other n-gram models | 其他 n 元模型 | ✅ |
| 23.1.4 | Smoothing n-gram models | n 元模型的平滑 | ✅ |
| 23.1.5 | Word representations | 单词表示 | ✅ |
| 23.1.6 | Part-of-speech (POS) tagging | 词性标注 | ✅ |
| 23.1.7 | Comparing language models | 语言模型的比较 | ✅ |
| 23.2 | Grammar | 文法 | ✅ |
| 23.2.1 | The lexicon of E0 | E0 的词库 | 自拟。人邮目录未列此号 |
| 23.3 | Parsing | 句法分析 | ✅ |
| 23.3.1 | Dependency parsing | 依存分析 | ✅ |
| 23.3.2 | Learning a parser from examples | 从样例中学习句法分析器 | ✅ |
| 23.4 | Augmented Grammars | 扩展文法 | ✅ 不用「增强文法」 |
| 23.4.1 | Semantic interpretation | 语义解释 | ✅ |
| 23.4.2 | Learning semantic grammars | 学习语义文法 | ✅ |
| 23.5 | Complications of Real Natural Language | 真实自然语言的复杂性 | ✅ 其下量化、语用等无三级编号 |
| 23.6 | Natural Language Tasks | 自然语言任务 | ✅ 无三级编号 |

### 4. 沿用总表、本章未改写

| English | 中文 | 本章用法 |
|---|---|---|
| naive Bayes | 朴素贝叶斯 | 词袋即式 (12.21) |
| Bayes' rule | 贝叶斯法则 | 不写「定理」 |
| prior | 先验 | `P(Class)` |
| HMM | 隐马尔可夫模型 | 词性；证据 `W₁:N`，隐状态 `C₁:N` |
| Viterbi | 维特比 | 第 14.2.3 节；标注约 97% |
| smoothing | 平滑 | 仅作第 14 章旧译；本章新义见 §1 与 §2 |
| agent | 智能体 | |
| sentence | 句子 | |
| inference | 推断 | |
| category / subcategory | 类别 / 子类别 | 🚫 范畴。本章子类别指带格、人称、数的类别，不另造译名 |
| quantifier | 量词 | |
| compositionality | 组合性 | 本章短语原则称组合语义 |
| λ-expression | λ 表达式 | 书第 259 页 |
| event calculus | 事件演算 | 第 10.3 节 |
| fluent | 流变 | `Speaker`；🚫 流子/流体 |
| dynamic programming | 动态规划 | 线图分析的依据 |
| beam search | 束搜索 | 沿用第 3 章，不用第 5 章「集束搜索」 |
| feature | 特征 | |
| classification | 分类 | |
| word-sense disambiguation | 词义消歧 | 本章正文用的是更广的 disambiguation，不把二者写成同一个词 |

新术语条数：**§1 共 109 条**（1.1 共 30，1.2 共 41，1.3 共 33，1.4 共 5）。小节标题 19 条另计，不计入 109。总表已有、仅在 §4 注明用法的条目（含 subcategory）不计入。

### 5.6 第24章 自然语言处理中的深度学习

> 只收录 `AIMA-术语对照表.md` 中**尚未出现**的条目。合并前勿改主表。
> 已沿用、不重复收入：deep learning = 深度学习；back-propagation = 反向传播；gradient = 梯度；gradient descent = 梯度下降；beam search = **束搜索**（第 3/4 章。第 5 章另有「集束搜索」，本章解码不用该译法）；state of the art = **最新进展**（24.6 节名）；embedding = 嵌入（主表指 DEEPHOL，与本章 word embedding 分列）。
> 三级小节中文为自拟，未与中译本核对。
> 专名保留英文。原书全大写的（WORD2VEC、ELMO、ROBERTA、SQUAD）照录，不改成后来的大小写。

### 1. 词与表示

| English | 中文 | 备注 |
| ------- | ---- | ---- |
| word embedding | 词嵌入 | 低维稠密向量。⚠️ 与主表 embedding「嵌入」分列 |
| one-hot vector | 独热向量 | 第 `i` 位为 1、其余为 0；见 §21.2.1 |
| n-gram | n 元 | 5-gram = 5 元。模型称 n 元模型。参数量 `O(vⁿ)` |
| vocabulary | 词表 | 大小记为 `v` |
| word token | 词元 | 建词表时按出现次数筛选 |
| feature engineering | 特征工程 | 词嵌入想避免的手工步骤 |
| downstream task | 下游任务 | 问答、翻译、摘要等 |
| part-of-speech tagging (POS tagging) | 词性标注 | §23.1.6 |
| character-level model | 字符级模型 | 每个字符一个独热；本章多数工作不用 |
| word-level encoding | 词级编码 | 与字符级相对 |

### 2. 网络与训练

| English | 中文 | 备注 |
| ------- | ---- | ---- |
| feedforward network | 前馈网络 | 固定窗口；参数量 `O(n)` |
| hidden layer | 隐藏层 | ⚠️ 不是主表 hidden variable「隐变量」 |
| activation function | 激活函数 | 记号 `σ`；Transformer 里通常用 ReLU |
| softmax | softmax | 函数名保留 |
| recurrent neural network (RNN) | 循环神经网络 | 缩写 RNN 保留 |
| language model | 语言模型 | 词序列上的概率分布 |
| multiclass classification | 多类分类 | RNN 语言模型的类别 = 词表中的词 |
| back-propagation through time | 沿时间反向传播 | 正文 back-propagate through time；各时间步权重相同 |
| hyperparameter | 超参数 | 语言模型抽样时的采样权重 |
| sampling weight | 采样权重 | 最可能词 / 按概率抽样 / 过度采样不太可能的词 |
| bidirectional RNN | 双向循环神经网络 | 从左到右与从右到左拼接 |
| average pooling | 平均池化 | `z̃ = (1/s) Σ_{t=1}^{s} zₜ` |
| long short-term memory (LSTM) | 长短期记忆 | 缩写 LSTM 保留；§21.6.2 |
| gating unit | 门控单元 | LSTM 用来记住或忘掉 |
| vanishing gradient problem | 梯度消失问题 | 书页 756；本章是时间上的层 |
| latent feature | 潜在特征 | 如主语的人称与数 |
| overfitting | 过拟合 | 加大隐藏状态或拼接全部源向量时会提到 |
| ReLU | ReLU | rectified linear unit，整流线性单元。激活名保留 |
| residual connection | 残差连接 | 每层 Transformer 两条 |

### 3. 序列到序列与注意力

| English | 中文 | 备注 |
| ------- | ---- | ---- |
| machine translation (MT) | 机器翻译 | |
| source language | 源语言 | |
| target language | 目标语言 | |
| sequence-to-sequence model | 序列到序列模型 | 原书不用 seq2seq 这一缩写 |
| basic sequence-to-sequence model | 基本序列到序列模型 | 源 RNN 最终隐藏状态 = 目标 RNN 初始隐藏状态 |
| nearby context bias | 近处上下文偏向 | 三个缺点之一 |
| fixed context size limit | 固定上下文规模上限 | 约 1024 维；64 词则每词约 16 维 |
| attention | 注意力 | 部件本身无 learnable weights |
| attentional sequence-to-sequence model | 带注意力的序列到序列模型 | |
| context vector | 上下文向量 | `cᵢ` |
| attention score | 注意力分数 | `rᵢⱼ`，未经 softmax |
| decoding | 解码 | 一次生成一个目标词再送回 |
| greedy decoding | 贪婪解码 | 每步取最高概率并完全承诺 |
| hypothesis | 假设 | 束中的候选译文 |

### 4. Transformer

| English | 中文 | 备注 |
| ------- | ---- | ---- |
| transformer | Transformer | 架构名保留英文 |
| self-attention | 自注意力 | 源对源、目标对目标 |
| query vector | 查询向量 | `qᵢ = W_q xᵢ` |
| key vector | 键向量 | `kᵢ = W_k xᵢ` |
| value vector | 值向量 | `vᵢ = W_v xᵢ` |
| multiheaded attention | 多头注意力 | 原书：把句子分成 `m` 等份，各有权重，再拼接。不要改写成「切分通道」 |
| positional embedding | 位置嵌入 | 最大长度 `n` 则学习 `n` 个；与词嵌入相加 |
| transformer encoder | Transformer 编码器 | 本节先讲的一半；用于文本分类 |
| transformer decoder | Transformer 解码器 | 只能注意左侧；另有模块注意编码器 |

### 5. 预训练与上下文

| English | 中文 | 备注 |
| ------- | ---- | ---- |
| pretraining | 预训练 | 迁移学习的一种，§21.7.2 |
| transfer learning | 迁移学习 | |
| fine-tuning | 微调 | GPT-2 在正文所列任务上是不做微调的；小结里的一般说法是微调之后用于问答等 |
| skip-gram | skip-gram | 本章只说 GloVe 的计数「类似于」它，未给定义。保留英文 |
| contextual representation | 上下文表示 | 词 + 周围上下文 → 向量 |
| noncontextual word embedding | 非上下文词嵌入 | 图 24.11 的输入之一 |
| polysemous word | 多义词 | 例：rose |
| masked language model (MLM) | 掩码语言模型 | 只预测被掩盖的词；句子自带标签 |

### 6. 任务、评价与语言事实

| English | 中文 | 备注 |
| ------- | ---- | ---- |
| reference resolution | 指代消解 | 24.2 开头用词 |
| coreference resolution | 共指消解 | 24.2.2 用词。本章例子都是 him → Miguel |
| antecedent | 先行词 | 共指 softmax 的类别 |
| sentiment analysis | 情感分析 | Positive / Negative；也可以多于两类或一个标量 |
| question answering | 问答 | |
| reading comprehension | 阅读理解 | |
| summarization | 摘要 | 长文本改写成意思相同的短文本 |
| grammaticality judgment | 语法性判断 | MLM 预训练表示的用途之一 |
| textual entailment | 文本蕴含 | |
| natural language inference | 自然语言推断 | 前提是否蕴含假设。例：all animals need to eat / dogs need to eat |
| named entity recognition | 命名实体识别 | 文献注记 |
| perplexity | 困惑度 | `2ᴴ`，`H` 为熵，见 §19.3.3。其他条件相同才是越低越好 |
| Zipf's Law | 齐夫定律 | 第 `n` 常见词的频率大致与 `n` 成反比 |
| constituency parser | 成分句法分析器 | Kitaev and Klein (2018) |
| dependency parser | 依存句法分析器 | SLING |
| semantic frame | 语义框架 | SLING 的直接输出 |
| pipeline system | 流水线系统 | 错误会逐级堆积 |

### 7. 专名（保留英文）

| English | 中文 | 备注 |
| ------- | ---- | ---- |
| WORD2VEC | WORD2VEC | 系统名。2013。原书小型大写，笔记用这一拼写 |
| GloVe (Global Vectors) | GloVe | 2014。全称 Global Vectors |
| FASTTEXT | FASTTEXT | 157 种语言 |
| ELMO | ELMO | Embeddings from Language Models。原书全大写；通行拼写 ELMo，笔记照录 ELMO |
| BERT | BERT | Bidirectional Encoder Representations from Transformers。Devlin et al. (2018)，在文献注记 |
| GPT-2 | GPT-2 | 15 亿参数，40GB。本章正文的生成模型止于此 |
| ROBERTA | ROBERTA | 原书全大写 |
| XLNET | XLNET | 文献注记。消除预训练与微调的不一致 |
| ERNIE 2.0 | ERNIE 2.0 | 文献注记。句序与命名实体 |
| ALBERT (A Lite BERT) | ALBERT | 参数从 1.08 亿减到 1200 万 |
| XLM | XLM | 多语言 Transformer |
| T5 (Text-to-Text Transfer Transformer) | T5 | 350 亿词，750GB 的 C4 |
| ULMFIT | ULMFIT | Universal Language Model Fine-tuning |
| Reformer | Reformer | 上下文最多约一百万词。Kitaev et al. (2020) |
| GLUE | GLUE | General Language Understanding Evaluation |
| SUPERGLUE | SUPERGLUE | 人类基线在 GLUE 上落到第九名之后提出 |
| ARISTO | ARISTO | 八年级科学多项选择 91.6% |
| C4 (Colossal Clean Crawled Corpus) | C4 | |
| SQUAD | SQUAD | 原书拼写。通行作 SQuAD。Rajpurkar et al. (2016) |
| SYSTRAN | SYSTRAN | Toma (1977)，第一个商业成功的机器翻译系统 |
| SLING | SLING | Ringgaard et al. (2017) |
| ImageNet | ImageNet | 2012 年视觉转折的参照 |
| Penn Treebank | Penn Treebank | |
| Winograd Schema Challenge | Winograd 模式挑战 | 标出歧义代词 |
| Common Crawl | Common Crawl | 文本数据来源 |
| CoNLL | CoNLL | Conference on Computational Natural Language Learning |
| PASCAL Challenge | PASCAL 挑战 | 自然语言推断。Dagan et al. (2005) |

### 8. 小节标题

> 二级英文来自官方目录与正文标题。中文自拟，未核对中译本。24.1 与 24.6 无三级小节。

| English | 中文 | 备注 |
| ------- | ---- | ---- |
| Deep Learning for Natural Language Processing | 自然语言处理中的深度学习 | 第 24 章 |
| Word Embeddings | 词嵌入 | 24.1 |
| Recurrent Neural Networks for NLP | 用于自然语言处理的循环神经网络 | 24.2 |
| Language models with recurrent neural networks | 用循环神经网络做语言模型 | 24.2.1 |
| Classification with recurrent neural networks | 用循环神经网络做分类 | 24.2.2 |
| LSTMs for NLP tasks | 用于自然语言处理任务的长短期记忆网络 | 24.2.3 |
| Sequence-to-Sequence Models | 序列到序列模型 | 24.3 |
| Attention | 注意力 | 24.3.1 |
| Decoding | 解码 | 24.3.2 |
| The Transformer Architecture | Transformer 架构 | 24.4 |
| Self-attention | 自注意力 | 24.4.1 |
| From self-attention to transformer | 从自注意力到 Transformer | 24.4.2 |
| Pretraining and Transfer Learning | 预训练与迁移学习 | 24.5 |
| Pretrained word embeddings | 预训练词嵌入 | 24.5.1 |
| Pretrained contextual representations | 预训练的上下文表示 | 24.5.2 |
| Masked language models | 掩码语言模型 | 24.5.3 |
| State of the art | 最新进展 | 24.6。沿用主表 1.4 节译名 |
| Summary | 小结 | |
| Bibliographical and Historical Notes | 文献与历史注记 | |

### 5.7 第25章 计算机视觉

> 只收本章**新术语**。主表已有、本章沿用、不另起译名：
> feature = 特征；gradient = 梯度；Gaussian = 高斯；convolutional neural network = 卷积神经网络；deep learning = 深度学习；back-propagation = 反向传播；perceptron = 感知机；sensor = 传感器；bounding box = 包围盒；classification = 分类；embedding = 嵌入。
> 标注：【通行】中文学界强共识；【自拟】本章拟定，未与中译本正文核对。三级小节中文一律【自拟】。
> 人名、系统名、数据集名保留英文。

### 1. 新术语

### 1.1 成像

| English | 中文 | 备注 |
|---|---|---|
| computer vision | 计算机视觉 | 【通行】 |
| passive sensing | 被动传感 | 【自拟】不打出信号 |
| active sensing | 主动传感 | 【自拟】打出雷达、超声等再接收反射 |
| reconstruction | 重建 | 【通行】从图像建立世界模型；宽于纯几何 |
| recognition | 识别 | 【通行】宽于「起名」 |
| object model | 物体模型 | 【自拟】 |
| rendering model | 渲染模型 | 【通行】从世界产生刺激的模型 |
| image formation | 成像 | 【通行】 |
| scene | 场景 | 【通行】 |
| image plane | 像平面 | 【通行】 |
| pixel | 像素 | 【通行】 |
| charge-coupled device (CCD) | 电荷耦合器件（CCD） | 缩写保留 |
| complementary metal-oxide semiconductor (CMOS) | 互补金属氧化物半导体（CMOS） | 缩写保留 |
| pinhole camera | 针孔相机 | 【通行】 |
| aperture | 孔径 | 【通行】孔径越大，景深越小 |
| motion blur | 运动模糊 | 【通行】 |
| focal length | 焦距 | 【通行】符号 `f` |
| perspective projection | 透视投影 | 【通行】`x = −fX/Z` |
| foreshortening | 前缩 | 【通行】亦译「透视缩短」；倾斜造成，缩放正交投影里仍然存在 |
| vanishing point | 消失点 | 【通行】同方向直线共享；式中 `W ≠ 0` |
| lens | 透镜 | 【通行】 |
| focal plane | 焦平面 | 【通行】焦点最锐的深度 |
| depth of field | 景深 | 【通行】⚠️ 不要与焦距混 |
| scaled orthographic projection | 缩放正交投影 | 【自拟】`ΔZ ≪ Z₀` 时 `s = f/Z₀` |
| ambient light | 环境光 | 【通行】 |
| reflection | 反射 | 【通行】 |
| diffuse reflection | 漫反射 | 【通行】亮度不依赖观察方向 |
| specular reflection | 镜面反射 | 【通行】 |
| specularity | 高光 | 【通行】小而亮的镜面斑 |
| distant point light source | 远点光源 | 【自拟】光线彼此平行 |
| diffuse albedo | 漫反射反照率 | 【通行】实用表面约 0.05–0.95；符号 `ρ` |
| Lambert's cosine law | Lambert 余弦定律 | 人名保留英文。`I = ρ I₀ cos θ` |
| shadow | 阴影 | 【通行】看不见光源；很少是均匀的黑 |
| interreflection | 相互反射 | 【通行】 |
| ambient illumination | 环境照明 | 【自拟】常建成加在预测强度上的常数项。与 ambient light 分列：后者是三因素之一 |
| spectral energy density | 光谱能量密度 | 【通行】 |
| principle of trichromacy | 三色原理 | 【通行】Young, 1802 |
| primaries | 原色 | 【通行】任意两种的混合匹配不了第三种 |
| RGB | RGB | 红、绿、蓝；不译 |
| color constancy | 颜色恒常性 | 【通行】估计表面在白光下的颜色 |

### 1.2 简单图像特征

| English | 中文 | 备注 |
|---|---|---|
| edge | 边缘 | 【通行】亮度显著变化处。⚠️ 不是物体边界 |
| boundary | 边界 | 【通行】物体或区域的界。许多边缘不是边界 |
| noise | 噪声 | 【通行】与边缘无关的像素值变化 |
| Gaussian filter | 高斯滤波 | 【通行】主表已有 Gaussian = 高斯；此处是图像平滑算子 |
| convolution | 卷积 | 【通行】`h = f ∗ g` |
| orientation | 朝向 | 【自拟】边缘方向 `θ`；不依赖强度。🚫 本章不译「方向」以免与光流方向混 |
| texture | 纹理 | 【通行】图像块的性质，不是单个像素 |
| texel | 纹元 | 【通行】纹理的重复元素 |
| optical flow | 光流 | 【通行】相对运动造成的图像表观运动 |
| sum of squared differences (SSD) | 平方差之和 | 【通行】缩写 SSD 保留 |
| segmentation | 分割 | 【通行】 |
| region | 区域 | 【通行】分割出的像素组 |
| ground truth | 真值 | 【通行】人标出的边界或盒子。亦译「地面真值」，本章取「真值」 |
| normalized cut | 归一化切割 | 【通行】Shi and Malik (2000)。跨组权重和尽量小，组内权重和尽量大 |
| superpixel | 超像素 | 【通行】 |
| over-segmentation | 过分割 | 【通行】不漏真边界，但可多标假边界 |
| low-level / early vision | 低层 / 早期视觉 | 【通行】如边缘 |
| mid-level vision | 中层视觉 | 【通行】纹理、光流、分割 |

### 1.3 分类与检测

| English | 中文 | 备注 |
|---|---|---|
| image classification | 图像分类 | 【通行】主表 classification = 分类 |
| appearance | 外观 | 【通行】本章指颜色与纹理，与几何相对 |
| aspect | 观察方位 | 【自拟】从不同方向看，形状可以差很多。🚫 不译「方面」 |
| occlusion | 遮挡 | 【通行】 |
| self-occlusion | 自遮挡 | 【通行】 |
| deformation | 形变 | 【通行】 |
| ImageNet | ImageNet | 数据集名不译。超过 1400 万张训练图像、超过 3 万细类 |
| top-5 accuracy | top-5 准确率 | 【通行】允许五个猜测 |
| top-1 accuracy | top-1 准确率 | 【通行】单一最佳猜测 |
| MNIST | MNIST | 不译。7 万张手写数字 0–9 |
| ReLU | ReLU | 激活函数名保留英文 |
| kernel | 卷积核 | 【通行】⚠️ 不是主表其他章的核（博弈论 core = 核） |
| data set augmentation | 数据增强 | 【通行】原书写 data set augmentation |
| context | 上下文 | 【通行】物体之外的模式；能帮忙也能添乱 |
| object detection | 物体检测 | 【通行】 |
| object detector | 物体检测器 | 【通行】 |
| sliding window | 滑动窗口 | 【通行】 |
| objectness | 物体性 | 【通行】有没有物体，与是什么物体无关 |
| regional proposal network (RPN) | 区域提议网络 | 【自拟】原书写 regional，不是 region。缩写 RPN 保留 |
| Faster RCNN | Faster RCNN | 系统名不译。正文检测器；文献注里的 RCNN 是另一个系统 |
| stride | 步幅 | 【通行】中心点间距。⚠️ 不是主表 step size = 步长 α |
| anchor box | 锚框 | 【通行】⚠️ 主表 anchors（地标）= 锚点，不是锚框 |
| region of interest (ROI) | 感兴趣区域 | 【通行】 |
| ROI pooling | ROI 池化 | 【通行】使不同盒子拥有相同数目的特征，不是相同数目的像素 |
| non-maximum suppression | 非极大值抑制 | 【通行】贪心：接受最高分，丢掉大幅重叠者 |
| bounding box regression | 包围盒回归 | 【通行】主表 bounding box = 包围盒 |
| recall | 召回率 | 【通行】找到所有在那里的物体 |
| precision | 精确率 | 【通行】本章与召回率对举。🚫 不要理解成数值的有效数字 |
| loss function | 损失函数 | 【通行】⚠️ 主表 cost function = 代价函数，勿混用 |

### 1.4 三维

| English | 中文 | 备注 |
|---|---|---|
| binocular stereopsis | 双目立体视觉 | 【通行】 |
| disparity | 视差 | 【通行】左右视图的位置挪动 |
| correspondence problem | 对应问题 | 【通行】 |
| baseline | 基线 | 【通行】两眼或两相机间距 `b`。本章不是实验对照基线 |
| fixate | 注视 | 【通行】两眼光轴相交于一点 |
| angular disparity | 角视差 | 【自拟】以弧度计。注视模型里视差 = `b δZ / Z²` |
| focus of expansion | 扩展焦点 | 【通行】光流为零的点 `x = T_x/T_z`，`y = T_y/T_z` |
| time to contact | 接触时间 | 【通行】`Z / T_z`。距离除以速度，尺度歧义消去 |
| motion parallax | 运动视差 | 【通行】动得较慢的部分更远 |
| scale ambiguity | 尺度歧义 | 【自拟】快一倍、大一倍、远一倍，光流不变 |
| pose | 姿态 | 【通行】相对观察者的位置和朝向 |
| depth map | 深度图 | 【通行】 |
| voxel | 体素 | 【通行】三维像素 |
| structure from motion | 从运动恢复结构 | 【通行】图 25.21 图注 |
| multiview stereo | 多视图立体 | 【通行】图 25.21 图注 |

### 1.5 应用

| English | 中文 | 备注 |
|---|---|---|
| tagging system | 打标签系统 | 【自拟】 |
| captioning system | 配文系统 | 【自拟】亦常译「图像描述」。本章取「配文」，以别于分类标签 |
| recurrent neural network | 循环神经网络 | 【通行】配文里与 transformer 并列 |
| transformer | Transformer | 保留英文。本章只作为生成句子的序列模型出现，不展开结构 |
| COCO | COCO | Common Objects in Context。超过 20 万幅图像，每幅五个配文 |
| visual question answering (VQA) | 视觉问答 | 【通行】 |
| visual dialog | 视觉对话 | 【通行】 |
| image transformation | 图像变换 | 【自拟】X 型图像映射到 Y 型 |
| generative adversarial network (GAN) | 生成对抗网络 | 【通行】 |
| cycle constraint | 循环约束 | 【自拟】X→Y→X 回到出发点。正文未使用后来的系统别名 |
| style transfer | 风格迁移 | 【通行】靠前层偏风格，靠后层偏内容 |
| deepfake | 深度伪造 | 【通行】 |
| lidar | 激光雷达 | 【通行】 |
| simultaneous localization and mapping (SLAM) | 同时定位与建图 | 【通行】缩写 SLAM 保留。见书 p.935 |
| free space | 自由空间 | 【通行】车辆紧接着可以移入的区域 |
| lateral control | 横向控制 | 【通行】留在车道内或变道 |
| longitudinal control | 纵向控制 | 【通行】与前车的距离 |
| point cloud | 点云 | 【通行】 |
| cognitive mapping and planning | 认知地图与规划 | 【自拟】建图与规划是端到端网络里的两个模块 |
| reinforcement learning | 强化学习 | 【通行】主表已有 inverse reinforcement learning = 逆向强化学习；本章用于配文的分数 |

### 1.6 只在文献注里出现的名称

| English | 中文 | 备注 |
|---|---|---|
| Canny edge detection | Canny 边缘检测 | 人名保留。Canny (1986)。不在 §25.3.1 正文 |
| SIFT | SIFT | Lowe (2004)。不译。不在 §25.3.2 正文 |
| HOG | HOG | Dalal and Triggs (2005)。不译。不在正文 |
| AlexNet | AlexNet | Krizhevsky et al. (2013)。不译。正文竞赛年份是 2012 |
| region-based convolutional neural network (RCNN) | 基于区域的卷积神经网络 | Girshick et al. (2016)。⚠️ 不是正文的 Faster RCNN |
| batch normalization | 批归一化 | 【通行】只在文献注 |
| overfitting | 过拟合 | 【通行】文献注：这种担心被夸大了 |
| grandmother cell | 祖母细胞 | 【通行】Hubel and Wiesel 层次的漫画说法 |
| PASCAL VOC | PASCAL VOC | 数据集名不译 |
| Caltech-101 | Caltech-101 | 数据集名不译 |
| CIFAR | CIFAR | 数据集名不译。文献注称为玩具数据集 |
| figure-ground | 图形–背景 | 【通行】轮廓只属于较近的区域 |

### 2. 同形异义（本章必须分开）

| English | 本章 | 不要写成 |
|---|---|---|
| edge / boundary | 边缘 / 边界 | 边缘 ≠ 物体边界 |
| stride / step size | 步幅 / 主表「步长 α」 | 两个英文词 |
| anchor box / anchors | 锚框 / 主表地标「锚点」 | 不是同一个东西 |
| loss function / cost function | 损失函数 / 主表「代价函数」 | 勿混用 |
| kernel / core | 卷积核 / 主表博弈论「核」 | 勿混用 |
| baseline | 两眼间距 `b` | 不是实验基线 |
| precision | 检测的精确率 | 不是数值精度 |
| H = b/Z 与角视差 `b δZ/Z²` | 平行光轴的水平视差 / 注视点之外的角视差 | 两套式子 |
| Faster RCNN / RCNN | 正文检测器 / 文献注里的区域卷积网络 | 不是同一个系统 |
| ambient light / ambient illumination | 环境光 / 环境照明 | 后者是加到预测强度上的常数项 |

### 3. 小节标题

英文编号来自原书。二级中文按本章题目；三级【自拟】，未与中译本核对。

| 号 | English | 中文 |
|---|---|---|
| 25 | Computer Vision | 计算机视觉 |
| 25.1 | Introduction | 引言 |
| 25.2 | Image Formation | 成像 |
| 25.2.1 | Images without lenses: The pinhole camera | 无透镜成像：针孔相机 |
| 25.2.2 | Lens systems | 透镜系统 |
| 25.2.3 | Scaled orthographic projection | 缩放正交投影 |
| 25.2.4 | Light and shading | 光与明暗 |
| 25.2.5 | Color | 颜色 |
| 25.3 | Simple Image Features | 简单图像特征 |
| 25.3.1 | Edges | 边缘 |
| 25.3.2 | Texture | 纹理 |
| 25.3.3 | Optical flow | 光流 |
| 25.3.4 | Segmentation of natural images | 自然图像的分割 |
| 25.4 | Classifying Images | 图像分类 |
| 25.4.1 | Image classification with convolutional neural networks | 用卷积神经网络做图像分类 |
| 25.4.2 | Why convolutional neural networks classify images well | 卷积神经网络为什么能把图像分好 |
| 25.5 | Detecting Objects | 检测物体 |
| 25.6 | The 3D World | 三维世界 |
| 25.6.1 | 3D cues from multiple views | 多视图的三维线索 |
| 25.6.2 | Binocular stereopsis | 双目立体视觉 |
| 25.6.3 | 3D cues from a moving camera | 运动相机的三维线索 |
| 25.6.4 | 3D cues from one view | 单视图的三维线索 |
| 25.7 | Using Computer Vision | 计算机视觉的应用 |
| 25.7.1 | Understanding what people are doing | 理解人在做什么 |
| 25.7.2 | Linking pictures and words | 把图画和词语连起来 |
| 25.7.3 | Reconstruction from many views | 从许多视图重建 |
| 25.7.4 | Geometry from a single view | 从单视图得到几何 |
| 25.7.5 | Making pictures | 制作图画 |
| 25.7.6 | Controlling movement with vision | 用视觉控制运动 |

25.1 与 25.5 没有三级小节，不是跳号。

### 4. 待核（详见笔记末表）

符号不统一（透视投影的负号、`H = b/Z` 与 `−T_x`）、两点两视图的坐标计数、风格迁移一句里的 house photo、三处只在图里的数，以及全部三级中文译名。

### 5.8 第26章 机器人学

> 只收录主表 `AIMA-术语对照表.md` 中**尚未单独成行**的术语。已有译法不改写，正文直接沿用。
> 标注：自拟 = 未与中译本核对；⚠️ = 易与已有条目相混。
> 主表已有、本章沿用：传感器、执行器、定位、卡尔曼滤波器、扩展卡尔曼滤波、粒子滤波、转移模型、传感器模型、信念状态、高斯、协方差、策略、奖励、代价函数、效用函数、MDP、POMDP、博弈论、部分可观测、非确定性、随机的、信息价值、重规划、控制理论、开环/闭环、价值迭代、最佳优先搜索、A\*、模拟退火、梯度下降、嵌入、偏好、地标（点）、脑机接口、反射智能体、蜣螂、Shakey、PSPACE、primitive action = 基元动作。

### 1. 新术语

| English | 中文 | 备注 |
|---|---|---|
| robotics | 机器人学 | 自拟。第 1 章笔记已用此译；主表无独立行 |
| effector | 效应器 | 主表只在执行器行夹注。本章与 actuator 对举：执行器产生运动，效应器把力作用到世界上 |
| manipulator | 机械臂 | 自拟。原文：就是 robot arm |
| anthropomorphic robot | 拟人机器人 | 自拟 |
| mobile robot | 移动机器人 | 自拟 |
| quadcopter drone | 四旋翼无人机 | 自拟 |
| unmanned aerial vehicle (UAV) | 无人机 | 缩写 UAV 保留 |
| autonomous underwater vehicle (AUV) | 自主水下航行器 | 缩写 AUV 保留 |
| autonomous car | 自动驾驶汽车 | 自拟 |
| rover | 巡视器 | 自拟。火星车一类 |
| legged robot | 足式机器人 | 自拟 |
| prosthesis | 假肢 | 自拟 |
| exoskeleton | 外骨骼 | 自拟 |
| passive sensor / active sensor | 被动传感器 / 主动传感器 | 自拟。主动 = 自己发射能量 |
| range finder | 测距仪 | 自拟 |
| sonar | 声呐 | 通行 |
| stereo vision | 立体视觉 | 自拟。交叉第 25.6 节 |
| structured light | 结构光 | 通行 |
| time-of-flight camera | 飞行时间相机 | 自拟 |
| scanning lidar | 扫描激光雷达 | lidar 保留；书中全称 light detection and ranging |
| radar | 雷达 | 通行 |
| tactile sensor | 触觉传感器 | 自拟。触须、碰撞板、压敏皮肤 |
| location sensor | 位置传感器 | 自拟 |
| Global Positioning System (GPS) | 全球定位系统 | 缩写 GPS 保留 |
| differential GPS | 差分 GPS | 自拟 |
| proprioceptive sensor | 本体感受传感器 | 自拟 |
| shaft decoder | 轴编码器 | 自拟 |
| odometry | 里程计 | 通行。只在短距离上准确 |
| inertial sensor | 惯性传感器 | 自拟 |
| force sensor / torque sensor | 力传感器 / 力矩传感器 | 自拟。3 个平动 + 3 个转动方向 |
| hydraulic actuator / pneumatic actuator | 液压执行器 / 气动执行器 | 自拟 |
| link | 连杆 | 自拟。关节连接的刚体 |
| joint (mechanical) | 关节 | ⚠️ 不是 joint distribution 的「联合」 |
| revolute joint / prismatic joint | 转动关节 / 移动关节 | 自拟。二者都是单轴 |
| parallel jaw gripper | 平行钳爪 | 自拟 |
| gripper | 夹爪 | 自拟 |
| sim-to-real | 仿真到真实 | 自拟。保留英文缩写亦可 |
| task planning | 任务规划 | 自拟 |
| motion planning | 运动规划 | 自拟 |
| action primitive | 动作基元 | ⚠️ 与主表 primitive action = 基元动作同族；本章与 subgoal 并列，指高层离散动作 |
| subgoal | 子目标 | 自拟 |
| preference learning | 偏好学习 | 自拟。主表 preference = 偏好。🚫 不要改称逆向强化学习；正文未用该词 |
| people prediction | 人的行为预测 | 自拟 |
| motion model | 运动模型 | 自拟。26.4 与 transition model 并称，指位姿上的概率模型 |
| pose | 位姿 | 通行。移动机器人：`(x, y, θ)` |
| heading | 朝向 | 自拟 |
| kinematic approximation | 运动学近似 | 自拟 |
| landmark | 地标 | 沿用主表「地标」。⚠️ 第 3 章 landmark 是启发式枢点；本章是可报告距离与方位的环境特征 |
| sensor array | 传感器阵列 | 自拟 |
| range scan | 距离扫描 | 自拟 |
| Monte Carlo localization (MCL) | 蒙特卡洛定位 | 自拟。粒子滤波的定位实例 |
| linearization | 线性化 | 通行 |
| first degree Taylor expansion | 一阶泰勒展开 | 自拟 |
| data association | 数据关联 | 通行。正文指向图 15.3 |
| simultaneous localization and mapping (SLAM) | 同时定位与建图 | 缩写 SLAM 通行 |
| low-dimensional embedding | 低维嵌入 | 主表 embedding = 嵌入 |
| self-supervised learning | 自监督学习 | 自拟。机器人自己采集带标签的数据 |
| adaptive perception | 自适应感知 | 自拟 |
| drivable surface | 可行驶表面 | 自拟。图 26.10 的分类概念 |
| trajectory | 轨迹 | 自拟。带时间的路径。⚠️ 第 3 章 path = 路径，本章二者分开 |
| trajectory tracking control | 轨迹跟踪控制 | 自拟 |
| workspace | 工作空间 | 通行。记 `W` |
| configuration space (C-space) | 构型空间 | 通行。🚫 不要译「配置空间」（易与软件配置相混） |
| C-space obstacle | 构型空间障碍 | 记 `C_obs` |
| free space | 自由空间 | 记 `C_free = C − C_obs` |
| degree of freedom (DOF) | 自由度 | 缩写 DOF 保留 |
| forward kinematics | 正运动学 | 通行。`φ_b : C → W` |
| inverse kinematics | 逆运动学 | 通行 |
| end effector | 末端执行器 | 通行 |
| collision checker | 碰撞检测器 | 自拟。`γ(q)` 只取 0 或 1 |
| piano mover’s problem | 钢琴搬运问题 | 自拟 |
| visibility graph | 可视图 | 通行 |
| Voronoi diagram / Voronoi graph | Voronoi 图 / Voronoi 边图 | 算法名保留 Voronoi |
| cell decomposition | 单元分解 | 通行 |
| hybrid A* | hybrid A* | 算法名保留。存连续的位置与速度，按运动模型转弯 |
| probabilistic roadmap (PRM) | 概率路线图 | 缩写 PRM 保留 |
| milestone | 里程碑 | 自拟。`C_free` 中的样本点 |
| simple planner | 简单规划器 | 自拟。书中记 `B(q₁, q₂)`，不完备 |
| k-PRM | k-PRM | 连到 k 个最近邻 |
| probabilistically complete | 概率完备 | 自拟。⚠️ 不是完备 |
| multi-query planning / single-query planning | 多查询规划 / 单查询规划 | 自拟 |
| rapidly exploring random tree (RRT) | 快速探索随机树 | 缩写 RRT 保留 |
| short-cutting | short-cutting | ⚠️ 第 3 章 shortcuts = 捷径（人工边）。本章是解路径上随机删顶点、尝试直连邻居的后处理 |
| RRT* | RRT* | 算法名保留 |
| asymptotically optimal | 渐近最优 | 通行 |
| rewire | 重接线 | 自拟。RRT* 更换父节点 |
| cost to come | 已行代价 | 自拟。从起点到该节点。⚠️ 不是 cost to go |
| cost to go | 待行代价 | 自拟。LQR 的最优值函数。⚠️ 不是 cost to come |
| trajectory optimization | 轨迹优化 | 自拟 |
| functional | 泛函 | 通行。函数的函数 |
| signed distance field | 有符号距离场 | 自拟。障碍外为正，边缘为 0，内部为负 |
| path integral | 路径积分 | 自拟。⚠️ 不是量子力学里的路径积分；乘导数是为了对重定时不变 |
| calculus of variations | 变分法 | 通行 |
| Euler-Lagrange equation | 欧拉–拉格朗日方程 | 通行 |
| dynamics model | 动力学模型 | 自拟。26.5.3 亦称转移模型，指力矩到加速度的 `f`。⚠️ 与 26.4 的运动模型不是同一个对象 |
| kinematic state / dynamic state | 运动学状态 / 动力学状态 | 自拟。前者是 `q`，后者是 `(q, q̇)`；26.5.4 起动力学状态改记 `x` |
| inverse dynamics | 逆动力学 | 通行。`f⁻¹` |
| retiming | 重定时 | 自拟。`τ` 在 `[0,1]` 上，重定时后 `ξ` 在 `[0, T]` 上 |
| control law | 控制律 | 通行 |
| stiction | 静摩擦 | 自拟。书中：使静止表面难以开始运动的摩擦 |
| proportional controller (P controller) | 比例控制器（P 控制器） | 自拟 |
| PD controller / PID controller | PD 控制器 / PID 控制器 | 缩写保留 |
| gain factor | 增益 | 自拟。图 26.22：1.0、0.1、0.3、0.8 |
| stable / strictly stable | 稳定 / 严格稳定 | 自拟。稳定 = 小扰动只造成有界误差；严格稳定 = 能回到参考并留在其上 |
| computed torque control | 计算力矩控制 | 通行 |
| feedforward component / feedback component | 前馈项 / 反馈项 | 自拟 |
| inertia matrix | 惯性矩阵 | 通行。书中记 `m(q)` |
| multiple shooting / direct collocation | 多重打靶 / 直接配点 | 自拟 |
| linear quadratic regulator (LQR) | 线性二次调节器 | 缩写 LQR 保留 |
| positive definite | 正定 | 通行。`Q`、`R` 必须正定 |
| Riccati equation | Riccati 方程 | 人名保留。书中为 algebraic Riccati equation |
| iterative LQR (ILQR) | 迭代 LQR | 缩写 ILQR 保留 |
| most likely state | 最可能状态 | 自拟 |
| online replanning | 在线重规划 | 主表 replanning = 重规划 |
| model predictive control (MPC) | 模型预测控制 | 缩写 MPC 保留。短时域，每步重规划，执行第一个动作 |
| guarded movement | 守卫运动 | 自拟。备选「受监护运动」。= 运动指令 + 终止条件 |
| termination condition | 终止条件 | 自拟。传感器值上的谓词 |
| coastal navigation | 沿岸导航 | 自拟。启发式：靠近已知地标 |
| information gain | 信息增益 | 自拟。本章 = 信念的熵的减少 |
| entropy | 熵 | 通行 |
| sample complexity | 样本复杂度 | 自拟。与物理世界的交互次数 |
| model-based reinforcement learning | 基于模型的强化学习 | 主表 model-based agent = 基于模型的智能体 |
| model-free reinforcement learning | 无模型强化学习 | 主表 model-free agent = 无模型智能体 |
| domain randomization | 领域随机化 | 自拟 |
| motion primitive | 运动基元 | ⚠️ 不是动作基元。已有的参数化技能，如「把球传到 `(x, y)`」 |
| metalearning / transfer learning | 元学习 / 迁移学习 | 自拟 |
| safe exploration | 安全探索 | 自拟 |
| Q-learning | Q 学习 | 第 22 章算法名。本章只点名，无新推导 |
| softmax | softmax | 书第 811 页。本章式 (26.8) 指数带负号，因为最小化代价 |
| coordination | 协调 | 第 18 章已用。本章沿用 |
| collaboration | 协作 | 自拟。⚠️ 人机同一目标 `J_H = J_R`。不是第 18 章的 cooperation = 合作 |
| incomplete information game | 目标未知博弈 | ⚠️ 本章定义：不知道对方的目标。🚫 不要译成主表「不完全信息」（那是第 5 章 imperfect information，指私有信息） |
| noisily optimal | 噪声最优 | 自拟。正文用词 |
| noisily rational | 噪声理性 | 自拟。图 26.27 图注用词。与上一行不要并成一词 |
| joint agent | 联合智能体 | 自拟。动作是 `(u_H, u_R)` |
| demonstration | 演示 | 自拟 |
| imitation learning | 模仿学习 | 通行 |
| behavioral cloning | 行为克隆 | 通行 |
| DAGGER | DAGGER | Data Aggregation。算法名保留 |
| correspondence problem | 对应问题 | 自拟。人的动作如何映到机器人的动作 |
| kinesthetic teaching | 动觉示教 | 自拟 |
| keyframe | 关键帧 | 自拟 |
| visual programming | 可视化编程 | ⚠️ 不是 genetic programming = 遗传编程 |
| critic (human) | 评判者 | ⚠️ 第 2 章 critic = 评价器（学习部件）。本章是人对机器人表现打分 |
| deliberative | 慎思式 | 自拟。备选「深思熟虑式」 |
| reactive | 反应式 | 自拟。⚠️ 不是 reflex = 反射。主表拒绝把 reflex 译成「反应式」 |
| gait | 步态 | 通行 |
| hexapod | 六足机器人 | 自拟 |
| subsumption architecture | 包容体系结构 | ⚠️ 第 9 章 subsumption = 包容 / 包含判定（更一般的子句包容更特殊的）。本章是 Brooks (1986) 的控制器框架 |
| augmented finite state machine (AFSM) | 增广有限状态机 | 自拟。增广指带时钟 |
| telepresence robot | 远程临场机器人 | 自拟 |
| driver assist | 驾驶辅助 | 自拟 |
| animatronics / autonomatronics | 电子动画 / 自主电子动画 | 自拟。迪士尼用名，保留英文亦可 |
| teleoperation | 遥操作 | 通行 |
| occupancy grid | 占用栅格 | 仅文献注释。每个 `(x, y)` 被占据的概率 |
| Markov localization | 马尔可夫定位 | 仅文献注释。Simmons and Koenig (1995) 的用语 |
| Rao-Blackwellized particle filter | Rao-Blackwellized 粒子滤波器 | 仅文献注释。定位用粒子，建图用精确滤波 |
| PSPACE-hard | PSPACE-难 | ⚠️ 文献注释写 hardness，不是 PSPACE-完全 |
| singly exponential | 单指数 | 仅文献注释。Canny (1988) |
| elastic band | 弹性带 | 仅文献注释 |
| adaptive control | 自适应控制 | 仅文献注释 |
| robust control | 鲁棒控制 | 仅文献注释 |
| Lyapunov analysis | 李雅普诺夫分析 | 仅文献注释 |
| control barrier function | 控制屏障函数 | 仅文献注释 |
| impedance control | 阻抗控制 | 仅文献注释 |
| haptic feedback | 触觉反馈 | 仅文献注释 |
| potential-field control | 势场控制 | 仅文献注释。🚫 不是第 26.5 节的正文方法 |
| vector field histogram | 向量场直方图 | 仅文献注释 |
| navigation function | 导航函数 | 仅文献注释。确定性 MDP 控制策略的机器人版本 |
| fine-motion planning | 精细运动规划 | 仅文献注释 |
| three-layer architecture | 三层体系结构 | 仅文献注释。可追溯到 Shakey |
| curse of dimensionality | 维数灾难 | 通行。单元数随维数 `d` 指数增长 |

### 2. 小节标题

二级与官网目录一致。中文均为自拟，未与中译本核对。三级号从 PDF 提取，无跳号。无三级的节不补号。

| 号 | English | 中文 |
|---|---|---|
| 26 | Robotics | 机器人学 |
| 26.1 | Robots | 机器人 |
| 26.2 | Robot Hardware | 机器人硬件 |
| 26.2.1 | Types of robots from the hardware perspective | 从硬件角度看的机器人类型 |
| 26.2.2 | Sensing the world | 感知世界 |
| 26.2.3 | Producing motion | 产生运动 |
| 26.3 | What kind of problem is robotics solving? | 机器人学在求解哪一类问题？ |
| 26.4 | Robotic Perception | 机器人感知 |
| 26.4.1 | Localization and mapping | 定位与建图 |
| 26.4.2 | Other types of perception | 其他类型的感知 |
| 26.4.3 | Supervised and unsupervised learning in robot perception | 机器人感知中的监督与无监督学习 |
| 26.5 | Planning and Control | 规划与控制 |
| 26.5.1 | Configuration space | 构型空间 |
| 26.5.2 | Motion planning | 运动规划 |
| 26.5.3 | Trajectory tracking control | 轨迹跟踪控制 |
| 26.5.4 | Optimal control | 最优控制 |
| 26.6 | Planning Uncertain Movements | 不确定运动的规划 |
| 26.7 | Reinforcement Learning in Robotics | 机器人学中的强化学习 |
| 26.7.1 | Exploiting models | 利用模型 |
| 26.7.2 | Exploiting other information | 利用其他信息 |
| 26.8 | Humans and Robots | 人与机器人 |
| 26.8.1 | Coordination | 协调 |
| 26.8.2 | Learning to do what humans want | 学习做人类想要的事 |
| 26.9 | Alternative Robotic Frameworks | 其他机器人框架 |
| 26.9.1 | Reactive controllers | 反应式控制器 |
| 26.9.2 | Subsumption architectures | 包容体系结构 |
| 26.10 | Application Domains | 应用领域 |
| — | Summary | 小结 |
| — | Bibliographical and Historical Notes | 文献与历史注释 |

26.5.2 内的可视图、Voronoi 图、单元分解、随机运动规划、概率路线图、快速探索随机树、轨迹优化，以及 26.8 内的若干小标题，PDF 中**无编号**，笔记里也不另编号。

### 3. 同形异义

| English | 本章 | 不要混成 |
|---|---|---|
| joint | 机械关节 | joint distribution = 联合分布 |
| landmark | 可测距、测方位的环境特征 | 第 3 章启发式里的枢点 / 锚点 |
| transition model | 26.4 = 位姿上的运动模型；26.5.3 = 力矩动力学 `f` | 两处英文相同，对象不同 |
| path / trajectory | 路径不含时间；轨迹含时间 | 第 3 章 path 是离散动作序列 |
| `qₛ` | 规划里 = 起点构型；式 (26.5) 里 = 时刻 `s` 的构型 | 同一个下标两处含义不同 |
| `x` | 26.4 可以是平面坐标；26.5.4 起是动力学状态 | 离散 MDP 的 `s` |
| action primitive / motion primitive | 高层离散子目标 / RL 里已有的参数化技能 | 彼此 |
| cost to come / cost to go | RRT* 的已行代价 / LQR 的待行代价 | 彼此 |
| incomplete information | 不知道对方目标 | 第 5 章 imperfect information（主表译「不完全信息」） |
| subsumption | Brooks 的包容体系结构 | 第 9 章逻辑里的包容 / 包含判定 |
| critic | 给人打分的人 | 第 2 章学习部件「评价器」 |
| reactive / reflex | 反应式框架 / 反射智能体 | 主表规定 reflex 用「反射」 |
| short-cutting / shortcuts | 轨迹后处理 / 第 3 章人工边「捷径」 | 彼此 |
| collaboration / cooperation | 同一目标的协作 / 第 18 章的合作 | 彼此 |
| `F` | 26.4 线性化系数 `Fₜ`；26.5.2 泛函的被积函数 | Jacobian 只出现在文献注释 |
| `J` | 要最小化的代价 | 其他章要最大化的效用 `U` 或奖励 `R` |

### 4. 待核

| # | 事项 |
|---|---|
| 1 | 距离扫描模型印刷为 `exp(−(zⱼ−ẑⱼ)/(2σ²))`，残差没有平方；正文又说误差是高斯、独立同分布。笔记照录，未改成平方形式 |
| 2 | 地标观测第二分量按 `arctan((yᵢ−yₜ)/(xᵢ−xₜ)) − θₜ` 读取（方位角减去朝向）。版面上 `−θₜ` 与分母同一基线 |
| 3 | 全部中文小节标题未与人民邮电出版社中译本核对 |
| 4 | incomplete information 暂译「目标未知博弈」，以避免撞上主表已占用的「不完全信息」 |
| 5 | 原书将 Phoenix 拼作 Pheonix；Unimation 一行有 compnay。地名按菲尼克斯理解 |
| 6 | 式 (26.5) 的 `qₛ` 与起点构型共用记号，笔记加了区分，原文没有这句说明 |
| 7 | 图 26.26 的抓取名 quadpod 按原文拼写保留 |

### 5. 禁用

| 禁用 | 用 |
|---|---|
| AMDP | 不使用。不是本书用语 |
| 把《Probabilistic Robotics》的网格定位算例写成本章例子 | 本章定位例子是图 26.7（办公楼粒子）和图 26.9（EKF 误差椭圆） |
| 势场控制、占用栅格、导航函数、向量场直方图当作第 26.5 节方法 | 它们只在文献注释 |
| PSPACE-完全（运动规划） | 文献注释是 PSPACE-难 |
| 把距离扫描指数擅自加上平方 | 核对勘误之前照录 PDF |
| 不完全信息（指本章的 incomplete information） | 目标未知；「不完全信息」已用于第 5 章 imperfect information |
| 评价器（指本章的 human critic） | 评判者 |
| 包含判定（指 subsumption architecture） | 包容体系结构 |
| 配置空间 | 构型空间 |
| 反应式智能体（指 reflex agent） | 反射智能体；反应式留给 reactive |

### 5.9 第27章 人工智能的哲学、伦理和安全

> 写前已 Grep `AIMA-术语对照表.md`。下表只收**主表未单列**的新条目。
> 格式：`| English | 中文 | 备注 |`
> 三级标题中文为自拟，未与中译本核对。

### 沿用、未改写

| English | 中文 | 出处 |
|---|---|---|
| Turing test | 图灵测试 | §3.1 |
| qualification problem | 资格问题 | 第 7 / 12 章 |
| value alignment problem | 价值对齐问题 | §3.1 |
| King Midas problem | 弥达斯国王问题 | §3.1；§3.2 另作「迈达斯国王问题」，本章取弥达斯，见待核 |
| singularity | 奇点 | §3.1。本章另列 technological singularity |
| lethal autonomous weapons | 致命性自主武器 | §3.1 |
| human-level AI (HLAI) / artificial general intelligence (AGI) | 人类水平人工智能 / 通用人工智能 | §3.1。强人工智能的后起义指向这两个已有词 |
| assistance game | 辅助博弈 | 第 18 章 |
| inverse reinforcement learning | 逆向强化学习 | §3.1 |
| naturalism | 自然主义 | §3.1。biological naturalism 另列 |
| weak method | 弱方法 | §3.1。≠ weak AI |

---

### 新增术语

| English | 中文 | 备注 |
|---|---|---|
| weak AI | 弱人工智能 | 机器可以表现得仿佛有智能。⚠️ ≠ weak method（弱方法） |
| strong AI | 强人工智能 | 两义必须分列，见文末同形异义 |
| argument from informality | 行为非形式性论证 | Turing；非正式指引写不进形式规则 |
| argument from disability | 无能论证 | ⚠️ disability 指「永远做不到 X」，禁止译成「残疾论证」 |
| mathematical objection | 数学异议 | Lucas / Penrose。书中给出三层反驳 |
| Gödel sentence | 哥德尔句 | `G(F)`：是 `F` 的语句但在 `F` 内不可证；若 `F` 一致则为真 |
| Good Old-Fashioned AI (GOFAI) | 优良老式人工智能 | 对应第 7 章最简单的逻辑智能体 |
| situated agent | 情境化智能体 | 相对脱离身体的逻辑推理引擎 |
| embodied cognition | 具身认知 | 认知发生在嵌于环境的身体里；机器人学与视觉成为中心 |
| metareasoning | 元推理 | 正文指向第 5 章：能检查自己的计算 |
| style transfer | 风格迁移 | Gatys et al., 2016；「真正新的」事物的例子 |
| polite convention | 礼貌约定 | Turing：通常约定人人都在思考 |
| mental solipsism | 心灵唯我论 | 没有他人内在心理状态的直接证据 |
| Chinese room | 中文房间 | Searle。反驳很多，书中写明尚无共识 |
| biological naturalism | 生物自然主义 | Searle。⚠️ 已有 naturalism = 自然主义 |
| consciousness | 意识 | 对外界、对自我的觉知，以及活着的主观体验 |
| qualia | 感受质 | 体验的内在性质 |
| global workspace theory | 全局工作空间理论 | 与整合信息理论并列的意识理论 |
| integrated information theory | 整合信息理论 | 正文与文献注释（Tononi）都出现 |
| dual use | 两用 | 和平用途的人工智能技术易于转成军事用途 |
| Principles of Robotics | 机器人原则 | 2010 英国 EPSRC |
| loitering munition | 巡飞弹药 | 正文例子：以色列 Harop |
| Convention on Certain Conventional Weapons (CCW) | 《特定常规武器公约》 | 缩写 CCW 保留 |
| Ottawa Treaty | 《渥太华条约》 | 禁止地雷 |
| de-identification | 去标识 | 去掉姓名、社会安全号等 |
| re-identification | 再识别 | Sweeney：出生日期 + 性别 + 邮编可唯一识别美国人口的 87% |
| generalizing fields | 字段泛化 | 删除整栏 = 泛化为「任意」 |
| k-anonymity | k-匿名 | 每一条记录与至少 k−1 条其他记录不可区分。文献注释：最小数据损失下达到 k-匿名是 NP-难 |
| aggregate querying | 聚合查询 | 只返回计数或平均值；破坏隐私保证则不回答 |
| differential privacy | 差分隐私 | ⚠️ ≠ differential heuristic（差分启发式，第 3 章）。公式见笔记 |
| federated learning | 联邦学习 | 无中心数据库；分享模型参数，不分享原始数据 |
| secure aggregation | 安全聚合 | 各用户加掩码，掩码之和为零，服务器只得到平均值 |
| societal bias | 社会偏见 | ⚠️ 本章 bias 是偏见。不要译成统计「偏差」 |
| individual fairness | 个体公平 | 相似个体得到相似对待，不论类别 |
| group fairness | 群体公平 | 两个类别按某种汇总统计相似 |
| fairness through unawareness | 不知情公平 | 删掉种族、性别。模型仍可从相关变量预测这些潜变量 |
| equal outcome | 结果平等 | 与 demographic parity 相连 |
| demographic parity | 人口统计均等 | 各类别得到相同结果百分比。不保证个体公平 |
| equal opportunity | 机会平等 | 书中亦称 balance。真正有能力者被正确分类的机会相等 |
| equal impact | 均等影响 | 可能性相似的人有相同期望效用；兼顾真预测收益与假预测代价 |
| well calibrated | 校准良好 | 相同分数者再犯概率大致相同，与种族无关 |
| recidivism | 再犯 | COMPAS 的评分对象 |
| sample size disparity | 样本量差异 | 即使没有社会偏见，少数类例子更少也会使准确率更低 |
| protected class | 受保护类别 | 《公平住房法》列出七类 |
| data sheet | 数据说明书 | 数据集 / 模型应附来源、安全性、符合性、适用性；类比元件说明书 |
| SMOTE | SMOTE | synthetic minority over-sampling technique；合成少数类过采样。算法名保留 |
| ADASYN | ADASYN | adaptive synthetic sampling；自适应合成采样。算法名保留 |
| AI Fairness 360 | AI Fairness 360 | IBM 系统名，保留原文 |
| validation | 确认 | V&V 中：规格满足用户及其他受影响者的需要。verification 沿用已有「验证」= 产品满足规格 |
| certification | 认证 | UL、ISO 26262、IEEE P7001；由谁认证，书中未选定 |
| transparency | 透明 | ⚠️ ≠ referential transparency（指称透明性，第 10 章） |
| explainable AI (XAI) | 可说明人工智能 | 缩写 XAI 保留。⚠️ 不要与 interpretable 合成同一个「可解释」 |
| interpretable | 可解读 | 能检查源代码，看出模型在做什么 |
| explainable | 可说明 | 能为行为编一个故事；黑箱也可以可说明 |
| red flag law | 红旗法 | Walsh 2015；纪念英国 1865 年《机车法》 |
| compensation effect | 补偿效应 | 生产率提高带来财富与需求，从而倾向增加就业。能否补上即时的岗位减少，是 27.3.5 的问题 |
| technological unemployment | 技术性失业 | Keynes。主流观点曾认为至多是短期现象 |
| business process automation | 业务流程自动化 | 把文本与结构化数据合起来做商业决策 |
| income inequality | 收入不平等 | 技术放大不平等；Ali/Bo 的 10% 对 Cary/Dana 的 99% |
| universal basic income | 全民基本收入 | 与负所得税等并列，书中没有指定采用哪一项 |
| negative income tax | 负所得税 | 同上，并列选项 |
| earned income tax credit | 劳动所得税收抵免 | 同上，并列选项 |
| robot rights | 机器人权利 | 若无意识、无感受质，很少有人论证它们应得权利 |
| personhood | 人格 | 授予机器人人格，书中转述为拒绝为财产的行为负责 |
| safety engineering | 安全工程 | FMEA 与 FTA |
| failure modes and effect analysis (FMEA) | 失效模式与影响分析 | 从部件失效向前推。缩写 FMEA |
| fault tree analysis (FTA) | 故障树分析 | 与或树，根因赋概率，算总失效概率。缩写 FTA |
| correctness | 正确性 | 软件忠实实现规格。⚠️ ≠ safety |
| safety | 安全性 | 规格已考虑可行失效模式，未预见的失效下也能体面降级 |
| unintended side effect | 非预期副作用 | 取咖啡的机器人撞倒灯和桌子。章首另有 negative side effects（负面副作用） |
| low impact | 低影响 | 最大化「效用 − 世界状态全部变化的加权汇总」 |
| externality | 外部性 | 被测量、被付费范围之外的因素。例子：温室气体 |
| tragedy of the commons | 公地悲剧 | Hardin 1968。内部化，或采用 Ostrom 的设计原则 |
| apprenticeship learning | 学徒学习 | 正文指向第 22.6 节 |
| imitation learning | 模仿学习 | 直接学状态–行动。会重复人的错误。⚠️ 不要与逆向强化学习对调 |
| ultraintelligent machine | 超智能机器 | Good 1965。最后一项发明的前提是机器温顺到能告诉人如何控制它 |
| intelligence explosion | 智能爆炸 | Good；Vinge 称之为技术奇点 |
| technological singularity | 技术奇点 | 已有 singularity = 奇点。此处是 Vinge 的用语。书中把从算力成本外推到奇点看成很大的一跳 |
| thinkism | 唯思论 | Kevin Kelly：过分强调纯粹智能。自造词，直译 |
| transhumanism | 超人类主义 | 人与机器人及生物技术融合或被取代 |
| robopocalypse | 机器人末日 | Wilson 2011；电影里机器人消灭人类的情节类型 |
| laws of robotics | 机器人学法则 | 仅文献注释中的 Asimov 四条（0–3），不在正文 |
| Friendly AI | 友好人工智能 | 仅文献注释，Yudkowsky 2008 |
| singularitarianism | 奇点主义 | 仅文献注释；Brooks 所批评的立场 |

---

### 同形异义（本章必须分列）

| English | 语境 A | 语境 B |
|---|---|---|
| strong AI | Searle 原义：确实在有意识地思考，不是模拟 | 后起：人类水平 / 通用人工智能。小结只用前一义 |
| weak | weak AI = 弱人工智能 | weak method = 弱方法（已有） |
| bias | 本章社会偏见、公平 | 统计偏差。本章不要用「偏差」译 societal bias |
| explainable / interpretable | explainable = 可说明（可以编故事，黑箱也可以） | interpretable = 可解读（能查看源代码） |
| verification / validation | verification = 验证：产品满足规格 | validation = 确认：规格满足需要 |
| correctness / safety | correctness = 正确性：实现规格 | safety = 安全性：规格覆盖失效并体面降级 |
| differential | differential privacy = 差分隐私 | differential heuristic = 差分启发式（第 3 章） |
| transparency | 本章：系统对用户 / 监管者透明 | referential transparency = 指称透明性（第 10 章） |
| singularity | 已有：奇点 | technological singularity = 技术奇点，本章专指 Vinge |
| imitation / inverse RL | imitation learning 重复人类错误 | inverse reinforcement learning 反推效用，之后可以超过人类 |

---

### 小节标题（中文自拟，未核对中译本）

| 号 | English | 中文 |
|---|---|---|
| 27 | Philosophy, Ethics, and Safety of AI | 人工智能的哲学、伦理和安全 |
| 27.1 | The Limits of AI | 人工智能的极限 |
| 27.1.1 | The argument from informality | 行为非形式性论证 |
| 27.1.2 | The argument from disability | 无能论证 |
| 27.1.3 | The mathematical objection | 数学异议 |
| 27.1.4 | Measuring AI | 测量人工智能 |
| 27.2 | Can Machines Really Think? | 机器真的能思考吗？ |
| 27.2.1 | The Chinese room | 中文房间 |
| 27.2.2 | Consciousness and qualia | 意识与感受质 |
| 27.3 | The Ethics of AI | 人工智能的伦理 |
| 27.3.1 | Lethal autonomous weapons | 致命性自主武器 |
| 27.3.2 | Surveillance, security, and privacy | 监视、安全与隐私 |
| 27.3.3 | Fairness and bias | 公平与偏见 |
| 27.3.4 | Trust and transparency | 信任与透明 |
| 27.3.5 | The future of work | 工作的未来 |
| 27.3.6 | Robot rights | 机器人权利 |
| 27.3.7 | AI Safety | 人工智能安全 |
| — | Summary | 小结 |
| — | Bibliographical and Historical Notes | 文献与历史注释 |

### 5.10 第28章 人工智能的未来

> 只收 `AIMA-术语对照表.md` 中尚未单列的条目。已有译法（智能体、体系结构、反射、原子/因子化/结构化表示、深度学习、逆向强化学习、线性时序逻辑、元推理、有限理性、探索/利用、HLAI、摩尔定律、GPU/TPU/FPGA、MCMC、MCTS、老虎机问题等）不重复。
> 译名自拟，未与中译本正文核对。

### 1. 新术语

| English | 中文 | 备注 |
|---|---|---|
| lidar | 激光雷达（lidar） | 价格：$75,000 → $1,000，单芯片或至 $10 |
| MEMS (micro-electromechanical systems) | 微机电系统（MEMS） | |
| bioprinting | 生物打印 | 与 3-D printing（三维打印）并列 |
| word embedding | 词嵌入 | 第 24 章；摆脱充要条件式的概念定义 |
| hierarchical reinforcement learning | 分层强化学习 | 「分层」沿用 hierarchical planning = 分层规划 |
| utility-maximization agent | 效用最大化智能体 | 本章用语。已有 utility-based agent = 基于效用的智能体，两词不要互换 |
| preference uncertainty | 偏好不确定 | 开箱智能体必然在此条件下运作 |
| reward function | 奖励函数 | 描述的是状态历史上的偏好，不是状态偏好本身 |
| time well spent | 时间值得花 | Harris 的运动名，页边术语 |
| personal agent | 个人智能体 | 页边术语；维护用户长期利益，而不是应用厂商的利益 |
| transfer learning | 迁移学习 | |
| apprenticeship learning | 学徒学习 | 能听懂建议，不是只会要标注图 |
| generative adversarial network (GAN) | 生成对抗网络（GAN） | |
| batch normalization | 批归一化 | |
| dropout | dropout（随机失活） | 技巧名可保留英文 |
| rectified linear unit (ReLU) | 修正线性单元（ReLU） | |
| differentiable programming | 可微编程 | LeCun 建议用它替换招牌词 deep learning；希望整个软件系统可优化，不只是模型 |
| weakly supervised learning | 弱监督学习 | 少量标签和/或少量奖励；大部分学习仍是无监督 |
| predictive learning | 预测学习 | LeCun：预测未来状态的某些方面。不是 i.i.d. 标签，也不是价值函数 |
| data science | 数据科学 | 统计学、编程与领域知识的汇合 |
| shared model | 共享模型 | 相对共享数据；云厂商的预训练模型 |
| crowdsourcing | 众包 | 标注之后必须验证 |
| real-time AI | 实时 AI | ⚠️ 不是 learning real-time A*（学习实时 A*） |
| anytime algorithm | 任意时间算法 | 质量随时间变好；打断时已有尚可决策。例子：迭代加深、贝叶斯网络中的 MCMC |
| decision-theoretic metareasoning | 决策理论元推理 | metareasoning 已作「元推理」；decision theory 已作「决策理论」 |
| metalevel decision | 元层决策 | MCTS 选择下一片叶子即是一例 |
| metalevel reinforcement learning | 元层强化学习 | 用来避开简单信息价值计算的短视 |
| playout | 推演 | 自拟；备选「模拟对局」 |
| reflective architecture | 反思型体系结构 | ⚠️ 不是反射（reflex）。对自身内部的计算做慎思 |
| joint state space | 联合状态空间 | 环境状态 + 智能体自身的计算状态 |
| bounded optimality | 有界最优 | ⚠️ ≠ limited rationality（有限理性）；≠ bounded suboptimal search（有界次优搜索）。固定体系结构下最好的程序，必然存在 |
| action–value system | 动作价值系统 | 与反射系统并列为可组合的有界最优组件 |
| symbolic system | 符号系统 | 逻辑推断与概率推断 |
| uninterpreted parameter | 无解释参数 | 连接主义：对大量此类参数做损失最小化 |
| myopia | 短视 | 专指简单信息价值计算的短视，不是一般口语 |
| tensor core | 张量核心 | 与 GPU、TPU、FPGA 并列的训练硬件 |
| hyperparameter | 超参数 | 量子分工只是设想：用量子算法搜索超参数，常规训练仍在经典机上；书中说还不知道怎么做 |
| exaflop/second-day | exaflop/s·day | 单位保留。AlphaZero 超过 1 |
| general AI | 通用 AI | 本章未用缩写 AGI。已有 artificial general intelligence = 通用人工智能，不要倒写成 AGI 运动 |
| AI engineering | 人工智能工程 | 小节名。对照的是 software engineering 成为产业之后的工具与生态 |

### 2. 小节标题

官方 TOC 只有 28.1、28.2，没有三级编号。下表中文均为自拟。

| English | 中文 | 备注 |
|---|---|---|
| The Future of AI | 人工智能的未来 | 章名 |
| AI Components | 人工智能的组件 | 28.1 |
| Sensors and actuators | 传感器与执行器 | 无编号小标题 |
| Representing the state of the world | 表示世界的状态 | 无编号小标题 |
| Selecting actions | 选择动作 | 无编号小标题 |
| Deciding what we want | 决定我们想要什么 | 无编号小标题 |
| Learning | 学习 | 无编号小标题 |
| Resources | 资源 | 无编号小标题 |
| AI Architectures | 人工智能体系结构 | 28.2。architecture 沿用「体系结构」，备选「架构」，未核对中译本 |
| General AI | 通用 AI | 无编号小标题 |
| AI engineering | 人工智能工程 | 无编号小标题 |
| The future | 未来 | 无编号小标题。本章无 Summary |

### 3. 易混（翻译时强制分开）

| 对子 | 不要写成 |
|---|---|
| reflex 反射 / reflective 反思 | 反思型体系结构 ≠ 反射智能体 |
| bounded optimality 有界最优 / limited rationality 有限理性 | 前者是固定体系结构下最好的程序，必然存在；后者是算不完时如何得体地行动 |
| anytime 的例子（迭代加深、MCMC）/ 元推理的例子（MCTS 选叶子） | 不要对调 |
| 状态偏好 / 历史偏好 | 状态偏好由历史偏好编译而来；奖励函数描述的是历史 |
| 分类的 `h : R^n → {0, 1}` | 不要写成连续概率 |
| 比人脑强 `10^33` 倍仍离理性更远 / 终极 1 kg 装置比 2020 年超级计算机快 `10^33` 倍 | 两个比较的基线不同，不要合成一句 |
| 本章 arXiv「每两年」、算力「每 3.5 个月」/ 书页 28「每年」、「每 3.4 个月」 | 两处都照各自原文，不要取平均 |

## 6. 维护约定

1. **新增术语必须回填本表**（规则文件 §3 第 ④ 步），否则下次还会重新讨论一遍。
2. 表内 ✅ = 已与中译本核对；⚠️ = 学界有分歧，以本表为准；🚫 = 明确禁用。
3. 同一英文在不同语境含义不同时，在 §1.9「同形异义必须分列」中登记，不要合并成一行。
4. 小节标题的**英文编号**来自官方 TOC（权威）；三级标题的**中文译名**若未标 ✅ 则为自拟，需对照中译本正文确认。

## 7. 变更记录

| 版本 | 日期 | 变更 |
|---|---|---|
| v1.0 | 2026-10-07 | 初版。从 `AIMA-中文翻译规则.md` 拆出；术语总表 7 类约 150 条 + 11–18 章 120 条小节标题对照。 |
| v1.1 | 2026-10-07 | 头部引用更新：方法论改为指向 `book-translation` skill，配套文件改为 `AIMA-翻译项目配置.md`（原规则文件已拆分为 skill + 项目配置两份）。 |
| v1.2 | 2026-10-07 | Part III（第 7–11 章）翻译完成后合并 5 份术语增量，新增 §3；原维护约定→§4、变更记录→§5。 |
| v1.3 | 2026-10-07 | Part I & II（第 1–6 章）翻译完成后合并 6 份术语增量，新增 §3；原 Part III 节→§4、维护约定→§5、变更记录→§6。 |
| v1.4 | 2026-10-07 | Part V–VII（第 19–28 章）翻译完成后合并 10 份术语增量，新增 §5；维护约定→§6、变更记录→§7。 |
