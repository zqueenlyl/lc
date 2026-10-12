# Lean 4 · 可核验的证明与程序

> **定位**：知识库五维里的「④ 表示与建模」再开一条。OWL 用描述逻辑推蕴含；运营本体管组织里的对象与动作；**Lean 4 要一份证明项，由很小的 kernel 检查到公理**。同一条数学命题，自然语言综述、检索片段、模型自述都不算这条线上的证据。
>
> 快照：**2026-10-12**。语言事实以 [Lean Language Reference](https://lean-lang.org/doc/reference/latest/) 公开预览为准，其 Introduction 写明所描述版本为 **`4.35.0-rc4`**（rc，不是发行说明里的稳定版号）。教材口径见 [Theorem Proving in Lean 4](https://lean-lang.org/theorem_proving_in_lean4/Introduction/)（下称 TPIL）。未在这些页面出现的性能数字、库规模实时值不写。

上级：[../README.md](../README.md) ｜ 五维总表：[../knowledge-base/](../knowledge-base/) ｜ 学术 OWL vs 运营本体：[../ontology/](../ontology/) ｜ Agent 把已有数学写成 Lean 的案例：[../../agent/multi-agent-research/anthropic.md](../../agent/multi-agent-research/anthropic.md)

示例按这个顺序读：[自然语言](./发货门禁.md) → [Lean](./ShipGate.lean) → [交互式证明](./发货门禁-证明.html)。场景是订单 A1042 的发货门禁。同一张订单上「收货方是否沿股权被制裁穿透」是另一问，用 OWL 2 RL 回答：[出口合规](../ontology/出口合规/)。十条状态的流转见 [订单流转](./订单流转.md) 与 [OrderFlow.lean](./OrderFlow.lean)，对照的本体在 [ontology/订单流转](../ontology/订单流转/)。

---

## 一、先分清三件事

混用会把「模型写了一段看起来像证明的话」当成 kernel 已接受，或把 Lean 3 的教程直接套到今天的工具链上。

| | **自动定理证明（ATP）** | **交互式定理证明（ITP）** | **Lean 4** |
|---|---|---|---|
| **回答的问题** | 能不能搜出一条证明？ | 这条声称的证明，逐步是否都落在公理上？ | 两者接在同一套类型论里：自动化产出证明项，kernel 检查证明项 |
| **TPIL 的原话** | 侧重 finding；SMT、SAT、代数系统可以很强，健全性不总是保证 | 侧重 verification；每一步回到定义、定理、公理，并给出可独立检查的 proof object | 把自动化放进仍要构造完整公理化证明的框架 |
| **失败长什么样** | 求解器超时、给出 unknown、或求解器自身有 bug | 证明写不完 | 目标没关上，或 `#print axioms` 里出现 `sorryAx` / 自加公理 |

版本：

| | **Lean 3** | **Lean 4** |
|---|---|---|
| **实现** | 证明器主体是 C++；策略、记法、顶层命令已能用 Lean 写 | **自托管**：参考手册写大约 90% 的实现本身是 Lean。4.0 于 **2023-09-08** 发布；开发自 2018 年起，手册写明不计划再重写一遍 |
| **库** | 末期 Mathlib 超过 100 万行 | 2023 年社区把 Mathlib 移植过来；手册 History 节写现已超过 **150 万行**，相对 Lean 3 末期大约增长 50%，Lean 4 检查更大的库仍快于 Lean 3 检查较小的库 |
| **今天该读的书** | 旧教程、旧 Mathlib 文档 | [TPIL](https://lean-lang.org/theorem_proving_in_lean4/Introduction/)、[Functional Programming in Lean](https://lean-lang.org/functional_programming_in_lean/)、[Language Reference](https://lean-lang.org/doc/reference/latest/)、社区 [Mathematics in Lean](https://leanprover-community.github.io/mathematics_in_lean/) |

和本目录另外两条「表示」并排：

| | **OWL / RDF** | **运营本体** | **Lean 4** | **RAG 里的一段文本** |
|---|---|---|---|---|
| **合法对象** | 类、属性、个体、公理 | object / link / action | 类型、项、命题、证明项 | 切片 |
| **「对」的意思** | reasoner 推出蕴含、一致性通过 | 动作在角色与校验下提交，各应用看到同一版 | kernel 接受该证明项，且陈述翻译无误 | 检索命中、生成看起来相关 |
| **写错了会怎样** | 本体不一致或推不出 | 动作被拒或写回错误源 | 目标剩余、类型错误，或公理列表不干净 | 仍可能被模型复述 |

选型口诀：

- 要跨机构共享概念、做开放世界蕴含 → [OWL](../ontology/)。
- 要让人和 Agent 在权限内改同一业务对象 → [运营本体](../ontology/)。
- 要让一条数学陈述或程序规约留下可独立复检的证明项 → **Lean 4**。
- 要回答「文档里怎么说」→ [RAG](../rag/)。检索不能代替 kernel。

---

## 二、语言在什么位置

[TPIL §1.2](https://lean-lang.org/theorem_proving_in_lean4/Introduction/)：Lean 由 Leonardo de Moura 于 2013 年在 Microsoft Research 启动，Apache 2.0。参考手册 History：0.1 于 2014-06-16 发布；3.0 系列首发 2017-01-20，数学社区在其上建起 Mathlib。2023-07 月 de Moura 与 Sebastian Ullrich 在 Convergent Research 下成立 **Lean FRO**（非营利）；资助方手册点名 Simons Foundation International、Alfred P. Sloan Foundation、Richard Merkin。手册写 FRO 当时有十名以上雇员。

引用论文（语言设计，早于 4.0 发行）：de Moura & Ullrich，*The Lean 4 Theorem Prover and Programming Language*，CADE 28，2021。[doi:10.1007/978-3-030-79876-5_37](https://doi.org/10.1007/978-3-030-79876-5_37)。摘要里的设计点，今天的参考手册仍沿用：

- 证明器与编程语言是同一门语言。用户用 Lean 写策略、判定过程、代码生成扩展，不必改 C++ 再重建。
- 卫生宏（hygienic macros）专为 ITP 设计。
- 类型类解析换成 tabled resolution，对付大型库上的性能问题。
- 运行时走引用计数，能就地更新紧凑数组（论文称之为 **functional but in-place**），因为大量证明自动化本身就是 Lean 程序。
- 可扩展的部分包括 parser、elaborator、tactics、pretty printer、code generator。

参考手册开篇把信任拆开：核心类型论放在**只检查证明项的 kernel**里，小到可以有独立实现。策略语言再强，也只是产出核心理论中的项；项仍由 kernel 检查。策略有 bug，不自动变成逻辑漏洞。手册同时写 Lean 是纯函数式语言：引用计数运行时、紧凑数组、多线程、单子 `IO`。本参考手册自身用 Lean 写的文档工具 Verso 生成。

逻辑基础，TPIL §1.3：一带归纳类型的 **Calculus of Constructions**。表达力够写常规数学定理，计算解释让同一套项既能当程序跑，也能当证明被检查。

---

## 三、信任边界：kernel、公理、`sorry`

一条声明被接受，分三层，缺一层都不算证完。

### 3.1 Kernel 检查项

策略、精简器、自动化都在 kernel 之外。它们的产物是项。参考手册：[Axioms](https://lean-lang.org/doc/reference/latest/Axioms/) 把标准公理列成四条，前三条是日常数学要用的，第四条是未完成证明的标记。

| 公理 | 官方类型（手册原文缩写） | 在证明里意味着什么 |
|---|---|---|
| `propext` | `(a ↔ b) → a = b` | 互相蕴含的命题相等（命题外延） |
| `Quot.sound` | `r a b → Quot.mk r a = Quot.mk r b` | 商：被关系连上的元素在商里是同一个 |
| `Classical.choice` | `Nonempty α → α` | 从「非空」取出一个元素；没有计算内容 |
| `sorryAx` | `α` | `sorry` 的实现。能证明任何东西。**完成的证明里不应出现** |

`Classical.choice` 能推出排中律（Diaconescu，还需 `propext` 与函数外延；TPIL [Axioms and Computation](https://lean-lang.org/theorem_proving_in_lean4/Axioms-and-Computation/) 有标准库里的证明梗概）。用它造数据的定义必须标 `noncomputable`。Mathlib 大部分自由使用排中律与选择公理；想避开选择公理的引理放在 `Decidable` 命名空间，并用 `#print axioms` 看列表里有没有 `Classical.choice`（[Mathlib/Logic/Basic.lean](https://github.com/leanprover-community/mathlib4/blob/master/Mathlib/Logic/Basic.lean) 文件头）。

手册还写了 kernel 以外的第二条信任根：用原生求值做的证明，会为每次被编译代码断言的计算单独引入公理，信任的是**整个编译器**，不只是 kernel。见到这类公理，不要把它说成「只依赖 kernel」。

查看一条声明传递依赖了哪些公理：

```lean
#print axioms excluded_middle
-- 'excluded_middle' depends on axioms: [propext, Classical.choice, Quot.sound]
```

社区核对清单（[did you prove it](https://github.com/leanprover-community/leanprover-community.github.io/blob/lean4/templates/did_you_prove_it.md)）把完成标准写成：`#print axioms` 的结果是 `{propext, Classical.choice, Quot.sound}` 的子集。出现自定义 `axiom` 或 `sorryAx`，证明未完成。同一份清单把另一件事分开：Mathlib 里费马大定理、黎曼猜想等条目是**陈述**，由维护者核对过「这句话是不是那条数学命题的翻译」。陈述在库里，不等于该命题已有证明。

### 3.2 `sorry` 是洞，不是证据

`sorry` 让声明先通过，目标仍空着。参考手册 Introduction 写明：`#eval` 因不健全而**拒绝**依赖 `sorry` 的表达式（包括间接依赖）；`#eval!` 才能强行算。警告文案是 `declaration uses sorry`。

因此 Agent 交上来的 Lean 文件，验收至少看两件事：目标已关上，以及 `#print axioms` 里没有 `sorryAx`。陈述是否忠于要证的数学命题，是第三件事，kernel 不代劳。

---

## 四、写证明时实际碰到的构造

不在这里讲策略目录。要记住的是项、命题、归纳类型、类型类这四块，其余是把项写完的界面。

**命题即类型。** `Prop` 是命题的类型。证明是该类型的项。下面两条是同一个定理：第一条把证明写成函数项，第二条用策略造出等价的项。

```lean
theorem and_swap (p q : Prop) : p ∧ q → q ∧ p :=
  fun h => And.intro (And.right h) (And.left h)

theorem and_swap' (p q : Prop) : p ∧ q → q ∧ p := by
  intro h
  exact And.intro h.right h.left
```

`theorem` 的类型是要证的命题，值是证明项。`def` 定义程序或数学对象。`example` 是不留名字的检查。

**归纳类型**同时承担代数数据类型和归纳谓词。参考手册里的偶数谓词就是这条路：`Even : Nat → Prop`，构造子 `zero : Even 0` 与 `plusTwo : Even n → Even (n + 2)`。对它做归纳，就是对构造子做分情况。

**Elaborator** 填隐式参数、重载、类型类实例。用户写的是省略后的表面语法，kernel 看到的是补全后的项。类型类解析在大型库里是性能关键路径（CADE 摘要里的 tabled resolution）。

**元编程在语言内。** 策略是 Lean 函数，定义完即可用，不必重启证明器或加载外部模块（参考手册开篇）。所以 Mathlib 的自动化与用户项目的自动化走同一条扩展 API。

---

## 五、工程栈（名称级）

| 件 | 角色 |
|---|---|
| [lean4](https://github.com/leanprover/lean4/) | 语言与证明器源码 |
| **elan** | 工具链版本。项目钉死的 Lean 版本必须能被别人复现；社区清单把「仓库 + 工具链文件」写成可独立编译的前提 |
| **Lake** | Lean 4 的构建与包管理。依赖哪一版 Mathlib，写在项目里，不写在口头约定里 |
| [mathlib4](https://github.com/leanprover-community/mathlib4) | 社区数学库。正式数学几乎都建在它上面，而不是从 `Nat` 重写 |
| 编辑器 | 官方路径是 VS Code + Lean 扩展：保存即检查，目标状态跟着光标走。TPIL 的例子可从文档面板打开 |

学习顺序，按 [lean-lang.org/learn](https://lean-lang.org/learn/) 的分工，而不是按论文年份：

1. 要写能跑的 Lean 程序 → [Functional Programming in Lean](https://lean-lang.org/functional_programming_in_lean/)（该书写明例子按 Lean `4.33.0` 测试；参考手册预览描述的是 `4.35.0-rc4`，两处版本针分开记）。
2. 要写证明、理解依赖类型 → TPIL。
3. 要跟着数学课本形式化 → Mathematics in Lean（用 Mathlib）。
4. 要查语法与命令的精确定义 → Language Reference（公开预览；引用时带上页内版本号）。

---

## 六、和本手册其它专题怎么拼

```
自然语言命题 / 论文 / 模型草稿
        │  翻译成类型（这一步 kernel 不检查「翻译是否忠实」）
        ▼
Lean 陈述 : Prop
        │  人写，或 Agent 写项 / 策略
        ▼
证明项 ──kernel──▶ 接受 / 拒绝
        │
        └─ #print axioms ∈ {propext, Classical.choice, Quot.sound} 的子集
```

| 需求 | 用 Lean 解决不了的部分 | 应对 |
|---|---|---|
| 「这篇论文的定理是否成立」 | 模型摘要 | 先有对齐过的陈述，再交 kernel；陈述对照见社区清单，多智能体案例见 [Anthropic 笔记](../../agent/multi-agent-research/anthropic.md) |
| 「这段检索和答案一致吗」 | 证明项 | [RAG](../rag/) + [Eval](../../reliability/eval/)；要机器证明时再形式化 |
| 「这个业务对象允许被改吗」 | 类型论 | [运营本体](../ontology/) 的 action + role，或应用层状态机 |
| 「类公理能否推出蕴含」 | 证明项库 | OWL reasoner |
| Agent 交了 `.lean` 文件 | 文件能解析 ≠ 证完 | 构建通过、无 `sorry`、公理列表干净、陈述由懂该领域的人签过 |

落地时把验收写成和测试一样的命令，而不是把模型的「我证明了」写入记忆：

1. **工具链钉死在仓库里**（elan + Lake），换一台机器仍是同一 Lean、同一 Mathlib。
2. **禁止把 `sorry` 留在要合并的定理上**；`sorryAx` 一出现就当失败。
3. **公理白名单只有标准三条**。项目若加自己的 `axiom`，要单独列出并说明为何不能是定理。
4. **陈述评审与证明评审分开**。Mathlib 已有的陈述优先引用，避免同一命题两套翻译。
5. **原生求值公理单独记账**。依赖编译器的证明不要写成「kernel 已独立检查」。

本手册里已经写过的规模数字（约 11 天、行数、token、Prove2Me 的 DAG）留在 [Anthropic 多智能体笔记](../../agent/multi-agent-research/anthropic.md)。本页只固定验收标准：Lean 是检查器，Agent 是提出证明项的一方。

---

## 七、证据边界

- 4.0 日期、自托管约 90%、Mathlib 行数与「不再重写」、FRO：参考手册 [Introduction / History](https://lean-lang.org/doc/reference/latest/Introduction/)，版本 `4.35.0-rc4`。行数是该页陈述，不是本页另做的 `cloc`。
- ATP / ITP 分工、CoC + 归纳类型、Apache 2.0： [TPIL Introduction](https://lean-lang.org/theorem_proving_in_lean4/Introduction/)。
- 四条标准公理、`#print axioms`、原生求值公理：参考手册 [Axioms](https://lean-lang.org/doc/reference/latest/Axioms/)。
- `propext` / `Quot.sound` / `Classical.choice` / `noncomputable`： [TPIL Axioms and Computation](https://lean-lang.org/theorem_proving_in_lean4/Axioms-and-Computation/)。
- 可扩展性、functional but in-place、tabled typeclass resolution：CADE 28 论文摘要（2021），与现行手册互证；论文早于 4.0 发行日。
- 完成标准与「陈述 ≠ 证明」：社区 [did you prove it](https://github.com/leanprover-community/leanprover-community.github.io/blob/lean4/templates/did_you_prove_it.md)。
- **未写**：当前稳定版号（本页只钉参考手册预览所描述的 rc）、Mathlib 实时行数、与 Rocq / Isabelle / Agda 的基准对照、kernel 的独立实现清单与审计结论。

---

## 延伸

- 示例（自然语言 → Lean → 交互式证明）：[发货门禁.md](./发货门禁.md) · [ShipGate.lean](./ShipGate.lean) · [发货门禁-证明.html](./发货门禁-证明.html)
- 学习入口：[lean-lang.org/learn](https://lean-lang.org/learn/) · [TPIL](https://lean-lang.org/theorem_proving_in_lean4/Introduction/) · [Language Reference](https://lean-lang.org/doc/reference/latest/)
- 源码与库：[leanprover/lean4](https://github.com/leanprover/lean4/) · [mathlib4](https://github.com/leanprover-community/mathlib4)
- 表示层的另外两条：[ontology/](../ontology/) · [知识库类型整理 §四](../knowledge-base/知识库类型整理.md)
- Agent 侧案例（数字不在本页重复）：[formalizing Fermat's Last Theorem](https://www.anthropic.com/research/formalizing-fermats-last-theorem) · 本手册 [anthropic.md](../../agent/multi-agent-research/anthropic.md)
