package original

import (
	"testing"
	"newbeginning6subdir/org/example"
)

func TestIsValid(t *testing.T) {
	if !example.CheckTargetIsValid("http://test.com") {
		t.Errorf("Should be valid")
	}
	if example.CheckTargetIsValid("invalid_string") {
		t.Errorf("Should not be valid")
	}
	if example.CheckTargetIsValid("") {
		t.Errorf("Should not be valid for empty string")
	}
}

func TestSanitize(t *testing.T) {
	if example.CheckTargetSanitize("abc") != "abc" {
		t.Errorf("Sanitize did not return same string")
	}
	if example.CheckTargetSanitize("") != "" {
		t.Errorf("Sanitize empty string failed")
	}
	if example.CheckTargetSanitize("") != "" {
		t.Errorf("Sanitize on empty string should be empty")
	}
}