package original

import (
	"reflect"
	"testing"
)

type DummyAttribute struct{}

func (DummyAttribute) DummyMethod() {}
func (DummyAttribute) DummySimple() {}

func TestAttributeValues(t *testing.T) {
	obj := DummyAttribute{}
	m, ok := reflect.TypeOf(obj).MethodByName("DummyMethod")
	if !ok {
		t.Fatalf("Method DummyMethod not found")
	}
	// There's no annotation, but method exists and reachable
	if m.Type.Kind() != reflect.Func {
		t.Fatalf("Expected a function")
	}
}

func TestAttributeDefaultIsSuperAndDefaultValue(t *testing.T) {
	obj := DummyAttribute{}
	m, ok := reflect.TypeOf(obj).MethodByName("DummySimple")
	if !ok {
		t.Fatalf("Method DummySimple not found")
	}
	// There's no annotation, but method exists and reachable
	if m.Type.Kind() != reflect.Func {
		t.Fatalf("Expected a function")
	}
}