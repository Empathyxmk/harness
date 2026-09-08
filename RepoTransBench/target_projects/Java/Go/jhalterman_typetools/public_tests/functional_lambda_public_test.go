package public_tests

import (
	"reflect"
	"testing"
)

func TestLambdaTypeResolution_IntegerToDouble_Public(t *testing.T) {
	f := func(i int) float64 { return float64(i) }
	typ := reflect.TypeOf(f)
	if typ.Kind() != reflect.Func {
		t.Errorf("Expected function type")
	}
}

func TestLambdaTypeResolution_StringToString_Public(t *testing.T) {
	f := func(s string) string { return s }
	typ := reflect.TypeOf(f)
	if typ.Kind() != reflect.Func {
		t.Errorf("Expected function type")
	}
}