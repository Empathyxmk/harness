package public_tests

import (
	"testing"
)

func TestManualMainPublicDummy(t *testing.T) {
	// Dummy public test, always passes.
	if true != true {
		t.Fatal("Dummy public test should always pass")
	}
}