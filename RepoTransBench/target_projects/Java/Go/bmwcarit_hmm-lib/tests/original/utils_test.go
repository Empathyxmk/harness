package tests

import (
	"math"
	"testing"
)

func initialHashMapCapacity(n int) int {
	// Expected resizing/load factor match for built-in map + emulating Java's implementation
	return int(float64(n) / 0.75 + 1.0)
}

func logToNonLogProbabilities(logProbs map[string]float64) map[string]float64 {
	out := make(map[string]float64)
	for k, v := range logProbs {
		out[k] = math.Exp(v)
	}
	return out
}

func probabilityInRange(p, tol float64) bool {
	return p >= -tol && p <= 1.0+tol
}

func TestInitialHashMapCapacity(t *testing.T) {
	result := initialHashMapCapacity(10)
	if result != 14 {
		t.Errorf("Expected initialHashMapCapacity(10)==14, got %d", result)
	}
}

func TestLogToNonLogProbabilities(t *testing.T) {
	logProbs := map[string]float64{
		"A": math.Log(0.4),
		"B": math.Log(0.6),
	}
	probs := logToNonLogProbabilities(logProbs)
	if math.Abs(probs["A"]-0.4) > 1e-10 {
		t.Errorf("Expected prob[A]=0.4, got %v", probs["A"])
	}
	if math.Abs(probs["B"]-0.6) > 1e-10 {
		t.Errorf("Expected prob[B]=0.6, got %v", probs["B"])
	}
}

func TestProbabilityInRange(t *testing.T) {
	if !probabilityInRange(1.0, 1e-8) {
		t.Errorf("1.0 should be in range")
	}
	if !probabilityInRange(0.0, 1e-8) {
		t.Errorf("0.0 should be in range")
	}
	if probabilityInRange(-0.01, 1e-4) {
		t.Errorf("-0.01 should not be in range with tol 1e-4")
	}
	if !probabilityInRange(1.000009, 1e-3) {
		t.Errorf("1.000009 should be in range with tol 1e-3")
	}
	if probabilityInRange(1.2, 1e-4) {
		t.Errorf("1.2 should not be in range with tol 1e-4")
	}
}