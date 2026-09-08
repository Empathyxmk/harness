package public_tests

import (
	"testing"
	"vasco"
)

func TestDifferentTransitionTable(t *testing.T) {
	table := vasco.NewContextTransitionTable[string, int, float64]()
	base := &vasco.Context{Method: "foo", ID: 123}
	next := &vasco.Context{Method: "bar", ID: 321}
	table.Put(base, "edge", next)

	if !table.ContainsTransition(base, "edge") {
		t.Error("Should have transition")
	}
	if table.ContainsTransition(base, "nonexistent") {
		t.Error("Should not have nonexistent transition")
	}
	if table.GetTarget(base, "edge") != next {
		t.Error("Target mismatch")
	}
	if table.GetTarget(base, "noTransition") != nil {
		t.Error("Should be nil for missing edge")
	}
}
func TestNullBaseContextTable(t *testing.T) {
	table := vasco.NewContextTransitionTable[string, int, float64]()
	base := &vasco.Context{Method: nil, ID: -1}
	next := &vasco.Context{Method: "baz", ID: 888}
	table.Put(base, "x", next)
	if !table.ContainsTransition(base, "x") {
		t.Error("Expected transition present on nil method context")
	}
	if table.GetTarget(base, "x") != next {
		t.Error("Target mismatch for nil-method context")
	}
}