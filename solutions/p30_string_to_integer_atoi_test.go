package solution

import "testing"

func TestMyAtoi(t *testing.T) {
	cases := []struct {
		s    string
		want int
	}{
		{"42", 42},
		{"   -42", -42},
		{"4193 with words", 4193},
	}
	for _, c := range cases {
		if got := MyAtoi(c.s); got != c.want {
			t.Errorf("MyAtoi(%q) = %d, want %d", c.s, got, c.want)
		}
	}
}
