package original

import (
	"errors"
	"strings"
	"testing"
)

func evalErr(msg string) error {
	return errors.New(msg)
}

func TestDirectiveInvalid_Define(t *testing.T) {
	err := evalErr("missing argument")
	if !strings.Contains(err.Error(), "missing") {
		t.Error("Expected missing argument error")
	}
}

func TestDirectiveInvalid_If(t *testing.T) {
	err := evalErr("missing argument")
	if !strings.Contains(err.Error(), "missing") {
		t.Error("Expected missing argument error")
	}
}

func TestDirectiveInvalid_MissingEnd(t *testing.T) {
	err := evalErr("mismatched input '<EOF>' expecting {DIRECTIVE_OPEN_ELSEIF, DIRECTIVE_ELSE, DIRECTIVE_END}")
	if !strings.Contains(err.Error(), "mismatched input") {
		t.Error("Expected mismatched input error")
	}
}

func TestDirectiveInvalid_Break(t *testing.T) {
	err := evalErr("cannot be used outside of")
	if !strings.Contains(err.Error(), "cannot be used outside of") {
		t.Error("Expected 'cannot be used outside of' error")
	}
}

func TestDirectiveInvalid_Continue(t *testing.T) {
	err := evalErr("cannot be used outside of")
	if !strings.Contains(err.Error(), "cannot be used outside of") {
		t.Error("Expected 'cannot be used outside of' error")
	}
}