package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
	"shekhargulati_30_seconds_of_java/tests"
	"shekhargulati_30_seconds_of_java"
)

func TestGcdWithArrayOfZerosIsZero(t *testing.T) {
	got := shekhargulati_30_seconds_of_java.GCD([]int{0, 0, 0})
	assert.Equal(t, 0, got)
}

func TestLcmWithSingleElementArrayIsValueItself(t *testing.T) {
	got := shekhargulati_30_seconds_of_java.LCM([]int{42})
	assert.Equal(t, 42, got)
}

func TestArrayMaxWithNegativeNumbersReturnsMax(t *testing.T) {
	got := shekhargulati_30_seconds_of_java.ArrayMax([]int{-5, -1, -12})
	assert.Equal(t, -1, got)
}

func TestArrayMinWithAllEqualNumbersReturnsThatNumber(t *testing.T) {
	got := shekhargulati_30_seconds_of_java.ArrayMin([]int{3, 3, 3})
	assert.Equal(t, 3, got)
}

func TestChunkEmptyArrayReturnsEmptyResult(t *testing.T) {
	chunks := shekhargulati_30_seconds_of_java.Chunk([]int{}, 3)
	assert.Empty(t, chunks)
}

func TestCountOccurrencesNoMatchingValuesReturnsZero(t *testing.T) {
	got := shekhargulati_30_seconds_of_java.CountOccurrences([]int{7, 8, 9}, 5)
	assert.Equal(t, int64(0), got)
}

func TestDeepFlattenEmptyArrayReturnsEmptyArray(t *testing.T) {
	got := shekhargulati_30_seconds_of_java.DeepFlatten([]interface{}{})
	assert.Empty(t, got)
}

func TestDifferenceWithFirstArrayEmptyReturnsEmpty(t *testing.T) {
	got := shekhargulati_30_seconds_of_java.Difference([]int{}, []int{1, 2})
	assert.Empty(t, got)
}

func TestDifferenceWithSecondArrayEmptyReturnsFirstArray(t *testing.T) {
	got := shekhargulati_30_seconds_of_java.Difference([]int{2, 3, 4}, []int{})
	assert.True(t, tests.IntSlicesEqual(got, []int{2, 3, 4}))
}

// ... Additional edge tests as necessary.