package public

import (
	"testing"
)

func Multiply(a, b int) int {
	return a * b
}

func TestMultiply(t *testing.T) {
	if Multiply(2, 3) != 6 {
		t.Errorf("Multiply(2,3) = %d, want 6", Multiply(2, 3))
	}
	if Multiply(-1, 2) != -2 {
		t.Errorf("Multiply(-1,2) = %d, want -2", Multiply(-1, 2))
	}
	if Multiply(0, 5) != 0 {
		t.Errorf("Multiply(0,5) = %d, want 0", Multiply(0, 5))
	}
}