package public_tests

import (
	"testing"
	"reflect"
	sqlmetadata "github.com/example/sqlmetadata"
)

func TestPublicComplexQueryAliases(t *testing.T) {
	query := `
SELECT
    X.x_id as xid,
    Y.y_value,
    SUM(Z.amount) as total_amount,
    subq.test_val as sub_val
FROM
    source_db.table_x X
    JOIN source_db.table_y Y ON X.y_id = Y.y_id
    LEFT JOIN (
        SELECT
            ref_id,
            MAX(some_val) as test_val
        FROM source_db.table_z
        GROUP BY ref_id
    ) subq ON X.x_id = subq.ref_id
WHERE
    Y.active_flag = 1
GROUP BY
    1, 2, 4
ORDER BY
    4 DESC
`
	parser := sqlmetadata.NewParser(query)
	wantAliases := map[string]string{
		"X":    "source_db.table_x",
		"Y":    "source_db.table_y",
		"subq": "source_db.table_z",
	}
	wantTables := []string{
		"source_db.table_x",
		"source_db.table_y",
		"source_db.table_z",
	}
	if !reflect.DeepEqual(parser.TablesAliases(), wantAliases) {
		t.Errorf("TablesAliases mismatch: got %v want %v", parser.TablesAliases(), wantAliases)
	}
	if !reflect.DeepEqual(parser.Tables(), wantTables) {
		t.Errorf("Tables mismatch: got %v want %v", parser.Tables(), wantTables)
	}
}