package public_tests

import "testing"

// Simulate hist.hist
func Hist(data []int, param interface{}, opts ...map[string]interface{}) {
	// param could be bins or bin_edges, as per usage
	_ = data
	_ = param
	_ = opts
}

func TestSimpleHistDiffData(t *testing.T) {
	data := []int{3, 6, 9, 3, 6, 9, 9}
	Hist(data, 3)
}

func TestHistLabelAndAscii(t *testing.T) {
	data := []int{7, 1, 6, 8, 7, 5, 5}
	Hist(data, 2, map[string]interface{}{
		"title":  "New Title",
		"xlabel": "Alternate X",
		"ylabel": "Alternate Y",
		"grid":   true,
		"ascii":  true,
	})
}