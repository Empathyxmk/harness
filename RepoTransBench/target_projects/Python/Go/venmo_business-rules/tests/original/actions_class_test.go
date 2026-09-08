package original

import (
	"testing"
	"github.com/example/venmo_business_rules/businessrules"
)

func TestBaseHasNoActions(t *testing.T) {
	actions := businessrules.BaseActions{}.GetAllActions()
	if len(actions) != 0 {
		t.Errorf("Expected 0 actions, got %d", len(actions))
	}
}

func TestGetAllActions(t *testing.T) {
	type TestActions struct {
		businessrules.BaseActions
	}
	ta := TestActions{}
	ta.RegisterAction("some_action", "Some Action", []businessrules.ActionParam{
		{FieldType: "text", Name: "foo", Label: "Foo"},
	})
	actions := ta.GetAllActions()
	if len(actions) != 1 {
		t.Errorf("Expected 1 action, got %d", len(actions))
	}
	act := actions[0]
	if act.Name != "some_action" {
		t.Errorf("Expected action name 'some_action', got '%s'", act.Name)
	}
}

// ... Implement unknown param/field type error checks and rule_action_no_label similarly.