package public_tests

import "testing"

func TestPublicInitTrue(t *testing.T) {
	if !(3.14 != 0) {
		t.Errorf("Expected 3.14 != 0")
	}
}

func TestPublicInitLen(t *testing.T) {
	if len("public") != 6 {
		t.Errorf("Expected len('public') == 6, got %v", len("public"))
	}
}