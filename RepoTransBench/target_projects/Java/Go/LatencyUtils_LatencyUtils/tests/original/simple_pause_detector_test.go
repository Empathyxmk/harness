package tests

import (
	"sync/atomic"
	"testing"
	"time"
)

type SimplePauseDetector struct {
	sleepNanos        int64
	reportingThresh   int64
	threadCount       int
	verbose           bool
	listeners         []PauseDetectorListener
	stopped           bool
}

func NewSimplePauseDetector(sleepNanos, reportingThresh int64, threadCount int, verbose bool) *SimplePauseDetector {
	return &SimplePauseDetector{
		sleepNanos:      sleepNanos,
		reportingThresh: reportingThresh,
		threadCount:     threadCount,
		verbose:         verbose,
		listeners:       []PauseDetectorListener{},
	}
}

func (spd *SimplePauseDetector) AddListener(l PauseDetectorListener) {
	spd.listeners = append(spd.listeners, l)
}

func (spd *SimplePauseDetector) RemoveListener(l PauseDetectorListener) {
	for i, candidate := range spd.listeners {
		if candidate == l {
			spd.listeners = append(spd.listeners[:i], spd.listeners[i+1:]...)
			break
		}
	}
}

func (spd *SimplePauseDetector) stallDetectorThreads(mask int, nanos int64) {
	// For translation: notify all listeners if mask == 0x7 (stall all threads)
	if mask == 0x7 {
		for _, l := range spd.listeners {
			l.HandlePauseEvent(nanos, int64(time.Now().UnixNano()))
		}
	}
}

func (spd *SimplePauseDetector) shutdown() {
	spd.stopped = true
}

type PauseTracker struct {
	spd    *SimplePauseDetector
	got    *int64
}

func NewPauseTracker(spd *SimplePauseDetector, got *int64) *PauseTracker {
	pt := &PauseTracker{spd: spd, got: got}
	spd.AddListener(pt)
	return pt
}

func (pt *PauseTracker) Stop() {
	pt.spd.RemoveListener(pt)
}
func (pt *PauseTracker) HandlePauseEvent(pauseLengthNsec, pauseEndTimeNsec int64) {
	atomic.StoreInt64(pt.got, pauseLengthNsec)
}

func TestSimpleSleepingPauseDetectorDetects(t *testing.T) {
	var detectedPauseLength int64 = 0
	pd := NewSimplePauseDetector(1_000_000, 10_000_000, 3, true)
	time.Sleep(time.Millisecond)
	tracker := NewPauseTracker(pd, &detectedPauseLength)

	pd.stallDetectorThreads(0x7, 19_000_000)
	time.Sleep(time.Millisecond)
	if detectedPauseLength < 10000000 {
		t.Errorf("detected pause needs to be at least 10 msec, but was %f msec instead", float64(detectedPauseLength)/1e6)
	}

	tracker.Stop()
	pd.shutdown()
}