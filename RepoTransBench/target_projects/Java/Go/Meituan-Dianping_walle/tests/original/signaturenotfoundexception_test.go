package original

import (
	"errors"
	"testing"
)

// SignatureNotFoundException replacement for Go.
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

func TestSignatureNotFoundException_ConstructorMessage(t *testing.T) {
	ex := NewSignatureNotFoundException("test message").(*SignatureNotFoundException)
	if ex.Message != "test message" {
		t.Errorf("expected message 'test message', got '%v'", ex.Message)
	}
	if ex.Cause != nil {
		t.Errorf("expected nil cause, got %v", ex.Cause)
	}
}

func TestSignatureNotFoundException_ConstructorMessageAndCause(t *testing.T) {
	cause := errors.New("cause")
	ex := NewSignatureNotFoundExceptionWithCause("err", cause).(*SignatureNotFoundException)
	if ex.Message != "err" {
		t.Errorf("expected message 'err', got '%v'", ex.Message)
	}
	if ex.Cause != cause {
		t.Errorf("expected cause '%v', got '%v'", cause, ex.Cause)
	}
}