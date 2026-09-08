package original

import (
	"testing"
)

type NoElementsError struct{ msg string }
type NullArgumentError struct{ msg string }
type NoMatchingElement struct{ msg string }
type MoreThanOneMatchingElement struct{ msg string }

func (e NoElementsError) Error() string               { return e.msg }
func (e NullArgumentError) Error() string             { return e.msg }
func (e NoMatchingElement) Error() string             { return e.msg }
func (e MoreThanOneMatchingElement) Error() string    { return e.msg }

func TestExceptionsInstantiation(t *testing.T) {
	e1 := NoElementsError{"msg"}
	e2 := NullArgumentError{"msg2"}
	e3 := NoMatchingElement{"msg3"}
	e4 := MoreThanOneMatchingElement{"msg4"}
	if e1.Error() != "msg" {
		t.Errorf("NoElementsError msg mismatch")
	}
	if e2.Error() != "msg2" {
		t.Errorf("NullArgumentError msg mismatch")
	}
	if e3.Error() != "msg3" {
		t.Errorf("NoMatchingElement msg mismatch")
	}
	if e4.Error() != "msg4" {
		t.Errorf("MoreThanOneMatchingElement msg mismatch")
	}
}