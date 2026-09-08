package singleton

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"sync"
)

// Singleton implementation for HelloWorldSingleton
type HelloWorldSingleton struct{}

var (
	instance     *HelloWorldSingleton
	once         sync.Once
)

func Instance() *HelloWorldSingleton {
	once.Do(func() {
		instance = &HelloWorldSingleton{}
	})
	return instance
}

func (h *HelloWorldSingleton) HelloWorld() string {
	return "Hello Singleton!"
}

func TestSingletonInstance_ReturnsSameInstance(t *testing.T) {
	inst1 := Instance()
	inst2 := Instance()
	assert.Same(t, inst1, inst2, "Instance() should always return the same instance")
}

func TestSingletonMessage(t *testing.T) {
	assert.Equal(t, "Hello Singleton!", Instance().HelloWorld())
}