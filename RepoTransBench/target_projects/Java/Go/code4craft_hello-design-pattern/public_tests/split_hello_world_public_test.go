package public_tests

import (
	"strings"
	"testing"
)

// Public test version: interjection returns "Hi", object "Universe"
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
	return s.interjection.Interjection() + " " + s.object.Object()
}

// Use one-method function adapter
type helloWorldInterjectionFunc func() string
func (f helloWorldInterjectionFunc) Interjection() string { return f() }
type helloWorldObjectFunc func() string
func (f helloWorldObjectFunc) Object() string { return f() }

func TestSplitHelloWorld_StringWithAnonymousClassesPublic(t *testing.T) {
	interj := helloWorldInterjectionFunc(func() string { return "Hi" })
	object := helloWorldObjectFunc(func() string { return "Universe" })
	s := NewSplitHelloWorld(interj, object)
	result := s.String()
	if !strings.Contains(result, "Hi") {
		t.Error("expected result to contain 'Hi'")
	}
	if !strings.Contains(result, "Universe") {
		t.Error("expected result to contain 'Universe'")
	}
}