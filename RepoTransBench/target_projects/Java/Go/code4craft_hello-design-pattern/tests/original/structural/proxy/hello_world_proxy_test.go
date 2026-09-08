package proxy

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type HelloWorld interface {
	HelloWorld() string
}

type DefaultHelloWorld struct{}

func (d *DefaultHelloWorld) HelloWorld() string {
	return "Hello Proxy!"
}

type HelloWorldProxy struct {
	target HelloWorld
}

func NewHelloWorldProxy(target HelloWorld) *HelloWorldProxy {
	return &HelloWorldProxy{target: target}
}

func (h *HelloWorldProxy) HelloWorld() string {
	return h.target.HelloWorld()
}

func TestHelloWorldFacade(t *testing.T) {
	proxy := NewHelloWorldProxy(&DefaultHelloWorld{})
	assert.Equal(t, "Hello Proxy!", proxy.HelloWorld())
}