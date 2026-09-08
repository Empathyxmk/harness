package original

import (
	"reflect"
	"testing"
	"serpy"
	. "tests"
)

// Field(label) test
type ExampleLabelField struct {
	serpy.Serializer
	FooLabel *serpy.Field `serpy:"foo_out"`
}

func TestLabelField(t *testing.T) {
	ex := ExampleLabelField{}
	o := NewObj(map[string]interface{}{"foo": "thing"})
	data := ex.SerializeWithAttr(o, map[string]string{"foo_label": "foo"})
	if data["foo_out"] != "thing" {
		t.Errorf("Expected foo_out to be 'thing', got %v", data["foo_out"])
	}
}

type ExampleToValue struct {
	serpy.Serializer
	One *serpy.IntField `serpy:"one"`
	Two *serpy.IntField `serpy:"two"`
}

func TestSerializerToValue(t *testing.T) {
	o := NewObj(map[string]interface{}{"one": 1, "two": 2})
	ex := ExampleToValue{}
	val := ex.ToValue(o)
	want := map[string]interface{}{"one": 1, "two": 2}
	if !reflect.DeepEqual(val, want) {
		t.Errorf("Expected %v, got %v", want, val)
	}
}

type ExampleMissingAttr struct {
	serpy.Serializer
	Foo *serpy.Field `serpy:"foo"`
}

func TestMissingAttr(t *testing.T) {
	o := NewObj(map[string]interface{}{"bar": "baz"})
	ex := ExampleMissingAttr{}
	data := ex.SerializeWithAttr(o, map[string]string{"foo": "bar"})
	if data["foo"] != "baz" {
		t.Errorf("Expected foo to be 'baz', got %v", data["foo"])
	}
}