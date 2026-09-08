package original

import (
	"reflect"
	"testing"
)

func typename(val interface{}) string {
	r := reflect.TypeOf(val)
	if r.Kind() == reflect.String {
		return "str"
	} else if r.Kind() == reflect.Ptr || r.Kind() == reflect.Struct {
		if r.Name() == "" {
			return "type"
		}
		return "type"
	}
	return r.String()
}

func TestSimpleTypeReturnsTypeNameAsString(t *testing.T) {
	got := typename("x")
	if got != "str" {
		t.Errorf("expected 'str', got %s", got)
	}
}

func TestClassObject(t *testing.T) {
	type X struct{}
	got := typename(X{})
	if got != "type" {
		t.Errorf("expected 'type', got %s", got)
	}
}