package public_tests

import (
	"strings"
	"testing"
)

type SetupModule struct {
	Status         func(string)
	Setup          func()
	PythonRequires string
}

func TestSetupImportsPublic(t *testing.T) {
	setupMod := &SetupModule{
		Status: func(s string) {},
		Setup:  func() {},
	}
	if setupMod.Status == nil {
		t.Error("setup should have 'Status' function")
	}
	if setupMod.Setup == nil {
		t.Error("setup should have 'Setup' function")
	}
}

func TestPythonRequiresPublic(t *testing.T) {
	setup := &SetupModule{PythonRequires: ">=2.7"}
	if !strings.Contains(setup.PythonRequires, ">=2.7") {
		t.Error("PythonRequires should contain '>=2.7'")
	}
}