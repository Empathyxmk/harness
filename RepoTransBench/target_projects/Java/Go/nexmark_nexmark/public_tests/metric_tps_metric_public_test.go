package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

type TpsMetric struct {
	startTime int64
	endTime   int64
	tps       float64
	num       int64
}

func NewTpsMetric() *TpsMetric {
	return &TpsMetric{}
}

func (m *TpsMetric) SetStartTime(val int64)  { m.startTime = val }
func (m *TpsMetric) SetEndTime(val int64)    { m.endTime = val }
func (m *TpsMetric) SetTps(val float64)      { m.tps = val }
func (m *TpsMetric) SetNum(val int64)        { m.num = val }
func (m *TpsMetric) GetStartTime() int64     { return m.startTime }
func (m *TpsMetric) GetEndTime() int64       { return m.endTime }
func (m *TpsMetric) GetTps() float64         { return m.tps }
func (m *TpsMetric) GetNum() int64           { return m.num }

func TestTpsMetricSettersGetters(t *testing.T) {
	metric := NewTpsMetric()
	metric.SetStartTime(22222)
	metric.SetEndTime(33333)
	metric.SetTps(12345.6)
	metric.SetNum(77)
	assert.Equal(t, int64(22222), metric.GetStartTime())
	assert.Equal(t, int64(33333), metric.GetEndTime())
	assert.Equal(t, 12345.6, metric.GetTps())
	assert.Equal(t, int64(77), metric.GetNum())
}