package public_tests

import (
	"testing"
)

type InvalidJsonException struct {
	msg string
}
func NewInvalidJsonException(msg string) *InvalidJsonException {
	return &InvalidJsonException{msg: msg}
}
func (e *InvalidJsonException) Error() string {
	return e.msg
}

func TestMessage_public(t *testing.T) {
	e := NewInvalidJsonException("New message for public test")
	if e.Error() != "New message for public test" {
		t.Errorf("expected message, got %q", e.Error())
	}
}

func TestNullMessage_public(t *testing.T) {
	e := NewInvalidJsonException("")
	if e.Error() != "" {
		t.Errorf("expected empty string, got %q", e.Error())
	}
}