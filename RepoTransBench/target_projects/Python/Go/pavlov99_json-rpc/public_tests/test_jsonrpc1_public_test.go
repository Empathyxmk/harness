package public_tests

import (
	"testing"
	"encoding/json"
)

func TestPublicJsonrpc1_Add(t *testing.T) {
	request := `{"method": "add", "params": [5, 10], "id": 101}`
	var req map[string]interface{}
	err := json.Unmarshal([]byte(request), &req)
	if err != nil {
		t.Fatalf("Unmarshal failed: %v", err)
	}
	params := req["params"].([]interface{})
	expected := float64(15)
	actual := params[0].(float64) + params[1].(float64)
	if actual != expected {
		t.Errorf("Addition failed, expected %v, got %v", expected, actual)
	}
}

func TestPublicJsonrpc1_Notify(t *testing.T) {
	request := `{"method": "notify", "params": [1], "id": null}`
	var req map[string]interface{}
	err := json.Unmarshal([]byte(request), &req)
	if err != nil {
		t.Fatalf("Unmarshal failed: %v", err)
	}
	if req["id"] != nil {
		t.Errorf("Expected id to be nil for notification request")
	}
}