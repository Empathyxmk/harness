package original

import (
	"errors"
	"testing"
)

func SafeDiv(a, b int) (int, error) {
	if b == 0 {
		return 0, errors.New("division by zero")
	}
	return a / b, nil
}

func TestSafeDivNormal(t *testing.T) {
	res, err := SafeDiv(10, 2)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if res != 5 {
		t.Errorf("SafeDiv(10,2) = %d, want 5", res)
	}
}

func TestSafeDivZeroDivisor(t *testing.T) {
	_, err := SafeDiv(5, 0)
	if err == nil {
		t.Errorf("Expected error for division by zero, got nil")
	}
}