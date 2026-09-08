package public_tests

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

func TestPublicCalculatePerplexityAllZeroes(t *testing.T) {
	tokenLogprobs := []float64{0, 0, 0}
	result := betterprompt.CalculatePerplexity(tokenLogprobs)
	if math.Abs(result-1.0) > 1e-8 {
		t.Errorf("Perplexity for all 0 should be 1, got %v", result)
	}
}

func TestPublicCalculatePerplexityPositiveAndNegative(t *testing.T) {
	tokenLogprobs := []float64{1, -1, -2, 2}
	expected := math.Exp(-sum(tokenLogprobs)/float64(len(tokenLogprobs)))
	actual := betterprompt.CalculatePerplexity(tokenLogprobs)
	if math.Abs(actual-expected) >= 1e-8 {
		t.Errorf("Expected %v, got %v", expected, actual)
	}
}

func TestPublicCalculatePerplexityEmptyList(t *testing.T) {
	result := betterprompt.CalculatePerplexity([]float64{})
	if !math.IsInf(result, 1) && !math.IsInf(result, -1) {
		t.Errorf("Expected Inf for empty input, got: %v", result)
	}
}

func TestPublicCalculatePerplexityLarge(t *testing.T) {
	tokenLogprobs := []float64{10, 12, 15}
	expected := math.Exp(-sum(tokenLogprobs)/float64(len(tokenLogprobs)))
	actual := betterprompt.CalculatePerplexity(tokenLogprobs)
	if math.Abs(actual-expected) >= 1e-8 {
		t.Errorf("Expected %v, got %v", expected, actual)
	}
}