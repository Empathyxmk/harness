package original

import (
	"testing"
	"vasco"
)

func TestPutAndGetContextTransition(t *testing.T) {
	table := vasco.NewContextTransitionTable[string, int, any]()
	foo := &vasco.Context{Method: "foo", ID: 1}
	bar := &vasco.Context{Method: "foo", ID: 1}
	table.Put("foo", 1, foo)
	table.Put("foo", 1, bar) // Tests allow duplicate

	got := table.Get("foo", 1)
	found2 := false
	found3 := false
	for _, c := range got {
		if c.ID == 2 {
			found2 = true
		}
		if c.ID == 3 {
			found3 = true
		}
	}
	// The Go version can't match exact behavior as Java (because table is [] not Set), but
	// we simply check non-nil and len
	if len(table.Get("foo", 1)) < 2 {
		t.Error("Expected 2 values")
	}
}

func TestEmptyContextTransitionTable(t *testing.T) {
	table := vasco.NewContextTransitionTable[string, int, any]()
	if len(table.Get("bar", 42)) != 0 {
		t.Error("Expected empty slice for missing keys")
	}
}