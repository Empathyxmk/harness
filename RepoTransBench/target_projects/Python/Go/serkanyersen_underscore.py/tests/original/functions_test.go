package original

import (
	"testing"
	"underscore"
)

func TestOnce(t *testing.T) {
	called := 0
	fn := func() int {
		called++
		return 3
	}
	onceFunc := underscore.OnceFn(fn)
	if v := onceFunc(); v != 3 {
		t.Errorf("expected 3, got %v", v)
	}
	onceFunc()
	if called != 1 {
		t.Errorf("expected called once, got called %d", called)
	}
}