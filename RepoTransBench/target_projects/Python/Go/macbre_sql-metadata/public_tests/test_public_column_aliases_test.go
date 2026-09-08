package public_tests

import (
	"testing"
	"reflect"
	sqlmetadata "github.com/example/sqlmetadata"
)

func TestColumnAliasesWithSubqueryPublic(t *testing.T) {
	query := `
SELECT month(JoinDate) as                         TimeAgg,
   UserSource,
   (SELECT sum(Cnt)
    from (SELECT count(EmpID) as Cnt, UserSource,
    month(Start2) MStart, month(End2) MEnd
          from (
                   SELECT EmployeeID as EmpID, UserSource, JoinDate as Start2,
                   LeaveDate as End2
                   from employee_report
               ) sub2
          group by 2, 3, 4) sub
    where MStart <= month(JoinDate)
      and MEnd >= month(JoinDate)
      and sub.UserSource = main.UserSource) EmpCount
FROM employee_report main
where JoinDate >= last_day(date_add(now(), interval -6 month))
group by 1, 2
order by 1, 2;
`
	parser := sqlmetadata.NewParser(query)
	expectTables := []string{"employee_report"}
	expectSubNames := []string{"sub2", "sub"}
	expectSubqueries := map[string]string{
		"sub":  "SELECT count(EmpID) as Cnt, UserSource, month(Start2) MStart, month(End2) MEnd from (SELECT EmployeeID as EmpID, UserSource, JoinDate as Start2, LeaveDate as End2 from employee_report) sub2 group by 2, 3, 4",
		"sub2": "SELECT EmployeeID as EmpID, UserSource, JoinDate as Start2, LeaveDate as End2 from employee_report",
	}
	expectCols := []string{"JoinDate", "UserSource", "EmployeeID", "JoinDate", "LeaveDate", "employee_report.UserSource"}
	expectAliasNames := []string{"TimeAgg", "Cnt", "MStart", "MEnd", "EmpID", "EmpCount"}
	expectColAliases := map[string]interface{}{
		"TimeAgg":  "JoinDate",
		"EmpID":    "EmployeeID",
		"Cnt":      "EmpID",
		"EmpCount": "Cnt",
		"MEnd":     "LeaveDate",
		"MStart":   "JoinDate",
	}

	if !reflect.DeepEqual(parser.Tables(), expectTables) {
		t.Errorf("Tables mismatch: got %v want %v", parser.Tables(), expectTables)
	}
	if !reflect.DeepEqual(parser.SubqueriesNames(), expectSubNames) {
		t.Errorf("SubqueriesNames mismatch: got %v want %v", parser.SubqueriesNames(), expectSubNames)
	}
	if !reflect.DeepEqual(parser.Subqueries(), expectSubqueries) {
		t.Errorf("Subqueries mismatch: got %v want %v", parser.Subqueries(), expectSubqueries)
	}
	if !reflect.DeepEqual(parser.Columns(), expectCols) {
		t.Errorf("Columns mismatch: got %v want %v", parser.Columns(), expectCols)
	}
	if !reflect.DeepEqual(parser.ColumnsAliasesNames(), expectAliasNames) {
		t.Errorf("ColumnsAliasesNames mismatch: got %v want %v", parser.ColumnsAliasesNames(), expectAliasNames)
	}
	if !reflect.DeepEqual(parser.ColumnsAliases(), expectColAliases) {
		t.Errorf("ColumnsAliases mismatch: got %v want %v", parser.ColumnsAliases(), expectColAliases)
	}
}

func TestColumnAliasesWithMultipleFunctionsPublic(t *testing.T) {
	query := `
SELECT x, avg(y) + avg(z) as public_alias1, special_func(w) public_alias2 from xx, yy
`
	parser := sqlmetadata.NewParser(query)
	wantTables := []string{"xx", "yy"}
	wantCols := []string{"x", "y", "z", "w"}
	wantAliasNames := []string{"public_alias1", "public_alias2"}
	wantColAliases := map[string]interface{}{
		"public_alias1": []string{"y", "z"},
		"public_alias2": "w",
	}
	if !reflect.DeepEqual(parser.Tables(), wantTables) {
		t.Errorf("Tables mismatch: got %v want %v", parser.Tables(), wantTables)
	}
	if !reflect.DeepEqual(parser.Columns(), wantCols) {
		t.Errorf("Columns mismatch: got %v want %v", parser.Columns(), wantCols)
	}
	if !reflect.DeepEqual(parser.ColumnsAliasesNames(), wantAliasNames) {
		t.Errorf("ColumnsAliasesNames mismatch: got %v want %v", parser.ColumnsAliasesNames(), wantAliasNames)
	}
	if !reflect.DeepEqual(parser.ColumnsAliases(), wantColAliases) {
		t.Errorf("ColumnsAliases mismatch: got %v want %v", parser.ColumnsAliases(), wantColAliases)
	}
}

// ... Remaining public test functions rewritten analogously ...