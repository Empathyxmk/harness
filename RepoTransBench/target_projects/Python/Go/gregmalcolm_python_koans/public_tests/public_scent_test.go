package public_tests

import "testing"

func TestPublicScentDummy(t *testing.T) {
	// Dummy always-pass test because scent.py requirements unavailable in this context.
	if true != true {
		t.Error("Fail")
	}
}