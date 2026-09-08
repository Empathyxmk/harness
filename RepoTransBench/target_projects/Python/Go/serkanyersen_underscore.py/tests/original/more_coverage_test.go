package original

import (
	"testing"
	"underscore"
)

func TestIsEmpty(t *testing.T) {
	if !underscore.IsEmpty([]interface{}{}) {
		t.Error("expected True for empty slice")
	}
	if underscore.IsEmpty([]int{1}) {
		t.Error("expected False for non-empty slice")
	}
}