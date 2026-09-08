package public_tests

import (
	"math"
	"testing"

	"github.com/stretchr/testify/assert"
)

func safeNorm(xs []float64) float64 {
	sq := 0.0
	for _, x := range xs {
		sq += x * x
	}
	return math.Sqrt(sq)
}

func safeExp(x float64) float64 {
	const maxExp = 709.0 // math.Exp(709) is about max float64 before Inf
	if x > maxExp {
		return math.Exp(maxExp)
	}
	return math.Exp(x)
}

func TestTensorNormalizationPublic(t *testing.T) {
	tensor := []float64{2.0, 8.0, 18.0}
	norm := safeNorm(tensor)
	assert.InDelta(t, norm, math.Sqrt(2*2+8*8+18*18), 1e-8)
}

func TestSafeExpPublic(t *testing.T) {
	assert.InDelta(t, safeExp(1.0), 2.7182818284, 1e-8)
	assert.True(t, safeExp(1000.0) < 1e308)
}