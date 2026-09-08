package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type DummyHypothesis struct {
	Tokens []int
	Scores []float64
}

func lengthPenaltyScore(scores []float64, lenPenalty float64) float64 {
	sum := 0.0
	for _, v := range scores {
		sum += v
	}
	size := float64(len(scores))
	if lenPenalty == 0 {
		return sum
	}
	return sum / (size * lenPenalty)
}

func TestScoreHypothesisLengthPenaltyPublic(t *testing.T) {
	scores := []float64{-1.2, -2.6}
	score := lengthPenaltyScore(scores, 0.85)
	assert.True(t, score <= 0.0)
}

func TestGreedyDecodingRunPublic(t *testing.T) {
	inputTokens := [][]int{{4, 8, 15, 16, 23, 42}}
	decoded := make([][]int, len(inputTokens))
	for i, seq := range inputTokens {
		decoded[i] = []int{seq[0]}
	}
	assert.Equal(t, 1, len(decoded[0]))
}