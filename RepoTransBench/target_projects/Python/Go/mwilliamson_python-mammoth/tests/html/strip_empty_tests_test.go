package html

import (
	"testing"
)

func TestTextNodesWithTextAreNotStripped(t *testing.T) {
	t.Skip("Requires Go html.strip_empty implementation")
}

func TestEmptyTextNodesAreStripped(t *testing.T) {
	t.Skip("Requires Go html.strip_empty implementation")
}

func TestElementsWithNonEmptyChildrenAreNotStripped(t *testing.T) {
	t.Skip("Requires Go html.strip_empty implementation")
}

func TestElementsWithNoChildrenAreStripped(t *testing.T) {
	t.Skip("Requires Go html.strip_empty implementation")
}

func TestElementsWithOnlyEmptyChildrenAreStripped(t *testing.T) {
	t.Skip("Requires Go html.strip_empty implementation")
}

func TestEmptyChildrenAreRemoved(t *testing.T) {
	t.Skip("Requires Go html.strip_empty implementation")
}

func TestSelfClosingElementsAreNeverEmpty(t *testing.T) {
	t.Skip("Requires Go html.strip_empty implementation")
}

func TestForceWritesAreNeverEmpty(t *testing.T) {
	t.Skip("Requires Go html.strip_empty implementation")
}