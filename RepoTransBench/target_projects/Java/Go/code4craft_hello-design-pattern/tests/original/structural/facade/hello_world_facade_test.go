package facade

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type HelloWorld interface {
	HelloWorld() string
}

type FacadeHelloWorld struct{}

func (f *FacadeHelloWorld) HelloWorld() string {
	return "Hello Facade!"
}

type HelloWorldFacade struct{}

func NewHelloWorldFacade() *HelloWorldFacade {
	return &HelloWorldFacade{}
}

func (h *HelloWorldFacade) FacadeHelloWorld() HelloWorld {
	return &FacadeHelloWorld{}
}

// Simulate singleton
var facadeInstance = NewHelloWorldFacade()

func Instance() *HelloWorldFacade {
	return facadeInstance
}

func TestHelloWorldFacade(t *testing.T) {
	facadeHelloWorld := Instance().FacadeHelloWorld()
	assert.Equal(t, "Hello Facade!", facadeHelloWorld.HelloWorld())
}