package original

import (
	"testing"
)

func TestAddition_IsCorrect(t *testing.T) {
	if 2+2 != 4 {
		t.Errorf("Expected 2+2=4, got %d", 2+2)
	}
}