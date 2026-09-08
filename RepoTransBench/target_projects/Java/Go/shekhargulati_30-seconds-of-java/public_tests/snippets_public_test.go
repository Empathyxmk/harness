package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"

	"shekhargulati_30_seconds_of_java"
	"shekhargulati_30_seconds_of_java/tests"
)

func TestGcdOfArrayContaining6_9_15Is3(t *testing.T) {
	got := shekhargulati_30_seconds_of_java.GCD([]int{6, 9, 15})
	assert.Equal(t, 3, got)
}

func TestGcdOfArrayContaining14_28_56Is14(t *testing.T) {
	got := shekhargulati_30_seconds_of_java.GCD([]int{14, 28, 56})
	assert.Equal(t, 14, got)
}

func TestLcmOfArrayContaining2_3_7Is42(t *testing.T) {
	got := shekhargulati_30_seconds_of_java.LCM([]int{2, 3, 7})
	assert.Equal(t, 42, got)
}

func TestLcmOfArrayContaining5_10_20Is20(t *testing.T) {
	got := shekhargulati_30_seconds_of_java.LCM([]int{5, 10, 20})
	assert.Equal(t, 20, got)
}

func TestMaxOfArrayContaining4_8_6Is8(t *testing.T) {
	got := shekhargulati_30_seconds_of_java.ArrayMax([]int{4, 8, 6})
	assert.Equal(t, 8, got)
}

func TestMinOfArrayContaining17_8_25Is8(t *testing.T) {
	got := shekhargulati_30_seconds_of_java.ArrayMin([]int{17, 8, 25})
	assert.Equal(t, 8, got)
}

func TestChunkBreaksInputArrayWithSize3(t *testing.T) {
	chunks := shekhargulati_30_seconds_of_java.Chunk([]int{10, 20, 30, 40, 50, 60, 70}, 3)
	assert.True(t, tests.IntSlicesOfSlicesEqual(chunks, [][]int{{10, 20, 30}, {40, 50, 60}, {70}}))
}

func TestChunkBreaksInputArrayEvenlyWithSize4(t *testing.T) {
	chunks := shekhargulati_30_seconds_of_java.Chunk([]int{2, 4, 6, 8, 10, 12, 14, 16}, 4)
	assert.True(t, tests.IntSlicesOfSlicesEqual(chunks, [][]int{{2, 4, 6, 8}, {10, 12, 14, 16}}))
}

func TestCountOccurrencesCountsOccurrencesOfValue5(t *testing.T) {
	got := shekhargulati_30_seconds_of_java.CountOccurrences([]int{5, 3, 5, 2, 5, 6}, 5)
	assert.Equal(t, int64(3), got)
}

func TestDeepFlattenFlattensVariedNestedArray(t *testing.T) {
	in := []interface{}{7, []interface{}{8, []interface{}{9, 10}}, 11}
	got := shekhargulati_30_seconds_of_java.DeepFlatten(in)
	assert.True(t, tests.IntSlicesEqual(got, []int{7, 8, 9, 10, 11}))
}

func TestDifferenceBetweenArray_9_8_7And_7_8_5Is9(t *testing.T) {
	got := shekhargulati_30_seconds_of_java.Difference([]int{9, 8, 7}, []int{7, 8, 5})
	assert.True(t, tests.IntSlicesEqual(got, []int{9}))
}

// ... Additional public tests for other methods as necessary, if more are needed