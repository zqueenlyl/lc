package solution

import (
	"reflect"
	"testing"
)

func TestSortArray(t *testing.T) {
	got := SortArray([]int{5, 2, 3, 1})
	want := []int{1, 2, 3, 5}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("SortArray() = %v, want %v", got, want)
	}
}
