package public_tests

import (
	"testing"
)

func TestMathDifferentInput(t *testing.T) {
	if got := 120 + 3; got != 123 {
		t.Errorf("expected 120 + 3 == 123, got %d", got)
	}
}