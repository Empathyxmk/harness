package original

import (
	"errors"
	"testing"
)

func checkState(condition bool, msg ...string) {
	if !condition {
		if len(msg) > 0 {
			panic(errors.New(msg[0]))
		}
		panic(errors.New("Illegal state"))
	}
}

func TestCheckState_TrueCondition(t *testing.T) {
	checkState(true, "This message should not be seen.")
}

func TestCheckState_FalseCondition(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for false condition")
		}
	}()
	checkState(false, "This is an error message.")
}

func TestCheckState_FalseConditionWithMessage(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for false condition")
		} else {
			if e, ok := r.(error); ok {
				if e.Error() != "Custom error message" {
					t.Errorf("Unexpected error message: %v", e.Error())
				}
			} else {
				t.Errorf("Unexpected panic type: %v", r)
			}
		}
	}()
	checkState(false, "Custom error message")
}