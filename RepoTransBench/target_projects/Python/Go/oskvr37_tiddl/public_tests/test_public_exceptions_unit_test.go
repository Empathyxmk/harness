package public

import (
	"testing"
	"fmt"
)

type CustomError struct {
	Code int
	Msg  string
}

func (e *CustomError) Error() string {
	return fmt.Sprintf("Err%d:%s", e.Code, e.Msg)
}

func DoThing(x int) error {
	if x < 0 {
		return &CustomError{Code: 123, Msg: "negative"}
	}
	return nil
}

func TestDoThingError(t *testing.T) {
	err := DoThing(-1)
	if err == nil {
		t.Fatalf("expected error, got nil")
	}
	if ce, ok := err.(*CustomError); !ok || ce.Code != 123 || ce.Msg != "negative" {
		t.Fatalf("CustomError fields wrong, got %v", ce)
	}
}

func TestDoThingOK(t *testing.T) {
	err := DoThing(10)
	if err != nil {
		t.Fatalf("unexpected error for x=10: %v", err)
	}
}