package original

import "testing"
import "errors"

// Simulate Preconditions static utility
func CheckNotNull(val interface{}, msg string) interface{} {
	if val == nil {
		panic(errors.New(msg))
	}
	return val
}
func CheckArgument(condition bool, msg string) {
	if !condition {
		panic(errors.New(msg))
	}
}

func TestCheckNotNullThrows(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Fatal("CheckNotNull did not panic when val is nil")
		}
	}()
	CheckNotNull(nil, "err")
}

func TestCheckNotNullNoThrow(t *testing.T) {
	val := "a"
	_ = CheckNotNull(val, "err") // Should not panic
}

func TestCheckArgumentThrows(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Fatal("CheckArgument did not panic when condition is false")
		}
	}()
	CheckArgument(false, "arg error")
}

func TestCheckArgumentNoThrow(t *testing.T) {
	CheckArgument(true, "ok arg")
}