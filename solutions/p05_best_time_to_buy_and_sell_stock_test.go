package solution

import "testing"

func TestMaxProfit(t *testing.T) {
	if got := MaxProfit([]int{7, 1, 5, 3, 6, 4}); got != 5 {
		t.Errorf("MaxProfit() = %d, want 5", got)
	}
}
