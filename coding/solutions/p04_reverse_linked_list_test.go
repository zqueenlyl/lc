package solution

import (
	"reflect"
	"testing"
)

func TestReverseList(t *testing.T) {
	got := listToSlice(ReverseList(buildList([]int{1, 2, 3, 4, 5})))
	want := []int{5, 4, 3, 2, 1}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("ReverseList() = %v, want %v", got, want)
	}
}
