package original

import (
	"testing"
	"underscore"
)

func TestRandom(t *testing.T) {
	num := underscore.Random(1, 10)
	if num < 1 || num > 10 {
		t.Errorf("expected between 1 and 10 inclusive, got %d", num)
	}
}