package original

import (
	"reflect"
	"strings"
	"testing"
	"serpy"
	. "tests"
)

type DummyObj struct {
	A         int
	B         int
	MethodVal int
	C         interface{}
}

func NewDummyObj(a int, b int, c interface{}, methodVal int) *DummyObj {
	return &DummyObj{A: a, B: b, C: c, MethodVal: methodVal}
}

func (d *DummyObj) Meth() int {
	return d.MethodVal
}

// Test simple serialization.
type ExSerializer struct {
	serpy.Serializer
	A *serpy.IntField `serpy:"a"`
	B *serpy.IntField `serpy:"b"`
}

func TestSimpleSerialization(t *testing.T) {
	o := NewDummyObj(4, 5, nil, 5)
	ex := ExSerializer{}
	got := ex.Serialize(o)
	want := map[string]interface{}{
		"a": 4,
		"b": 5,
	}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("Expected %v, got %v", want, got)
	}
}

// Test MethodField with custom label.
type ExMethodLabelSerializer struct {
	serpy.Serializer
	Foo *serpy.MethodField `serpy:"maybe"`
}

func (e *ExMethodLabelSerializer) GetFoo(obj *DummyObj) interface{} {
	return obj.MethodVal
}

func TestMethodAndCustomLabels(t *testing.T) {
	o := NewDummyObj(1, 2, nil, 42)
	ex := ExMethodLabelSerializer{}
	data := ex.Serialize(o)
	if _, ok := data["maybe"]; !ok {
		t.Errorf("'maybe' label not present in serialized data")
	}
	if data["maybe"] != 42 {
		t.Errorf("Expected 'maybe' to be 42, got %v", data["maybe"])
	}
}

// DictSerializer test.
type DSer struct {
	serpy.DictSerializer
	X *serpy.IntField `serpy:"x"`
	Y *serpy.IntField `serpy:"y"`
}

func TestDictSerializer(t *testing.T) {
	d := map[string]interface{}{"x": 10, "y": 21}
	ex := DSer{}
	got := ex.SerializeDict(d)
	want := map[string]interface{}{
		"x": 10,
		"y": 21,
	}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("Expected %v, got %v", want, got)
	}
}

// Edge case and repr
type ExampleReprSerializer struct {
	serpy.Serializer
	Foo *serpy.Field `serpy:"foo"`
}

func TestEdgeCasesAndRepr(t *testing.T) {
	o := NewObj(map[string]interface{}{"foo": "edgecase"})
	ex := ExampleReprSerializer{}
	reprStr := ex.String()
	if !strings.Contains(reprStr, "ExampleReprSerializer") {
		t.Errorf("Expected string representation to include ExampleReprSerializer, got %s", reprStr)
	}
}