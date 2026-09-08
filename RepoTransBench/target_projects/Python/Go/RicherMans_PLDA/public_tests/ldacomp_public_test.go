package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"richermans_plda/liblda"
)

func TestLDAFitAndTransformPublic(t *testing.T) {
	X := [][]float64{
		{2, 6, 4},
		{1, 5, 8},
		{4, 2, 9},
	}
	y := []int{1, 0, 0}
	lda := liblda.NewLDAWithNComponents(2)
	lda.Fit(X, y)
	Xtrans := lda.Transform(X)
	assert.Equal(t, 3, len(Xtrans))
	assert.Equal(t, 2, len(Xtrans[0]))
}