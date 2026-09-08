package original

import (
	"testing"
	"underscore"
)

func TestIdentity(t *testing.T) {
	if v := underscore.Identity(42); v != 42 {
		t.Errorf("expected 42, got %v", v)
	}
}