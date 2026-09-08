package tests

import (
	"bytes"
	"fmt"
	"strings"
	"testing"

	"nathanrooy.com/particle-swarm-optimization/pso"
)

func simpleCost(x []float64) float64 {
	res := 0.0
	for _, v := range x {
		res += v * v
	}
	return res
}

func TestParticleInstanceAndAttributes(t *testing.T) {
	x0 := []float64{1, -1}
	p := pso.NewParticle(x0)
	if len(p.Position) != len(x0) {
		t.Errorf("particle Position len, want %d, got %d", len(x0), len(p.Position))
	}
	if len(p.Velocity) != len(x0) {
		t.Errorf("particle Velocity len, want %d, got %d", len(x0), len(p.Velocity))
	}
	// These are pointers to slices, so just checking presence
	_ = p.BestPosition
	_ = p.BestError
	_ = p.CurrentError
}

func TestParticleEvaluateAndPersonalBest(t *testing.T) {
	x0 := []float64{2, 3}
	p := pso.NewParticle(x0)
	p.Evaluate(simpleCost)
	errFirst := p.BestError
	p.Position = []float64{4, 5}
	p.Evaluate(simpleCost)
	valOld := errFirst
	valNew := simpleCost([]float64{4, 5})
	if p.BestError != valOld && p.BestError != valNew {
		t.Errorf("BestError not as expected, got %v, want %v or %v", p.BestError, valOld, valNew)
	}
	if p.CurrentError != valNew {
		t.Errorf("CurrentError after evaluate wrong, got %v", p.CurrentError)
	}
}

func TestParticleUpdateVelocityAndPosition(t *testing.T) {
	x0 := []float64{0.5, -0.5}
	p := pso.NewParticle(x0)
	p.BestPosition = append([]float64{}, x0...)
	posBestG := []float64{0.1, 0.2}
	oldV := append([]float64{}, p.Velocity...)

	p.UpdateVelocity(posBestG)
	if len(p.Velocity) != len(oldV) {
		t.Errorf("velocity length not preserved")
	}

	bounds := [][2]float64{{-1, 1}, {-1, 1}}
	p.Velocity = []float64{2, -2}
	p.UpdatePosition(bounds)
	for i, v := range p.Position {
		if v < -1 || v > 1 {
			t.Errorf("position[%d]=%v out of bounds [-1,1]", i, v)
		}
	}
}

func TestMinimizeBasic(t *testing.T) {
	x0 := []float64{1, 2}
	bounds := [][2]float64{{-5, 5}, {-5, 5}}
	errVal, pos := pso.Minimize(simpleCost, x0, bounds, 5, 10, false)
	if _, ok := errVal.(float64); !ok {
		t.Errorf("errVal is not a float64")
	}
	if len(pos) != len(x0) {
		t.Errorf("pos len got %d, want %d", len(pos), len(x0))
	}
}

func TestMinimizeVerboseOutput(t *testing.T) {
	x0 := []float64{0, 0}
	bounds := [][2]float64{{-1, 1}, {-1, 1}}

	var output bytes.Buffer
	pso.SetOutput(&output)
	defer pso.SetOutput(nil)

	_, _ = pso.Minimize(simpleCost, x0, bounds, 3, 2, true)
	got := output.String()
	if !strings.Contains(got, "iter:") {
		t.Errorf("verbose output missing 'iter:', got %q", got)
	}
	if !strings.Contains(got, "FINAL SOLUTION") {
		t.Errorf("verbose output missing 'FINAL SOLUTION', got %q", got)
	}
}

func TestMinimizeEdgeCaseZeroIterations(t *testing.T) {
	x0 := []float64{5, 7}
	bounds := [][2]float64{{-10, 10}, {-10, 10}}
	errVal, pos := pso.Minimize(simpleCost, x0, bounds, 2, 0, false)
	switch errVal.(type) {
	case float64, int:
	default:
		t.Errorf("errVal type %T not float64/int", errVal)
	}
	if len(pos) != len(x0) {
		t.Errorf("pos len got %d, want %d", len(pos), len(x0))
	}
}

func TestUpdatePositionHitsUpperBound(t *testing.T) {
	x0 := []float64{0.9, 0.0}
	p := pso.NewParticle(x0)
	bounds := [][2]float64{{0, 1}, {0, 1}}
	p.Velocity = []float64{0.5, 0.0}
	p.UpdatePosition(bounds)
	if p.Position[0] != 1.0 {
		t.Errorf("position[0] should be upper-bound, got %v", p.Position[0])
	}
	expected := x0[1] + p.Velocity[1]
	if p.Position[1] != expected {
		t.Errorf("position[1] should be %v, got %v", expected, p.Position[1])
	}
}

func TestUpdatePositionHitsLowerBound(t *testing.T) {
	x0 := []float64{0.0, -0.9}
	p := pso.NewParticle(x0)
	bounds := [][2]float64{{-1, 0}, {-1, 0}}
	p.Velocity = []float64{0.0, -0.5}
	p.UpdatePosition(bounds)
	if p.Position[1] != -1.0 {
		t.Errorf("position[1] should hit lower bound, got %v", p.Position[1])
	}
	expected := x0[0] + p.Velocity[0]
	if p.Position[0] != expected {
		t.Errorf("position[0] should be %v, got %v", expected, p.Position[0])
	}
}