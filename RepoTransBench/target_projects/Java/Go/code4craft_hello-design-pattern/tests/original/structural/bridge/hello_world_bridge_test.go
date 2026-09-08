package bridge

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type HelloWorld interface {
	HelloWorld() string
}

type JavaHelloWorldImpl struct{}

func (j *JavaHelloWorldImpl) HelloWorld() string {
	return "Hello Java!"
}

type DesignPatternWorldImpl struct{}

func (d *DesignPatternWorldImpl) HelloWorld() string {
	return "Hello Bridge!"
}

type HelloWorldBridge struct {
	impl HelloWorld
}

func NewHelloWorldBridge(impl HelloWorld) *HelloWorldBridge {
	return &HelloWorldBridge{impl: impl}
}

func (h *HelloWorldBridge) HelloWorld() string {
	return h.impl.HelloWorld()
}

func TestHelloWorldAdapter(t *testing.T) {
	bridgeHelloWorld := NewHelloWorldBridge(&JavaHelloWorldImpl{})
	assert.Equal(t, "Hello Java!", bridgeHelloWorld.HelloWorld())
	bridgeHelloWorld = NewHelloWorldBridge(&DesignPatternWorldImpl{})
	assert.Equal(t, "Hello Bridge!", bridgeHelloWorld.HelloWorld())
}