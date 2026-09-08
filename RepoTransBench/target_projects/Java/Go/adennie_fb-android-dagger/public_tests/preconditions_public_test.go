package public_tests

import (
	"errors"
	"testing"
)

func checkNotNull(obj interface{}, msg ...string) {
	if obj == nil {
		if len(msg) > 0 {
			panic(errors.New(msg[0]))
		}
		panic(errors.New("NullPointerException"))
	}
}

func checkState(condition bool, msg ...string) {
	if !condition {
		if len(msg) > 0 {
			panic(errors.New(msg[0]))
		}
		panic(errors.New("IllegalStateException"))
	}
}

func TestCheckNotNullNotNullPublic(t *testing.T) {
	myString := "notNullPublic"
	checkNotNull(myString, "Must not be null")
	checkNotNull(myString)
	myInt := 5
	checkNotNull(myInt)
}

func TestCheckNotNullNullPublic(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for nil value")
		}
	}()
	checkNotNull(nil, "Error: is null")
}

func TestCheckStateTruePublic(t *testing.T) {
	checkState(2 > 1, "True expected")
	checkState(true)
}

func TestCheckStateFalsePublic(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for false state")
		}
	}()
	checkState(3 < 1, "Should fail")
}