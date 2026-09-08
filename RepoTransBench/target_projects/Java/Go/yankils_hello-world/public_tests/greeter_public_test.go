package public_tests

import (
	"testing"
	. "hello"
)

func TestGreetAnotherName(t *testing.T) {
	greeter := Greeter{}
	result := greeter.Greet("Alice")
	expected := "Hello, Alice!"
	if result != expected {
		t.Errorf("Expected %q, got %q", expected, result)
	}
}

func TestGreetWithDifferentName(t *testing.T) {
	greeter := Greeter{}
	result := greeter.Greet("Charlie")
	expected := "Hello, Charlie!"
	if result != expected {
		t.Errorf("Expected %q, got %q", expected, result)
	}
}

func TestGreetWithEmptyString(t *testing.T) {
	greeter := Greeter{}
	result := greeter.Greet("")
	expected := "Hello, !"
	if result != expected {
		t.Errorf("Expected %q, got %q", expected, result)
	}
}

func TestGreetWithSpecialCharacters(t *testing.T) {
	greeter := Greeter{}
	result := greeter.Greet("@User#123")
	expected := "Hello, @User#123!"
	if result != expected {
		t.Errorf("Expected %q, got %q", expected, result)
	}
}