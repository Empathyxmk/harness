package public_tests

import (
	"testing"
	sqlmetadata "github.com/example/sqlmetadata"
)

func TestPublicDropTable(t *testing.T) {
	parser := sqlmetadata.NewParser("DROP TABLE bar")
	if parser.QueryType() != sqlmetadata.QueryTypeDrop {
		t.Errorf("Expected QueryType.Drop, got %v", parser.QueryType())
	}
	wantTables := []string{"bar"}
	wantCols := []string{}
	if !EqualStringSlices(parser.Tables(), wantTables) {
		t.Errorf("Tables mismatch: got %v want %v", parser.Tables(), wantTables)
	}
	if !EqualStringSlices(parser.Columns(), wantCols) {
		t.Errorf("Columns mismatch: got %v want %v", parser.Columns(), wantCols)
	}
}

// Helper for slices equality
func EqualStringSlices(a, b []string) bool {
	if len(a) != len(b) {
		return false
	}
	for i := range a {
		if a[i] != b[i] {
			return false
		}
	}
	return true
}