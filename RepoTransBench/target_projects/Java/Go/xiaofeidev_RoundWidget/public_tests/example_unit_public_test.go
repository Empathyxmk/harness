package public_tests

import (
	"testing"
)

func TestAdditionIsCorrectPublic(t *testing.T) {
	if got := 5 + 5; got != 10 {
		t.Errorf("expected 10, got %v", got)
	}
}