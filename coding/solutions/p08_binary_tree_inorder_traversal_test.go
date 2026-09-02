package solution

import (
	"reflect"
	"testing"
)

func TestInorderTraversal(t *testing.T) {
	root := buildTree(1, nil, 2, 3)
	got := InorderTraversal(root)
	want := []int{1, 3, 2}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("InorderTraversal() = %v, want %v", got, want)
	}
}
