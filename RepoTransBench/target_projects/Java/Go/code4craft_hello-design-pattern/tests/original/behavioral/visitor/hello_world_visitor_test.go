package visitor

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// Accepts a visitor for "Hello Visitor!" (Visitor pattern)
type HelloWorldCharacterElements struct {
	runes []rune
}

func NewHelloWorldCharacterElements(runes []rune) *HelloWorldCharacterElements {
	return &HelloWorldCharacterElements{runes: runes}
}

type HelloWorldCharacterVisitor struct {
	acc []rune
}

func NewHelloWorldCharacterVisitor() *HelloWorldCharacterVisitor {
	return &HelloWorldCharacterVisitor{}
}

func (e *HelloWorldCharacterElements) Accept(visitor *HelloWorldCharacterVisitor) {
	visitor.acc = append(visitor.acc, e.runes...)
}

func (v *HelloWorldCharacterVisitor) HelloWorld() string {
	return string(v.acc)
}

func TestHelloWorldVisitor(t *testing.T) {
	elements := NewHelloWorldCharacterElements([]rune("Hello Visitor!"))
	visitor := NewHelloWorldCharacterVisitor()
	elements.Accept(visitor)
	assert.Equal(t, "Hello Visitor!", visitor.HelloWorld())
}