package solution

import (
	"reflect"
	"testing"
)

func TestMergeTwoLists(t *testing.T) {
	l1 := buildList([]int{1, 2, 4})
	l2 := buildList([]int{1, 3, 4})
	got := listToSlice(MergeTwoLists(l1, l2))
	want := []int{1, 1, 2, 3, 4, 4}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("MergeTwoLists() = %v, want %v", got, want)
	}
}
