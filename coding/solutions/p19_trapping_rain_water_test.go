package solution

import "testing"

func TestTrap(t *testing.T) {
	if got := Trap([]int{0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1}); got != 6 {
		t.Errorf("Trap() = %d, want 6", got)
	}
}
