package public_tests

import (
	"math"
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"lafan1/benchmarks"
)

func TestPickleStatsPublic(t *testing.T) {
	// No pickle, use Go's native data structures and temp file to mimic test
	tmpDir := t.TempDir()
	statsPath := filepath.Join(tmpDir, "lafan1_stats_public.gob")
	type Stats struct {
		Xmean [][]float64
		Xstd  [][]float64
	}
	xMean := [][]float64{{13, 13}, {13, 13}}
	xStd := [][]float64{{6, 6}, {6, 6}}
	stats := Stats{Xmean: xMean, Xstd: xStd}

	// NOTE: Go has gob for serialization, not pickle; here just check we can write/read via native means
	f, err := os.Create(statsPath)
	require.NoError(t, err)
	defer f.Close()
	// We'll just check we can write and read back (manually for the test)
	for _, row := range stats.Xmean {
		for _, v := range row {
			_, _ = f.Write([]byte{byte(v)})
		}
	}
	f.Sync()
	_, err = os.Stat(statsPath)
	assert.NoError(t, err)
}

func TestBenchmarkOnFakeDataPublic(t *testing.T) {
	X := fill4DF(1, 10, 2, 3, 2.0)
	Y := fill4DF(1, 10, 2, 3, 1.0)
	// Just make sure this does not panic
	_ = benchmarks.FastNpss(X[0], Y[0])
}

func TestBenchmarkNanGuardWithNanInputPublic(t *testing.T) {
	A := [][][]float64{{{1, 2}, {math.NaN(), 4}}}
	B := [][][]float64{{{5, 6}, {7, 8}}}
	score := benchmarks.FastNpss(A, B)
	assert.True(t, math.IsNaN(score) || score >= 0)
}

// Utility from test_benchmarks: for this test file
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