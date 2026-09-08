package public_tests

import (
	"strings"
	"testing"
)

func TestDummyValuePublic(t *testing.T) {
	if strings.ToLower("DUMMY") == "DUMMY" {
		t.Errorf(`"DUMMY" should not be lowercase`)
	}
	// Equivalent to "DUMMY".islower() == False in Python:
	if strings.ToLower("DUMMY") == "DUMMY" {
		t.Errorf(`"DUMMY" .islower() is False in Python`)
	}
}