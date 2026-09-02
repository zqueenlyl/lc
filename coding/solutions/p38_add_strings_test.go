package solution

import "testing"

func TestAddStrings(t *testing.T) {
	if got := AddStrings("11", "123"); got != "134" {
		t.Errorf("AddStrings(\"11\", \"123\") = %q, want \"134\"", got)
	}
}
