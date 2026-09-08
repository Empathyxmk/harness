package public_tests

import (
	"testing"
	"github.com/example/venmo_business_rules/businessrules"
)

func TestBaseTypeValuePublic(t *testing.T) {
	bt := businessrules.BaseType{Value: "Value1"}
	if bt.Value != "Value1" {
		t.Errorf("Expected Value1, got %v", bt.Value)
	}
}
// ...All other inheritance checks.