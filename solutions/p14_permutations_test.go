package solution

import (
	"fmt"
	"testing"
)

func TestPermute(t *testing.T) {
	got := Permute([]int{1, 2, 3})
	want := map[string]bool{
		"1,2,3": true,
		"1,3,2": true,
		"2,1,3": true,
		"2,3,1": true,
		"3,1,2": true,
		"3,2,1": true,
	}
	if len(got) != len(want) {
		t.Fatalf("Permute() returned %d permutations, want %d", len(got), len(want))
	}
	for _, p := range got {
		key := fmt.Sprintf("%d,%d,%d", p[0], p[1], p[2])
		if !want[key] {
			t.Errorf("Permute() contains unexpected permutation %v", p)
		}
	}
}
