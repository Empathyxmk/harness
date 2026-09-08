package original

import "testing"

func TestSocksLeonids_AdditionIsCorrect(t *testing.T) {
	if 2+2 != 4 {
		t.Errorf("Expected 2+2=4, got %v", 2+2)
	}
}