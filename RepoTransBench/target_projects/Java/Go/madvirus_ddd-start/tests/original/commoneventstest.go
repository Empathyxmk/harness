package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

var calledFlags map[string]bool

func ResetFlags() {
	calledFlags = map[string]bool{}
}

func EventAListener() {
	calledFlags["A"] = true
}

func EventBListener() {
	calledFlags["B"] = true
}

func FireEventA() {
	EventAListener()
}

func FireEventB() {
	EventBListener()
}

func TestEventsAreDispatched(t *testing.T) {
	ResetFlags()
	FireEventA()
	FireEventB()
	assert.True(t, calledFlags["A"], "EventA should be called.")
	assert.True(t, calledFlags["B"], "EventB should be called.")
}

func TestFlagsReset(t *testing.T) {
	ResetFlags()
	FireEventA()
	assert.True(t, calledFlags["A"])
	ResetFlags()
	assert.False(t, calledFlags["A"])
}