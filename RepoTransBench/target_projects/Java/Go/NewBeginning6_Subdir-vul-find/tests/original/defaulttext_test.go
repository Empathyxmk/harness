package original

import (
	"testing"
	"newbeginning6subdir/org/example"
)

func TestDefaultTextGetDefault(t *testing.T) {
	val := example.DefaultTextGetDefault()
	if val == "" {
		t.Error("DefaultTextGetDefault returned empty string")
	}
}