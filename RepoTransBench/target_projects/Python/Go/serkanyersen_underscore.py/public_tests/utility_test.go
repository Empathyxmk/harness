package public_tests

import (
	"testing"
	"underscore"
)

func TestRandomPublic(t *testing.T) {
	num := underscore.Random(20, 25)
	if num < 20 || num > 25 {
		t.Errorf("expected random between 20 and 25 inclusive, got %d", num)
	}
}