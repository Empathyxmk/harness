package original

import (
	"testing"
	"github.com/example/venmo_business_rules/businessrules"
)

func TestBaseHasNoVariables(t *testing.T) {
	vars := businessrules.BaseVariables{}.GetAllVariables()
	if len(vars) != 0 {
		t.Errorf("Expected 0 variables, got %d", len(vars))
	}
}

func TestGetAllVariables(t *testing.T) {
	type SomeVariables struct {
		businessrules.BaseVariables
	}
	// mock registry for decorator effect
	ruleName := "this_is_rule_1"
	label := "This Is Rule 1"
	sv := SomeVariables{}
	sv.RegisterVariable(ruleName, label, "string", []string{})

	vars := sv.GetAllVariables()
	if len(vars) != 1 {
		t.Fatalf("Expected 1 variable, got %d", len(vars))
	}
	v := vars[0]
	if v.Name != ruleName {
		t.Errorf("Expected variable name %s, got %s", ruleName, v.Name)
	}
	if v.Label != label {
		t.Errorf("Expected label %s, got %s", label, v.Label)
	}
	if v.FieldType != "string" {
		t.Errorf("Expected field_type string, got %s", v.FieldType)
	}
	if len(v.Options) != 0 {
		t.Errorf("Expected no options, got %v", v.Options)
	}

	if len((&sv).GetAllVariables()) != 1 {
		t.Error("Expected GetAllVariables to work on instance")
	}
}