package public_tests

import (
	"reflect"
	"testing"
)

type AttrPublicStruct struct{}

func (AttrPublicStruct) PublicMethod(param string) {}
func (AttrPublicStruct) AttrMethod(param string)   {}

func TestAttributeAnnotationPublicPresent(t *testing.T) {
	m, ok := reflect.TypeOf(AttrPublicStruct{}).MethodByName("PublicMethod")
	if !ok {
		t.Fatalf("Expected method 'PublicMethod' to exist")
	}
	if m.Type.Kind() != reflect.Func {
		t.Fatalf("Expected 'PublicMethod' to be function kind")
	}
}

func TestParameterAnnotationPublicPresent(t *testing.T) {
	m, ok := reflect.TypeOf(AttrPublicStruct{}).MethodByName("PublicMethod")
	if !ok {
		t.Fatalf("Expected method 'PublicMethod' to exist")
	}
	if m.Type.NumIn() != 2 {
		t.Fatalf("Expected number of input params = 2 (receiver + param), got %d", m.Type.NumIn())
	}
}