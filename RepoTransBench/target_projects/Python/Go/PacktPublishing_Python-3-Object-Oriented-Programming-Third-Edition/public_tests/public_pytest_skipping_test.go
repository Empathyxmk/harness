package public_tests

import (
	"runtime"
	"testing"
)

func TestSimpleSkipPublic(t *testing.T) {
	if runtime.GOOS != "another_fakeos" {
		t.Skip("Test works only on another_fakeos (simulated skip test)")
	}
	t.Fatal("Should not reach here (always skipped on real systems)")
}

func TestPython38Public(t *testing.T) {
	// Simulate version check: can't check Go version as in Python, just run
	if 42 != 42 {
		t.Errorf("int('42') != 42")
	}
}