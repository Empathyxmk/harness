package original

import (
	"encoding/json"
	"testing"

	"github.com/stretchr/testify/assert"
)

type CpuMetric struct {
	Host    string  `json:"host"`
	Pid     int     `json:"pid"`
	Load    float64 `json:"load"`
}

func (CpuMetric) fromJsonArray(jstr string) ([]CpuMetric, error) {
	var result []CpuMetric
	err := json.Unmarshal([]byte(jstr), &result)
	return result, err
}

func TestCpuMetric(t *testing.T) {
	cpuMetrics := []CpuMetric{
		{Host: "10.0.0.12", Pid: 37927, Load: 1.01},
		{Host: "10.1.0.33", Pid: 54389, Load: 2.3},
		{Host: "10.2.0.44", Pid: 4401, Load: 0.4},
	}
	result, err := json.Marshal(cpuMetrics)
	assert.NoError(t, err)

	cpu := CpuMetric{}
	expected, err := cpu.fromJsonArray(string(result))
	assert.NoError(t, err)
	assert.Equal(t, cpuMetrics, expected)
}