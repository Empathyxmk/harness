package composite

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// HelloWorld interface for composite pattern
type HelloWorld interface {
	HelloWorld() string
}

type CompositeHelloWorld struct {
	children []HelloWorld
}

func NewCompositeHelloWorld(children ...HelloWorld) *CompositeHelloWorld {
	return &CompositeHelloWorld{children: children}
}

type DefaultHelloWorld struct{}

func (d *DefaultHelloWorld) HelloWorld() string {
	return "Hello Composite!"
}

func (c *CompositeHelloWorld) HelloWorld() string {
	if len(c.children) == 0 {
		return ""
	}
	res := ""
	for _, child := range c.children {
		res += child.HelloWorld()
	}
	return res
}

func TestCompositeHelloWorld(t *testing.T) {
	empty := NewCompositeHelloWorld()
	assert.Empty(t, empty.HelloWorld())
	composite := NewCompositeHelloWorld(&DefaultHelloWorld{})
	assert.Equal(t, "Hello Composite!", composite.HelloWorld())
}