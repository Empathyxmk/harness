package original

import (
	"testing"
)

func TestFieldUtilsUsage(t *testing.T) {
	// Simulated test: Utility function usage.
	val := helperAdd(2, 3)
	if val != 5 {
		t.Errorf("Expected 2 + 3 to equal 5, got %d", val)
	}
}

func helperAdd(a, b int) int {
	return a + b
}