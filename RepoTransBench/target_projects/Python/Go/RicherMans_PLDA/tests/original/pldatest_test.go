package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"richermans_plda/liblda"
)

func TestPLDAFit(t *testing.T) {
	X := [][]float64{
		{1, 2},
		{3, 4},
		{5, 6},
	}
	y := []int{0, 1, 0}
	plda := liblda.NewPLDA()
	out := plda.Fit(X, y)
	assert.True(t, plda.Trained)
	assert.Equal(t, plda, out)
}

func TestPLDAPredict(t *testing.T) {
	X := [][]float64{
		{1, 2},
		{3, 4},
		{5, 6},
	}
	y := []int{0, 1, 0}
	plda := liblda.NewPLDA()
	plda.Fit(X, y)
	pred := plda.Predict(X)
	for _, p := range pred {
		assert.Equal(t, 0, p)
	}
}

func TestPLDAPredictWithoutFit(t *testing.T) {
	X := [][]float64{
		{1, 2},
		{3, 4},
		{5, 6},
	}
	p := liblda.NewPLDA()
	_, err := p.PredictWithErr(X)
	assert.Error(t, err)
}