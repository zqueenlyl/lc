package solution

import (
	"reflect"
	"testing"
)

func TestTwoSum(t *testing.T) {
	got := TwoSum([]int{2, 7, 11, 15}, 9)
	want := []int{0, 1}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("TwoSum() = %v, want %v", got, want)
	}
}
