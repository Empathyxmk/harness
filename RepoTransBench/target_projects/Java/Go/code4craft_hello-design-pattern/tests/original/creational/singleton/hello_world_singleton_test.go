package singleton

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestHelloWorldSingleton(t *testing.T) {
	helloWorld := Instance()
	assert.Equal(t, "Hello Singleton!", helloWorld.HelloWorld())
}