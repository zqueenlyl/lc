package solution

import (
	"reflect"
	"testing"
)

func TestMerge(t *testing.T) {
	got := Merge([][]int{{1, 3}, {2, 6}, {8, 10}, {15, 18}})
	want := [][]int{{1, 6}, {8, 10}, {15, 18}}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("Merge() = %v, want %v", got, want)
	}
}
