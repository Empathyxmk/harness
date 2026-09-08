package original

import (
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"sam31415_timeseriescv/timeseriescv"
)

// dummyCV implements a concrete CrossValidator that just returns the parent's split
type dummyCV struct {
	timeseriescv.BaseTimeSeriesCrossValidator
}

func (d *dummyCV) Split(X [][]float64, y []int, predTimes []time.Time, evalTimes []time.Time) ([]timeseriescv.TrainTestSplit, error) {
	// For error tests, we can call the parent's Split directly, or simulate error scenarios.
	return d.BaseTimeSeriesCrossValidator.Split(X, y, predTimes, evalTimes)
}

func TestNSplitsType(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Fatalf("Expected panic for non-integral n_splits")
		}
	}()
	timeseriescv.NewBaseTimeSeriesCrossValidatorFromInterface("not_an_int")
}

func TestNSplitsTooLow(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Fatalf("Expected panic for n_splits < 2")
		}
	}()
	timeseriescv.NewBaseTimeSeriesCrossValidator(1)
}

func TestSplitInvalidXType(t *testing.T) {
	cv := &dummyCV{*timeseriescv.NewBaseTimeSeriesCrossValidator(2)}
	defer func() {
		if r := recover(); r == nil {
			t.Fatalf("Expected panic for invalid X type")
		}
	}()
	cv.Split(nil, nil, nil, nil)
}

func TestSplitInvalidYType(t *testing.T) {
	cv := &dummyCV{*timeseriescv.NewBaseTimeSeriesCrossValidator(2)}
	X := [][]float64{{1, 2}, {3, 4}}
	predTimes := []time.Time{time.Now(), time.Now().Add(time.Second)}
	evalTimes := []time.Time{time.Now(), time.Now().Add(time.Second)}
	defer func() {
		if r := recover(); r == nil {
			t.Fatalf("Expected panic for invalid y type")
		}
	}()
	cv.Split(X, nil, predTimes, evalTimes)
}

func TestSplitInvalidPredTimesType(t *testing.T) {
	cv := &dummyCV{*timeseriescv.NewBaseTimeSeriesCrossValidator(2)}
	X := [][]float64{{1, 2}}
	y := []int{1}
	evalTimes := []time.Time{time.Now()}
	defer func() {
		if r := recover(); r == nil {
			t.Fatalf("Expected panic for invalid predTimes type")
		}
	}()
	cv.Split(X, y, nil, evalTimes)
}

func TestSplitInvalidEvalTimesType(t *testing.T) {
	cv := &dummyCV{*timeseriescv.NewBaseTimeSeriesCrossValidator(2)}
	X := [][]float64{{1, 2}}
	y := []int{1}
	predTimes := []time.Time{time.Now()}
	defer func() {
		if r := recover(); r == nil {
			t.Fatalf("Expected panic for invalid evalTimes type")
		}
	}()
	cv.Split(X, y, predTimes, nil)
}

func TestSplitIndexMismatchY(t *testing.T) {
	cv := &dummyCV{*timeseriescv.NewBaseTimeSeriesCrossValidator(2)}
	X := [][]float64{{1}, {2}}
	y := []int{1, 2, 3} // mismatched length
	predTimes := []time.Time{time.Now(), time.Now()}
	evalTimes := []time.Time{time.Now(), time.Now()}
	defer func() {
		if r := recover(); r == nil {
			t.Fatalf("Expected panic for X and y index mismatch")
		}
	}()
	cv.Split(X, y, predTimes, evalTimes)
}

func TestSplitIndexMismatchPredTimes(t *testing.T) {
	cv := &dummyCV{*timeseriescv.NewBaseTimeSeriesCrossValidator(2)}
	X := [][]float64{{1}, {2}}
	y := []int{1, 2}
	predTimes := []time.Time{time.Now()} // mismatched
	evalTimes := []time.Time{time.Now(), time.Now()}
	defer func() {
		if r := recover(); r == nil {
			t.Fatalf("Expected panic for X and predTimes index mismatch")
		}
	}()
	cv.Split(X, y, predTimes, evalTimes)
}

func TestSplitIndexMismatchEvalTimes(t *testing.T) {
	cv := &dummyCV{*timeseriescv.NewBaseTimeSeriesCrossValidator(2)}
	X := [][]float64{{1}, {2}}
	y := []int{1, 2}
	predTimes := []time.Time{time.Now(), time.Now()}
	evalTimes := []time.Time{time.Now()} // mismatched
	defer func() {
		if r := recover(); r == nil {
			t.Fatalf("Expected panic for X and evalTimes index mismatch")
		}
	}()
	cv.Split(X, y, predTimes, evalTimes)
}

func TestSplitPredTimesNotSorted(t *testing.T) {
	cv := &dummyCV{*timeseriescv.NewBaseTimeSeriesCrossValidator(2)}
	X := [][]float64{{1}, {2}}
	y := []int{1, 2}
	predTimes := []time.Time{time.Now().Add(2 * time.Hour), time.Now()}
	evalTimes := []time.Time{time.Now(), time.Now().Add(time.Hour)}
	defer func() {
		if r := recover(); r == nil {
			t.Fatalf("Expected panic for unsorted predTimes")
		}
	}()
	cv.Split(X, y, predTimes, evalTimes)
}

func TestSplitEvalTimesNotSorted(t *testing.T) {
	cv := &dummyCV{*timeseriescv.NewBaseTimeSeriesCrossValidator(2)}
	X := [][]float64{{1}, {2}}
	y := []int{1, 2}
	predTimes := []time.Time{time.Now(), time.Now().Add(time.Hour)}
	evalTimes := []time.Time{time.Now().Add(2 * time.Hour), time.Now()}
	defer func() {
		if r := recover(); r == nil {
			t.Fatalf("Expected panic for unsorted evalTimes")
		}
	}()
	cv.Split(X, y, predTimes, evalTimes)
}