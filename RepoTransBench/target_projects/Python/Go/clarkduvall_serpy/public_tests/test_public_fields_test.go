package public_tests

import (
	"strings"
	"testing"
	"serpy"
	. "tests"
)

func TestStrField(t *testing.T) {
	type TestSerializer struct {
		serpy.Serializer
		Foo *serpy.StrField `serpy:"foo"`
	}
	o := NewObj(map[string]interface{}{"foo": "differentstr"})
	ser := TestSerializer{}
	data := ser.Serialize(o)
	if data["foo"] != "differentstr" {
		t.Errorf("Expected foo to be 'differentstr', got %v", data["foo"])
	}
}

func TestIntField(t *testing.T) {
	type TestSerializer struct {
		serpy.Serializer
		Bar *serpy.IntField `serpy:"bar"`
	}
	o := NewObj(map[string]interface{}{"bar": 100})
	ser := TestSerializer{}
	data := ser.Serialize(o)
	if data["bar"] != 100 {
		t.Errorf("Expected bar to be 100, got %v", data["bar"])
	}
}

func TestMethodField(t *testing.T) {
	type TestSerializer struct {
		serpy.Serializer
		Special *serpy.MethodField `serpy:"special"`
	}
	var ser TestSerializer
	ser.GetSpecial = func(obj *Obj) interface{} {
		s, ok := obj.Get("foo").(string)
		if !ok {
			t.Fatalf("foo field is not a string: %v", obj.Get("foo"))
		}
		return strings.ToUpper(s)
	}
	o := NewObj(map[string]interface{}{"foo": "public"})
	data := ser.Serialize(o)
	if data["special"] != "PUBLIC" {
		t.Errorf("Expected special to be 'PUBLIC', got %v", data["special"])
	}
}

func TestMissingValueField(t *testing.T) {
	type TestSerializer struct {
		serpy.Serializer
		Bar *serpy.MethodField `serpy:"bar"`
	}
	var ser TestSerializer
	ser.GetBar = func(obj *Obj) interface{} {
		if v, ok := obj.data["bar"]; ok {
			return v
		}
		return nil
	}
	o := NewObj(map[string]interface{}{})
	data := ser.Serialize(o)
	if data["bar"] != nil {
		t.Errorf("Expected bar to be nil, got %v", data["bar"])
	}
}