package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"sam31415_timeseriescv/timeseriescv"
)

func TestErrorsNSplitsPublic(t *testing.T) {
	df := make([][]float64, 15)
	for i := range df {
		df[i] = []float64{0.0}
	}
	defer func() {
		if r := recover(); r == nil {
			t.Fatalf("Expected panic for n_splits > rows")
		}
	}()
	cv := timeseriescv.NewPurgedWalkForwardCVWithParams(16, 1, 1, 0)
	cv.Split(df, nil, nil, nil)
}

func TestErrorsTrainLengthPublic(t *testing.T) {
	df := make([][]float64, 12)
	for i := range df {
		df[i] = []float64{0.0}
	}
	defer func() {
		if r := recover(); r == nil {
			t.Fatalf("Expected panic for train_length > data")
		}
	}()
	cv := timeseriescv.NewPurgedWalkForwardCVWithParams(3, 11, 2, 0)
	cv.Split(df, nil, nil, nil)
}

func TestErrorsTestLengthPublic(t *testing.T) {
	df := make([][]float64, 10)
	for i := range df {
		df[i] = []float64{0.0}
	}
	defer func() {
		if r := recover(); r == nil {
			t.Fatalf("Expected panic for test_length > data")
		}
	}()
	cv := timeseriescv.NewPurgedWalkForwardCVWithParams(2, 2, 9, 0)
	cv.Split(df, nil, nil, nil)
}

func TestErrorsLookaheadNegativePublic(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Fatalf("Expected panic for negative lookahead")
		}
	}()
	timeseriescv.NewPurgedWalkForwardCVWithParams(2, 2, 2, -4)
}

func TestBaseCVSplitSignaturePublic(t *testing.T) {
	df := make([][]float64, 4)
	for i := range df {
		df[i] = []float64{0.0}
	}
	// dummyCVSplitSignature does not implement Split
	cv := &dummyCVSplitSignature{}
	defer func() {
		if r := recover(); r == nil {
			t.Fatalf("Expected panic for missing Split implementation")
		}
	}()
	cv.Split(df, nil, nil, nil)
}

type dummyCVSplitSignature struct{}

func (c *dummyCVSplitSignature) Split(X [][]float64, y []int, predTimes []interface{}, evalTimes []interface{}) ([]timeseriescv.TrainTestSplit, error) {
	panic("not implemented")
}