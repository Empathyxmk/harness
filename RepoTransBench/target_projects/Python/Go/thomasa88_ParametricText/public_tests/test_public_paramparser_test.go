package public_tests

import (
	"testing"
	"fmt"
)

type ParamSpec struct {
	ParamName  string
	ParamValue string
}
func NewParamSpec(name, val string) ParamSpec {
	return ParamSpec{ParamName: name, ParamValue: val}
}
func (p ParamSpec) String() string {
	return fmt.Sprintf("(%s, %s)", p.ParamName, p.ParamValue)
}
func (a ParamSpec) Equal(b ParamSpec) bool {
	return a.ParamName == b.ParamName && a.ParamValue == b.ParamValue
}

func TestParamSpecBasic(t *testing.T) {
	p := NewParamSpec("anotherparam", "anotherval")
	if p.ParamName == "" {
		t.Errorf("Expected ParamName, got empty")
	}
}

func TestParamSpecStr(t *testing.T) {
	p := NewParamSpec("customparam", "val42")
	exp := "(customparam, val42)"
	if p.String() != exp {
		t.Errorf("Expected %q, got %q", exp, p.String())
	}
}

func TestParamSpecEq(t *testing.T) {
	p1 := NewParamSpec("eqtest", "a")
	p2 := NewParamSpec("eqtest", "a")
	p3 := NewParamSpec("eqtest", "b")
	if !p1.Equal(p2) {
		t.Errorf("p1 == p2 expected")
	}
	if p1.Equal(p3) {
		t.Errorf("p1 != p3 expected")
	}
}