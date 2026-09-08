package original

import (
	"testing"
)

func isDefaultModifier(modifiers []Modifier) bool {
	hasVisibility := false
	for _, m := range modifiers {
		if m == Public || m == Private || m == Protected {
			hasVisibility = true
			break
		}
	}
	return !hasVisibility
}

func TestIsDefaultModifier(t *testing.T) {
	if isDefaultModifier([]Modifier{Public}) {
		t.Errorf("Expected false for Public")
	}
	if isDefaultModifier([]Modifier{Private}) {
		t.Errorf("Expected false for Private")
	}
	if isDefaultModifier([]Modifier{Protected}) {
		t.Errorf("Expected false for Protected")
	}
	if !isDefaultModifier([]Modifier{Final, Static}) {
		t.Errorf("Expected true for just Final, Static")
	}
}