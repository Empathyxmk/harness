package original

import (
	"testing"
	"reflect"
	"github.com/example/xworkflows/src/xworkflows"
)

func TestIterclassTraversal(t *testing.T) {
	type A struct{ a int }
	type B struct {
		A
		b int
	}
	// Simulate setting static fields as in Python
	type_ := reflect.TypeOf(B{})
	m := xworkflows.Iterclass(type_) // This will not include actual values due to Go's limitations
	// Instead, check field names present
	if _, ok := m["a"]; !ok {
		t.Errorf("expected to find 'a' in iterclass keys")
	}
	if _, ok := m["b"]; !ok {
		t.Errorf("expected to find 'b' in iterclass keys")
	}
}

func TestIterclassOverrides(t *testing.T) {
	type A struct{ foo int }
	type B struct {
		A
		foo int
	}
	type_ := reflect.TypeOf(B{})
	m := xworkflows.Iterclass(type_)
	if _, ok := m["foo"]; !ok {
		t.Errorf("expected to find 'foo' in iterclass keys (override)")
	}
}