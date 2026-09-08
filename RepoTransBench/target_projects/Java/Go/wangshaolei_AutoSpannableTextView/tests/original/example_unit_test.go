package original

import (
	"testing"
)

func TestAdditionIsCorrect(t *testing.T) {
	result := 2 + 2
	expected := 4
	if result != expected {
		t.Errorf("Addition is not correct: got %d, want %d", result, expected)
	}
}