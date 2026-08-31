package solution

import "testing"

func TestIsSymmetric(t *testing.T) {
	cases := []struct {
		root *TreeNode
		want bool
	}{
		{buildTree(1, 2, 2, 3, 4, 4, 3), true},
		{buildTree(1, 2, 2, nil, 3, nil, 3), false},
	}
	for _, c := range cases {
		if got := IsSymmetric(c.root); got != c.want {
			t.Errorf("IsSymmetric() = %v, want %v", got, c.want)
		}
	}
}
