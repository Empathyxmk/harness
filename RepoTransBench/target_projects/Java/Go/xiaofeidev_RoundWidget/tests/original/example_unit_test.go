package original

import (
	"testing"
)

func TestAdditionIsCorrect(t *testing.T) {
	if 4 != 2+2 {
		t.Errorf("expected 4 == 2+2, but got %v", 2+2)
	}
}