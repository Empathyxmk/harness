package original

import (
	"errors"
	"strings"
	"testing"
)

type InvalidJsonException struct {
	msg string
	cause error
}

func NewInvalidJsonException(msg string, cause error) *InvalidJsonException {
	return &InvalidJsonException{msg: msg, cause: cause}
}
func (e *InvalidJsonException) Error() string {
	return e.msg
}
func (e *InvalidJsonException) Cause() error {
	return e.cause
}

func TestConstructorWithMessageAndThrowable(t *testing.T) {
	cause := errors.New("test")
	ex := NewInvalidJsonException("message", cause)
	if !strings.Contains(ex.Error(), "message") {
		t.Error("Message not contained in Error()")
	}
	if ex.Cause() != cause {
		t.Error("Cause not set or does not match")
	}
}