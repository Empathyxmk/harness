package public_tests

import (
	"testing"
	"underscore"
)

func TestIsEmptyPublic(t *testing.T) {
	if !underscore.IsEmpty(map[string]interface{}{}) {
		t.Error("expected True for empty map")
	}
	if underscore.IsEmpty(map[string]interface{}{"a": "z"}) {
		t.Error("expected False for non-empty map")
	}
}