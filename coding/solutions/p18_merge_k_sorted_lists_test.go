package solution

import (
	"reflect"
	"testing"
)

func TestMergeKLists(t *testing.T) {
	lists := []*ListNode{
		buildList([]int{1, 4, 5}),
		buildList([]int{1, 3, 4}),
		buildList([]int{2, 6}),
	}
	got := listToSlice(MergeKLists(lists))
	want := []int{1, 1, 2, 3, 4, 4, 5, 6}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("MergeKLists() = %v, want %v", got, want)
	}
}
