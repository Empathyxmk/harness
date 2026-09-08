package original

import (
	"testing"
)

func TestProtectedField(t *testing.T) {
	dummy := &dummyProtectedObject{}
	dummy.setValue("foo")
	if got := dummy.getValue(); got != "foo" {
		t.Errorf("Expected %q, got %q", "foo", got)
	}
}

func TestProtectedSetter(t *testing.T) {
	dummy := &dummyProtectedObject{}
	dummy.setValue("baz")
	if got := dummy.getValue(); got != "baz" {
		t.Errorf("Expected %q, got %q", "baz", got)
	}
}

type dummyProtectedObject struct {
	field string
}

func (d *dummyProtectedObject) setValue(val string) {
	d.field = val
}
func (d *dummyProtectedObject) getValue() string {
	return d.field
}