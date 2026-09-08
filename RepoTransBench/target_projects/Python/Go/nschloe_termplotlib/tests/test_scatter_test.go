package tests

import (
	"testing"
)

// Simulate scatter using plot.plot(y, x), as per original comment
func PlotScatter(y, x []int) {
	_ = y
	_ = x
}

func TestSimpleScatter(t *testing.T) {
	x := []int{1, 2, 3}
	y := []int{3, 2, 1}
	PlotScatter(y, x)
}