package solution

import "testing"

func TestLongestCommonPrefix(t *testing.T) {
	cases := []struct {
		strs []string
		want string
	}{
		{[]string{"flower", "flow", "flight"}, "fl"},
		{[]string{"dog", "racecar", "car"}, ""},
	}
	for _, c := range cases {
		if got := LongestCommonPrefix(c.strs); got != c.want {
			t.Errorf("LongestCommonPrefix(%v) = %q, want %q", c.strs, got, c.want)
		}
	}
}
