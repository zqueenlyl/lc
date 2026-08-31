package solution

import "testing"

func TestUniquePaths(t *testing.T) {
	if got := UniquePaths(3, 7); got != 28 {
		t.Errorf("UniquePaths(3, 7) = %d, want 28", got)
	}
}
