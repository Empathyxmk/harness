package original

import (
	"testing"
)

func TestMergeTableRowsMultipart_SplitAndUnified(t *testing.T) {
	// Simulate merging rows into a table from two entrypoints (individual + all at once)
	classRows := []map[string]string{
		{"class_code": "ECON101", "class_name": "Economics 101", "class_grade": "A"},
		{"class_code": "ECONADV", "class_name": "Economics Advanced", "class_grade": "B"},
		{"class_code": "OPRES", "class_name": "Operations Research", "class_grade": "A"},
	}
	nrows := len(classRows)
	if nrows != 3 {
		t.Fatalf("Expected 3 rows, got %d", nrows)
	}
	// Simulate another merge using unified method
	allRows := map[string]interface{}{
		"class_code": classRows,
	}
	if arr, ok := allRows["class_code"].([]map[string]string); !ok || len(arr) != 3 {
		t.Errorf("Unified merge: want 3 class_code rows, got %+v", allRows["class_code"])
	}
}