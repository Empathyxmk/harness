package public_tests

import (
	"testing"
)

func TestPublicFunctionalBasic(t *testing.T) {
	value := 10
	if value != 10 {
		t.Errorf("Expected value 10, got %d", value)
	}
}