package public_tests

import (
	"testing"
	"github.com/HdrHistogram/hdrhistogram-go"
)

type LatencyStatsPublic struct {
	histogram *hdrhistogram.Histogram
}

func NewLatencyStatsPublic() *LatencyStatsPublic {
	return &LatencyStatsPublic{
		histogram: hdrhistogram.New(1, 1e9, 2),
	}
}
func (ls *LatencyStatsPublic) recordLatency(latency int64) {
	ls.histogram.RecordValue(latency)
}
func (ls *LatencyStatsPublic) getIntervalHistogram() *hdrhistogram.Histogram {
	return ls.histogram
}

func TestRecordAndEstimate(t *testing.T) {
	stats := NewLatencyStatsPublic()
	for i := 0; i < 50; i++ {
		stats.recordLatency(2000 + int64(i*2))
	}
	est := stats.getIntervalHistogram().Max()
	if est < 2000 {
		t.Errorf("Expected max >= 2000, got %d", est)
	}
}