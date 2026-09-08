package public_tests

import "testing"

// Use the fibonacci implementation from original tests

func fibonacci(n int) int {
	if n <= 2 {
		return 1
	}
	return fibonacci(n-1) + fibonacci(n-2)
}

func TestFibonacciLow(t *testing.T) {
	if got := fibonacci(7); got != 13 {
		t.Errorf("Expected 13, got %d", got)
	}
	if got := fibonacci(8); got != 21 {
		t.Errorf("Expected 21, got %d", got)
	}
}

func TestFibonacciHighDifferentInputs(t *testing.T) {
	if got := fibonacci(10); got != 55 {
		t.Errorf("Expected 55, got %d", got)
	}
	if got := fibonacci(11); got != 89 {
		t.Errorf("Expected 89, got %d", got)
	}
	if got := fibonacci(12); got != 144 {
		t.Errorf("Expected 144, got %d", got)
	}
}

func TestFibonacciEdge(t *testing.T) {
	if fibonacci(1) != 1 {
		t.Errorf("Expected fibonacci(1)==1")
	}
	if fibonacci(2) != 1 {
		t.Errorf("Expected fibonacci(2)==1")
	}
}