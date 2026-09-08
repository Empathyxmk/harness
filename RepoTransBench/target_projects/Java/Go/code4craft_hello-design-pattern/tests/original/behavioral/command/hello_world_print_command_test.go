package command

import (
	"testing"
)

type HelloWorldPrintCommand struct{}

func (h *HelloWorldPrintCommand) Execute() {
	// Just a no-op; intended only to not throw
}

func TestPrintCommand(t *testing.T) {
	cmd := &HelloWorldPrintCommand{}
	cmd.Execute() // Should not panic
}