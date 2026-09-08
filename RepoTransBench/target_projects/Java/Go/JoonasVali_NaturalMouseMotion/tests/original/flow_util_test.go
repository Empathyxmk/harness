package original

import (
	"math"
	"testing"
)

// Simulate FlowUtil with only minimal stretchFlow and reduceFlow logic for test
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

func average(array []float64) float64 {
	sum := 0.0
	for _, v := range array {
		sum += v
	}
	return sum / float64(len(array))
}

func sum(array []float64) float64 {
	s := 0.0
	for _, v := range array {
		s += v
	}
	return s
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

func TestStretchFlow3to9(t *testing.T) {
	flow := []float64{1, 2, 3}
	result := stretchFlow(flow, 9, func(v float64) float64 { return v })
	expect := []float64{1, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0}
	assertArrayEquals(t, expect, result, 1e-5)
	assertArraySum(t, average(flow)*9, result, 1e-5)
}

func TestStretchFlow1to9(t *testing.T) {
	flow := []float64{1}
	result := stretchFlow(flow, 9, func(v float64) float64 { return v })
	expect := []float64{1, 1, 1, 1, 1, 1, 1, 1, 1}
	assertArrayEquals(t, expect, result, 1e-5)
	assertArraySum(t, average(flow)*9, result, 1e-5)
}

func TestStretchFlow3to5(t *testing.T) {
	flow := []float64{1, 2, 3}
	result := stretchFlow(flow, 5, func(v float64) float64 { return v })
	expect := []float64{1.0, 1.5, 2.0, 2.5, 3}
	assertArrayEquals(t, expect, result, 1e-5)
	assertArraySum(t, average(flow)*5, result, 1e-5)
}

func TestStretchFlow3to5WithModifier(t *testing.T) {
	flow := []float64{1, 2, 3}
	mod := func(x float64) float64 { return x * 2 }
	result := stretchFlow(flow, 5, mod)
	expect := []float64{2.0, 3.0, 4.0, 5.0, 6.0}
	assertArrayEquals(t, expect, result, 1e-5)
	assertArraySum(t, average(flow)*2*5, result, 1e-5)
}

func TestStretchFlow3to6WithModifier(t *testing.T) {
	flow := []float64{1, 2, 3}
	mod := math.Floor
	result := stretchFlow(flow, 6, mod)
	expect := []float64{1, 1, 1, 2, 2, 2}
	assertArrayEquals(t, expect, result, 1e-5)
}

func TestStretchFlow2to9(t *testing.T) {
	flow := []float64{1, 2}
	result := stretchFlow(flow, 9, func(v float64) float64 { return v })
	expect := []float64{1.0, 1.125, 1.25, 1.375, 1.5, 1.625, 1.75, 1.875, 2.0}
	assertArrayEquals(t, expect, result, 1e-5)
	assertArraySum(t, average(flow)*9, result, 1e-5)
}

func TestStretchFlow2to8(t *testing.T) {
	flow := []float64{1, 2}
	result := stretchFlow(flow, 8, func(v float64) float64 { return v })
	expect := []float64{1.0, 1.142857, 1.285714, 1.428571, 1.571428, 1.714285, 1.857142, 2.0}
	assertArrayEquals(t, expect, result, 1e-5)
	assertArraySum(t, average(flow)*8, result, 1e-5)
}

func TestStretchFlow3to6(t *testing.T) {
	flow := []float64{1, 2, 3}
	result := stretchFlow(flow, 6, func(v float64) float64 { return v })
	expect := []float64{1.047619, 1.428571, 1.809523, 2.190476, 2.571428, 2.952380}
	assertArrayEquals(t, expect, result, 1e-5)
	assertArraySum(t, average(flow)*6, result, 1e-5)
}

func TestStretchFlow3to18(t *testing.T) {
	flow := []float64{1.1, 1.2, 1.3}
	result := stretchFlow(flow, 18, func(v float64) float64 { return v })
	expect := []float64{
		1.102795, 1.113978, 1.125161, 1.136774,
		1.148602, 1.159784, 1.170967, 1.183010,
		1.194408, 1.205591, 1.216989, 1.229032,
		1.240215, 1.251397, 1.263225, 1.274838,
		1.286021, 1.297204}
	assertArrayEquals(t, expect, result, 1e-5)
	assertArraySum(t, average(flow)*18, result, 1e-5)
}

func TestReduceFlow5to3(t *testing.T) {
	flow := []float64{1, 1.5, 2, 2.5, 3}
	result := reduceFlow(flow, 3)
	expect := []float64{1.2, 2, 2.8}
	assertArrayEquals(t, expect, result, 1e-5)
	assertArraySum(t, average(flow)*3, result, 1e-5)
}

func TestReduceFlow10to3(t *testing.T) {
	flow := []float64{5, 5, 4, 4, 3, 3, 2, 2, 1, 1}
	result := reduceFlow(flow, 3)
	expect := []float64{4.6, 3.0, 1.4}
	assertArrayEquals(t, expect, result, 1e-5)
	assertArraySum(t, average(flow)*3, result, 1e-5)
}

func TestReduceFlow10to1(t *testing.T) {
	flow := []float64{5, 5, 4, 4, 3, 3, 2, 2, 1, 1}
	result := reduceFlow(flow, 1)
	expect := []float64{3.0}
	assertArrayEquals(t, expect, result, 1e-5)
	assertArraySum(t, average(flow)*1, result, 1e-5)
}