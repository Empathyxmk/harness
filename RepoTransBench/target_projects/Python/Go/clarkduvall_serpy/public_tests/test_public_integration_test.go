package public_tests

import (
	"reflect"
	"strings"
	"testing"
	"serpy"
	. "tests"
)

// IntegrationPublicSerializer mirrors the Python test
type IntegrationPublicSerializer struct {
	serpy.Serializer
	A *serpy.IntField     `serpy:"a"`
	B *serpy.StrField     `serpy:"b"`
	C *serpy.MethodField  `serpy:"c"`
	D *serpy.MethodField  `serpy:"d"`
}

func (s *IntegrationPublicSerializer) GetC(obj *Obj) interface{} {
	val, ok := obj.data["b"]
	if !ok {
		return ""
	}
	b, ok := val.(string)
	if ok {
		return b + b
	}
	return val
}

func (s *IntegrationPublicSerializer) GetD(obj *Obj) interface{} {
	if d, ok := obj.data["d"]; ok {
		return d
	} else {
		return nil
	}
}

func TestAllFields(t *testing.T) {
	obj := NewObj(map[string]interface{}{"a": 99, "b": "foo", "d": 255})
	ser := IntegrationPublicSerializer{}
	data := ser.Serialize(obj)
	want := map[string]interface{}{
		"a": 99,
		"b": "foo",
		"c": "foofoo",
		"d": 255,
	}
	if !reflect.DeepEqual(data, want) {
		t.Errorf("Expected %v, got %v", want, data)
	}
}

func TestMissingField(t *testing.T) {
	obj := NewObj(map[string]interface{}{"a": 44, "b": "echo"})
	ser := IntegrationPublicSerializer{}
	data := ser.Serialize(obj)
	want := map[string]interface{}{
		"a": 44,
		"b": "echo",
		"c": "echoecho",
		"d": nil,
	}
	if !reflect.DeepEqual(data, want) {
		t.Errorf("Expected %v, got %v", want, data)
	}
}

// Many support
func TestListMany(t *testing.T) {
	objs := []*Obj{
		NewObj(map[string]interface{}{"a": 8, "b": "a"}),
		NewObj(map[string]interface{}{"a": 9, "b": "Xx", "d": 777}),
	}
	ser := IntegrationPublicSerializer{}
	res := []map[string]interface{}{}
	for _, o := range objs {
		res = append(res, ser.Serialize(o))
	}
	expected := []map[string]interface{}{
		{"a": 8, "b": "a", "c": "aa", "d": nil},
		{"a": 9, "b": "Xx", "c": "XxXx", "d": 777},
	}
	if !reflect.DeepEqual(res, expected) {
		t.Errorf("Expected %v, got %v", expected, res)
	}
}