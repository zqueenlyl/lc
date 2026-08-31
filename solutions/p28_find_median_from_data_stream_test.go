package solution

import "testing"

func TestMedianFinder(t *testing.T) {
	m := NewMedianFinder()
	m.AddNum(1)
	m.AddNum(2)
	if got := m.FindMedian(); got != 1.5 {
		t.Errorf("FindMedian() = %v, want 1.5", got)
	}
	m.AddNum(3)
	if got := m.FindMedian(); got != 2.0 {
		t.Errorf("FindMedian() = %v, want 2.0", got)
	}
}
