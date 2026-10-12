# 订单流转 · 状态图

> 本目录是这台状态机的 OWL 2 RL 写法。业务规则、十四条边，以及 Lean 证明了哪一半，见 [订单流转](../../lean/订单流转.md)。
>
> 本体：[order.ttl](./order.ttl)。推理：[reason.py](./reason.py)。

订单 A1042 当前是已发货，订单 B7 当前是已取消。推理器把状态上的阶段抬到订单上：

```bash
python3 reason.py
```

应推出 `A1042 a FulfilledOrder`、`B7 a BeforePayOrder`。边 `mayProceedTo` 仍是写进去的事实。

```bash
python3 reason.py --contradict
```

给 A1042 再写一个草稿状态。函数性的 `hasStatus` 会把草稿和已发货并成同一个体，付款前与已履约相交，推理器报告不一致。

「走到已发货的历史一定付过款」不在这次物化里。那条归纳在 [OrderFlow.lean](../../lean/OrderFlow.lean) 的 `funded_saw_paid`。
