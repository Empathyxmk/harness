package componentbase

import (
	"testing"
)

func TestSubtractionIsCorrect(t *testing.T) {
	if 5-3 != 2 {
		t.Errorf("Expected 2, got %d", 5-3)
	}
}

func TestMultiplicationIsCorrect(t *testing.T) {
	if 3*5 != 15 {
		t.Errorf("Expected 15, got %d", 3*5)
	}
}