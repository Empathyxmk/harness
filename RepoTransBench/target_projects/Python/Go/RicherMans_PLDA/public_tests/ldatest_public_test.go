package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"richermans_plda/liblda"
)

func TestFitPublic(t *testing.T) {
	X := [][]float64{
		{3, 8, 1},
		{6, 2, 7},
		{5, 4, 0},
		{9, 1, 2},
	}
	y := []int{2, 2, 1, 1}
	lda := liblda.NewLDAWithNComponents(2)
	model := lda.Fit(X, y)
	assert.IsType(t, &liblda.LDA{}, model)
	assert.Equal(t, 4, lda.Model[0][0])
}

func TestTransformPublic(t *testing.T) {
	X := [][]float64{
		{3, 8, 1},
		{6, 2, 7},
		{5, 4, 0},
		{9, 1, 2},
	}
	y := []int{2, 2, 1, 1}
	lda := liblda.NewLDAWithNComponents(2)
	lda.Fit(X, y)
	Xnew := lda.Transform(X)
	assert.Equal(t, 2, len(Xnew[0]))
}

func TestFitTransformPublic(t *testing.T) {
	X := [][]float64{
		{3, 8, 1},
		{6, 2, 7},
		{5, 4, 0},
		{9, 1, 2},
	}
	y := []int{2, 2, 1, 1}
	lda := liblda.NewLDAWithNComponents(2)
	Xnew := lda.FitTransform(X, y)
	assert.Equal(t, 2, len(Xnew[0]))
}

func TestTransformNComponentsNonePublic(t *testing.T) {
	X := [][]float64{
		{3, 8, 1},
		{6, 2, 7},
		{5, 4, 0},
		{9, 1, 2},
	}
	y := []int{2, 2, 1, 1}
	lda := liblda.NewLDAWithNComponents(-1)
	lda.Fit(X, y)
	Xnew := lda.Transform(X)
	assert.Equal(t, len(X[0]), len(Xnew[0]))
	assert.Equal(t, len(X), len(Xnew))
}