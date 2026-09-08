package public_tests

import (
	"testing"
	"underscore"
)

func TestOncePublic(t *testing.T) {
	called := 0
	fn := func() string {
		called++
		return "foo"
	}
	onceFunc := underscore.OnceFn(fn)
	if v := onceFunc(); v != "foo" {
		t.Errorf("expected foo, got %v", v)
	}
	onceFunc()
	if called != 1 {
		t.Errorf("expected function to be called only once, got %d calls", called)
	}
}