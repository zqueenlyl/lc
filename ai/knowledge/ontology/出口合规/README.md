# 出口合规 · 订单 A1042 的制裁穿透

> 本目录的第 1 站。先跑通这一页，再回 [上级](../README.md) 读定义。源系统只写股权和名单；「Harbor 受制裁」「这票货要阻断」是推理器推出来的。
>
> 本体：[trade.ttl](./trade.ttl)。推理：[reason.py](./reason.py)（[owlrl](https://github.com/RDFLib/OWL-RL) 7.6.2 的 `OWLRL_Semantics`，前向链物化）。不需要 Java，也不声称这是 OWL 2 DL。

同一张订单的另一道门在 [发货门禁](../../lean/发货门禁.md)：已支付、欺诈排除、有库存、地址核验，用 Lean 证明「可以发货」。那是闭世界的命题依赖。本页是开放世界的类蕴含，回答另一句问话：**收货方会不会沿股权被制裁名单穿透。**

---

## 一、源系统愿意签字的事实

订单 A1042 的收货方是 Harbor Ltd。三个系统各写一条，谁都不写结论：

| 谁 | 写下的事实 |
|---|---|
| 股权 | Harbor 是 Acme 的子公司，Acme 是 Globex 的子公司 |
| 制裁名单 | Globex 列在 SDN 上 |
| 人事 | Harbor 雇用 Alice |

没有「Globex 是组织」的显式类型。没有「Harbor 受制裁」。没有「A1042 阻断」。

## 二、本体承诺的四条公理

类：参与方、人、组织、制裁名单、受制裁参与方、装运、阻断装运。人与组织不相交。

```owl-functional
TransitiveObjectProperty( subsidiaryOf )
ObjectPropertyDomain( subsidiaryOf Organization )
ObjectPropertyRange( subsidiaryOf Organization )

SubClassOf( ObjectSomeValuesFrom( listedOn SanctionList ) SanctionedParty )
SubClassOf( ObjectSomeValuesFrom( subsidiaryOf SanctionedParty ) SanctionedParty )
SubClassOf( ObjectSomeValuesFrom( consignedTo SanctionedParty ) BlockedShipment )
```

第三条配合传递性，就是股权穿透：子公司的子公司仍然受制裁。完整 Turtle 在 [trade.ttl](./trade.ttl)。存在限制写在子类公理的**左侧**，所以落在 OWL 2 RL 里，前向链推得出新类型。

`subsidiaryOf` 的定义域和值域是蕴含。谁出现在这条边的两端，就被推出为组织，写入不会因此失败。

## 三、推理

在本目录执行（需 `rdflib` 与 `owlrl`）：

```bash
python3 reason.py
```

本次物化实际打印：

```
断言（trade.ttl 里写了的）
  A1042  a  Shipment
  A1042  consignedTo  harbor
  acme  subsidiaryOf  globex
  globex  listedOn  sdn
  harbor  employs  alice
  harbor  subsidiaryOf  acme
  sdn  a  SanctionList
推出（物化后新出现的）
  A1042  a  BlockedShipment
  acme  a  Organization
  acme  a  Party
  acme  a  SanctionedParty
  alice  a  Party
  alice  a  Person
  alice  employedBy  harbor
  globex  a  Organization
  globex  a  Party
  globex  a  SanctionedParty
  harbor  a  Organization
  harbor  a  Party
  harbor  a  SanctionedParty
  harbor  subsidiaryOf  globex
```

脚本会核对上表里的关键推断，缺一条就以非 0 退出。

| 推出 | 靠的公理 |
|---|---|
| `globex a SanctionedParty` | Globex 列在 SDN 上，SDN 是制裁名单 |
| `globex a Organization` | Acme `subsidiaryOf` Globex，值域是组织 |
| `acme a SanctionedParty` | Acme 是受制裁参与方 Globex 的子公司 |
| `harbor subsidiaryOf globex` | `subsidiaryOf` 传递 |
| `harbor a SanctionedParty` | Harbor 是受制裁参与方的子公司 |
| `harbor a Organization` | `employs` / `subsidiaryOf` 的定义域 |
| `alice a Person` | `employs` 的值域 |
| `alice employedBy harbor` | `employs` 与 `employedBy` 互逆 |
| `A1042 a BlockedShipment` | 收货方 Harbor 已被推出为受制裁参与方 |

业务上这张订单应被阻断。阻断不是名单系统写的，是股权链和三条类公理算出来的。

## 四、再推一次：把 Harbor 标成人

定义域已经推出 Harbor 是组织。若再断言它是人，人和组织不相交，本体不一致。

```bash
python3 reason.py --contradict
```

owlrl 记下一则错误：`Person` 与 `Organization` 有共同个体 `harbor`。类型三元组仍然会被物化出来——RL 引擎是在闭合之后报告冲突，不是在写入时拒收。拒收表单要另做 SHACL 或 API 校验，见 [学术本体](../学术本体.md)。

## 五、这份本体故意不回答的

- **未支付就不能发货。** 那是否定，在 [Lean 发货门禁](../../lean/发货门禁.md) 里。OWL 的开放世界不会把「没写已支付」当成「未支付」。
- **另一张没写收货方的订单。** 不会变成阻断装运。没写 `consignedTo` 只表示还不知道收货方。
- **批准、派工、回写源系统。** 那是运营本体的动作，不是这几条公理。
