package original

import (
	"testing"
)

// Simulate the core logic: merge rows functionality and that it produces the correct row count
func mergeTableRows(classRows []map[string]string) int {
	return len(classRows)
}

func TestMergeTableRows(t *testing.T) {
	classRows := []map[string]string{
		{"class_code": "ECON101", "class_name": "Economics 101", "class_grade": "A"},
		{"class_code": "ECONADV", "class_name": "Economics Advanced", "class_grade": "B"},
		{"class_code": "OPRES", "class_name": "Operations Research", "class_grade": "A"},
	}
	n := mergeTableRows(classRows)
	if n != 3 {
		t.Errorf("Expected 3 rows to be merged, got %d", n)
	}
}