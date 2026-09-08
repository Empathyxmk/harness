package public_tests

import (
	"fmt"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"sam31415_timeseriescv/timeseriescv"
)

func TestPurgedWalkForwardCVNondefaultPublic(t *testing.T) {
	df := make([][]float64, 30)
	for i := range df {
		df[i] = []float64{40 + float64(i)}
	}
	cv := timeseriescv.NewPurgedWalkForwardCVWithParams(5, 6, 2, 1)
	splits, err := cv.Split(df, nil, nil, nil)
	assert.NoError(t, err)
	assert.Equal(t, 5, len(splits))
	assert.Equal(t, 0, splits[0].Train[0])
	lastTest := splits[len(splits)-1].Test
	assert.Equal(t, len(df)-1, lastTest[len(lastTest)-1])
}

func TestEmbargoPublic(t *testing.T) {
	arr := make([]bool, 20)
	timeseriescv.EmbargoPublic(arr, 6, 13, 4)
	for i := 13; i < 17; i++ {
		if !arr[i] {
			t.Errorf("arr[%d] should be embargoed", i)
		}
	}
	if arr[12] {
		t.Errorf("arr[12] should NOT be embargoed")
	}
}

func TestWalkforwardLengthPublic(t *testing.T) {
	X := make([][]float64, 34)
	for i := range X {
		X[i] = []float64{30 + float64(i)}
	}
	cv := timeseriescv.NewPurgedWalkForwardCVWithParams(2, 12, 9, 2)
	splits, err := cv.Split(X, nil, nil, nil)
	assert.NoError(t, err)
	assert.Equal(t, 2, len(splits))
	last := -1
	for _, split := range splits {
		assert.True(t, split.Test[0] > last)
		last = split.Test[len(split.Test)-1]
	}
}

func TestReprPublic(t *testing.T) {
	cv := timeseriescv.NewPurgedWalkForwardCVWithParams(3, 8, 3, 3)
	rp := fmt.Sprintf("%v", cv)
	assert.Contains(t, rp, "PurgedWalkForwardCV")
	assert.Contains(t, rp, "nSplits:3")
}

func TestCrossValidatorBasePublic(t *testing.T) {
	cv := &dummyCVPublic{}
	X := make([][]float64, 10)
	for i := range X {
		X[i] = []float64{float64(i)}
	}
	splits, err := cv.Split(X, nil, nil, nil)
	assert.NoError(t, err)
	assert.Equal(t, 1, len(splits))
	trainIdx, testIdx := splits[0].Train, splits[0].Test
	assert.True(t, len(trainIdx) > 0)
	assert.True(t, len(testIdx) > 0)
	for _, v := range trainIdx {
		for _, w := range testIdx {
			if v == w {
				t.Fatalf("Sets overlap")
			}
		}
	}
}

type dummyCVPublic struct{}

func (c *dummyCVPublic) Split(X [][]float64, y []int, predTimes []time.Time, evalTimes []time.Time) ([]timeseriescv.TrainTestSplit, error) {
	n := len(X)
	return []timeseriescv.TrainTestSplit{
		{
			Train: makeRange(0, n/3),
			Test:  makeRange(n/3, n/2),
		},
	}, nil
}

func makeRange(a, b int) []int {
	out := make([]int, b-a)
	for i := range out {
		out[i] = a + i
	}
	return out
}

func TestPurgedWalkForwardCVGetNSplitsPublic(t *testing.T) {
	df := make([][]float64, 29)
	for i := range df {
		df[i] = []float64{30 + float64(i)}
	}
	cv := timeseriescv.NewPurgedWalkForwardCVWithParams(3, 7, 2, 2)
	assert.Equal(t, 3, cv.GetNSplits(df, nil, nil, nil))
}

func TestSplitIndicesNonOverlapPublic(t *testing.T) {
	df := make([][]float64, 24)
	for i := range df {
		df[i] = []float64{70 + float64(i)}
	}
	cv := timeseriescv.NewPurgedWalkForwardCVWithParams(4, 5, 5, 3)
	splits, err := cv.Split(df, nil, nil, nil)
	assert.NoError(t, err)
	for _, split := range splits {
		assert.True(t, isDisjoint(split.Train, split.Test))
	}
}

func isDisjoint(a, b []int) bool {
	set := make(map[int]struct{})
	for _, v := range a {
		set[v] = struct{}{}
	}
	for _, v := range b {
		if _, ok := set[v]; ok {
			return false
		}
	}
	return true
}

func TestLargeEmbargoEdgePublic(t *testing.T) {
	mask := make([]bool, 12)
	timeseriescv.EmbargoPublic(mask, 8, 10, 4)
	for i := 10; i < 12; i++ {
		if !mask[i] {
			t.Errorf("mask[%d] should be embargoed", i)
		}
	}
}