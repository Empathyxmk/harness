package original

import (
	"testing"
	. "hello"
)

func TestGreetNormal(t *testing.T) {
	greeter := Greeter{}
	result := greeter.Greet("World")
	expected := "Hello, World!"
	if result != expected {
		t.Errorf("Expected %q, got %q", expected, result)
	}
}

func TestGreetEmpty(t *testing.T) {
	greeter := Greeter{}
	result := greeter.Greet("")
	expected := "Hello, !"
	if result != expected {
		t.Errorf("Expected %q, got %q", expected, result)
	}
}

func TestGreetWhitespace(t *testing.T) {
	greeter := Greeter{}
	result := greeter.Greet("   ")
	expected := "Hello,    !"
	if result != expected {
		t.Errorf("Expected %q, got %q", expected, result)
	}
}

func TestGreetNull(t *testing.T) {
	greeter := Greeter{}
	// In Go, string cannot be nil, but zero string "" is the closest.
	// For Java null, Go will treat it as "null" if we mimic the Java behavior.
	// Therefore, we'll pass the string "null" just like Java's String.valueOf(null)
	result := greeter.Greet("null")
	expected := "Hello, null!"
	if result != expected {
		t.Errorf("Expected %q, got %q", expected, result)
	}
}

func TestGreetCustomName(t *testing.T) {
	greeter := Greeter{}
	result := greeter.Greet("Alice")
	expected := "Hello, Alice!"
	if result != expected {
		t.Errorf("Expected %q, got %q", expected, result)
	}
}