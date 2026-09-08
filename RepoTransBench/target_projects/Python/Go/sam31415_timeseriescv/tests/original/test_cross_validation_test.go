package original

import (
	"errors"
	"fmt"
	"reflect"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"sam31415_timeseriescv/timeseriescv"
)

func makeSimpleData(n int, seed int64) (df [][]float64, y []int, predTimes, evalTimes []time.Time) {
	// Go doesn't have numpy or pandas, so we construct slice-based structures
	df = make([][]float64, n)
	for i := 0; i < n; i++ {
		df[i] = []float64{float64(i) + 0.1, float64(i) + 0.2, float64(i) + 0.3}
	}
	predTimes = make([]time.Time, n)
	evalTimes = make([]time.Time, n)
	y = make([]int, n)
	for i := 0; i < n; i++ {
		predTimes[i] = time.Date(2021, 1, 1, 0, 0, 0, 0, time.UTC).AddDate(0, 0, i)
		evalTimes[i] = predTimes[i].AddDate(0, 0, 1)
		y[i] = i % 2
	}
	return
}

func TestBaseTimeSeriesCVNSplitsProperty(t *testing.T) {
	cv := timeseriescv.NewBaseTimeSeriesCrossValidator(5)
	assert.Equal(t, 5, cv.NSplits())
	cv.SetNSplits(6)
	assert.Equal(t, 6, cv.NSplits())
}

func TestPurgeBasicObject(t *testing.T) {
	cv := &dummyCVForPurge{
		BaseTimeSeriesCrossValidator: *timeseriescv.NewBaseTimeSeriesCrossValidator(2),
	}
	inTrain := timeseriescv.Purge(cv, 4, 5, 5)
	assert.IsType(t, []int{}, inTrain)
}

type dummyCVForPurge struct {
	timeseriescv.BaseTimeSeriesCrossValidator
}

func (c *dummyCVForPurge) PredTimes() []time.Time {
	return []time.Time{
		time.Date(2023, 1, 1, 0, 0, 0, 0, time.UTC),
		time.Date(2023, 1, 2, 0, 0, 0, 0, time.UTC),
		time.Date(2023, 1, 3, 0, 0, 0, 0, time.UTC),
		time.Date(2023, 1, 4, 0, 0, 0, 0, time.UTC),
		time.Date(2023, 1, 5, 0, 0, 0, 0, time.UTC),
		time.Date(2023, 1, 6, 0, 0, 0, 0, time.UTC),
	}
}
func (c *dummyCVForPurge) EvalTimes() []time.Time {
	pt := c.PredTimes()
	evals := make([]time.Time, len(pt))
	for i := range pt {
		evals[i] = pt[i].AddDate(0, 0, 1)
	}
	return evals
}
func (c *dummyCVForPurge) Indices() []int {
	return []int{0, 1, 2, 3, 4, 5}
}

func TestEmbargoBasicObject(t *testing.T) {
	cv := &dummyCVForEmbargo{
		BaseTimeSeriesCrossValidator: *timeseriescv.NewBaseTimeSeriesCrossValidator(2),
	}
	trainIndices := []int{0, 1, 2, 3, 4, 5, 6, 7}
	testIndices := []int{8, 9}
	embargoed := timeseriescv.Embargo(cv, trainIndices, testIndices, 9)
	assert.IsType(t, []int{}, embargoed)
	assert.True(t, len(embargoed) <= len(trainIndices))
}

type dummyCVForEmbargo struct {
	timeseriescv.BaseTimeSeriesCrossValidator
}

func (c *dummyCVForEmbargo) PredTimes() []time.Time {
	out := make([]time.Time, 10)
	for i := range out {
		out[i] = time.Date(2022, 1, 1+i, 0, 0, 0, 0, time.UTC)
	}
	return out
}
func (c *dummyCVForEmbargo) EvalTimes() []time.Time {
	pt := c.PredTimes()
	evals := make([]time.Time, len(pt))
	for i := range pt {
		evals[i] = pt[i].AddDate(0, 0, 1)
	}
	return evals
}
func (c *dummyCVForEmbargo) Indices() []int {
	ix := make([]int, 10)
	for i := range ix {
		ix[i] = i
	}
	return ix
}
func (c *dummyCVForEmbargo) EmbargoTD() time.Duration { return 86400 * time.Second } // 1 day

func TestComputeFoldBoundsObject(t *testing.T) {
	cv := &dummyCVForComputeFoldBounds{
		BaseTimeSeriesCrossValidator: *timeseriescv.NewBaseTimeSeriesCrossValidator(2),
	}
	bounds := timeseriescv.ComputeFoldBounds(cv, false)
	assert.IsType(t, []timeseriescv.FoldBound{}, bounds)
}

type dummyCVForComputeFoldBounds struct {
	timeseriescv.BaseTimeSeriesCrossValidator
}

