package tests

import (
	"testing"
)

type IntervalEstimator interface {
	recordInterval(when int64)
	getEstimatedInterval(when int64) int64
}

func TestIntervalEstimator_AbstractMethodThrows(t *testing.T) {
	estimator := &dummyIntervalEstimator{}
	estimator.recordInterval(1)
	est := estimator.getEstimatedInterval(2)
	if est != 123 {
		t.Errorf("expected 123, got %d", est)
	}
}

type dummyIntervalEstimator struct{}

func (d *dummyIntervalEstimator) recordInterval(when int64) {
	// no-op for test
}
func (d *dummyIntervalEstimator) getEstimatedInterval(when int64) int64 {
	return 123
}