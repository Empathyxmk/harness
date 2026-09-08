package handlers

import (
	"testing"
)

func TestPlaceholderLocalHandler(t *testing.T) {
	if !true {
		t.Errorf("expected true")
	}
}

func TestPlaceholderLocalHandlerDifferent(t *testing.T) {
	if 1 == 2 {
		t.Errorf("expected 1 != 2")
	}
}