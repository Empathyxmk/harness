package public_tests

import (
	"testing"
)

func TestPlaceholderMiddlewareCore(t *testing.T) {
	m := map[string]int{"foo": 123}
	if m["foo"] != 123 {
		t.Errorf("map lookup failed")
	}
}