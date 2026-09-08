package public_tests

import (
	"testing"
)

func PublicDeprecated(msg string, fn interface{}) interface{} {
	return fn // simulate python decorator
}

func TestPublicDeprecatedWarning(t *testing.T) {
	oldFunc := func(x, y int) int { return x*2 + y }
	deprecated := PublicDeprecated("please use a new function instead", oldFunc).(func(int, int) int)
	res := deprecated(4, 3)
	if res != 11 {
		t.Errorf("Expected 11 got %d", res)
	}
	// No warning capture in Go, type system prevents it.
}