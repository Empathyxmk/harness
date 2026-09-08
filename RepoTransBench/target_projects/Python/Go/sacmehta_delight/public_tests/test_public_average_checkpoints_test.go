package public_tests

import (
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

func TestPublicAverageCheckpointsMean(t *testing.T) {
	params0 := map[string][]float64{"weights": {6.0, 2.0}}
	params1 := map[string][]float64{"weights": {4.0, 10.0}}
	result := averageCheckpoints([]map[string][]float64{params0, params1})

	assert.InDeltaSlice(t, []float64{5.0, 6.0}, result["weights"], 1e-6)
}

func TestPublicAverageCheckpointsSingleFile(t *testing.T) {
	params0 := map[string][]float64{"weights": {1.3, 3.2, 4.4}}
	result := averageCheckpoints([]map[string][]float64{params0})
	assert.InDeltaSlice(t, params0["weights"], result["weights"], 1e-6)
}