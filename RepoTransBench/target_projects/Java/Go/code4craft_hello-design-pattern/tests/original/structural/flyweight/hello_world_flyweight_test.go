package flyweight

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type HelloWorld interface {
	HelloWorld() string
}

type helloWorldFlyWeight struct {
	msg string
}

func (h *helloWorldFlyWeight) HelloWorld() string {
	return h.msg
}

type HelloWorldFlyWeightFactory struct{}

func NewHelloWorldFlyWeightFactory() *HelloWorldFlyWeightFactory {
	return &HelloWorldFlyWeightFactory{}
}

func (f *HelloWorldFlyWeightFactory) CreateHelloWorld(msg string) HelloWorld {
	return &helloWorldFlyWeight{msg: msg}
}

// Simulate static singleton instance pattern from Java
var flyweightFactoryInstance = NewHelloWorldFlyWeightFactory()

func TestHelloWorldFlyWeight(t *testing.T) {
	hw1 := flyweightFactoryInstance.CreateHelloWorld("Hello Flyweight!")
	assert.Equal(t, "Hello Flyweight!", hw1.HelloWorld())
	hw2 := flyweightFactoryInstance.CreateHelloWorld("Hello Flyweight!")
	assert.Equal(t, "Hello Flyweight!", hw2.HelloWorld())
}