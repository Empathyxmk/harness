package public_tests

import (
	"strings"
	"testing"
)

// Public alphanumericOnly implementation as in source
func alphanumericOnly(s string) string {
	var out strings.Builder
	for _, r := range s {
		if (r >= 'A' && r <= 'Z') ||
			(r >= 'a' && r <= 'z') ||
			(r >= '0' && r <= '9') {
			out.WriteRune(r)
		}
	}
	return out.String()
}

func TestAlphanumericOnlyPublic(t *testing.T) {
	if got := alphanumericOnly("xyz789GH@#!"); got != "xyz789GH" {
		t.Errorf(`alphanumericOnly("xyz789GH@#!") = %q, want %q`, got, "xyz789GH")
	}
	if got := alphanumericOnly(" **&$  321 "); got != "321" {
		t.Errorf(`alphanumericOnly(" **&$  321 ") = %q, want %q`, got, "321")
	}
}