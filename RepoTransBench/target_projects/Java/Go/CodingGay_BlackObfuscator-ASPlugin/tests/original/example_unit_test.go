package original

import (
	"testing"
)

func TestAdditionIsCorrect(t *testing.T) {
	if got := 2 + 2; got != 4 {
		t.Errorf("expected 2 + 2 == 4, got %d", got)
	}
}