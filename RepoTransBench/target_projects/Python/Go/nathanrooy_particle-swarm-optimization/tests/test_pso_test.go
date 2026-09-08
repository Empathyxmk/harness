package tests

import (
	"testing"
	"nathanrooy.com/particle-swarm-optimization/pso"
)

func TestMinimizeWithSphereFunction(t *testing.T) {
	x0 := []float64{1.0, 2.0}
	bounds := [][2]float64{{-5, 5}, {-5, 5}}
	err, pos := pso.Minimize(pso.Sphere, x0, bounds, 4, 15, false)
	if err > pso.Sphere(x0) {
		t.Errorf("err %v > sphere(x0)=%v", err, pso.Sphere(x0))
	}
	if len(pos) != len(x0) {
		t.Errorf("len(pos)=%d, want %d", len(pos), len(x0))
	}
}