package tests

import (
	"testing"
	"nathanrooy.com/particle-swarm-optimization/pso"
)

func TestSphereAllZeros(t *testing.T) {
	res := pso.Sphere([]float64{0, 0, 0})
	if res != 0 {
		t.Errorf("expected 0, got %v", res)
	}
}

func TestSphereSingleValue(t *testing.T) {
	res := pso.Sphere([]float64{3})
	if res != 9 {
		t.Errorf("expected 9, got %v", res)
	}
}

func TestSphereNegativeValues(t *testing.T) {
	res := pso.Sphere([]float64{-1, -2})
	if res != 5 {
		t.Errorf("expected 5, got %v", res)
	}
}

func TestSphereMixedValues(t *testing.T) {
	res := pso.Sphere([]float64{1, -2, 3})
	if res != 14 { // 1 + 4 + 9
		t.Errorf("expected 14, got %v", res)
	}
}

func TestSphereEmpty(t *testing.T) {
	res := pso.Sphere([]float64{})
	if res != 0 {
		t.Errorf("expected 0 for empty input, got %v", res)
	}
}

// In Go, can't simulate __main__ guard in same way, but check that Sphere exists
func TestModuleHasSphere(t *testing.T) {
	// If function doesn't exist, won't compile. Test is semantic placeholder.
	if pso.Sphere == nil {
		t.Error("Sphere function not found")
	}
}