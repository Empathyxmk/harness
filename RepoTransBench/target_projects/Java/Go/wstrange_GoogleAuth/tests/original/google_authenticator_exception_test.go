package original

import (
	"errors"
	"testing"
)

type GoogleAuthenticatorExceptionGo struct {
	msg   string
	cause error
}

func (e *GoogleAuthenticatorExceptionGo) Error() string {
	return e.msg
}

func (e *GoogleAuthenticatorExceptionGo) Unwrap() error {
	return e.cause
}

func TestExceptionMessage(t *testing.T) {
	ex := &GoogleAuthenticatorExceptionGo{msg: "A message"}
	if ex.Error() != "A message" {
		t.Errorf("Expected 'A message', got '%s'", ex.Error())
	}
}

func TestExceptionCause(t *testing.T) {
	root := errors.New("root")
	ex := &GoogleAuthenticatorExceptionGo{msg: "A message", cause: root}
	if ex.Error() != "A message" {
		t.Errorf("Expected 'A message', got '%s'", ex.Error())
	}
	if ex.cause != root {
		t.Errorf("Expected cause set, got %v", ex.cause)
	}
}