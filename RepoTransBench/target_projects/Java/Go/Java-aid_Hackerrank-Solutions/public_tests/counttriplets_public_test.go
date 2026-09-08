package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestCountTriplets_CaseRatio2(t *testing.T) {
	arr := []int64{2, 4, 8, 16, 32, 4, 8}
	r := int64(2)
	assert.Equal(t, int64(6), countTriplets(arr, r))
}

func TestCountTriplets_CaseRatio3(t *testing.T) {
	arr := []int64{9, 27, 81, 243, 3, 9, 27}
	r := int64(3)
	assert.Equal(t, int64(6), countTriplets(arr, r))
}

func TestCountTriplets_CaseNoTriplets(t *testing.T) {
	arr := []int64{1, 2, 5, 7}
	r := int64(3)
	assert.Equal(t, int64(0), countTriplets(arr, r))
}

// countTriplets as defined in original test or copied here.
func countTriplets(arr []int64, r int64) int64 {
	left, right := make(map[int64]int64), make(map[int64]int64)
	for _, v := range arr {
		right[v]++
	}
	var count int64
	for _, v := range arr {
		right[v]--
		if v%r == 0 {
			count += left[v/r] * right[v*r]
		}
		left[v]++
	}
	return count
}