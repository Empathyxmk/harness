package middleware

import (
	"strings"
	"testing"
)

func TestPlaceholderStarlette(t *testing.T) {
	if !strings.Contains("starlette", "star") {
		t.Errorf(`expected "starlette" to contain "star"`)
	}
}