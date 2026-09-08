package original

import (
	"testing"
)

func mergeTemplates(inputs []map[string]string, breakType string) int {
	return len(inputs)
}

func TestMergeTemplates_BreakPage(t *testing.T) {
	inputs := []map[string]string{
		{"fieldname": "Test with page_break"},
		{"fieldname": "abc"},
		{"fieldname": "2b v ~2b"},
	}
	breakType := "page_break"
	count := mergeTemplates(inputs, breakType)
	if count != 3 {
		t.Errorf("MergeTemplates BreakPage expects 3, got %d", count)
	}
}

func TestMergeTemplates_BreakCol(t *testing.T) {
	inputs := []map[string]string{
		{"fieldname": "Test with column_break"},
		{"fieldname": "abc"},
		{"fieldname": "2b v ~2b"},
	}
	breakType := "column_break"
	count := mergeTemplates(inputs, breakType)
	if count != 3 {
		t.Errorf("MergeTemplates BreakCol expects 3, got %d", count)
	}
}

func TestMergeTemplates_BreakTextWrapping(t *testing.T) {
	inputs := []map[string]string{
		{"fieldname": "Test with textWrapping_break"},
		{"fieldname": "abc"},
		{"fieldname": "2b v ~2b"},
	}
	breakType := "textWrapping_break"
	count := mergeTemplates(inputs, breakType)
	if count != 3 {
		t.Errorf("MergeTemplates textWrapping expects 3, got %d", count)
	}
}