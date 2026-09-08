package public_tests

import (
	"testing"
	"strings"
	"newbeginning6subdir/org/example"
)

func TestDefaultTextPublicGetDefault(t *testing.T) {
	text := example.DefaultTextGetDefault()
	if text == "" {
		t.Error("DefaultTextGetDefault() returned empty")
	}
	if !strings.Contains(text, "text") && len(text) <= 10 {
		t.Error("DefaultTextGetDefault() does not contain 'text' and is not longer than 10 characters")
	}
}