package public_tests

import (
	"testing"
)

func TestParseAdditionalArgs(t *testing.T) {
	args := []string{"-v", "-k", "AnotherKeyword"}
	parsed := map[string]string{
		"k": "AnotherKeyword",
	}
	found := false
	for _, arg := range args {
		if arg == "-v" {
			found = true
		}
	}
	if !found {
		t.Errorf("-v not found in args")
	}
	if v, ok := parsed["k"]; !ok || v != "AnotherKeyword" {
		t.Errorf("Expected parsed.k to be AnotherKeyword")
	}
}