package solution

import "testing"

func TestMaxArea(t *testing.T) {
	if got := MaxArea([]int{1, 8, 6, 2, 5, 4, 8, 3, 7}); got != 49 {
		t.Errorf("MaxArea() = %d, want 49", got)
	}
}
