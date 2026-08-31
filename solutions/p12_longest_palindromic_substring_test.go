package solution

import "testing"

func TestLongestPalindrome(t *testing.T) {
	// "babad" 的最长回文可为 "bab" 或 "aba"。
	if got := LongestPalindrome("babad"); got != "bab" && got != "aba" {
		t.Errorf("LongestPalindrome(%q) = %q, want \"bab\" or \"aba\"", "babad", got)
	}
	if got := LongestPalindrome("cbbd"); got != "bb" {
		t.Errorf("LongestPalindrome(%q) = %q, want \"bb\"", "cbbd", got)
	}
}
