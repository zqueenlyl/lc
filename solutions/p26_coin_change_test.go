package solution

import "testing"

func TestCoinChange(t *testing.T) {
	cases := []struct {
		coins  []int
		amount int
		want   int
	}{
		{[]int{1, 2, 5}, 11, 3},
		{[]int{2}, 3, -1},
	}
	for _, c := range cases {
		if got := CoinChange(c.coins, c.amount); got != c.want {
			t.Errorf("CoinChange(%v, %d) = %d, want %d", c.coins, c.amount, got, c.want)
		}
	}
}
