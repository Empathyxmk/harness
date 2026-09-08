package public_tests

import (
	"testing"
)

// Dummy Abx implementation
func abxAdd(a, b int) int {
	return a + b
}
func abxIsPositive(n int) bool {
	return n > 0
}

func TestAddDifferentValues(t *testing.T) {
	if got := abxAdd(7, 6); got != 13 {
		t.Errorf("expected abxAdd(7,6) == 13, got %d", got)
	}
	if got := abxAdd(-3, 3); got != 0 {
		t.Errorf("expected abxAdd(-3,3) == 0, got %d", got)
	}
}

func TestIsPositiveDifferentData(t *testing.T) {
	if !abxIsPositive(2024) {
		t.Error("expected abxIsPositive(2024) == true")
	}
	if abxIsPositive(-2025) {
		t.Error("expected abxIsPositive(-2025) == false")
	}
}