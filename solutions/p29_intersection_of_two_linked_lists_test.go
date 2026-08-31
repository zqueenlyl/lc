package solution

import "testing"

func TestGetIntersectionNode(t *testing.T) {
	// 共享尾节点 [8,4,5]；A 前缀 [4,1]，B 前缀 [5,6,1]。
	common := buildList([]int{8, 4, 5})
	a := &ListNode{Val: 4, Next: &ListNode{Val: 1, Next: common}}
	b := &ListNode{Val: 5, Next: &ListNode{Val: 6, Next: &ListNode{Val: 1, Next: common}}}

	if got := GetIntersectionNode(a, b); got != common {
		t.Errorf("GetIntersectionNode() = %v, want node with val 8", got)
	}

	// 不相交。
	if got := GetIntersectionNode(buildList([]int{1, 2}), buildList([]int{3, 4})); got != nil {
		t.Errorf("GetIntersectionNode() = %v, want nil", got)
	}
}
