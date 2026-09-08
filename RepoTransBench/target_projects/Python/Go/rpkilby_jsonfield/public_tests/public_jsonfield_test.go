package public_tests

import (
	"encoding/json"
	"testing"
)

func TestPublicEncodeSimpleDict(t *testing.T) {
	data := map[string]interface{}{"planet": "Saturn", "rings": true}
	encoded, _ := json.Marshal(data)
	want1 := `{"planet":"Saturn","rings":true}`
	want2 := `{"rings":true,"planet":"Saturn"}`
	if string(encoded) != want1 && string(encoded) != want2 {
		t.Errorf("Expected %s or %s, got %s", want1, want2, string(encoded))
	}
}

func TestPublicEncodeListNumbers(t *testing.T) {
	data := []int{5, 7, 11}
	encoded, _ := json.Marshal(data)
	if string(encoded) != `[5,7,11]` {
		t.Errorf("Expected [5,7,11], got %s", string(encoded))
	}
}

func TestPublicDecodeUnicode(t *testing.T) {
	inputStr := `{"emoji": "\u263A"}`
	var out map[string]string
	err := json.Unmarshal([]byte(inputStr), &out)
	if err != nil {
		t.Errorf("JSON unmarshal failed: %v", err)
	}
	if out["emoji"] != "\u263A" {
		t.Errorf("Expected ☺, got %v", out["emoji"])
	}
}

func TestPublicInvalidJSONRaises(t *testing.T) {
	input := "{invalid: true,}"
	var out interface{}
	err := json.Unmarshal([]byte(input), &out)
	if err == nil {
		t.Error("Expected error on invalid JSON")
	}
}

func TestPublicNativeFloatEncoding(t *testing.T) {
	data := 42.42
	encoded, _ := json.Marshal(data)
	if string(encoded) != "42.42" {
		t.Errorf("Expected 42.42, got %s", string(encoded))
	}
	var num float64
	err := json.Unmarshal([]byte("42.42"), &num)
	if err != nil || num != 42.42 {
		t.Errorf("Failed to decode 42.42: err=%v, got=%v", err, num)
	}
}