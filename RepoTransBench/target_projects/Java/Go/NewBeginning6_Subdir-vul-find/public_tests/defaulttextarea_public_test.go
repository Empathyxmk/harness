package public_tests

import (
	"testing"
	"newbeginning6subdir/org/example"
	"strings"
)

func TestDefaultTextareaPublicGetDefault(t *testing.T) {
	val := example.DefaultTextareaGetDefault()
	if strings.TrimSpace(val) == "" {
		t.Error("DefaultTextareaGetDefault returned empty or whitespace string")
	}
}