package state

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestInitialState(t *testing.T) {
	ctx := NewHelloWorldStateContext()
	assert.NotNil(t, ctx)
	// Simulate toString
	assert.NotNil(t, ctx.HelloWorld())
}

func TestStateTransitionsManual(t *testing.T) {
	ctx := NewHelloWorldStateContext()
	// In Java: transition through all states using reflection (private)
	// In Go, we just simulate calling AppendWord to transition, no reflection
	ctx.AppendWord("Hello")
	ctx.AppendWord("State")
	ctx.AppendWord("Final")
	// If this panics or errors, the test fails; otherwise, pass.
}