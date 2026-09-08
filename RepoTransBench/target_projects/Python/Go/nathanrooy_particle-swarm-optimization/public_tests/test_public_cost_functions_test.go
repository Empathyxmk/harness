package public_tests

import (
	"testing"
	"nathanrooy.com/particle-swarm-optimization/pso"
)

func TestSphereAllZerosPublic(t *testing.T) {
	res := pso.Sphere([]float64{0, 0, 0, 0})
	if res != 0 {
		t.Errorf("expected 0, got %v", res)
	}
}

func TestSphereSingleValuePublic(t *testing.T) {
	res := pso.Sphere([]float64{4})
	if res != 16 {
		t.Errorf("expected 16, got %v", res)
	}
}

func TestSphereNegativeValuesPublic(t *testing.T) {
	res := pso.Sphere([]float64{-3, -2})
	if res != 13 {
		t.Errorf("expected 13, got %v", res)
	}
}

func TestSphereMixedValuesPublic(t *testing.T) {
	res := pso.Sphere([]float64{2, -3, 4})
	if res != 29 { // 4 + 9 + 16
		t.Errorf("expected 29, got %v", res)
	}
}

func TestSphereEmptyPublic(t *testing.T) {
	res := pso.Sphere([]float64{})
	if res != 0 {
		t.Errorf("expected 0 for empty input, got %v", res)
	}
}

// In Go, can't simulate __main__ guard; just check function exists.
func TestModuleHasSpherePublic(t *testing.T) {
	if pso.Sphere == nil {
		t.Error("Sphere function not found")
	}
}