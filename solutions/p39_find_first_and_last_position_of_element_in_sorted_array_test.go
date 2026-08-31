package solution

import (
	"reflect"
	"testing"
)

func TestSearchRange(t *testing.T) {
	cases := []struct {
		nums   []int
		target int
		want   []int
	}{
		{[]int{5, 7, 7, 8, 8, 10}, 8, []int{3, 4}},
		{[]int{5, 7, 7, 8, 8, 10}, 6, []int{-1, -1}},
	}
	for _, c := range cases {
		if got := SearchRange(c.nums, c.target); !reflect.DeepEqual(got, c.want) {
			t.Errorf("SearchRange(%v, %d) = %v, want %v", c.nums, c.target, got, c.want)
		}
	}
}
