package solution

import "testing"

func TestIsMatch(t *testing.T) {
	cases := []struct {
		s, p string
		want bool
	}{
		{"aab", "c*a*b", true},
		{"mississippi", "mis*is*p*.", false},
	}
	for _, c := range cases {
		if got := IsMatch(c.s, c.p); got != c.want {
			t.Errorf("IsMatch(%q, %q) = %v, want %v", c.s, c.p, got, c.want)
		}
	}
}
