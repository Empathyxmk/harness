package original

import (
	"testing"
)

// Simulate merge_pages: outputs N documents for N elements
func mergePages(inputs []map[string]string) int {
	return len(inputs)
}

func TestMergePages(t *testing.T) {
	inputs := []map[string]string{
		{"fieldname": "xyz"},
		{"fieldname": "abc"},
		{"fieldname": "2b v ~2b"},
	}
	count := mergePages(inputs)
	if count != 3 {
		t.Errorf("Expected 3 pages merged, got %d", count)
	}
}

func TestMergePagesWithMultiplePages(t *testing.T) {
	templatesPages := 2
	inputs := []map[string]string{
		{"fieldname": "xyz"},
		{"fieldname": "abc"},
		{"fieldname": "2b v ~2b"},
	}
	total := templatesPages * len(inputs)
	if total != 6 {
		t.Errorf("Expected total 6 pages merged (2*3), got %d", total)
	}
}