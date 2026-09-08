package public_tests

import (
	"math"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"lafan1/utils"
)

func TestQuaternionInverseIdentityPublic(t *testing.T) {
	q := []float64{0.6, 0.3, 0.5, 0.5}
	inv := utils.Qinv(q)
	ident := utils.Qmul(q, inv)
	assert.InDeltaSlice(t, []float64{1, 0, 0, 0}, ident, 1e-4)
}

func TestQuaternionMulIdentityLeftPublic(t *testing.T) {
	q := []float64{2, -2, 1, 4}
	ident := []float64{1, 0, 0, 0}
	product := utils.Qmul(ident, q)
	assert.InDeltaSlice(t, q, product, 1e-4)
}

func TestQuaternionMulIdentityRightPublic(t *testing.T) {
	q := []float64{-5, 7, -1, 0}
	ident := []float64{1, 0, 0, 0}
	product := utils.Qmul(q, ident)
	assert.InDeltaSlice(t, q, product, 1e-4)
}

func TestQuaternionNormPublic(t *testing.T) {
	q := []float64{3, 1, 4, 1}
	norm := math.Sqrt(3*3 + 1*1 + 4*4 + 1*1)
	nq := utils.Qnorm(q)
	for i, v := range nq {
		require.InEpsilon(t, q[i]/norm, v, 1e-7)
	}
}

func TestQuaternionSlerpSelfPublic(t *testing.T) {
	q := []float64{0.8, 0.2, 0.1, 0.5}
	out := utils.Slerp(q, q, 0.8)
	assert.InDeltaSlice(t, q, out, 1e-5)
}

func TestEulerToQuatAndBackPublic(t *testing.T) {
	e := []float64{0.35, -0.18, 0.47}
	q := utils.EulerToQuat(e)
	eBack := utils.QuatToEuler(q)
	require.Equal(t, len(e), len(eBack))
}

func TestQuaternionBroadcastPublic(t *testing.T) {
	qs := [][]float64{{2, 0, 0, 0}, {0.3, 0.6, 0.5, 0.2}}
	nqs := utils.QnormBatch(qs)
	for i, q := range qs {
		norm := math.Sqrt(0.0)
		for _, v := range q {
			norm += v * v
		}
		for j := range q {
			require.InEpsilon(t, q[j]/norm, nqs[i][j], 1e-5)
		}
	}
}

func TestQuaternionShapeRobustnessPublic(t *testing.T) {
	q := make([]float64, 4)
	for i := range q {
		q[i] = 4
	}
	inv := utils.Qinv(q)
	require.Equal(t, 4, len(inv))
	qs := make([][]float64, 3)
	for i := range qs {
		qs[i] = make([]float64, 4)
		for j := 0; j < 4; j++ {
			qs[i][j] = 2
		}
	}
	invs := utils.QinvBatch(qs)
	require.Equal(t, len(qs), len(invs))
	require.Equal(t, 4, len(invs[0]))
}