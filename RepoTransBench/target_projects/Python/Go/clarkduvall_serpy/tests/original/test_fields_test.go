package original

import (
	"reflect"
	"testing"
	"serpy"
	. "tests"
)

type ExampleStrField struct {
	serpy.Serializer
	Foo *serpy.StrField `serpy:"foo"`
}

func TestStrField(t *testing.T) {
	o := NewObj(map[string]interface{}{"foo": "hello"})
	ex := ExampleStrField{}
	data := ex.Serialize(o)
	result := data["foo"]
	if result != "hello" {
		t.Errorf("Expected foo to be 'hello', got %v", result)
	}
}

type ExampleIntField struct {
	serpy.Serializer
	Foo *serpy.IntField `serpy:"foo"`
}

func TestIntField(t *testing.T) {
	o := NewObj(map[string]interface{}{"foo": "23"})
	ex := ExampleIntField{}
	data := ex.Serialize(o)
	result := data["foo"]
	if result != 23 {
		t.Errorf("Expected foo to be 23, got %v (type %T)", result, result)
	}
}

type ExampleFloatField struct {
	serpy.Serializer
	Foo *serpy.FloatField `serpy:"foo"`
}

func TestFloatField(t *testing.T) {
	o := NewObj(map[string]interface{}{"foo": 2})
	ex := ExampleFloatField{}
	data := ex.Serialize(o)
	result := data["foo"]
	if result != 2.0 && result != float64(2.0) {
		t.Errorf("Expected foo to be 2.0, got %v", result)
	}
}

type ExampleBoolField struct {
	serpy.Serializer
	Foo *serpy.BoolField `serpy:"foo"`
}

func TestBoolField(t *testing.T) {
	o := NewObj(map[string]interface{}{"foo": 1})
	ex := ExampleBoolField{}
	data := ex.Serialize(o)
	result := data["foo"]
	if result != true {
		t.Errorf("Expected foo to be true, got %v", result)
	}
}

// Method field tests
type ExampleMethodField struct {
	serpy.Serializer
	Foo *serpy.MethodField `serpy:"foo"`
}

func (e *ExampleMethodField) GetFoo(obj *Obj) interface{} {
	return obj.Get("foo").(int) * 2
}

func TestMethodField(t *testing.T) {
	o := NewObj(map[string]interface{}{"foo": 3})
	ex := ExampleMethodField{}
	data := ex.Serialize(o)
	result := data["foo"]
	if result != 6 {
		t.Errorf("Expected foo to be 6, got %v", result)
	}
}