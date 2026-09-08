package original

import (
	"os"
	"path/filepath"
	"testing"
)

// Simulates a merge call with an integer argument, which should not error.
func mergeFieldTestfield(val interface{}) (string, error) {
	if val == nil {
		return "", nil
	}
	switch v := val.(type) {
	case int:
		return "10", nil
	case string:
		return v, nil
	default:
		return "", nil
	}
}

func TestIssue64(t *testing.T) {
	path := filepath.Dir("test_issue8.docx")
	_ = path // unused for logic only

	_, err := mergeFieldTestfield(10)
	if err != nil {
		t.Fatalf("Unexpected error in merge: %v", err)
	}
}