package public_tests

import (
	"testing"
)

func TestTimingDecoratorSimulation(t *testing.T) {
	var called bool
	timer := func(fn func()) func() {
		return func() {
			called = true
			fn()
		}
	}
	f := timer(func() {})
	f()
	if !called {
		t.Fatalf("decorator didn't set called to true")
	}
}

func TestWithArgsDecoratorSimulation(t *testing.T) {
	var called bool
	withArgs := func(a int, fn func(b int)) func(int) {
		return func(b int) {
			called = (a == 42 && b == 99)
			fn(b)
		}
	}
	wrapped := withArgs(42, func(int) {})
	wrapped(99)
	if !called {
		t.Fatalf("decorator with args didn't set called to true")
	}
}