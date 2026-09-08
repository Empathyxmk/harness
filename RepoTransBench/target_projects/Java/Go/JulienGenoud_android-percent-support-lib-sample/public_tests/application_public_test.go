package public_tests

import (
	"testing"
)

// See description in ApplicationPublicTest.java: Tests instantiation with different class name.

type Application struct{}

func NewApplication() *Application {
	return &Application{}
}

func TestApplicationPublicInstantiation(t *testing.T) {
	app := NewApplication()
	if app == nil {
		t.Error("Expected Application instance to be not nil in public test")
	}
}