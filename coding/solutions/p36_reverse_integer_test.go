package solution

import "testing"

func TestReverse(t *testing.T) {
	cases := []struct {
		x    int
		want int
	}{
		{123, 321},
		{-120, -21},
	}
	for _, c := range cases {
		if got := Reverse(c.x); got != c.want {
			t.Errorf("Reverse(%d) = %d, want %d", c.x, got, c.want)
		}
	}
}
