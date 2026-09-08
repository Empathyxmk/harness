package public_tests

import (
	"math"
	"testing"
)

func stretchFlow(flow []float64, n int, modifier func(float64) float64) []float64 {
	length := len(flow)
	result := make([]float64, n)
	if length == 1 {
		for i := range result {
			result[i] = modifier(flow[0])
		}
		return result
	}
	for i := 0; i < n; i++ {
		ix := float64(i) * float64(length-1) / float64(n-1)
		lo := int(math.Floor(ix))
		hi := int(math.Ceil(ix))
		f := ix - float64(lo)
		v := (1-f)*flow[lo] + f*flow[hi]
		result[i] = modifier(v)
	}
	return result
}
func reduceFlow(flow []float64, n int) []float64 {
	result := make([]float64, n)
	chunk := float64(len(flow)) / float64(n)
	for i := 0; i < n; i++ {
		start := int(math.Round(float64(i) * chunk))
		end := int(math.Round(float64(i+1) * chunk))
		if end > len(flow) {
			end = len(flow)
		}
		sum := 0.0
		for j := start; j < end; j++ {
			sum += flow[j]
		}
		if end > start {
			result[i] = sum / float64(end-start)
		}
	}
	return result
}
func sum(array []float64) float64 {
	s := 0.0
	for _, v := range array {
		s += v
	}
	return s
}
func average(array []float64) float64 {
	return sum(array) / float64(len(array))
}
func assertArrayEquals(t *testing.T, expected, actual []float64, delta float64) {
	if len(expected) != len(actual) {
		t.Fatalf("Arrays differ in length: %d vs %d", len(expected), len(actual))
	}
	for i := range expected {
		if math.Abs(expected[i]-actual[i]) > delta {
			t.Errorf("Array mismatch at %d: expected %v got %v", i, expected[i], actual[i])
		}
	}
}
func assertArraySum(t *testing.T, expected float64, actual []float64, delta float64) {
	got := sum(actual)
	if math.Abs(expected-got) > delta {
		t.Errorf("Sum mismatch: expected %f, got %f (allow delta %f)", expected, got, delta)
	}
}

func TestStretchFlow2to6(t *testing.T) {
	flow := []float64{2, 4}
	result := stretchFlow(flow, 6, func(v float64) float64 { return v })
	expect := []float64{2.0, 2.4, 2.8, 3.2, 3.6, 4.0}
	assertArrayEquals(t, expect, result, 1e-5)
	assertArraySum(t, average(flow)*6, result, 1e-5)
}
func TestStretchFlow2to11(t *testing.T) {
	flow := []float64{2}
	result := stretchFlow(flow, 11, func(v float64) float64 { return v })
	expect := []float64{2,2,2,2,2,2,2,2,2,2,2}
	assertArrayEquals(t, expect, result, 1e-5)
	assertArraySum(t, average(flow)*11, result, 1e-5)
}
func TestStretchFlow4to8(t *testing.T) {
	flow := []float64{1, 3, 5, 7}
	result := stretchFlow(flow, 8, func(v float64) float64 { return v })
	expect := []float64{1.0, 1.75, 2.5, 3.25, 4.0, 4.75, 5.5, 7.0}
	assertArrayEquals(t, expect, result, 1e-5)
	assertArraySum(t, average(flow)*8, result, 1e-5)
}
func TestStretchFlow4to8WithModifier(t *testing.T) {
	flow := []float64{1, 3, 5, 7}
	mod := func(x float64) float64 { return x * 3 }
	result := stretchFlow(flow, 8, mod)
	expect := []float64{3.0, 5.25, 7.5, 9.75, 12.0, 14.25, 16.5, 21.0}
	assertArrayEquals(t, expect, result, 1e-5)
	assertArraySum(t, average(flow)*3*8, result, 1e-5)
}
func TestStretchFlow2to7WithModifier(t *testing.T) {
	flow := []float64{2, 5}
	mod := math.Round
	result := stretchFlow(flow, 7, mod)
	expect := []float64{2,2,3,3,4,4,5}
	assertArrayEquals(t, expect, result, 1e-5)
}
func TestStretchFlow3to7(t *testing.T) {
	flow := []float64{1, 4, 7}
	result := stretchFlow(flow, 7, func(v float64) float64 { return v })
	expect := []float64{1.0, 1.5, 2.0, 3.0, 4.0, 5.5, 7.0}
	assertArrayEquals(t, expect, result, 1e-5)
	assertArraySum(t, average(flow)*7, result, 1e-5)
}
func TestStretchFlow3to9(t *testing.T) {
	flow := []float64{1, 3, 5}
	result := stretchFlow(flow, 9, func(v float64) float64 { return v })
	expect := []float64{1.0, 1.25, 1.5, 1.75, 2.0, 2.75, 3.5, 4.25, 5.0}
	assertArrayEquals(t, expect, result, 1e-5)
	assertArraySum(t, average(flow)*9, result, 1e-5)
}
func TestStretchFlow4to12(t *testing.T) {
	flow := []float64{1.2, 3.4, 5.6, 7.8}
	result := stretchFlow(flow, 12, func(v float64) float64 { return v })
	expect := []float64{1.2,1.45,1.7,2.25,2.8,3.35,3.9,4.45,5.0,5.55,6.1,7.8}
	assertArrayEquals(t, expect, result, 1e-5)
	assertArraySum(t, average(flow)*12, result, 1e-5)
}
func TestReduceFlow6to2(t *testing.T) {
	flow := []float64{3, 1, 5, 9, 2, 12}
	result := reduceFlow(flow, 2)
	expect := []float64{5.0, 7.0}
	assertArrayEquals(t, expect, result, 1e-5)
	assertArraySum(t, average(flow)*2, result, 1e-5)
}
func TestReduceFlow7to2(t *testing.T) {
	flow := []float64{10, 8, 6, 4, 2, 12, 14}
	result := reduceFlow(flow, 2)
	expect := []float64{6.0, 11.0}
	assertArrayEquals(t, expect, result, 1e-5)
	assertArraySum(t, average(flow)*2, result, 1e-5)
}
func TestReduceFlow12to3(t *testing.T) {
	flow := []float64{12,8,4,12,16,20,24,24,8,8,8,8}
	result := reduceFlow(flow, 3)
	expect := []float64{9.0, 20.0, 8.0}
	assertArrayEquals(t, expect, result, 1e-5)
	assertArraySum(t, average(flow)*3, result, 1e-5)
}