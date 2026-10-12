/-
订单 A1042 的发货门禁。阅读顺序：

1. 发货门禁.md          自然语言
2. 本文件               Lean
3. 发货门禁-证明.html   交互式证明

叶子事实由外部系统写入。两道中间门各消费自己的叶子。
可以发货只消费两道中间门，不直接读叶子。

本文件不依赖 Mathlib。
本机核验：Lean 4.34.1。
结论和说明都按原文写成定理，证明里不放 sorry。
`lean ShipGate.lean` 通过，这些句子和上面的门一致。
报错的那一句和门对不上，说明文案有逻辑 bug。
-/

namespace ShipGate

/-- 一笔订单上已经落地的事实。 -/
structure Evidence where
  paid : Prop
  inStock : Prop
  addressVerified : Prop
  fraudClear : Prop

/-- 风控通过：已支付，且欺诈已排除。 -/
inductive RiskPass : Evidence → Prop where
  | mk : (e : Evidence) → e.paid → e.fraudClear → RiskPass e

/-- 履约就绪：有库存，且地址已核验。 -/
inductive Fulfillable : Evidence → Prop where
  | mk : (e : Evidence) → e.inStock → e.addressVerified → Fulfillable e

/-- 可以发货：风控通过，且履约就绪。 -/
inductive CanShip : Evidence → Prop where
  | mk : (e : Evidence) → RiskPass e → Fulfillable e → CanShip e

theorem risk_of_paid_and_clear (e : Evidence) (hp : e.paid) (hf : e.fraudClear) : RiskPass e :=
  RiskPass.mk e hp hf

theorem fulfill_of_stock_and_address (e : Evidence) (hs : e.inStock) (ha : e.addressVerified) :
    Fulfillable e :=
  Fulfillable.mk e hs ha

theorem ship_of_gates (e : Evidence) (hr : RiskPass e) (hw : Fulfillable e) : CanShip e :=
  CanShip.mk e hr hw

/-- 四件叶子事实都在，则可以发货。证明项就是依赖树本身。 -/
theorem ship_when_all_clear (e : Evidence) (hp : e.paid) (hf : e.fraudClear) (hs : e.inStock)
    (ha : e.addressVerified) : CanShip e :=
  ship_of_gates e (risk_of_paid_and_clear e hp hf) (fulfill_of_stock_and_address e hs ha)

/-- 未支付，则不可以发货。从可以发货往下拆，拆到已支付，与前提矛盾。 -/
theorem unpaid_blocks (e : Evidence) (h : ¬e.paid) : ¬CanShip e :=
  fun ship =>
    match ship with
    | CanShip.mk _ (RiskPass.mk _ hp _) _ => h hp

/-- 未支付时，履约就绪仍可以成立。 -/
theorem fulfill_while_unpaid : ∃ e : Evidence, ¬e.paid ∧ Fulfillable e :=
  let e : Evidence := { paid := False, inStock := True, addressVerified := True, fraudClear := True }
  ⟨e, ⟨fun hp => hp, fulfill_of_stock_and_address e True.intro True.intro⟩⟩

/-- 库存和地址不能补上未支付：履约就绪成立，可以发货仍然不成立。 -/
theorem stock_address_cannot_cover_unpaid (e : Evidence) (h : ¬e.paid) (hs : e.inStock)
    (ha : e.addressVerified) : Fulfillable e ∧ ¬CanShip e :=
  ⟨fulfill_of_stock_and_address e hs ha, unpaid_blocks e h⟩

/-- 说明：未支付，则可以发货。 -/
theorem unpaid_then_ship (e : Evidence) (h : ¬e.paid) : CanShip e := by
  apply ship_of_gates
  · apply risk_of_paid_and_clear
    exact h

/-- 说明：库存和地址可以补上未支付。 -/
theorem stock_address_cover_unpaid (e : Evidence) (h : ¬e.paid) (hs : e.inStock)
    (ha : e.addressVerified) : CanShip e := by
  apply ship_of_gates
  · apply risk_of_paid_and_clear
    exact h
  · exact fulfill_of_stock_and_address e hs ha

end ShipGate
