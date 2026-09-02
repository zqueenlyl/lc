package solution

import "testing"

func TestNumIslands(t *testing.T) {
	grid := [][]byte{
		{'1', '1', '0', '0', '0'},
		{'1', '1', '0', '0', '0'},
		{'0', '0', '1', '0', '0'},
		{'0', '0', '0', '1', '1'},
	}
	if got := NumIslands(grid); got != 3 {
		t.Errorf("NumIslands() = %d, want 3", got)
	}
}
