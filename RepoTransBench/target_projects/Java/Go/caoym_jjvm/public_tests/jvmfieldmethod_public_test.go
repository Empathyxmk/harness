package public_tests

import (
	"testing"
)

type JvmField struct {
	name  string
	typ   string
	value interface{}
	_stat bool
}

func NewJvmField(name, typ string, value interface{}, stat bool) *JvmField {
	return &JvmField{name: name, typ: typ, value: value, _stat: stat}
}

func (f *JvmField) getValue() interface{}            { return f.value }
func (f *JvmField) setValue(val interface{})         { f.value = val }

func TestAccessDifferentPrimitiveFields(t *testing.T) {
	intField := NewJvmField("score", "I", 7, false)
	boolField := NewJvmField("visible", "Z", true, false)

	if intField.getValue() != 7 {
		t.Errorf("Expected 7, got %v", intField.getValue())
	}
	if boolField.getValue() != true {
		t.Errorf("Expected true, got %v", boolField.getValue())
	}

	intField.setValue(42)
	if intField.getValue() != 42 {
		t.Errorf("Expected 42 after set, got %v", intField.getValue())
	}

	boolField.setValue(false)
	if boolField.getValue() != false {
		t.Errorf("Expected false after set, got %v", boolField.getValue())
	}
}

func TestStringFieldDifferentValue(t *testing.T) {
	strField := NewJvmField("owner", "Ljava/lang/String;", "robot", false)
	if strField.getValue() != "robot" {
		t.Errorf("Expected 'robot', got %v", strField.getValue())
	}

	strField.setValue("android")
	if strField.getValue() != "android" {
		t.Errorf("Expected 'android' after set, got %v", strField.getValue())
	}
}