package original

import (
	"math"
	"testing"

	"betterprompt"
)

func sum(arr []float64) float64 {
	s := 0.0
	for _, v := range arr {
		s += v
	}
	return s
}

func TestCalculatePerplexityAllNone(t *testing.T) {
	// Simulate None in Python with sentinel value -100
	tokenLogprobs := []float64{-100, -100}
	result := betterprompt.CalculatePerplexity(tokenLogprobs)
	if !math.IsFinite(result) {
		t.Errorf("Expected finite, got: %v", result)
	}
}

func TestCalculatePerplexityRegular(t *testing.T) {
	tokenLogprobs := []float64{0, -1, -2}
	expected := math.Exp(-sum(tokenLogprobs) / float64(len(tokenLogprobs)))
	actual := betterprompt.CalculatePerplexity(tokenLogprobs)
	if math.Abs(actual-expected) >= 1e-8 {
		t.Errorf("Expected %v, got %v", expected, actual)
	}
}

func TestCalculatePerplexityEmptyList(t *testing.T) {
	result := betterprompt.CalculatePerplexity([]float64{})
	if !math.IsInf(result, 1) && !math.IsInf(result, -1) {
		t.Errorf("Expected Inf for empty input, got: %v", result)
	}
}

func TestCalculatePerplexityNaN(t *testing.T) {
	result := math.Exp(math.NaN())
	if !math.IsNaN(result) {
		t.Errorf("Expected NaN, got: %v", result)
	}
}