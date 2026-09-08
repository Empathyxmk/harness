package public_tests

import (
	"testing"

	"yourmodule/rajinipp/rajiniworld"
)

func TestPublicVarsAndFunctionsDictNonEmpty(t *testing.T) {
	if rajiniworld.Vars == nil {
		t.Error("rajiniworld.Vars should not be nil")
	}
	if rajiniworld.Funcs == nil {
		t.Error("rajiniworld.Funcs should not be nil")
	}
}