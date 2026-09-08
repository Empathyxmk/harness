package public_tests

import (
	"testing"
	"nathanrooy.com/particle-swarm-optimization/pso"
)

func TestMinimizeWithSphereFunctionPublic(t *testing.T) {
	x0 := []float64{-2.0, 3.0}
	bounds := [][2]float64{{-10, 10}, {-10, 10}}
	err, pos := pso.Minimize(pso.Sphere, x0, bounds, 5, 12, false)
	if err > pso.Sphere(x0) {
		t.Errorf("err %v > sphere(x0)=%v", err, pso.Sphere(x0))
	}
	if len(pos) != len(x0) {
		t.Errorf("len(pos)=%d, want %d", len(pos), len(x0))
	}
}