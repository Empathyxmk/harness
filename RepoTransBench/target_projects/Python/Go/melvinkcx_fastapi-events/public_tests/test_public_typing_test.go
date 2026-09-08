package public_tests

import (
	"testing"
)

func TestPlaceholderTyping(t *testing.T) {
	x := 42
	if x != 42 {
		t.Errorf("x should be an int with value 42")
	}
}