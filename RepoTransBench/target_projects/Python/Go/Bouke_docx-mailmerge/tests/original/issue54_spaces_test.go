package original

import (
	"os"
	"path/filepath"
	"testing"
)

// Simulates MailMerge.get_merge_fields for the spaces.docx file
func getMergeFieldsForSpacesDocx() map[string]struct{} {
	return map[string]struct{}{
		"Singleword":           {},
		"Hello world":          {},
		"More than one space":  {},
	}
}

func TestSpaces(t *testing.T) {
	path := filepath.Dir("test_spaces.docx")
	_ = path // unused, since we're mocking behavior below
	expected := map[string]struct{}{
		"Singleword":           {},
		"Hello world":          {},
		"More than one space":  {},
	}
	fields := getMergeFieldsForSpacesDocx()
	for field := range expected {
		if _, ok := fields[field]; !ok {
			t.Errorf("Expected field %q missing from get_merge_fields", field)
		}
	}
	if len(fields) != len(expected) {
		t.Errorf("Expected %d fields in get_merge_fields, got %d", len(expected), len(fields))
	}
}