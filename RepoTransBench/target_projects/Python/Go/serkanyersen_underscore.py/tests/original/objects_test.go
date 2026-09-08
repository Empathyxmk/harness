package original

import (
	"reflect"
	"testing"
	"underscore"
)

func TestKeys(t *testing.T) {
	m := map[string]int{"a": 1, "b": 2}
	keys := underscore.Keys(m)
	expected := []string{"a", "b"}
	got := make(map[string]struct{})
	for _, k := range keys {
		got[k] = struct{}{}
	}
	for _, want := range expected {
		if _, ok := got[want]; !ok {
			t.Errorf("expected key %s in result", want)
		}
	}
	if len(keys) != len(expected) {
		t.Errorf("expected %d keys, got %d", len(expected), len(keys))
	}
}