package original

import (
	"testing"
	"github.com/example/venmo_business_rules/businessrules"
	"reflect"
)

func TestStringEqualTo(t *testing.T) {
	s := businessrules.StringType("foo")
	if !s.EqualTo("foo") {
		t.Error("Expected EqualTo to return true for identical strings")
	}
	if s.EqualTo("Foo") {
		t.Error("Expected EqualTo to return false for case-sensitive difference")
	}
}

// ... Implement all string, numeric, boolean, select, selectMultiple operator tests