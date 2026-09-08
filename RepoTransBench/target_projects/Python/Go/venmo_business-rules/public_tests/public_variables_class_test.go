package public_tests

import (
	"testing"
	"github.com/example/venmo_business_rules/businessrules"
)

func TestBaseHasNoVariablesPublic(t *testing.T) {
	vars := businessrules.BaseVariables{}.GetAllVariables()
	if len(vars) != 0 {
		t.Errorf("Expected 0 variables")
	}
}

func TestGetAllVariablesPublic(t *testing.T) {
	type PubVar struct{ businessrules.BaseVariables }
	pv := PubVar{}
	pv.RegisterVariable("another_rule", "Public Rule Label", "string", []string{})
	vars := pv.GetAllVariables()
	if len(vars) != 1 {
		t.Fatal("Should have one public variable")
	}
	v := vars[0]
	if v.Name != "another_rule" {
		t.Errorf("Expected name another_rule, got %s", v.Name)
	}
	if v.Label != "Public Rule Label" {
		t.Errorf("Label mismatch: got %s", v.Label)
	}
}