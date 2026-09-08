package tests

import (
	"math"
	"testing"

	"github.com/stretchr/testify/assert"
)

// Dummy implementations for LabelSmoothing logic
// These are only for placeholder until the actual logic of fairseq is migrated.
// Here, we simulate a label smoothing loss computation.

func labelSmoothedNLLLoss(lprobs [][]float64, target []int, epsilon float64) (float64, float64) {
	// For a real translation, nll_loss is the negative log likelihood for correct tokens,
	// loss is smoothed loss: (1-eps)*NLL + eps*(mean over class).
	nToks := len(target)
	nll := 0.0
	for i, tgt := range target {
		p := lprobs[i][tgt]
		nll -= p
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

func almostEqual(a, b float64, tol float64) bool {
	return math.Abs(a-b) < tol
}

func TestLabelSmoothedCrossEntropyBasic(t *testing.T) {
	// Simulate log softmax (natural log)
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

func TestLabelSmoothedNLLLossIgnoreIndex(t *testing.T) {
	// Ignore index means some targets are skipped. Here, we test no skip.
	lprobs := [][]float64{
		{math.Log(0.9), math.Log(0.05), math.Log(0.05)},
	}
	target := []int{0}
	epsilon := 0.15

	loss, nllLoss := labelSmoothedNLLLoss(lprobs, target, epsilon)
	assert.True(t, loss >= 0)
	assert.True(t, nllLoss >= 0)
}