package original

import (
	"math"
	"testing"
)

// Simulate MathUtil with only roundTowards for test.
func roundTowards(value float64, target int) int {
	if value < float64(target) {
		return int(math.Ceil(value))
	} else if value > float64(target) {
		return int(math.Floor(value))
	}
	return int(value)
}

func TestRoundTowards_lowValueLowerThanTarget(t *testing.T) {
	if got := roundTowards(0.3, 1); got != 1 {
		t.Errorf("Expected 1, got %d", got)
	}
}
func TestRoundTowards_lowValueHigherThanTarget(t *testing.T) {
	if got := roundTowards(0.3, 0); got != 0 {
		t.Errorf("Expected 0, got %d", got)
	}
}
func TestRoundTowards_highValueHigherThanTarget(t *testing.T) {
	if got := roundTowards(2.9, 2); got != 2 {
		t.Errorf("Expected 2, got %d", got)
	}
}
func TestRoundTowards_highValueLowerThanTarget(t *testing.T) {
	if got := roundTowards(2.9, 3); got != 3 {
		t.Errorf("Expected 3, got %d", got)
	}
}
func TestRoundTowards_valueEqualToTarget(t *testing.T) {
	if got := roundTowards(2.0, 2); got != 2 {
		t.Errorf("Expected 2, got %d", got)
	}
}
func TestRoundTowards_valueExactlyOneBiggerToLowerTarget(t *testing.T) {
	if got := roundTowards(3.0, 2); got != 3 {
		t.Errorf("Expected 3, got %d", got)
	}
}
func TestRoundTowards_valueExactlyOneSmallerToHigherTarget(t *testing.T) {
	if got := roundTowards(1.0, 2); got != 1 {
		t.Errorf("Expected 1, got %d", got)
	}
}
func TestRoundTowards_specialHighNumberToHigherTarget(t *testing.T) {
	hundredLow := 111 / 1.11 // 99.999999..
	if got := roundTowards(hundredLow, 100); got != 100 {
		t.Errorf("Expected 100, got %d", got)
	}
}
func TestRoundTowards_specialHighNumberToLowerTarget(t *testing.T) {
	hundredLow := 111 / 1.11
	if got := roundTowards(hundredLow+1, 100); got != 100 {
		t.Errorf("Expected 100, got %d", got)
	}
}
func TestRoundTowards_specialLowNumberToHigherTarget(t *testing.T) {
	highZero := 100 - (111 / 1.11)
	if got := roundTowards(5+highZero, 6); got != 6 {
		t.Errorf("Expected 6, got %d", got)
	}
}
func TestRoundTowards_specialLowNumberToLowerTarget(t *testing.T) {
	highZero := 100 - (111 / 1.11)
	if got := roundTowards(5+highZero, 5); got != 5 {
		t.Errorf("Expected 5, got %d", got)
	}
}