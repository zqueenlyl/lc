package solution

import "testing"

func TestRob(t *testing.T) {
	if got := Rob([]int{1, 2, 3, 1}); got != 4 {
		t.Errorf("Rob() = %d, want 4", got)
	}
}
