package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"lafan1/extract"
)

func TestExtractFuncIdentityPublic(t *testing.T) {
	data := []int{10, 12, 11, 8}
	identity := func(x int) int { return x }
	result := extract.FilterMap(identity, data)
	assert.Equal(t, data, result)
}

func TestFilterMapAppliesFunctionPublic(t *testing.T) {
	result := extract.FilterMap(func(x int) int { return x * 2 }, []int{5, 0, 2})
	assert.Equal(t, []int{10, 0, 4}, result)
}

func TestSplitByLenMultipleCasesPublic(t *testing.T) {
	seqs := [][]int{{0, 0, 0, 3}, {7, 8}, {10}}
	out := extract.SplitByLen(seqs, 3)
	assert.Equal(t, [][2][]int{
		{[]int{0, 0, 0}, []int{3}},
		{[]int{7, 8}, []int{}},
		{[]int{10}, []int{}},
	}, out)
}

func TestSplitByLenAllShorterPublic(t *testing.T) {
	seqs := [][]int{{-1}, {0}, {1}}
	out := extract.SplitByLen(seqs, 3)
	assert.Equal(t, [][2][]int{
		{[]int{-1}, []int{}},
		{[]int{0}, []int{}},
		{[]int{1}, []int{}},
	}, out)
}

func TestPadOrTrimPublic(t *testing.T) {
	arr := []int{9}
	desired := 4
	padded := extract.PadOrTrim(arr, desired, -1)
	assert.Equal(t, []int{9, -1, -1, -1}, padded)
	trimmed := extract.PadOrTrim([]int{7, 1, 3, 8, 6}, 2, 99)
	assert.Equal(t, []int{7, 1}, trimmed)
}

func TestUnpadPublic(t *testing.T) {
	arr := []int{2, 3, 0, 0}
	out := extract.Unpad(arr, 0)
	assert.Equal(t, []int{2, 3}, out)
	arr2 := []int{4, 4, 4, 0}
	out2 := extract.Unpad(arr2, 0)
	assert.Equal(t, []int{4, 4, 4}, out2)
}

func TestFilterMapEmptyDataPublic(t *testing.T) {
	f := func(x int) int { return 0 }
	out := extract.FilterMap(f, []int{})
	assert.Empty(t, out)
}