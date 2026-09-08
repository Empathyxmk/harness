package original

import (
	"testing"
)

// See above for the test fibonacci(n) implementation.

func TestFibonacciZeroAndNegative(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for fibonacci(0)")
		}
	}()
	fibonacci(0)

	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for fibonacci(-5)")
		}
	}()
	fibonacci(-5)
}