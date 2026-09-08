package public_tests

import "testing"

// Simulate barh.barh(y, x)
func Barh(y, x []int) {
	_ = y
	_ = x
}

func TestSimpleBarhDifferentData(t *testing.T) {
	y := []int{6, 1, 4}
	x := []int{7, 8, 9}
	Barh(y, x)
}