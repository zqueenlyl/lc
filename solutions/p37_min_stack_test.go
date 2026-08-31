package solution

import "testing"

func TestMinStack(t *testing.T) {
	s := NewMinStack()
	s.Push(-2)
	s.Push(0)
	s.Push(-3)
	if got := s.GetMin(); got != -3 {
		t.Errorf("GetMin() = %d, want -3", got)
	}
	s.Pop()
	if got := s.Top(); got != 0 {
		t.Errorf("Top() = %d, want 0", got)
	}
	if got := s.GetMin(); got != -2 {
		t.Errorf("GetMin() = %d, want -2", got)
	}
}
