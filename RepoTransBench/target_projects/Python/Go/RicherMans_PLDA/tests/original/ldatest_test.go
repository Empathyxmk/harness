package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"richermans_plda/liblda"
)

func TestLDAFit(t *testing.T) {
	X := [][]float64{
		{1, 2, 3},
		{4, 5, 6},
		{7, 8, 9},
		{2, 3, 4},
	}
	y := []int{0, 1, 0, 1}
	lda := liblda.NewLDAWithNComponents(2)
	model := lda.Fit(X, y)
	// Check returned type and model shape
	assert.IsType(t, &liblda.LDA{}, model)
	assert.Equal(t, 4, lda.Model[0][0]) // n_samples
}

func TestLDATransform(t *testing.T) {
	X := [][]float64{
		{1, 2, 3},
		{4, 5, 6},
		{7, 8, 9},
		{2, 3, 4},
	}
	y := []int{0, 1, 0, 1}
	lda := liblda.NewLDAWithNComponents(2)
	lda.Fit(X, y)
	Xnew := lda.Transform(X)
	assert.Equal(t, 2, len(Xnew[0]))
}

func TestLDAFitTransform(t *testing.T) {
	X := [][]float64{
		{1, 2, 3},
		{4, 5, 6},
		{7, 8, 9},
		{2, 3, 4},
	}
	y := []int{0, 1, 0, 1}
	lda := liblda.NewLDAWithNComponents(2)
	Xnew := lda.FitTransform(X, y)
	assert.Equal(t, 2, len(Xnew[0]))
}

func TestTransformNComponentsNone(t *testing.T) {
	X := [][]float64{
		{1, 2, 3},
		{4, 5, 6},
		{7, 8, 9},
		{2, 3, 4},
	}
	y := []int{0, 1, 0, 1}
	lda := liblda.NewLDAWithNComponents(-1)
	lda.Fit(X, y)
	Xnew := lda.Transform(X)
	assert.Equal(t, len(X[0]), len(Xnew[0]))
	assert.Equal(t, len(X), len(Xnew))
}