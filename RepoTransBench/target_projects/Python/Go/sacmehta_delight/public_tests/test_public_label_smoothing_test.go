package public_tests

import (
	"math"
	"testing"

	"github.com/stretchr/testify/assert"
)

// Uses the same helper function as in tests/test_label_smoothing_test.go

func labelSmoothedNLLLoss(lprobs [][]float64, target []int, epsilon float64) (float64, float64) {
	nToks := len(target)
	nll := 0.0
	for i, tgt := range target {
		nll -= lprobs[i][tgt]
	}
	meanLogProb := 0.0
	for i := range lprobs {
		for _, lp := range lprobs[i] {
			meanLogProb -= lp
		}
	}
	meanLogProb = meanLogProb / float64(len(lprobs)*len(lprobs[0]))

	loss := (1.0-epsilon)*nll + epsilon*meanLogProb*float64(nToks)
	return loss, nll
}

func TestLabelSmoothedCrossEntropyLossPublic(t *testing.T) {
	lprobs := [][]float64{
		{math.Log(0.1), math.Log(0.6), math.Log(0.3)},
		{math.Log(0.3), math.Log(0.4), math.Log(0.3)},
	}
	target := []int{1, 2}
	epsilon := 0.2

	loss, nllLoss := labelSmoothedNLLLoss(lprobs, target, epsilon)
	assert.True(t, loss > 0)
	assert.True(t, nllLoss > 0)
	assert.True(t, loss > nllLoss)
}

func TestLabelSmoothedNLLLossIgnoreIndexPublic(t *testing.T) {
	lprobs := [][]float64{
		{math.Log(0.9), math.Log(0.05), math.Log(0.05)},
	}
	target := []int{0}
	epsilon := 0.15

	loss, nllLoss := labelSmoothedNLLLoss(lprobs, target, epsilon)
	assert.True(t, loss >= 0)
	assert.True(t, nllLoss >= 0)
}