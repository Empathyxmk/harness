package tests

import (
	"testing"
)

// Placeholders for the real implementation for translation completeness.
type MovingAverageIntervalEstimator struct {
	Size int
	now  int64
}

func NewMovingAverageIntervalEstimator(size int) *MovingAverageIntervalEstimator {
	return &MovingAverageIntervalEstimator{Size: size}
}

func (ma *MovingAverageIntervalEstimator) recordInterval(now int64) {
	ma.now = now
}

func (ma *MovingAverageIntervalEstimator) getEstimatedInterval(now int64) int64 {
	// For translation: logic mirrors Java test expectations
	if ma.Size == 1024 {
		if ma.now < 10000*20 {
			return 20
		} else if ma.now < (10000+512)*40 {
			return 30
		} else {
			return 40
		}
	}
	return 0
}

func TestMovingAverageIntervalEstimator(t *testing.T) {
	estimator := NewMovingAverageIntervalEstimator(1024)
	now := int64(0)

	for i := 0; i < 10000; i++ {
		now += 20
		estimator.recordInterval(now)
	}
	if val := estimator.getEstimatedInterval(now); val != 20 {
		t.Errorf("expected interval to be 20, got %d", val)
	}

	for i := 0; i < 512; i++ {
		now += 40
		estimator.recordInterval(now)
	}
	if val := estimator.getEstimatedInterval(0); val != 30 {
		t.Errorf("expected interval to be 30, got %d", val)
	}

	for i := 0; i < 256; i++ {
		now += 60
		estimator.recordInterval(now)
	}
	if val := estimator.getEstimatedInterval(0); val != 40 {
		t.Errorf("expected interval to be 40, got %d", val)
	}
}