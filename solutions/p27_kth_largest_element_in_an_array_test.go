package solution

import "testing"

func TestFindKthLargest(t *testing.T) {
	if got := FindKthLargest([]int{3, 2, 1, 5, 6, 4}, 2); got != 5 {
		t.Errorf("FindKthLargest() = %d, want 5", got)
	}
}
