package solution

import "testing"

func TestClimbStairs(t *testing.T) {
	if got := ClimbStairs(3); got != 3 {
		t.Errorf("ClimbStairs(3) = %d, want 3", got)
	}
}
