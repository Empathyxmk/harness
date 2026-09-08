package original

import (
	"testing"
	"encoding/json"
)

func TestJsonrpc2ParseValidRequest(t *testing.T) {
	request := `{"jsonrpc": "2.0", "method": "subtract", "params": [7, 3], "id": 2}`
	var req map[string]interface{}
	err := json.Unmarshal([]byte(request), &req)
	if err != nil {
		t.Fatalf("JSON parse fail: %v", err)
	}
	version, ok := req["jsonrpc"].(string)
	if !ok || version != "2.0" {
		t.Errorf("Expected jsonrpc version '2.0', got %v", req["jsonrpc"])
	}
	params, ok := req["params"].([]interface{})
	if !ok || len(params) != 2 {
		t.Fatalf("Expected list params, got %T, %v", req["params"], req["params"])
	}
	expected := float64(4)
	actual := params[0].(float64) - params[1].(float64)
	if actual != expected {
		t.Errorf("Subtraction logic error: want %v, got %v", expected, actual)
	}
}

func TestJsonrpc2Notification(t *testing.T) {
	request := `{"jsonrpc": "2.0", "method": "ping", "params": [], "id": null}`
	var req map[string]interface{}
	err := json.Unmarshal([]byte(request), &req)
	if err != nil {
		t.Fatalf("Unmarshal fail: %v", err)
	}
	_, ok := req["id"]
	if !ok {
		t.Errorf("Expected id key to exist (possibly null)")
	}
	if req["id"] != nil {
		t.Errorf("For notification, id must be null, got %v", req["id"])
	}
}

func TestJsonrpc2BatchRequest(t *testing.T) {
	request := `[{"jsonrpc":"2.0","method":"sum","params":[1,2,3,4,5],"id":"1"},{"jsonrpc":"2.0","method":"notify_hello","params":[7]}]`
	var req []map[string]interface{}
	err := json.Unmarshal([]byte(request), &req)
	if err != nil {
		t.Fatalf("Unmarshal fail: %v", err)
	}
	if len(req) != 2 {
		t.Fatalf("Expected array of 2 batch elements, got %d", len(req))
	}
	batch := req[0]
	if batch["method"] != "sum" {
		t.Errorf("Expected 'sum', got %v", batch["method"])
	}
}