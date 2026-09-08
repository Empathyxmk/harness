package public_tests

import (
	"errors"
	"math"
	"testing"
)

// These utility functions simulate Utils in original code.
// If the input is empty or contains nil, exceptions are simulated with panics.

func normalizeProbabilities(probs map[string]float64) map[string]float64 {
	if len(probs) == 0 {
		panic("IllegalArgumentException: map is empty")
	}
	var sum float64
	for _, v := range probs {
		if math.IsNaN(v) {
			panic("NullPointerException: map contains nil/NaN value")
		}
		sum += v
	}
	if sum == 0.0 {
		panic("IllegalArgumentException: sum is zero")
	}
	result := make(map[string]float64)
	for k, v := range probs {
		result[k] = v / sum
	}
	return result
}

func sumSlice(vals []float64) float64 {
	res := 0.0
	for _, v := range vals {
		res += v
	}
	return res
}

// log2 returns log-base-2 with error for <=0
func log2(x float64) float64 {
	if x <= 0 {
		panic("IllegalArgumentException: x <= 0")
	}
	return math.Log2(x)
}

// logSumExp for slice
func logSumExpSlice(vals []float64) float64 {
	if len(vals) == 0 {
		return -math.MaxFloat64
	}
	m := vals[0]
	for _, v := range vals {
		if v > m {
			m = v
		}
	}
	var sum float64
	for _, v := range vals {
		sum += math.Exp(v - m)
	}
	return m + math.Log(sum)
}

func logSumExpArray(vals []float64) float64 {
	// identical to Slice version
	return logSumExpSlice(vals)
}

func TestNormalizeProbabilitiesDifferent(t *testing.T) {
	probs := map[string]float64{"orange": 4.0, "banana": 6.0}
	norm := normalizeProbabilities(probs)
	if math.Abs(norm["orange"]-0.4) > 1e-10 {
		t.Errorf("Expected 0.4, got %v", norm["orange"])
	}
	if math.Abs(norm["banana"]-0.6) > 1e-10 {
		t.Errorf("Expected 0.6, got %v", norm["banana"])
	}
	if math.Abs(probs["orange"]-4.0) > 1e-10 {
		t.Errorf("Original should not be modified")
	}
	if math.Abs(probs["banana"]-6.0) > 1e-10 {
		t.Errorf("Original should not be modified")
	}
}

func TestNormalizeEmptyDifferent(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for empty map")
		}
	}()
	normalizeProbabilities(map[string]float64{})
}

func TestNormalizeNullValueDifferent(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for nil/NaN value in map")
		}
	}()
	p := map[string]float64{"something": math.NaN()}
	normalizeProbabilities(p)
}

func TestSumDifferentValues(t *testing.T) {
	vals := []float64{2.5, 3.0, 7.5}
	if sumSlice(vals) != 13.0 {
		t.Errorf("Expected sum 13.0, got %v", sumSlice(vals))
	}
}

func TestLog2DifferentInputs(t *testing.T) {
	cases := []struct {
		x, want float64
	}{
		{2.0, 1.0},
		{4.0, 2.0},
		{1.0, 0.0},
	}
	for _, c := range cases {
		if math.Abs(log2(c.x)-c.want) > 1e-10 {
			t.Errorf("log2(%v): got %v, want %v", c.x, log2(c.x), c.want)
		}
	}
}

func TestLog2ZeroDifferent(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for log2(0)")
		}
	}()
	log2(0.0)
}

func TestLog2NegativeDifferent(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for log2(-2)")
		}
	}()
	log2(-2.0)
}

func TestLogSumExpListDifferent(t *testing.T) {
	d := []float64{math.Log(2.0), math.Log(10.0)}
	expected := math.Log(2.0 + 10.0)
	if math.Abs(logSumExpSlice(d)-expected) > 1e-10 {
		t.Errorf("logSumExpSlice: got %v, want %v", logSumExpSlice(d), expected)
	}
}

func TestLogSumExpArrayDifferent(t *testing.T) {
	arr := []float64{math.Log(5), math.Log(3)}
	expected := math.Log(5.0 + 3.0)
	if math.Abs(logSumExpArray(arr)-expected) > 1e-10 {
		t.Errorf("logSumExpArray: got %v, want %v", logSumExpArray(arr), expected)
	}
}