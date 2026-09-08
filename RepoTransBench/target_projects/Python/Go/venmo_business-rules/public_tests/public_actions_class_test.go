package public_tests

import (
	"testing"
	"github.com/example/venmo_business_rules/businessrules"
)

func TestGetAllActionsPublic(t *testing.T) {
	type TestActions struct{ businessrules.BaseActions }
	ta := TestActions{}
	ta.RegisterAction("bye_public", "Omega", []businessrules.ActionParam{
		{FieldType: "text", Label: "Bar Foo", Name: "bar_foo"},
	})
	actions := ta.GetAllActions()
	if len(actions) != 1 {
		t.Fatalf("Should have one action, got %d", len(actions))
	}
	if actions[0].Name != "bye_public" {
		t.Errorf("Expected bye_public, got %s", actions[0].Name)
	}
}