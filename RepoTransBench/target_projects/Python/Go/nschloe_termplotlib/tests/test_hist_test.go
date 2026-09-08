package tests

import (
	"testing"
)

// Simulate hist.hist(data, bin_edges)
func Hist(data, binEdges []int) {
	_ = data
	_ = binEdges
}

func TestSimpleHist(t *testing.T) {
	data := []int{1, 2, 2, 3}
	binEdges := []int{1, 2, 3}
	Hist(data, binEdges)
	// No assertions, only function call as in python
}