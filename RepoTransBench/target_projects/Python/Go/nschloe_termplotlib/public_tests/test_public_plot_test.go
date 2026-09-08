package public_tests

import "testing"

// Simulate plot.plot(y, x)
func Plot(y, x []int) {
	_ = y
	_ = x
}

func TestSimplePlotDifferentData(t *testing.T) {
	y := []int{0, 4, 2}
	x := []int{10, 15, 20}
	Plot(y, x)
}