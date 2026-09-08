package public_tests

import (
	"math"
	"testing"
)

func capValue(val, min, max float64) float64 {
	if val < min {
		return min
	}
	if val > max {
		return max
	}
	return val
}
func averagePublic(a, b float64) float64 {
	return (a + b) / 2.0
}

func TestCapIncreasesSmall(t *testing.T) {
	if capValue(7.0, 2.0, 20.0) != 7.0 {
		t.Error("Expected 7.0")
	}
}
func TestCapCapsHigh(t *testing.T) {
	if capValue(30.0, 5.0, 25.0) != 25.0 {
		t.Error("Expected 25.0")
	}
}
func TestCapCapsLow(t *testing.T) {
	if capValue(1.5, 3.5, 10.0) != 3.5 {
		t.Error("Expected 3.5")
	}
}
func TestAverageWide(t *testing.T) {
	if math.Abs(averagePublic(2.0, 8.0) - 5.0) > 1e-8 {
		t.Error("Expected 5.0")
	}
}
func TestAverageNegative(t *testing.T) {
	if math.Abs(averagePublic(-5.0, 0.0) - -2.5) > 1e-8 {
		t.Error("Expected -2.5")
	}
}