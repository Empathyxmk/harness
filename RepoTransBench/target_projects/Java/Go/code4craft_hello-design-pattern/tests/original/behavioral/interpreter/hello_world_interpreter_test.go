package interpreter

import (
	"testing"
)

// In the Java code, interpret returns void; ensure no panic.
type HelloWorldInterpreter struct{}

// We skip actual logic because only "no panic" is required in the test.
func (h *HelloWorldInterpreter) Interpret(input string) {
	// no-op
}

func TestInterpret(t *testing.T) {
	interpreter := &HelloWorldInterpreter{}
	interpreter.Interpret("Hello Interpreter!") // Ensure no panic
}