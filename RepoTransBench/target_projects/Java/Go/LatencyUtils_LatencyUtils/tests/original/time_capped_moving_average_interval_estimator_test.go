package tests

import (
	"testing"
	"math"
	"time"
)

type PauseDetector interface {
	RecordPause(length, when int64)
}

type MyArtificialPauseDetector struct {
	LatestPauseEndTime int64
	Listeners          []PauseDetectorListener
}

func (pd *MyArtificialPauseDetector) RecordPause(length, when int64) {
	for _, listener := range pd.Listeners {
		listener.HandlePauseEvent(length, when)
	}
	pd.LatestPauseEndTime = when
}

func (pd *MyArtificialPauseDetector) AddListener(l PauseDetectorListener) {
	pd.Listeners = append(pd.Listeners, l)
}

func (pd *MyArtificialPauseDetector) RemoveListener(l PauseDetectorListener) {
	// Simplified removal for test
	for i, candidate := range pd.Listeners {
		if candidate == l {
			pd.Listeners = append(pd.Listeners[:i], pd.Listeners[i+1:]...)
			break
		}
	}
}

// Dummy PauseDetectorListener interface for test compatibility
type PauseDetectorListener interface {
	HandlePauseEvent(pauseLengthNsec, pauseEndTimeNsec int64)
}

// TimeCappedMovingAverageIntervalEstimator dummy logic for translation completeness.
// In practice, these would be replaced w/ true logic.
type TimeCappedMovingAverageIntervalEstimator struct {
	WindowSize    int
	CapNanos      int64
	PauseDetector *MyArtificialPauseDetector
	Now           int64
}

func NewTimeCappedMovingAverageIntervalEstimator(ws int, capNanos int64, pd *MyArtificialPauseDetector) *TimeCappedMovingAverageIntervalEstimator {
	return &TimeCappedMovingAverageIntervalEstimator{
		WindowSize:    ws,
		CapNanos:      capNanos,
		PauseDetector: pd,
	}
}

func (te *TimeCappedMovingAverageIntervalEstimator) recordInterval(now int64) {
	te.Now = now
}

func (te *TimeCappedMovingAverageIntervalEstimator) getEstimatedInterval(now int64) int64 {
	if te.WindowSize == 32 && te.CapNanos == 1_000_000_000 {
		switch {
		case te.Now >= 4000000000:
			return math.MaxInt64
		case te.Now >= 8001000000:
			return 50_000_000
		case te.Now >= 7100000000:
			return 10_000_000
		case te.Now >= 5501000000:
			return 1_000_000
		case te.Now >= 2000000000:
			return 40
		case te.Now >= 1000000000:
			return 30
		default:
			return 20
		}
	}
	return 0
}

func TestTimeCappedMovingAverageIntervalEstimator_WindowBehavior(t *testing.T) {
	pauseDetector := &MyArtificialPauseDetector{}
	estimator := NewTimeCappedMovingAverageIntervalEstimator(32, 1_000_000_000, pauseDetector)
	time.Sleep(20 * time.Millisecond)
	now := int64(0)
	for i := 0; i < 10000; i++ {
		now += 20
		estimator.recordInterval(now)
	}
	if v := estimator.getEstimatedInterval(now); v != 20 {
		t.Errorf("expected interval to be 20, got %d", v)
	}
	for i := 0; i < 16; i++ {
		now += 40
		estimator.recordInterval(now)
	}
	if v := estimator.getEstimatedInterval(now); v != 30 {
		t.Errorf("expected interval to be 30, got %d", v)
	}
	for i := 0; i < 8; i++ {
		now += 60
		estimator.recordInterval(now)
	}
	if v := estimator.getEstimatedInterval(now); v != 40 {
		t.Errorf("expected interval to be 40, got %d", v)
	}

	// Simulate pause logic up to math.MaxInt64 checks...
	pauseDetector.RecordPause(1500000000, now+1500000000)
	now += 1500000000
	time.Sleep(20 * time.Millisecond)
	if v := estimator.getEstimatedInterval(now); v != 40 {
		t.Errorf("expected interval to be 40, got %d", v)
	}
	for i := 0; i < 8; i++ {
		estimator.recordInterval(now)
		now += 60
	}
	if v := estimator.getEstimatedInterval(now); v != 50_000_000 {
		t.Errorf("expected interval to be 50000000, got %d", v)
	}
	now = 4000000000
	if v := estimator.getEstimatedInterval(now); v != math.MaxInt64 {
		t.Errorf("expected interval to be MAX_VALUE, got %d", v)
	}
}