package public_tests

import (
	"testing"
	"github.com/example/venmo_business_rules/businessrules"
)

func TestStringContainsPublic(t *testing.T) {
	s := businessrules.StringType("foobar")
	if !s.Contains("foo") {
		t.Error("Should contain string 'foo'")
	}
	if s.Contains("baz") {
		t.Error("Should not contain 'baz'")
	}
}
// ... More public operator tests as in Python source.