package public_tests

import (
	"testing"
)

type HelloWorld interface {
	HelloWorld() string
}

type implPublicHelloWorld struct{}

func (i implPublicHelloWorld) HelloWorld() string {
	return "different"
}

func TestHelloWorldInterfaceImpl_Public(t *testing.T) {
	var hw HelloWorld = implPublicHelloWorld{}
	got := hw.HelloWorld()
	if got != "different" {
		t.Errorf("Expected 'different', got '%s'", got)
	}
}