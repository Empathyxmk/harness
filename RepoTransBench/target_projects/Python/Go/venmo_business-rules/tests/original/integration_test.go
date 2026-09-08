package original

import (
	"testing"
	"github.com/example/venmo_business_rules/businessrules"
)

type SomeVariables struct {
	businessrules.BaseVariables
}

func (SomeVariables) Foo() string      { return "foo" }
func (SomeVariables) Ten() int         { return 10 }
func (SomeVariables) TrueBool() bool   { return true }

type SomeActions struct {
	businessrules.BaseActions
}

func (SomeActions) SomeAction(foo int)                     {}
func (SomeActions) SomeOtherAction(bar string)             {}
func (SomeActions) SomeSelectAction(baz string)            {}

func TestTrueBooleanVariable(t *testing.T) {
	cond := businessrules.Condition{Name: "true_bool", Operator: "is_true", Value: ""}
	if !businessrules.CheckCondition(cond, SomeVariables{}) {
		t.Error("Expected true_bool to be true")
	}
}

func TestFalseBooleanVariable(t *testing.T) {
	cond := businessrules.Condition{Name: "true_bool", Operator: "is_false", Value: ""}
	if businessrules.CheckCondition(cond, SomeVariables{}) {
		t.Error("Expected false for is_false operator")
	}
}

// ... implement all the other integration tests: contains, export_rule_data, error cases, etc.