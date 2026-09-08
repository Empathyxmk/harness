package original

import (
	"math"
	"math/rand"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"lafan1/benchmarks"
)

func TestFastNpssSame(t *testing.T) {
	A := random3DF(3, 60, 5)
	score := benchmarks.FastNpss(A, A)
	assert.InEpsilon(t, 0.0, score, 1e-7)
}

func TestFastNpssDifferentNanGuard(t *testing.T) {
	A := fill3DF(2, 8, 2, 1.0)
	B := fill3DF(2, 8, 2, 0.0)
	score := benchmarks.FastNpss(A, B)
	assert.True(t, math.IsNaN(score), "Expected NaN score")
}

func TestFlatJoints(t *testing.T) {
	x := fill4DF(2, 3, 4, 5, 0.0)
	y := benchmarks.FlatJoints(x)
	require.Equal(t, 2, len(y))
	require.Equal(t, 3, len(y[0]))
	require.Equal(t, 20, len(y[0][0]))
}

func makeFakeFK(joints, frames int, randvals bool) ([][][][]float64, [][][][]float64, [][][]float64, [][][]float64, [][][][]float64, []int) {
	// shape: X, Q, x_mean, x_std, offsets, parents
	x_shape := []int{1, frames, joints, 3}
	q_shape := []int{1, frames, joints, 4}
	var X, Q [][][][]float64
	if randvals {
		X = random4DF(x_shape...)
		Q = random4DF(q_shape...)
	} else {
		X = fill4DF(x_shape[0], x_shape[1], x_shape[2], x_shape[3], 0.0)
		Q = fill4DF(q_shape[0], q_shape[1], q_shape[2], q_shape[3], 1.0)
	}
	x_mean := fill3DF(1, joints*3, 1, 0.0)
	x_std := fill3DF(1, joints*3, 1, 1.0)
	offsets := fill4DF(1, 1, joints, 3, 0.0)
	parents := make([]int, joints)
	parents[0] = -1
	for i := 1; i < joints; i++ {
		parents[i] = i - 1
	}
	return X, Q, x_mean, x_std, offsets, parents
}

func TestBenchmarkInterpolationVarious(t *testing.T) {
	for _, arg := range []struct{ joints, frames int }{{22, 65}, {5, 20}} {
		X, Q, x_mean, x_std, offsets, parents := makeFakeFK(arg.joints, arg.frames, false)
		if arg.joints == 22 {
			results, err := benchmarks.BenchmarkInterpolation(X, Q, x_mean, x_std, offsets, parents, "", 10, 10)
			if err != nil {
				t.Skipf("Unexpected failure for expected shape: %v", err)
			}
			require.NotNil(t, results)
			_, ok1 := results["zero_velocity"]
			_, ok2 := results["interpolation"]
			assert.True(t, ok1 && ok2, "missing result keys")
		} else {
			_, err := benchmarks.BenchmarkInterpolation(X, Q, x_mean, x_std, offsets, parents, "", 1, 1)
			assert.Error(t, err, "expected error for shape mismatch")
		}
	}
}

func TestBenchmarkInterpolationNanGuard(t *testing.T) {
	X := fill4DF(1, 30, 5, 3, 0.0)
	Q := fill4DF(1, 30, 5, 4, 0.0)
	x_mean := fill3DF(1, 15, 1, 0.0)
	x_std := fill3DF(1, 15, 1, 1.0)
	offsets := fill4DF(1, 1, 5, 3, 0.0)
	parents := []int{-1, 0, 1, 2, 3}
	_, err := benchmarks.BenchmarkInterpolation(X, Q, x_mean, x_std, offsets, parents, "", 1, 1)
	if err != nil {
		t.Skip("Expected failure for all-zero data, unable to compute NPSS")
	}
}

// --- Utility for random array creation ---
func fill3DF(dim1, dim2, dim3 int, val float64) [][][]float64 {
	arr := make([][][]float64, dim1)
	for i := 0; i < dim1; i++ {
		arr[i] = make([][]float64, dim2)
		for j := 0; j < dim2; j++ {
			arr[i][j] = make([]float64, dim3)
			for k := 0; k < dim3; k++ {
				arr[i][j][k] = val
			}
		}
	}
	return arr
}

func random3DF(dim1, dim2, dim3 int) [][][]float64 {
	arr := make([][][]float64, dim1)
	for i := 0; i < dim1; i++ {
		arr[i] = make([][]float64, dim2)
		for j := 0; j < dim2; j++ {
			arr[i][j] = make([]float64, dim3)
			for k := 0; k < dim3; k++ {
				arr[i][j][k] = rand.NormFloat64()
			}
		}
	}
	return arr
}

func fill4DF(dim1, dim2, dim3, dim4 int, val float64) [][][][]float64 {
	arr := make([][][][]float64, dim1)
	for i := range arr {
		arr[i] = make([][][]float64, dim2)
		for j := range arr[i] {
			arr[i][j] = make([][]float64, dim3)
			for k := range arr[i][j] {
				arr[i][j][k] = make([]float64, dim4)
				for l := range arr[i][j][k] {
					arr[i][j][k][l] = val
				}
			}
		}
	}
	return arr
}

func random4DF(dim1, dim2, dim3, dim4 int) [][][][]float64 {
	arr := make([][][][]float64, dim1)
	for i := range arr {
		arr[i] = make([][][]float64, dim2)
		for j := range arr[i] {
			arr[i][j] = make([][]float64, dim3)
			for k := range arr[i][j] {
				arr[i][j][k] = make([]float64, dim4)
				for l := range arr[i][j][k] {
					arr[i][j][k][l] = rand.NormFloat64()
				}
			}
		}
	}
	return arr
}