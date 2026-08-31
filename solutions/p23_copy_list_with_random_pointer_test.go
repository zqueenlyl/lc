package solution

import (
	"reflect"
	"testing"
)

func TestCopyRandomList(t *testing.T) {
	// 构造 [[7,null],[13,0],[11,4],[10,2],[1,0]]
	n0 := &RandomNode{Val: 7}
	n1 := &RandomNode{Val: 13}
	n2 := &RandomNode{Val: 11}
	n3 := &RandomNode{Val: 10}
	n4 := &RandomNode{Val: 1}
	n0.Next = n1
	n1.Next = n2
	n2.Next = n3
	n3.Next = n4
	n1.Random = n0
	n2.Random = n4
	n3.Random = n2
	n4.Random = n0

	got := CopyRandomList(n0)

	nodes := []*RandomNode{}
	vals := []int{}
	for cur := got; cur != nil; cur = cur.Next {
		nodes = append(nodes, cur)
		vals = append(vals, cur.Val)
	}
	if want := []int{7, 13, 11, 10, 1}; !reflect.DeepEqual(vals, want) {
		t.Fatalf("CopyRandomList() vals = %v, want %v", vals, want)
	}
	if nodes[0].Random != nil {
		t.Error("node 0 random should be nil")
	}
	if nodes[1].Random != nodes[0] {
		t.Error("node 1 random should point to node 0")
	}
	if nodes[2].Random != nodes[4] {
		t.Error("node 2 random should point to node 4")
	}
	if nodes[3].Random != nodes[2] {
		t.Error("node 3 random should point to node 2")
	}
	if nodes[4].Random != nodes[0] {
		t.Error("node 4 random should point to node 0")
	}
}
