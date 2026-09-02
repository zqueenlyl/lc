package solution

import "testing"

func TestLowestCommonAncestor(t *testing.T) {
	root := buildTree(3, 5, 1, 6, 2, 0, 8, nil, nil, 7, 4)

	// p=5(root.Left), q=1(root.Right)，LCA 应为 root。
	if got := LowestCommonAncestor(root, root.Left, root.Right); got != root {
		t.Errorf("LowestCommonAncestor(p=5, q=1) = %v, want node 3", got)
	}

	// p=5(root.Left), q=4(root.Left.Right.Right)，LCA 应为 5。
	if got := LowestCommonAncestor(root, root.Left, root.Left.Right.Right); got != root.Left {
		t.Errorf("LowestCommonAncestor(p=5, q=4) = %v, want node 5", got)
	}
}
