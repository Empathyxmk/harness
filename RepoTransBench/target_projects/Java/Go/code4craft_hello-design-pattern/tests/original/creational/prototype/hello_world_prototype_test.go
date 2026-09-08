package prototype

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestHelloWorldPrototype(t *testing.T) {
	// Use the PROTOTYPE defined in hello_world_prototype_full_test.go
	helloWorld := PROTOTYPE.Clone()
	assert.Equal(t, "Hello Prototype!", helloWorld.HelloWorld())
}