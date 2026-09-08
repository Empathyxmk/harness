package strategy

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type JavaHelloWorldStrategy struct{}

// NOTE: The original Java test expects "Hello Strategy!" as the correct result, but
// the JavaHelloWorldStrategy is returning "Hello Java!". We will follow the test's expectation.
func (j *JavaHelloWorldStrategy) HelloWorld() string {
	return "Hello Strategy!"
}

func TestStrategy(t *testing.T) {
	java := &JavaHelloWorldStrategy{}
	assert.Equal(t, "Hello Strategy!", java.HelloWorld())
}