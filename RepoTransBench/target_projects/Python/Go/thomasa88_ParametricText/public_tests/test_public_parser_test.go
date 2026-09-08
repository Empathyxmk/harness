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

func TestParamSpecNameValue(t *testing.T) {
	spec := NewParamSpec("public_name", "17")
	if spec.ParamName != "public_name" {
		t.Errorf("Expected ParamName 'public_name', got %q", spec.ParamName)
	}
	if spec.ParamValue != "17" {
		t.Errorf("Expected ParamValue '17', got %q", spec.ParamValue)
	}
}

func TestParamSpecStrAndEq(t *testing.T) {
	spec1 := NewParamSpec("ab", "9")
	spec2 := NewParamSpec("ab", "9")
	spec3 := NewParamSpec("ab", "8")
	if exp := "(ab, 9)"; spec1.String() != exp {
		t.Errorf("Expected %q, got %q", exp, spec1.String())
	}
	if !spec1.Equal(spec2) {
		t.Errorf("spec1 == spec2 expected")
	}
	if spec1.Equal(spec3) {
		t.Errorf("spec1 != spec3 expected")
	}
}