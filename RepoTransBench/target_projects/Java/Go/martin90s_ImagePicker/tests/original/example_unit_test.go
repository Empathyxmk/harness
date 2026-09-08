package original

import (
	"testing"
)

func TestAdditionIsCorrect(t *testing.T) {
	if 2+2 != 4 {
		t.Error("Expected 2 + 2 == 4")
	}
}