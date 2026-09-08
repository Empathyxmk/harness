package public_tests

import (
	"testing"
)

func TestMultiplicationIsCorrectPublic(t *testing.T) {
	result := 3 * 5
	expected := 15
	if result != expected {
		t.Errorf("Multiplication is not correct: got %d, want %d", result, expected)
	}
}