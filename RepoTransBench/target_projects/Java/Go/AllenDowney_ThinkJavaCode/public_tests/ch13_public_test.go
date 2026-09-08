package public_tests

import "testing"

func TestPublicLogicCh13(t *testing.T) {
	if 5 > 10 {
		t.Errorf("Should be false for public tests")
	}
}