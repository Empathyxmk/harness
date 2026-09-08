package tests

import (
	"testing"
)

func TestBasicTestPass(t *testing.T) {
	assertTrue(t, true)
}

func TestBasicTestFail(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Fatalf("expected panic but none occurred")
		}
	}()
	assertTrue(t, false)
}