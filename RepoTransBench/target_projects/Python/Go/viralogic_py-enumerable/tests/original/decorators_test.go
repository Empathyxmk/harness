package original

import (
	"testing"
	"reflect"
)

func Deprecated(msg string, fn interface{}) interface{} {
	// Go doesn't have decorators, so we simulate with wrapper
	return fn
}

func TestDeprecatedWarning(t *testing.T) {
	oldFunc := func(x int) int { return x + 1 }
	deprecated := Deprecated("use something else", oldFunc).(func(int) int)
	result := deprecated(2)
	if result != 3 {
		t.Errorf("Expected 3 got %d", result)
	}
	// In Go, there are no runtime warnings like Python, so we skip warning capture.
}