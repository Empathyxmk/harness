package original

import "testing"

func TestAdditionIsCorrect(t *testing.T) {
	if 2+2 != 4 {
		t.Errorf("2 + 2 should equal 4")
	}
}