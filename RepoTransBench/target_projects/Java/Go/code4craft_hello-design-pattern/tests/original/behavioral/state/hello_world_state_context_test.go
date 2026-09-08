package state

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// Simulated HelloWorldStateContext for test logic
type HelloWorldStateContext struct {
	content string
	final   bool
}

func NewHelloWorldStateContext() *HelloWorldStateContext {
	return &HelloWorldStateContext{}
}

func (s *HelloWorldStateContext) AppendWord(word string) {
	if s.final {
		return
	}
	if s.content == "" {
		s.content = word + " "
		if word == "Hello" {
			// not finalized yet
			return
		}
	}
	if word == "State" && s.content == "Hello " {
		s.content = "Hello State!"
		s.final = true
	}
}

func (s *HelloWorldStateContext) HelloWorld() string {
	return s.content
}

func TestHelloWorldStateContext(t *testing.T) {
	ctx := NewHelloWorldStateContext()
	ctx.AppendWord("Hello")
	assert.Equal(t, "Hello ", ctx.HelloWorld())
	ctx.AppendWord("State")
	assert.Equal(t, "Hello State!", ctx.HelloWorld())
	ctx.AppendWord("Whatever")
	assert.Equal(t, "Hello State!", ctx.HelloWorld())
}