func (c *dummyCVForComputeFoldBounds) Indices() []int {
	return []int{0, 1, 2, 3, 4, 5, 6, 7}
}

func TestPurgedWalkForwardCVSplit(t *testing.T) {
	X, y, predTimes, evalTimes := makeSimpleData(20, 0)
	cv := timeseriescv.NewPurgedWalkForwardCV(5)
	splits, err := cv.Split(X, y, predTimes, evalTimes)
	require.NoError(t, err)
	assert.Equal(t, 3, len(splits))
	for _, pair := range splits {
		assert.True(t, isDisjoint(pair.Train, pair.Test))
		assert.True(t, len(pair.Test) > 0)
	}
}

func TestCombPurgedKFoldCVSplit(t *testing.T) {
	X, y, predTimes, evalTimes := makeSimpleData(12, 0)
	cv := timeseriescv.NewCombPurgedKFoldCV(3)
	splits, err := cv.Split(X, y, predTimes, evalTimes)
	require.NoError(t, err)
	assert.Equal(t, 3, len(splits))
	for _, pair := range splits {
		assert.True(t, isDisjoint(pair.Train, pair.Test))
	}
}

func TestReprMethods(t *testing.T) {
	cv1 := timeseriescv.NewPurgedWalkForwardCV(4)
	cv2 := timeseriescv.NewCombPurgedKFoldCV(3)
	r1 := fmt.Sprintf("%T", cv1)
	r2 := fmt.Sprintf("%T", cv2)
	assert.Contains(t, r1, "PurgedWalkForwardCV")
	assert.Contains(t, r2, "CombPurgedKFoldCV")
}

func TestBaseRepr(t *testing.T) {
	cv := timeseriescv.NewBaseTimeSeriesCrossValidator(10)
	r := fmt.Sprintf("%T", cv)
	assert.Contains(t, r, "BaseTimeSeriesCrossValidator")
}

func TestPurgeEmptyObject(t *testing.T) {
	cv := &dummyCVForEmptyPurge{
		BaseTimeSeriesCrossValidator: *timeseriescv.NewBaseTimeSeriesCrossValidator(2),
	}
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("The code did not panic as expected")
		}
	}()
	timeseriescv.Purge(cv, 0, 0, 0)
}

type dummyCVForEmptyPurge struct {
	timeseriescv.BaseTimeSeriesCrossValidator
}

func (c *dummyCVForEmptyPurge) PredTimes() []time.Time {
	return []time.Time{}
}
func (c *dummyCVForEmptyPurge) EvalTimes() []time.Time {
	return []time.Time{}
}
func (c *dummyCVForEmptyPurge) Indices() []int {
	return []int{}
}

func TestEmbargoNoEmbargoObject(t *testing.T) {
	cv := &dummyCVNoEmbargo{
		BaseTimeSeriesCrossValidator: *timeseriescv.NewBaseTimeSeriesCrossValidator(2),
	}
	trainIndices := []int{0, 4}
	testIndices := []int{0, 4}
	embargoed := timeseriescv.Embargo(cv, trainIndices, testIndices, 4)
	assert.True(t, subset(embargoed, trainIndices))
}

type dummyCVNoEmbargo struct {
	timeseriescv.BaseTimeSeriesCrossValidator
}

func (c *dummyCVNoEmbargo) PredTimes() []time.Time {
	out := make([]time.Time, 5)
	for i := range out {
		out[i] = time.Date(2020, 1, 1+i, 0, 0, 0, 0, time.UTC)
	}
	return out
}
func (c *dummyCVNoEmbargo) EvalTimes() []time.Time {
	pt := c.PredTimes()
	evals := make([]time.Time, len(pt))
	for i := range pt {
		evals[i] = pt[i].AddDate(0, 0, 1)
	}
	return evals
}
func (c *dummyCVNoEmbargo) Indices() []int {
	ix := make([]int, 5)
	for i := range ix {
		ix[i] = i
	}
	return ix
}
func (c *dummyCVNoEmbargo) EmbargoTD() time.Duration { return 0 }

func subset(a, b []int) bool {
	mb := make(map[int]struct{}, len(b))
	for _, v := range b {
		mb[v] = struct{}{}
	}
	for _, v := range a {
		if _, ok := mb[v]; !ok {
			return false
		}
	}
	return true
}

func TestPurgedWalkForwardCVInvalidNTestSplits(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for invalid n_test_splits")
		}
	}()
	timeseriescv.NewPurgedWalkForwardCVWithOptions(2, 1)
}

func TestCombPurgedKFoldCVInvalid(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for CombPurgedKFoldCV invalid n_splits")
		}
	}()
	timeseriescv.NewCombPurgedKFoldCV(1)
}

// --- helpers ---

func isDisjoint(a, b []int) bool {
	mb := make(map[int]bool)
	for _, v := range a {
		mb[v] = true
	}
	for _, v := range b {
		if mb[v] {
			return false
		}
	}
	return true
}