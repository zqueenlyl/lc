package solution

import "testing"

func TestSearch(t *testing.T) {
	cases := []struct {
		nums   []int
		target int
		want   int
	}{
		{[]int{4, 5, 6, 7, 0, 1, 2}, 0, 4},  // target 在右半边
		{[]int{4, 5, 6, 7, 0, 1, 2}, 6, 2},  // target 在左半边
		{[]int{4, 5, 6, 7, 0, 1, 2}, 3, -1}, // target 不存在
		{[]int{1, 2, 3, 4, 5}, 1, 0},        // 未旋转
		{[]int{1}, 1, 0},                    // 单元素命中
		{[]int{1}, 2, -1},                   // 单元素未命中
	}
	for _, c := range cases {
		if got := Search(c.nums, c.target); got != c.want {
			t.Errorf("Search(%v, %d) = %d, want %d", c.nums, c.target, got, c.want)
		}
	}
}
