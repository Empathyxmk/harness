package public_tests

import (
	"errors"
	"testing"
)

type PaperDbException struct {
	message string
	cause   error
}

func (e *PaperDbException) Error() string {
	return e.message
}
func (e *PaperDbException) Unwrap() error {
	return e.cause
}

func TestMessageConstructorPublic(t *testing.T) {
	ex := &PaperDbException{message: "fail-public"}
	if ex.Error() != "fail-public" {
		t.Errorf("Expected message 'fail-public', got %q", ex.Error())
	}
}

func TestMessageAndThrowableConstructorPublic(t *testing.T) {
	tCause := errors.New("public-cause")
	ex := &PaperDbException{message: "fail-public2", cause: tCause}
	if ex.Error() != "fail-public2" {
		t.Errorf("Expected message 'fail-public2', got %q", ex.Error())
	}
	if !errors.Is(ex, tCause) && ex.cause != tCause {
		t.Errorf("Expected cause 'public-cause', got %+v", ex.cause)
	}
}