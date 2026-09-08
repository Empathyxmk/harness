package middleware

import (
	"strings"
	"testing"
)

func TestPlaceholderStarlite(t *testing.T) {
	if !strings.Contains("starlite", "lite") {
		t.Errorf(`expected "starlite" to contain "lite"`)
	}
}