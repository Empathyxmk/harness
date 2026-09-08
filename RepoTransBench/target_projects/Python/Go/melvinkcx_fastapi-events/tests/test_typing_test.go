package tests

import (
	"testing"
)

type DummyEnum int

const (
	A DummyEnum = 1
)

func TestEventTypingUnionAndAliases(t *testing.T) {
	// In Python, Event = tuple[str|Enum, Any]
	e1 := []interface{}{"test", map[string]interface{}{"k": 1}}
	e2 := []interface{}{A, "val"}

	// Python: assert isinstance(e1, tuple)
	if len(e1) != 2 {
		t.Errorf("e1 should be of length 2")
	}
	if len(e2) != 2 {
		t.Errorf("e2 should be of length 2")
	}

	if s, ok := e1[1].(map[string]interface{}); !ok || s["k"] != 1 {
		t.Errorf("e1[1] should be map with 'k' == 1")
	}
	if e2[0] != A || e2[1] != "val" {
		t.Errorf("e2 should match assigned values")
	}

	// Scope/Message types are MutableMapping
	dummyScope := map[string]interface{}{"type": "http"}
	dummyMsg := map[string]interface{}{"a": 1}
	if dummyScope["type"] != "http" {
		t.Errorf("dummyScope[\"type\"] == \"http\" expected")
	}
	if dummyMsg["a"] != 1 {
		t.Errorf("dummyMsg[\"a\"] == 1 expected")
	}
}

func TestAsgiappTypes(t *testing.T) {
	mockReceive := func() {}
	mockSend := func(msg interface{}) {}
	mockAsgiapp := func(scope, rec, snd interface{}) {}
	if mockReceive == nil || mockSend == nil || mockAsgiapp == nil {
		t.Errorf("functions should be callable")
	}
}