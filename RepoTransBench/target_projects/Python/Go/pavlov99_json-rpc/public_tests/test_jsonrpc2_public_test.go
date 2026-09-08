package public_tests

import (
	"testing"
	"encoding/json"
)

func TestPublicJsonrpc2_BasicMethodCall(t *testing.T) {
	req := `{"jsonrpc":"2.0","method":"foo","params":[4,8],"id":42}`
	var m map[string]interface{}
	if err := json.Unmarshal([]byte(req), &m); err != nil {
		t.Fatalf("Unmarshal error: %v", err)
	}
	if m["jsonrpc"] != "2.0" {
		t.Errorf("Wrong jsonrpc version, want 2.0 got %v", m["jsonrpc"])
	}
	params := m["params"].([]interface{})
	expected := float64(12)
	got := params[0].(float64) + params[1].(float64)
	if got != expected {
		t.Errorf("Addition logic error: want %v, got %v", expected, got)
	}
}

func TestPublicJsonrpc2_InvalidIDType(t *testing.T) {
	req := `{"jsonrpc":"2.0","method":"foo","params":[],"id":{}}`
	var m map[string]interface{}
	if err := json.Unmarshal([]byte(req), &m); err != nil {
		t.Fatalf("Unmarshal error: %v", err)
	}
	switch m["id"].(type) {
	case map[string]interface{}:
	default:
		t.Errorf("Expected id to be an object")
	}
}