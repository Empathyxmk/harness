package mediator

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// Dummy HelloWorldObject implementation
type HelloWorldObject struct{}

func NewHelloWorldObject() *HelloWorldObject {
	return &HelloWorldObject{}
}

func TestDefaultConstructorHelloWorldObject(t *testing.T) {
	obj := NewHelloWorldObject()
	assert.NotNil(t, obj)
}