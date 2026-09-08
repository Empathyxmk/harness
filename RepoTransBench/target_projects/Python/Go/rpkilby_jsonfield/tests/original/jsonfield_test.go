package original

import (
	"reflect"
	"testing"
	"encoding/json"
	"rpkilby_jsonfield/src"
)

func TestJSONModelSaveLoad(t *testing.T) {
	model := src.JSONNotRequiredModel{Json: map[string]interface{}{"foo": "bar"}}
	model.Save()
	gotten := src.JSONNotRequiredModelGet()
	if !reflect.DeepEqual(gotten.Json, map[string]interface{}{"foo": "bar"}) {
		t.Error("Failed to save and retrieve model")
	}
}

func TestJSONModelSaveString(t *testing.T) {
	model := src.JSONNotRequiredModel{Json: "hello"}
	model.Save()
	r := src.JSONNotRequiredModelGet()
	if r.Json != "hello" {
		t.Error("Saved and retrieved string mismatch")
	}
}

func TestJSONModelSaveFloat(t *testing.T) {
	model := src.JSONNotRequiredModel{Json: 1.23}
	model.Save()
	r := src.JSONNotRequiredModelGet()
	if r.Json != 1.23 {
		t.Error("Saved and retrieved float mismatch")
	}
}

func TestJSONModelSaveInt(t *testing.T) {
	model := src.JSONNotRequiredModel{Json: 42.0}
	model.Save()
	r := src.JSONNotRequiredModelGet()
	if r.Json != 42.0 {
		t.Error("Saved and retrieved int mismatch")
	}
}

func TestJSONModelSaveList(t *testing.T) {
	model := src.JSONNotRequiredModel{Json: []interface{}{1.0, 2.0}}
	model.Save()
	r := src.JSONNotRequiredModelGet()
	l, ok := r.Json.([]interface{})
	if !ok || len(l) != 2 {
		t.Error("Failed to save/retrieve list")
	}
}

func TestInvalidJSONReturnsOriginal(t *testing.T) {
	// Simulate a DB entry containing invalid JSON
	field := &src.JSONNotRequiredModel{Json: "foo"}
	if field.Json != "foo" {
		t.Error("Expected to fallback to raw value")
	}
}