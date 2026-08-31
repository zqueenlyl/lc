package solution

import (
	"reflect"
	"testing"
)

func TestReorderList(t *testing.T) {
	head := buildList([]int{1, 2, 3, 4})
	ReorderList(head)
	got := listToSlice(head)
	want := []int{1, 4, 2, 3}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("ReorderList() = %v, want %v", got, want)
	}
}
