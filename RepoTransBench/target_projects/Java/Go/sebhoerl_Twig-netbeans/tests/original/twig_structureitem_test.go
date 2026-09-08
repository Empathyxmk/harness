package original

import (
	"testing"
	"twigmodule/tests"
)

func TestTwigStructureItemMethods(t *testing.T) {
	item := tests.NewTwigStructureItem("block", "METHOD", 1, 11)
	if item.GetName() != "block" {
		t.Errorf("Expected name 'block', got '%s'", item.GetName())
	}
	if item.GetKind() != "METHOD" {
		t.Errorf("Expected kind 'METHOD', got '%s'", item.GetKind())
	}
	if item.GetOffset() != 1 {
		t.Errorf("Expected offset 1, got %d", item.GetOffset())
	}
	if item.GetEndOffset() != 11 {
		t.Errorf("Expected end offset 11, got %d", item.GetEndOffset())
	}
}