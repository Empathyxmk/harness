package tests

import (
	"math"
	"testing"

	"github.com/stretchr/testify/assert"
)

func averageCheckpoints(paramsList []map[string][]float64) map[string][]float64 {
	out := make(map[string][]float64)
	keys := []string{}
	for k := range paramsList[0] {
		keys = append(keys, k)
	}
	for _, k := range keys {
		l := len(paramsList[0][k])
		out[k] = make([]float64, l)
		for i := 0; i < l; i++ {
			sum := 0.0
			for j := range paramsList {
				sum += paramsList[j][k][i]
			}
			out[k][i] = sum / float64(len(paramsList))
		}
	}
	return out
}

func almostSliceEqual(a, b []float64, tol float64) bool {
	if len(a) != len(b) {
		return false
	}
	for i := range a {
		if math.Abs(a[i]-b[i]) > tol {
			return false
		}
	}
	return true
}

func TestAverageCheckpoints(t *testing.T) {
	params0 := map[string][]float64{
		"a": {100.0},
		"b": {1.0, 2.0, 3.0, 4.0, 5.0, 6.0},
	}
	params1 := map[string][]float64{
		"a": {1.0},
		"b": {1.0, 1.0, 1.0, 1.0, 1.0, 1.0},
	}
	paramsAVG := map[string][]float64{
		"a": {50.5},
		"b": {1.0, 1.5, 2.0, 2.5, 3.0, 3.5},
	}
	result := averageCheckpoints([]map[string][]float64{params0, params1})

	assert.True(t, almostSliceEqual(paramsAVG["a"], result["a"], 1e-6))
	assert.True(t, almostSliceEqual(paramsAVG["b"], result["b"], 1e-6))
}