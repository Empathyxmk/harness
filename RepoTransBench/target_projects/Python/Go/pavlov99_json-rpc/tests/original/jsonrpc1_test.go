package original

import (
	"testing"
	"encoding/json"
)

func TestJsonrpc1ParseValidRequest(t *testing.T) {
	request := `{"method": "add", "params": [1, 2], "id": 1}`
	var req map[string]interface{}
	err := json.Unmarshal([]byte(request), &req)
	if err != nil {
		t.Fatalf("Failed to unmarshal valid request: %v", err)
	}
	if req["method"] != "add" {
		t.Errorf("Expected method to be 'add', got %v", req["method"])
	}
	if req["id"] != float64(1) {
		t.Errorf("Expected id to be 1, got %v", req["id"])
	}
	params, ok := req["params"].([]interface{})
	if !ok {
		t.Fatalf("Expected params to be a list, got %T", req["params"])
	}
	if len(params) != 2 || params[0] != float64(1) || params[1] != float64(2) {
		t.Errorf("Params do not match expected: %v", params)
	}
}

func TestJsonrpc1ParseInvalidRequest(t *testing.T) {
	badRequest := `{"method": "add", "params": "notalist", "id": 1}`
	var req map[string]interface{}
	err := json.Unmarshal([]byte(badRequest), &req)
	if err != nil {
		t.Fatalf("Failed to unmarshal malformed request: %v", err)
	}
	// 'params' is a string, not a list.
	_, ok := req["params"].([]interface{})
	if ok {
		t.Errorf("Expected params to not be list, but was")
	}
}

func TestJsonrpc1MissingMethod(t *testing.T) {
	badRequest := `{"params": [1,2], "id": 2}`
	var req map[string]interface{}
	err := json.Unmarshal([]byte(badRequest), &req)
	if err != nil {
		t.Fatalf("JSON unmarshal failed: %v", err)
	}
	if _, ok := req["method"]; ok {
		t.Errorf("Expected no 'method' element, but found one")
	}
}

func TestJsonrpc1NullIDAllowed(t *testing.T) {
	request := `{"method": "foo", "params": [42], "id": null}`
	var req map[string]interface{}
	err := json.Unmarshal([]byte(request), &req)
	if err != nil {
		t.Fatalf("Unmarshal failed: %v", err)
	}
	if _, ok := req["id"]; !ok {
		t.Errorf("Expected 'id' key present (even if null)")
	}
}

func TestJsonrpc1Notification(t *testing.T) {
	request := `{"method": "notify", "params": [], "id": null}`
	var req map[string]interface{}
	err := json.Unmarshal([]byte(request), &req)
	if err != nil {
		t.Fatalf("JSON decode error: %v", err)
	}
	if req["method"] != "notify" {
		t.Errorf("Expected 'notify' method, got %v", req["method"])
	}
	if req["id"] != nil {
		t.Errorf("Expected id to be nil for notification, got %v", req["id"])
	}
}