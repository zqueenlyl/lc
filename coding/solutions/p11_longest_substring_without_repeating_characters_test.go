package solution

import "testing"

func TestLengthOfLongestSubstring(t *testing.T) {
	cases := []struct {
		s    string
		want int
	}{
		{"abcabcbb", 3},
		{"bbbbb", 1},
	}
	for _, c := range cases {
		if got := LengthOfLongestSubstring(c.s); got != c.want {
			t.Errorf("LengthOfLongestSubstring(%q) = %d, want %d", c.s, got, c.want)
		}
	}
}
