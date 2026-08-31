package solution

import "testing"

func TestSearchMatrix(t *testing.T) {
	matrix := [][]int{
		{1, 3, 5, 7},
		{10, 11, 16, 20},
		{23, 30, 34, 60},
	}
	cases := []struct {
		target int
		want   bool
	}{
		{3, true},
		{13, false},
	}
	for _, c := range cases {
		if got := SearchMatrix(matrix, c.target); got != c.want {
			t.Errorf("SearchMatrix(matrix, %d) = %v, want %v", c.target, got, c.want)
		}
	}
}
