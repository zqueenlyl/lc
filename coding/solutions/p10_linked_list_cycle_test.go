package solution

import "testing"

func TestHasCycle(t *testing.T) {
	// 构造 [3,2,0,-4]，尾节点指向下标 1 的节点（值为 2）。
	n3 := &ListNode{Val: 3}
	n2 := &ListNode{Val: 2}
	n0 := &ListNode{Val: 0}
	n4 := &ListNode{Val: -4}
	n3.Next = n2
	n2.Next = n0
	n0.Next = n4
	n4.Next = n2
	if !HasCycle(n3) {
		t.Error("HasCycle() = false, want true")
	}

	// 无环链表。
	if HasCycle(buildList([]int{1, 2, 3})) {
		t.Error("HasCycle() = true, want false")
	}
}
