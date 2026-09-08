package public_tests

import (
	"reflect"
	"testing"

	"github.com/example/xworkflows/src/xworkflows"
)

func TestIterclassTraversalDifferent(t *testing.T) {
	type C struct{ x int }
	type D struct {
		C
		y int
	}
	type_ := reflect.TypeOf(D{})
	m := xworkflows.Iterclass(type_)
	if _, ok := m["x"]; !ok {
		t.Errorf("expected to find 'x' in iterclass keys")
	}
	if _, ok := m["y"]; !ok {
		t.Errorf("expected to find 'y' in iterclass keys")
	}
}

func TestIterclassOverridesDifferent(t *testing.T) {
	type C struct{ alpha int }
	type D struct {
		C
		alpha int
	}
	type_ := reflect.TypeOf(D{})
	m := xworkflows.Iterclass(type_)
	if _, ok := m["alpha"]; !ok {
		t.Errorf("expected to find 'alpha' in iterclass keys (override)")
	}
}