package public_tests

import (
	"reflect"
	"testing"
)

func typename(val interface{}) string {
	r := reflect.TypeOf(val)
	if r.Kind() == reflect.String {
		return "str"
	} else if r.Kind() == reflect.Ptr || r.Kind() == reflect.Struct {
		return "type"
	}
	return r.String()
}

func TestSimpleTypeReturnsTypeNameAsStringPublic(t *testing.T) {
	got := typename("abc")
	if got != "str" {
		t.Errorf("expected 'str', got %s", got)
	}
}

func TestClassObjectPublic(t *testing.T) {
	type Y struct{}
	got := typename(Y{})
	if got != "type" {
		t.Errorf("expected 'type', got %s", got)
	}
}