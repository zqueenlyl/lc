package solution

import (
	"reflect"
	"testing"
)

func TestThreeSum(t *testing.T) {
	got := ThreeSum([]int{-1, 0, 1, 2, -1, -4})
	want := [][]int{{-1, -1, 2}, {-1, 0, 1}}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("ThreeSum() = %v, want %v", got, want)
	}
}
