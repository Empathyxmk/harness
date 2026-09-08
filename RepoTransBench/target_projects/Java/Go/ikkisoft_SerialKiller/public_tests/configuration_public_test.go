package public_tests

import (
	"testing"
)

func TestPropertyLoadDifferentKey(t *testing.T) {
	props := map[string]string{}
	props["public.test.key"] = "publicValue"
	if val, ok := props["public.test.key"]; !ok {
		t.Errorf("expected property to be present")
	} else if val != "publicValue" {
		t.Errorf("expected 'publicValue', got %q", val)
	}
	if _, ok := props["nonexistent.key"]; ok {
		t.Errorf("expected nonexistent.key to be absent")
	}
}