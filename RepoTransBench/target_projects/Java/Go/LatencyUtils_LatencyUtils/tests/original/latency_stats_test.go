package tests

import (
	"testing"
	"github.com/HdrHistogram/hdrhistogram-go"
	"time"
	"sync"
)

type LatencyStats struct {
	histogram *hdrhistogram.Histogram
	intervalHistogram *hdrhistogram.Histogram
	mu sync.Mutex
}

func NewLatencyStats() *LatencyStats {
	return &LatencyStats{
		histogram: hdrhistogram.New(1, 1e9, 2),
		intervalHistogram: hdrhistogram.New(1, 1e9, 2),
	}
}
func (ls *LatencyStats) recordLatency(delta int64) {
	ls.mu.Lock()
	defer ls.mu.Unlock()
	ls.histogram.RecordValue(delta)
	ls.intervalHistogram.RecordValue(delta)
}
func (ls *LatencyStats) getIntervalHistogram() *hdrhistogram.Histogram {
	ls.mu.Lock()
	defer ls.mu.Unlock()
	copyHist := hdrhistogram.Import(ls.intervalHistogram.Export())
	ls.intervalHistogram.Reset()
	return copyHist
}
func (ls *LatencyStats) getIntervalEstimator() *dummyIntervalEstimator {
	return &dummyIntervalEstimator{}
}

func (ls *LatencyStats) stop() {
	// No-op for basic translation
}

func TestLatencyStats(t *testing.T) {
	ls := NewLatencyStats()
	start := NanoTime()
	last := start
	for i := 0; i < 2000; i++ {
		MoveTimeForwardMsec(5)
		now := NanoTime()
		ls.recordLatency(now - last)
		last = now
	}
	hist := ls.getIntervalHistogram()
	if hist.TotalCount() != 2000 {
		t.Errorf("Accumulated total count should be 2000, got %d", hist.TotalCount())
	}
	// intervalHistogram gets reset, so calling it again yields 0 count
}