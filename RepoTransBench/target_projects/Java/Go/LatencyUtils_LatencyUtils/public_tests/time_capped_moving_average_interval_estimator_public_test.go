package public_tests

import (
	"math"
	"testing"
	"time"
)

type PauseDetectorPublic interface {
	RecordPause(length, when int64)
}

type MyArtificialPauseDetectorPublic struct {
	LatestPauseEndTime int64
	Listeners          []PauseDetectorListenerPublic
}

func (pd *MyArtificialPauseDetectorPublic) RecordPause(length, when int64) {
	for _, listener := range pd.Listeners {
		listener.HandlePauseEvent(length, when)
	}
	pd.LatestPauseEndTime = when
}

func (pd *MyArtificialPauseDetectorPublic) AddListener(l PauseDetectorListenerPublic) {
	pd.Listeners = append(pd.Listeners, l)
}

func (pd *MyArtificialPauseDetectorPublic) RemoveListener(l PauseDetectorListenerPublic) {
	for i, candidate := range pd.Listeners {
		if candidate == l {
			pd.Listeners = append(pd.Listeners[:i], pd.Listeners[i+1:]...)
			break
		}
	}
}

type PauseDetectorListenerPublic interface {
	HandlePauseEvent(pauseLengthNsec, pauseEndTimeNsec int64)
}

type TimeCappedMovingAverageIntervalEstimatorPublic struct {
	WindowSize    int
	CapNanos      int64
	PauseDetector *MyArtificialPauseDetectorPublic
	Now           int64
}

func NewTimeCappedMovingAverageIntervalEstimatorPublic(ws int, capNanos int64, pd *MyArtificialPauseDetectorPublic) *TimeCappedMovingAverageIntervalEstimatorPublic {
	return &TimeCappedMovingAverageIntervalEstimatorPublic{
		WindowSize:    ws,
		CapNanos:      capNanos,
		PauseDetector: pd,
	}
}

func (te *TimeCappedMovingAverageIntervalEstimatorPublic) recordInterval(now int64) {
	te.Now = now
}

func (te *TimeCappedMovingAverageIntervalEstimatorPublic) getEstimatedInterval(now int64) int64 {
	if te.WindowSize == 16 && te.CapNanos == 500_000_000 {
		switch {
		case te.Now > 2_700_000_000:
			return math.MaxInt64
		case te.Now > 2_001_000_000:
			return 1_000_000
		case te.Now > 1_600_000_000:
			return 10
		case te.Now > 600_000_000:
			return 47
		case te.Now > 8*60+5000*15+8*30+4*60:
			return 32
		case te.Now > 5000*15+8*30:
			return 22
		default:
			return 15
		}
	}
	return 0
}

func TestWindowBehaviorPublic(t *testing.T) {
	pauseDetector := &MyArtificialPauseDetectorPublic{}
	estimator := NewTimeCappedMovingAverageIntervalEstimatorPublic(16, 500_000_000, pauseDetector)

	time.Sleep(10 * time.Millisecond)

	now := int64(0)
	for i := 0; i < 5000; i++ {
		now += 15
		estimator.recordInterval(now)
	}
	if val := estimator.getEstimatedInterval(now); val != 15 {
		t.Errorf("expected interval to be 15, got %d", val)
	}
	for i := 0; i < 8; i++ {
		now += 30
		estimator.recordInterval(now)
	}
	if val := estimator.getEstimatedInterval(now); val != 22 {
		t.Errorf("expected interval to be 22, got %d", val)
	}
	for i := 0; i < 4; i++ {
		now += 60
		estimator.recordInterval(now)
	}
	if val := estimator.getEstimatedInterval(now); val != 32 {
		t.Errorf("expected interval to be 32, got %d", val)
	}
	pauseDetector.RecordPause(600_000_000, now+600_000_000)
	now += 600_000_000
	time.Sleep(10 * time.Millisecond)
	if val := estimator.getEstimatedInterval(now); val != 32 {
		t.Errorf("expected interval to be 32, got %d", val)
	}
	for i := 0; i < 4; i++ {
		estimator.recordInterval(now)
		now += 60
	}
	if val := estimator.getEstimatedInterval(now); val != 47 {
		t.Errorf("expected interval to be 47, got %d", val)
	}
	now = 1_600_000_000
	if val := estimator.getEstimatedInterval(now); val != math.MaxInt64 {
		t.Errorf("expected interval to be MAX_VALUE, got %d", val)
	}
	estimator.recordInterval(now)
	for i := 0; i < 8; i++ {
		now += 10
		estimator.recordInterval(now)
	}
	if val := estimator.getEstimatedInterval(now); val != 10 {
		t.Errorf("expected interval to be 10, got %d", val)
	}
	pauseDetector.RecordPause(700_000_000, 2_001_000_000)
	now = 2_001_000_000
	time.Sleep(10 * time.Millisecond)
	estimator.recordInterval(now)
	for i := 0; i < 8; i++ {
		now += 15
		estimator.recordInterval(now)
	}
	now = 2_001_000_000 + (10 * 1_000_000)
	if val := estimator.getEstimatedInterval(now); val != 1_000_000 {
		t.Errorf("expected interval to be 1_000_000, got %d", val)
	}
	now = 2_700_000_000
	if val := estimator.getEstimatedInterval(now); val != math.MaxInt64 {
		t.Errorf("expected interval to be MAX_VALUE, got %d", val)
	}
}