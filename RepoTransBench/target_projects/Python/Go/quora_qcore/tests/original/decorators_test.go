package tests

import (
	"testing"
)

func TestDecoratorTiming(t *testing.T) {
	// Simulating a timing decorator using a wrapper/signature in Go
	var called bool

	timedFunc := func(fn func()) func() {
		return func() {
			called = true
			fn()
		}
	}

	f := timedFunc(func() {
		// do something
	})

	f() // Should set called = true
	assertTrue(t, called)
}

func TestDecoratorArgs(t *testing.T) {
	var called bool
	withArgs := func(a int, fn func(b int)) func(int) {
		return func(b int) {
			called = (a == 5 && b == 10)
			fn(b)
		}
	}
	f := withArgs(5, func(b int) {})
	f(10)
	assertTrue(t, called)
}