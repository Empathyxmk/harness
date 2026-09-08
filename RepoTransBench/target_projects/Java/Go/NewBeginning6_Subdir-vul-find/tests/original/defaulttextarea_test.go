package original

import (
	"testing"
	"newbeginning6subdir/org/example"
)

func TestDefaultTextareaGetDefault(t *testing.T) {
	val := example.DefaultTextareaGetDefault()
	if val == "" {
		t.Error("DefaultTextareaGetDefault returned empty string")
	}
}