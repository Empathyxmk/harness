package original

import (
	"testing"
)

// Simulate the Series class with needed functions for testing.
// These would normally reference actual implementation in ap01/series.go.

func fibonacci(n int) int {
	if n <= 2 {
		return 1
	}
	return fibonacci(n-1) + fibonacci(n-2)
}

// --- From ap01/SeriesTest.java (JUnit 3 style) ---

func TestSeriesFibonacci(t *testing.T) {
	if res := fibonacci(1); res != 1 {
		t.Errorf("Expected fibonacci(1) == 1, got %d", res)
	}
	if res := fibonacci(2); res != 1 {
		t.Errorf("Expected fibonacci(2) == 1, got %d", res)
	}
	if res := fibonacci(3); res != 2 {
		t.Errorf("Expected fibonacci(3) == 2, got %d", res)
	}
}

// --- From src/test/java/ap01/SeriesTest.java (JUnit 5) ---

func TestFibonacciBaseCases(t *testing.T) {
	if got := fibonacci(1); got != 1 {
		t.Errorf("Expected fibonacci(1) == 1, got %d", got)
	}
	if got := fibonacci(2); got != 1 {
		t.Errorf("Expected fibonacci(2) == 1, got %d", got)
	}
}

func TestFibonacciSmallN(t *testing.T) {
	if got := fibonacci(3); got != 2 {
		t.Errorf("Expected fibonacci(3) == 2, got %d", got)
	}
	if got := fibonacci(4); got != 3 {
		t.Errorf("Expected fibonacci(4) == 3, got %d", got)
	}
	if got := fibonacci(5); got != 5 {
		t.Errorf("Expected fibonacci(5) == 5, got %d", got)
	}
}

func TestFibonacciLargerN(t *testing.T) {
	if got := fibonacci(8); got != 21 {
		t.Errorf("Expected fibonacci(8) == 21, got %d", got)
	}
}