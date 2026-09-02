package solution

import "testing"

func TestLRUCache(t *testing.T) {
	c := NewLRUCache(2)
	c.Put(1, 1)
	c.Put(2, 2)
	if got := c.Get(1); got != 1 {
		t.Errorf("Get(1) = %d, want 1", got)
	}
	c.Put(3, 3) // 淘汰 key 2
	if got := c.Get(2); got != -1 {
		t.Errorf("Get(2) = %d, want -1", got)
	}
	c.Put(4, 4) // 淘汰 key 1
	if got := c.Get(1); got != -1 {
		t.Errorf("Get(1) = %d, want -1", got)
	}
	if got := c.Get(3); got != 3 {
		t.Errorf("Get(3) = %d, want 3", got)
	}
	if got := c.Get(4); got != 4 {
		t.Errorf("Get(4) = %d, want 4", got)
	}
}
