package tests

import (
	"testing"
)

type HelloWorld interface {
	HelloWorld() string
}

type implHelloWorld struct{}

func (i implHelloWorld) HelloWorld() string {
	return "custom"
}

func TestHelloWorldInterfaceImpl(t *testing.T) {
	var hw HelloWorld = implHelloWorld{}
	got := hw.HelloWorld()
	if got != "custom" {
		t.Errorf("Expected 'custom', got '%s'", got)
	}
}