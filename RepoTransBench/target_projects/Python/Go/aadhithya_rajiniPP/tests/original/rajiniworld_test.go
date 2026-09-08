package original

import (
	"testing"

	"yourmodule/rajinipp/rajiniworld"
)

func TestVarsAndFunctionsAreDicts(t *testing.T) {
	if rajiniworld.Vars == nil {
		t.Error("rajinipp.__rajiniworld__.Vars should not be nil")
	}
	if rajiniworld.Funcs == nil {
		t.Error("rajinipp.__rajiniworld__.Funcs should not be nil")
	}
}