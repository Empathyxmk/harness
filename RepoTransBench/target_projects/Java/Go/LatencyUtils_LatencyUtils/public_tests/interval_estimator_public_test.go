package public_tests

import (
	"testing"
)

type IntervalEstimatorPublic interface {
	recordInterval(when int64)
	getEstimatedInterval(when int64) int64
}

type dummyIntervalEstimatorPublic struct{}

func (d *dummyIntervalEstimatorPublic) recordInterval(when int64) {
}

func (d *dummyIntervalEstimatorPublic) getEstimatedInterval(when int64) int64 {
	return 456
}

func TestAbstractMethodReturnsDifferentValue(t *testing.T) {
	estimator := &dummyIntervalEstimatorPublic{}
	estimator.recordInterval(100)
	est := estimator.getEstimatedInterval(101)
	if est != 456 {
		t.Errorf("expected 456, got %d", est)
	}
}