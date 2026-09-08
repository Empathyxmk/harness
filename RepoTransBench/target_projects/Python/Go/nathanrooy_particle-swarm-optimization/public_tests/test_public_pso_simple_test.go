package public_tests

import (
	"bytes"
	"strings"
	"testing"

	"nathanrooy.com/particle-swarm-optimization/pso"
)

func publicCost(x []float64) float64 {
	res := 0.0
	for _, v := range x {
		res += v * v
	}
	return res + 1
}

func TestParticleInstanceAndAttributesPublic(t *testing.T) {
	x0 := []float64{7, -3, 2}
	p := pso.NewParticle(x0)
	if len(p.Position) != len(x0) {
		t.Errorf("particle Position len, want %d, got %d", len(x0), len(p.Position))
	}
	if len(p.Velocity) != len(x0) {
		t.Errorf("particle Velocity len, want %d, got %d", len(x0), len(p.Velocity))
	}
	_ = p.BestPosition
	_ = p.BestError
	_ = p.CurrentError
}

func TestParticleEvaluateAndPersonalBestPublic(t *testing.T) {
	x0 := []float64{5, 6}
	p := pso.NewParticle(x0)
	p.Evaluate(publicCost)
	errFirst := p.BestError
	p.Position = []float64{1, 2}
	p.Evaluate(publicCost)
	valOld := errFirst
	valNew := publicCost([]float64{1, 2})
	if p.BestError != valOld && p.BestError != valNew {
		t.Errorf("BestError not as expected, got %v, want %v or %v", p.BestError, valOld, valNew)
	}
	if p.CurrentError != valNew {
		t.Errorf("CurrentError after evaluate wrong, got %v", p.CurrentError)
	}
}

func TestParticleUpdateVelocityAndPositionPublic(t *testing.T) {
	x0 := []float64{0.75, -0.25, 0.50}
	p := pso.NewParticle(x0)
	p.BestPosition = append([]float64{}, x0...)
	posBestG := []float64{0.0, 0.5, -0.5}
	oldV := append([]float64{}, p.Velocity...)

	p.UpdateVelocity(posBestG)
	if len(p.Velocity) != len(oldV) {
		t.Errorf("velocity length not preserved")
	}

	bounds := [][2]float64{{-2, 2}, {-2, 2}, {-2, 2}}
	p.Velocity = []float64{3, -3, 4}
	p.UpdatePosition(bounds)
	for i, v := range p.Position {
		if v < -2 || v > 2 {
			t.Errorf("position[%d]=%v out of bounds [-2,2]", i, v)
		}
	}
}

func TestMinimizeBasicPublic(t *testing.T) {
	x0 := []float64{2, -3, 1}
	bounds := [][2]float64{{-7, 7}, {-7, 7}, {-7, 7}}
	err, pos := pso.Minimize(publicCost, x0, bounds, 4, 8, false)
	if _, ok := err.(float64); !ok {
		t.Errorf("err is not float64")
	}
	if len(pos) != len(x0) {
		t.Errorf("pos len got %d, want %d", len(pos), len(x0))
	}
}

func TestMinimizeVerboseOutputPublic(t *testing.T) {
	x0 := []float64{-1, 1}
	bounds := [][2]float64{{-2, 2}, {-2, 2}}

	var output bytes.Buffer
	pso.SetOutput(&output)
	defer pso.SetOutput(nil)

	_, _ = pso.Minimize(publicCost, x0, bounds, 3, 2, true)
	got := output.String()
	if !strings.Contains(got, "iter:") {
		t.Errorf("verbose output missing 'iter:', got %q", got)
	}
	if !strings.Contains(got, "FINAL SOLUTION") {
		t.Errorf("verbose output missing 'FINAL SOLUTION', got %q", got)
	}
}

func TestMinimizeEdgeCaseZeroIterationsPublic(t *testing.T) {
	x0 := []float64{6, 8}
	bounds := [][2]float64{{-20, 20}, {-20, 20}}
	err, pos := pso.Minimize(publicCost, x0, bounds, 2, 0, false)
	switch err.(type) {
	case float64, int:
	default:
		t.Errorf("err type %T not float64/int", err)
	}
	if len(pos) != len(x0) {
		t.Errorf("pos len got %d, want %d", len(pos), len(x0))
	}
}

func TestUpdatePositionHitsUpperBoundPublic(t *testing.T) {
	x0 := []float64{0.7, 0.4}
	p := pso.NewParticle(x0)
	bounds := [][2]float64{{0, 1}, {0, 1}}
	p.Velocity = []float64{0.0, 0.8}
	p.UpdatePosition(bounds)
	if p.Position[1] != 1.0 {
		t.Errorf("position[1] should be upper-bound, got %v", p.Position[1])
	}
	expected := x0[0] + p.Velocity[0]
	if p.Position[0] != expected {
		t.Errorf("position[0] should be %v, got %v", expected, p.Position[0])
	}
}

func TestUpdatePositionHitsLowerBoundPublic(t *testing.T) {
	x0 := []float64{-0.8, 0.2}
	p := pso.NewParticle(x0)
	bounds := [][2]float64{{-1, 0}, {-1, 0}}
	p.Velocity = []float64{-0.5, 0.0}
	p.UpdatePosition(bounds)
	if p.Position[0] != -1.0 {
		t.Errorf("position[0] should hit lower bound, got %v", p.Position[0])
	}
	expected := x0[1] + p.Velocity[1]
	if p.Position[1] != expected {
		t.Errorf("position[1] should be %v, got %v", expected, p.Position[1])
	}
}