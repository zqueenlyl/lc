package solution

import "testing"

func TestLengthOfLIS(t *testing.T) {
	if got := LengthOfLIS([]int{10, 9, 2, 5, 3, 7, 101, 18}); got != 4 {
		t.Errorf("LengthOfLIS() = %d, want 4", got)
	}
}
