package tests

import (
	"testing"
)

// Simulate plot.plot(y, x)
func Plot(y, x []int) {
	_ = y
	_ = x
}

func TestSimplePlot(t *testing.T) {
	y := []int{2, 3, 1}
	x := []int{1, 2, 3}
	Plot(y, x)
	// No assertions
}