package public_tests

import (
	"testing"
)

func TestMultiplicationIsCorrect(t *testing.T) {
	if 7*3 != 21 {
		t.Errorf("Expected 7 * 3 == 21")
	}
}