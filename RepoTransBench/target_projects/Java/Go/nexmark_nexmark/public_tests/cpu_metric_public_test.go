package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

type CpuMetric struct {
	processCpuTimeSeconds   float64
	processTotalCpuMillis   int64
	processCpuLoad          float32
	systemCpuLoad           float64
	hostName                string
}

func NewCpuMetric(procTime float64, procMillis int64, procLoad float32, sysLoad float64, host string) CpuMetric {
	return CpuMetric{procTime, procMillis, procLoad, sysLoad, host}
}

func (c CpuMetric) GetProcessCpuTimeSeconds() float64   { return c.processCpuTimeSeconds }
func (c CpuMetric) GetProcessTotalCpuMilliseconds() int64 { return c.processTotalCpuMillis }
func (c CpuMetric) GetProcessCpuLoad() float32           { return c.processCpuLoad }
func (c CpuMetric) GetSystemCpuLoad() float64            { return c.systemCpuLoad }
func (c CpuMetric) GetHostName() string                  { return c.hostName }
func (c CpuMetric) String() string                       { return c.hostName }

func TestCpuMetricDifferentValues(t *testing.T) {
	metric := NewCpuMetric(234.56, 1900, 14.7, 100.2, "nodeX")
	assert.Equal(t, 234.56, metric.GetProcessCpuTimeSeconds())
	assert.Equal(t, int64(1900), metric.GetProcessTotalCpuMilliseconds())
	assert.Equal(t, float32(14.7), metric.GetProcessCpuLoad())
	assert.Equal(t, 100.2, metric.GetSystemCpuLoad())
	assert.Equal(t, "nodeX", metric.GetHostName())
}

func TestToStringNotEmpty(t *testing.T) {
	metric := NewCpuMetric(0.99, 99, 2.2, 88.1, "hostY")
	s := metric.String()
	assert.Contains(t, s, "hostY")
	assert.True(t, len(s) > 0)
}