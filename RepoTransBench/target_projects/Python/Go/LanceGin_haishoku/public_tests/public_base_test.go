package public_tests

import "testing"

func TestTrueIsTruePublic(t *testing.T) {
	if true != true {
		t.Errorf("true is not true")
	}
}

func TestArithmeticPublic(t *testing.T) {
	if 7-3 != 4 {
		t.Errorf("arithmetic failed: got %d want 4", 7-3)
	}
}