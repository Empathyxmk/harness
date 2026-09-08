package public_tests

import "testing"

func PlotScatter(y, x []int) {
	_ = y
	_ = x
}

func TestSimpleScatterDifferentData(t *testing.T) {
	x := []int{4, 5, 6}
	y := []int{6, 5, 4}
	PlotScatter(y, x)
}