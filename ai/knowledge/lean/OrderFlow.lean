/-
订单 A1042 的流转。阅读顺序：

1. 订单流转.md     状态、边、以及 Ontology 做不到的那一半
2. 本文件           Lean

十条状态，十四条边。边是归纳构造子，没有别的入口。
本文件不依赖 Mathlib。证明里不放 sorry。
本机核验：Lean 4.34.1，`lean OrderFlow.lean` 通过。
-/

namespace OrderFlow

/-- 订单所处的状态。同一时刻只停在其中一个。 -/
inductive Status where
  | draft
  | submitted
  | paid
  | riskHold
  | allocated
  | shipped
  | delivered
  | cancelled
  | refunding
  | closed
  deriving DecidableEq

namespace Status

/-- 钱已经进过这笔订单的状态。已关闭不在此列：未支付取消也能关闭。 -/
inductive Funded : Status → Prop where
  | paid : Funded paid
  | riskHold : Funded riskHold
  | allocated : Funded allocated
  | shipped : Funded shipped
  | delivered : Funded delivered
  | refunding : Funded refunding

end Status

/-- 唯一允许的状态迁移。 -/
inductive Step : Status → Status → Prop where
  | submit : Step .draft .submitted
  | pay : Step .submitted .paid
  | cancelUnpaid : Step .submitted .cancelled
  | allocateClear : Step .paid .allocated
  | flagRisk : Step .paid .riskHold
  | refundPaid : Step .paid .refunding
  | releaseHold : Step .riskHold .allocated
  | rejectHold : Step .riskHold .refunding
  | refundAllocated : Step .allocated .refunding
  | ship : Step .allocated .shipped
  | deliver : Step .shipped .delivered
  | closeDelivered : Step .delivered .closed
  | closeRefund : Step .refunding .closed
  | closeCancelled : Step .cancelled .closed

/-- 从草稿出发的一条历史，停在 `s`。 -/
inductive Hist : Status → Type where
  | start : Hist .draft
  | go : Hist s → Step s t → Hist t

/-- 这条历史曾经停在已支付。 -/
inductive PaidSeen : {s : Status} → Hist s → Prop where
  | here : (h : Hist .paid) → PaidSeen h
  | earlier : PaidSeen h → PaidSeen (.go h step)

theorem no_exit_closed (t : Status) (h : Step .closed t) : False := by
  cases h

theorem draft_cannot_ship (h : Step .draft .shipped) : False := by
  cases h

theorem ship_only_from_allocated (s : Status) (h : Step s .shipped) : s = .allocated := by
  cases h
  rfl

/-- 停在「钱已进过」的状态上，则历史上一定到过已支付。 -/
theorem funded_saw_paid {s : Status} (h : Hist s) (hf : Status.Funded s) : PaidSeen h := by
  induction h with
  | start => cases hf
  | go prev step ih =>
    cases hf with
    | paid =>
      cases step
      exact PaidSeen.here (Hist.go prev Step.pay)
    | riskHold =>
      cases step
      exact PaidSeen.earlier (ih Status.Funded.paid)
    | allocated =>
      cases step with
      | allocateClear => exact PaidSeen.earlier (ih Status.Funded.paid)
      | releaseHold => exact PaidSeen.earlier (ih Status.Funded.riskHold)
    | refunding =>
      cases step with
      | refundPaid => exact PaidSeen.earlier (ih Status.Funded.paid)
      | rejectHold => exact PaidSeen.earlier (ih Status.Funded.riskHold)
      | refundAllocated => exact PaidSeen.earlier (ih Status.Funded.allocated)
    | shipped =>
      cases step
      exact PaidSeen.earlier (ih Status.Funded.allocated)
    | delivered =>
      cases step
      exact PaidSeen.earlier (ih Status.Funded.shipped)

/-- 草稿，确认，支付，直接占库，发货，签收。 -/
def happy : Hist .delivered :=
  .go (.go (.go (.go (.go .start .submit) .pay) .allocateClear) .ship) .deliver

/-- 支付之后先被风控挂起，排除后再发货。 -/
def heldThenShip : Hist .shipped :=
  .go (.go (.go (.go (.go .start .submit) .pay) .flagRisk) .releaseHold) .ship

/-- 提交后未支付就取消，然后关闭。这条历史不到已支付。 -/
def cancelUnpaid : Hist .closed :=
  .go (.go (.go .start .submit) .cancelUnpaid) .closeCancelled

theorem happy_saw_paid : PaidSeen happy :=
  funded_saw_paid happy .delivered

theorem held_saw_paid : PaidSeen heldThenShip :=
  funded_saw_paid heldThenShip .shipped

theorem draft_not_seen (h : Hist .draft) (ps : PaidSeen h) : False := by
  cases h with
  | start => cases ps
  | go _ step => cases step

theorem submitted_not_seen (h : Hist .submitted) (ps : PaidSeen h) : False := by
  cases h with
  | go prev step =>
    cases step
    cases ps with
    | earlier earlierPs => exact draft_not_seen prev earlierPs

theorem cancelled_not_seen (h : Hist .cancelled) (ps : PaidSeen h) : False := by
  cases h with
  | go prev step =>
    cases step
    cases ps with
    | earlier earlierPs => exact submitted_not_seen prev earlierPs

theorem cancel_unpaid_never_paid (ps : PaidSeen cancelUnpaid) : False := by
  cases ps with
  | earlier psCancelled => exact cancelled_not_seen _ psCancelled

end OrderFlow
