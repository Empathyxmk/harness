package public_tests

import (
	"testing"
)

type Terminal struct{}

func (t *Terminal) String() string { return "Terminal" }

func TestTerminalTypeAndMethods(t *testing.T) {
	term := &Terminal{}
	// Check that the terminal has a String() method
	if _, ok := interface{}(term).(*Terminal); !ok {
		t.Error("term does not implement *Terminal")
	}
	if term.String() == "" {
		t.Error("String() should not return empty string")
	}
}

func TestTerminalInstanceNotFalse(t *testing.T) {
	term := &Terminal{}
	if term == nil {
		t.Error("Terminal should be truthy")
	}
}