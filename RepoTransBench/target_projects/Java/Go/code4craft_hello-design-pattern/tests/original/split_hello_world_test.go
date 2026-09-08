package tests

import (
	"strings"
	"testing"
)

// SplitHelloWorld with injected interjection and object
type HelloWorldInterjection interface {
	Interjection() string
}
type HelloWorldObject interface {
	Object() string
}
type SplitHelloWorld struct {
	interjection HelloWorldInterjection
	object       HelloWorldObject
}

func NewSplitHelloWorld(interjection HelloWorldInterjection, object HelloWorldObject) *SplitHelloWorld {
	return &SplitHelloWorld{interjection, object}
}

func (s *SplitHelloWorld) String() string {
	// Simulate the Java toString which combines interjection + object
	return s.interjection.Interjection() + " " + s.object.Object()
}

func TestSplitHelloWorld_StringWithAnonymousClasses(t *testing.T) {
	interj := &struct{ HelloWorldInterjection }{
		HelloWorldInterjection: struct{ HelloWorldInterjection }{},
	}
	object := &struct{ HelloWorldObject }{
		HelloWorldObject: struct{ HelloWorldObject }{},
	}
	interj.Interjection = func() string { return "Hello" }
	object.Object = func() string { return "World" }

	// OR we can just use function types in Go since interface method is 1
	interj2 := helloWorldInterjectionFunc(func() string { return "Hello" })
	object2 := helloWorldObjectFunc(func() string { return "World" })

	s := NewSplitHelloWorld(interj2, object2)
	result := s.String()
	if !strings.Contains(result, "Hello") {
		t.Error("expected result to contain 'Hello'")
	}
	if !strings.Contains(result, "World") {
		t.Error("expected result to contain 'World'")
	}
}

// Allow using func() string as interface
type helloWorldInterjectionFunc func() string
func (f helloWorldInterjectionFunc) Interjection() string { return f() }
type helloWorldObjectFunc func() string
func (f helloWorldObjectFunc) Object() string { return f() }