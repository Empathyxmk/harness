package public_tests

import (
	"reflect"
	"testing"
	"serpy"
	. "tests"
)

type AnotherPublicSerializer struct {
	serpy.Serializer
	Name  *serpy.StrField `serpy:"name"`
	Value *serpy.IntField `serpy:"value"`
}

type MethodPublicSerializer struct {
	serpy.Serializer
	Foo    *serpy.StrField    `serpy:"foo"`
	Double *serpy.MethodField `serpy:"double"`
}

func (s *MethodPublicSerializer) GetDouble(obj *Obj) interface{} {
	val := obj.Get("foo")
	if str, ok := val.(string); ok {
		return str + str
	}
	return val
}

func TestSerializerBasic(t *testing.T) {
	o := NewObj(map[string]interface{}{"name": "other", "value": 13})
	ser := AnotherPublicSerializer{}
	data := ser.Serialize(o)
	want := map[string]interface{}{"name": "other", "value": 13}
	if !reflect.DeepEqual(data, want) {
		t.Errorf("Expected %v, got %v", want, data)
	}
}

func TestSerializerMany(t *testing.T) {
	objects := []*Obj{
		NewObj(map[string]interface{}{"name": "x", "value": 2}),
		NewObj(map[string]interface{}{"name": "y", "value": 7}),
	}
	ser := AnotherPublicSerializer{}
	expected := []map[string]interface{}{
		{"name": "x", "value": 2},
		{"name": "y", "value": 7},
	}
	result := []map[string]interface{}{}
	for _, o := range objects {
		result = append(result, ser.Serialize(o))
	}
	if !reflect.DeepEqual(result, expected) {
		t.Errorf("Expected %v, got %v", expected, result)
	}
}

func TestMethodSerializer(t *testing.T) {
	o := NewObj(map[string]interface{}{"foo": "hello"})
	ser := MethodPublicSerializer{}
	data := ser.Serialize(o)
	want := map[string]interface{}{"foo": "hello", "double": "hellohello"}
	if !reflect.DeepEqual(data, want) {
		t.Errorf("Expected %v, got %v", want, data)
	}
}

func TestMethodSerializerMany(t *testing.T) {
	objects := []*Obj{
		NewObj(map[string]interface{}{"foo": "abc"}),
		NewObj(map[string]interface{}{"foo": "de"}),
	}
	ser := MethodPublicSerializer{}
	expected := []map[string]interface{}{
		{"foo": "abc", "double": "abcabc"},
		{"foo": "de", "double": "dede"},
	}
	result := []map[string]interface{}{}
	for _, o := range objects {
		result = append(result, ser.Serialize(o))
	}
	if !reflect.DeepEqual(result, expected) {
		t.Errorf("Expected %v, got %v", expected, result)
	}
}