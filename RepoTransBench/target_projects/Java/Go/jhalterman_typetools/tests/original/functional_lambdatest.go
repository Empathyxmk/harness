package original

import (
	"reflect"
	"testing"
)

func TestLambda_IntegerToInt(t *testing.T) {
	f := func(i int) int { return i }
	typ := reflect.TypeOf(f)
	if typ.Kind() != reflect.Func {
		t.Errorf("Expected function type")
	}
}

func TestLambda_StringToString(t *testing.T) {
	f := func(s string) string { return s }
	typ := reflect.TypeOf(f)
	if typ.Kind() != reflect.Func {
		t.Errorf("Expected function type")
	}
}