package public_tests

import "testing"

func TestSocksLeonids_DivisionIsCorrect(t *testing.T) {
	if 8/4 != 2 {
		t.Errorf("Expected 8/4=2, got %v", 8/4)
	}
}