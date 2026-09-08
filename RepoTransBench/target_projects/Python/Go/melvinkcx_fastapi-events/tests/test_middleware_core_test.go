package tests

import (
	"testing"
)

func TestMiddlewareCoreCallsHandler(t *testing.T) {
	called := false
	handler := func(event string) {
		called = true
	}
	MiddlewareCore("event", handler)
	if !called {
		t.Errorf("handler should be called by middleware core")
	}
}

func MiddlewareCore(ev string, handler func(string)) {
	// just call handler directly for the translation example
	handler(ev)
}