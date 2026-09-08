package public_tests

import (
	"testing"
)

func TestPublicTestSimpleAssert(t *testing.T) {
	if 2+2 != 4 {
		t.Fatalf("math failed")
	}
}

func TestPublicTestShouldFail(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Fatalf("expected panic but none occurred")
		}
	}()
	panic("should panic")
}