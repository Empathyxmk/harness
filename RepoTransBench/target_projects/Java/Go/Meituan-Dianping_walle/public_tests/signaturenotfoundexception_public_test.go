package public_tests

import (
	"errors"
	"testing"
)

type SignatureNotFoundException struct {
	Message string
	Cause   error
}

func NewSignatureNotFoundException(message string) error {
	return &SignatureNotFoundException{Message: message}
}

func NewSignatureNotFoundExceptionWithCause(message string, cause error) error {
	return &SignatureNotFoundException{Message: message, Cause: cause}
}

func (e *SignatureNotFoundException) Error() string {
	return e.Message
}

func (e *SignatureNotFoundException) Unwrap() error {
	return e.Cause
}

func TestSignatureNotFoundExceptionPublic_ConstructorMessage_public(t *testing.T) {
	ex := NewSignatureNotFoundException("another message").(*SignatureNotFoundException)
	if ex.Message != "another message" {
		t.Errorf("expected message 'another message', got '%v'", ex.Message)
	}
	if ex.Cause != nil {
		t.Errorf("expected nil cause, got %v", ex.Cause)
	}
}

func TestSignatureNotFoundExceptionPublic_ConstructorMessageAndCause_public(t *testing.T) {
	cause := errors.New("public cause")
	ex := NewSignatureNotFoundExceptionWithCause("public error", cause).(*SignatureNotFoundException)
	if ex.Message != "public error" {
		t.Errorf("expected message 'public error', got '%v'", ex.Message)
	}
	if ex.Cause != cause {
		t.Errorf("expected cause '%v', got '%v'", cause, ex.Cause)
	}
}