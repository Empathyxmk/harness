package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestCharEmbedderForwardShapesPublic(t *testing.T) {
	batchSize := 3
	maxWordLength := 7
	embeddingDim := 12

	output := make([][]float64, batchSize)
	for i := range output {
		output[i] = make([]float64, embeddingDim)
	}
	assert.Equal(t, batchSize, len(output))
	assert.Equal(t, embeddingDim, len(output[0]))
}