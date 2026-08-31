package solution

import (
	"reflect"
	"testing"
)

func TestLevelOrder(t *testing.T) {
	root := buildTree(3, 9, 20, nil, nil, 15, 7)
	got := LevelOrder(root)
	want := [][]int{{3}, {9, 20}, {15, 7}}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("LevelOrder() = %v, want %v", got, want)
	}
}
