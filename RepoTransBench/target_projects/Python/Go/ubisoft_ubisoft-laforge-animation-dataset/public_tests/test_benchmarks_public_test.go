package public_tests

import (
	"math"
	"testing"

	"github.com/stretchr/testify/assert"
	"lafan1/benchmarks"
)

func TestFastNpssSimplePublic(t *testing.T) {
	A := linspaceReshape(1, 2*12, 1, 1, 2)
	B := linspaceReshape(1, 2*12, 1, 2, 3)
	score := benchmarks.FastNpss(A, B)
	assert.False(t, math.IsNaN(score))
}

func TestFastNpssDifferentNanGuardPublic(t *testing.T) {
	A := linspaceReshape(1, 2*12, 1, 0, 3)
	B := linspaceReshape(1, 2*12, 1, 1, 4)
	score := benchmarks.FastNpss(A, B)
	assert.False(t, math.IsNaN(score))
}

// Dummy skipped test for coverage symmetry
func TestDummySkipPublic(t *testing.T) {
	t.Skip("Testing skip for public test coverage symmetry")
}

// Helper for linspace + reshape for above tests
func linspaceReshape(batch, rows, cols int, start, end float64) [][][]float64 {
	size := batch * rows * cols
	step := (end - start) / float64(size-1)
	result := make([][][]float64, batch)
	for b := 0; b < batch; b++ {
		result[b] = make([][]float64, rows)
		for r := 0; r < rows; r++ {
			result[b][r] = make([]float64, cols)
			for c := 0; c < cols; c++ {
				flatIdx := b*rows*cols + r*cols + c
				result[b][r][c] = start + step*float64(flatIdx)
			}
		}
	}
	return result
}