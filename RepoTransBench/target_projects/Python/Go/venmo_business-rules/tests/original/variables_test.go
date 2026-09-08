package original

import (
	"testing"
	"github.com/example/venmo_business_rules/businessrules"
)

func TestPrettyLabel(t *testing.T) {
	label := businessrules.FnNameToPrettyLabel("some_name_Of_a_thing")
	if label != "Some Name Of A Thing" {
		t.Errorf("Unexpected pretty label: %s", label)
	}
}

func TestRuleVariableRequiresBaseType(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("Expected panic on non-BaseType in rule_variable")
		}
	}()
	businessrules.RuleVariable("a_string", "foo", nil)
}

// ...Full test coverage for decorator internals, wrappers, and options for every rule variable type.