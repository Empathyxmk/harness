package public_tests

import (
	"testing"
	"underscore"
)

func TestKeysPublic(t *testing.T) {
	m := map[string]int{"x": 42, "y": 100}
	keys := underscore.Keys(m)
	found := map[string]struct{}{}
	for _, k := range keys {
		found[k] = struct{}{}
	}
	if _, ok := found["x"]; !ok {
		t.Error("expected key 'x' in keys")
	}
	if _, ok := found["y"]; !ok {
		t.Error("expected key 'y' in keys")
	}
	if len(keys) != 2 {
		t.Errorf("expected 2 keys, got %d", len(keys))
	}
}