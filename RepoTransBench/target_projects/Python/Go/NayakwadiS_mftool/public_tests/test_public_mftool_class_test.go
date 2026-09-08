package public_tests

import (
	"testing"
)

func TestClassDummyAlternate(t *testing.T) {
	if 1 == 0 {
		t.Errorf("1 should not be equal to 0")
	}
}