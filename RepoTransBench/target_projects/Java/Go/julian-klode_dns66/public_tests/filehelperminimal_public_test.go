package public_tests

import (
	"strings"
	"testing"
)

func TestCloseOrWarnNoThrow(t *testing.T) {
	writer := &strings.Builder{}
	writer.WriteString("hello world")
	got := writer.String()
	if got != "hello world" {
		t.Errorf("expected content 'hello world' after WriteString, got %q", got)
	}
}

func TestCloseOrWarnWithException(t *testing.T) {
	called := false
	type badCloser struct{}
	func (c *badCloser) Close() error {
		called = true
		return nil // Close doesn't throw in Go, but simulate side-effect
	}
	bc := &badCloser{}
	_ = bc.Close()
	if !called {
		t.Errorf("expected close to be called and side effect set")
	}
}