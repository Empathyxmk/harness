package public_tests

import "testing"

func TestLibraryExampleUnit_MultiplicationIsCorrect(t *testing.T) {
	if 3*4 != 12 {
		t.Errorf("Expected 3*4=12, got %v", 3*4)
	}
}