package original

import (
	"math"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"lafan1/utils"
)

func TestQuatInvUnitIdentity(t *testing.T) {
	x := []float64{1.0, 0.0, 0.0, 0.0}
	inv := utils.QuatInvUnit(x)
	qMult := utils.QuatMultUnit(x, inv)
	assert.InEpsilonSlice(t, []float64{1.0, 0.0, 0.0, 0.0}, qMult, 1e-7)
}

func TestQuatMultUnitBasic(t *testing.T) {
	x := []float64{1.0, 0.0, 0.0, 0.0}
	y := []float64{1.0, 0.0, 0.0, 0.0}
	z := utils.QuatMultUnit(x, y)
	assert.InEpsilonSlice(t, []float64{1.0, 0.0, 0.0, 0.0}, z, 1e-7)
}

func TestQuatMultUnitNontrivial(t *testing.T) {
	x := []float64{0.0, 1.0, 0.0, 0.0}
	y := []float64{0.0, 0.0, 1.0, 0.0}
	z := utils.QuatMultUnit(x, y)
	absZ := make([]float64, len(z))
	for i, val := range z {
		absZ[i] = math.Abs(val)
	}
	expect := []float64{0, 0, 0, 1}
	assert.ElementsMatch(t, expect, absZ)
}

func TestQuatMultUnitBroadcast(t *testing.T) {
	q1 := [][]float64{{1, 0, 0, 0}, {0, 1, 0, 0}}
	q2 := [][]float64{{1, 0, 0, 0}, {0, 1, 0, 0}}
	z := utils.QuatMultUnitBatch(q1, q2)
	if len(z) != 2 || len(z[0]) != 4 || len(z[1]) != 4 {
		t.Fatalf("shape mismatch got %v", z)
	}
}

func TestQuatMultUnitBadshape(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for invalid quaternion shape")
		}
	}()
	x := []float64{1, 0, 0} // wrong size
	y := []float64{1, 0, 0, 0}
	_ = utils.QuatMultUnit(x, y)
}

func TestQuatFkWrongShape(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for FK shape error")
		}
	}()
	lrot := make([][]float64, 2)
	for i := range lrot {
		lrot[i] = make([]float64, 4)
	}
	lpos := make([][]float64, 3)
	for i := range lpos {
		lpos[i] = make([]float64, 3)
	}
	parents := []int{-1, 0}
	utils.QuatFK(lrot, lpos, parents)
}

func TestQuatFkBadNumParents(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for wrong #parents")
		}
	}()
	lrot := make([][]float64, 2)
	for i := range lrot {
		lrot[i] = make([]float64, 4)
	}
	lpos := make([][]float64, 2)
	for i := range lpos {
		lpos[i] = make([]float64, 3)
	}
	parents := []int{-1, 1, 5}
	utils.QuatFK(lrot, lpos, parents)
}

func TestQuatFkRootLinked(t *testing.T) {
	lrot := make([][]float64, 2)
	lpos := make([][]float64, 2)
	for i := 0; i < 2; i++ {
		lrot[i] = make([]float64, 4)
		lpos[i] = []float64{1, 1, 1}
	}
	parents := []int{-1, 0}
	grot, gpos := utils.QuatFK(lrot, lpos, parents)
	require.Equal(t, len(grot), 2)
	require.Equal(t, len(grot[0]), 4)
	require.Equal(t, len(gpos), 2)
	require.Equal(t, len(gpos[0]), 3)
}