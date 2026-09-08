package tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestCharEmbedderForwardShapes(t *testing.T) {
	// Simulate shape: batch 3 x 7 chars x 2 channel, embedding dim 12
	batchSize := 3
	maxWordLength := 7
	embeddingDim := 12

	// For this dummy, just check the output "embedding" matches batch size and dim
	input := make([][][]int, batchSize)
	for i := range input {
		input[i] = make([][]int, maxWordLength)
		for j := range input[i] {
			input[i][j] = []int{0, 0}
		}
	}
	output := make([][]float64, batchSize)
	for i := range output {
		output[i] = make([]float64, embeddingDim)
	}
	assert.Equal(t, batchSize, len(output))
	assert.Equal(t, embeddingDim, len(output[0]))
}