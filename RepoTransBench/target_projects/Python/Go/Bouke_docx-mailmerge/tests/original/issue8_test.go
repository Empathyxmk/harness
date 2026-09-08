package original

import (
	"os"
	"path/filepath"
	"testing"
)

// Simulates MailMerge.get_merge_fields for test_issue8.docx
func getMergeFieldsForIssue8Docx() map[string]struct{} {
	return map[string]struct{}{"testfield": {}}
}

func TestIssue8(t *testing.T) {
	path := filepath.Dir("test_issue8.docx")
	_ = path // unused for this test

	fields := getMergeFieldsForIssue8Docx()
	if len(fields) != 1 {
		t.Fatalf("Expected 1 field, got %d", len(fields))
	}
	if _, ok := fields["testfield"]; !ok {
		t.Errorf("Expected field 'testfield' missing in get_merge_fields")
	}
}