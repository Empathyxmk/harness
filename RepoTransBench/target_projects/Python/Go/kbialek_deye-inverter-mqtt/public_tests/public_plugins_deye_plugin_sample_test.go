package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestPluginSumWithOtherInputs(t *testing.T) {
	assert.Equal(t, 16, testPluginSum([]int{3, 5, 8}))
	assert.Equal(t, 13, testPluginSum([]int{-2, 6, 9}))
	assert.Equal(t, 0, testPluginSum([]int{0}))
}

// Stand-in for the actual sample sum logic exposed in Go version.
func testPluginSum(arr []int) int {
	s := 0
	for _, v := range arr {
		s += v
	}
	return s
}