package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"

	"shekhargulati_30_seconds_of_java"
	"shekhargulati_30_seconds_of_java/tests"
)

func TestGcdWithArrayOfZerosIsZero_Public(t *testing.T) {
	got := shekhargulati_30_seconds_of_java.GCD([]int{0, 0, 0})
	assert.Equal(t, 0, got)
}

func TestLcmWithSingleElementArrayIsValueItself_Public(t *testing.T) {
	got := shekhargulati_30_seconds_of_java.LCM([]int{99})
	assert.Equal(t, 99, got)
}

func TestArrayMaxWithNegativeNumbersReturnsMax_Public(t *testing.T) {
	got := shekhargulati_30_seconds_of_java.ArrayMax([]int{-9, -2, -17})
	assert.Equal(t, -2, got)
}

func TestArrayMinWithAllEqualNumbersReturnsThatNumber_Public(t *testing.T) {
	got := shekhargulati_30_seconds_of_java.ArrayMin([]int{7, 7, 7})
	assert.Equal(t, 7, got)
}

func TestChunkEmptyArrayReturnsEmptyResult_Public(t *testing.T) {
	chunks := shekhargulati_30_seconds_of_java.Chunk([]int{}, 5)
	assert.Empty(t, chunks)
}

func TestCountOccurrencesNoMatchingValuesReturnsZero_Public(t *testing.T) {
	got := shekhargulati_30_seconds_of_java.CountOccurrences([]int{8, 9, 10}, 5)
	assert.Equal(t, int64(0), got)
}

func TestDeepFlattenEmptyArrayReturnsEmptyArray_Public(t *testing.T) {
	got := shekhargulati_30_seconds_of_java.DeepFlatten([]interface{}{})
	assert.Empty(t, got)
}

func TestDifferenceWithFirstArrayEmptyReturnsEmpty_Public(t *testing.T) {
	got := shekhargulati_30_seconds_of_java.Difference([]int{}, []int{2, 3})
	assert.Empty(t, got)
}

func TestDifferenceWithSecondArrayEmptyReturnsFirstArray_Public(t *testing.T) {
	got := shekhargulati_30_seconds_of_java.Difference([]int{4, 5, 6}, []int{})
	assert.True(t, tests.IntSlicesEqual(got, []int{4, 5, 6}))
}

// ... Additional edge public tests as in original source