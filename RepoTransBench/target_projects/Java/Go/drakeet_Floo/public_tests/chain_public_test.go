package public_tests

import (
	"testing"
)

type Chain[T any] interface {
	Proceed(input T) T
}
type chainString struct{}
func (c chainString) Proceed(input string) string {
	return input + "_public"
}

type chainInt struct{}
func (c chainInt) Proceed(input int) int {
	return input + 42
}

func TestProceedReturnsData_public(t *testing.T) {
	var ch Chain[string] = chainString{}
	got := ch.Proceed("hello")
	if got != "hello_public" {
		t.Errorf("expected %q, got %q", "hello_public", got)
	}
}

func TestProceedWithDifferentData_public(t *testing.T) {
	var ch Chain[int] = chainInt{}
	got := ch.Proceed(8)
	if got != 50 {
		t.Errorf("expected 50, got %v", got)
	}
}