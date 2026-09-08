package tests

import (
	"testing"
	"strings"
)

type SelectBuilder struct {
	columns   []string
	table     string
	whereClauses []string
	joinClauses  []string
	orderClauses []string
	forUpdate    bool
	limitClause  string
	unionBuilder *SelectBuilder
}

func NewSelectBuilder(table ...string) *SelectBuilder {
	sb := &SelectBuilder{}
	if len(table) > 0 {
		sb.table = table[0]
	}
	return sb
}

func (sb *SelectBuilder) column(name string) *SelectBuilder {
	sb.columns = append(sb.columns, name)
	return sb
}

func (sb *SelectBuilder) from(table string) *SelectBuilder {
	sb.table = table
	return sb
}

func (sb *SelectBuilder) where(clause string) *SelectBuilder {
	sb.whereClauses = append(sb.whereClauses, clause)
	return sb
}

func (sb *SelectBuilder) join(clause string) *SelectBuilder {
	sb.joinClauses = append(sb.joinClauses, clause)
	return sb
}

func (sb *SelectBuilder) orderBy(clause string) *SelectBuilder {
	sb.orderClauses = append(sb.orderClauses, clause)
	return sb
}

func (sb *SelectBuilder) forUpdate() *SelectBuilder {
	sb.forUpdate = true
	return sb
}

func (sb *SelectBuilder) limit(args ...int) *SelectBuilder {
	if len(args) == 1 {
		sb.limitClause = "limit " + itoa(args[0])
	} else if len(args) == 2 {
		sb.limitClause = "limit " + itoa(args[0]) + ", " + itoa(args[1])
	}
	return sb
}

func (sb *SelectBuilder) union(other *SelectBuilder) *SelectBuilder {
	sb.unionBuilder = other
	return sb
}

func (sb *SelectBuilder) String() string {
	parts := []string{"select"}
	if len(sb.columns) == 0 {
		parts = append(parts, "*")
	} else {
		parts = append(parts, strings.Join(sb.columns, ", "))
	}
	parts = append(parts, "from", sb.table)
	if len(sb.joinClauses) > 0 {
		for _, j := range sb.joinClauses {
			parts = append(parts, "join", j)
		}
	}
	if len(sb.whereClauses) > 0 {
		parts = append(parts, "where")
		parts = append(parts, strings.Join(sb.whereClauses, " and "))
	}
	if sb.unionBuilder != nil {
		parts = append(parts, "union", sb.unionBuilder.String())
	}
	if len(sb.orderClauses) > 0 {
		parts = append(parts, "order by")
		parts = append(parts, strings.Join(sb.orderClauses, ", "))
	}
	if sb.limitClause != "" {
		parts = append(parts, sb.limitClause)
	}
	if sb.forUpdate {
		parts = append(parts, "for update")
	}
	return strings.Join(parts, " ")
}

func TestSelectBuilder_Basics(t *testing.T) {
	sb := NewSelectBuilder("Employee")
	if got := sb.String(); got != "select * from Employee" {
		t.Errorf("expected 'select * from Employee', got %v", got)
	}

	sb = NewSelectBuilder("Employee e")
	if got := sb.String(); got != "select * from Employee e" {
		t.Errorf("expected 'select * from Employee e', got %v", got)
	}

	sb = NewSelectBuilder("Employee e").column("name")
	if got := sb.String(); got != "select name from Employee e" {
		t.Errorf("expected 'select name from Employee e', got %v", got)
	}

	sb = NewSelectBuilder("Employee e").column("name").column("age")
	if got := sb.String(); got != "select name, age from Employee e" {
		t.Errorf("expected 'select name, age from Employee e', got %v", got)
	}

	sb = NewSelectBuilder("Employee e").column("name as n").column("age")
	if got := sb.String(); got != "select name as n, age from Employee e" {
		t.Errorf("expected 'select name as n, age from Employee e', got %v", got)
	}

	sb = NewSelectBuilder("Employee e").where("name like 'Bob%'")
	if got := sb.String(); got != "select * from Employee e where name like 'Bob%'" {
		t.Errorf("expected where, got %v", got)
	}

	sb = NewSelectBuilder("Employee e").where("name like 'Bob%'").where("age > 37")
	if got := sb.String(); got != "select * from Employee e where name like 'Bob%' and age > 37" {
		t.Errorf("expected double where, got %v", got)
	}

	sb = NewSelectBuilder("Employee e").join("Department d on e.dept_id = d.id")
	if got := sb.String(); got != "select * from Employee e join Department d on e.dept_id = d.id" {
		t.Errorf("expected join, got %v", got)
	}

	sb = NewSelectBuilder("Employee e").join("Department d on e.dept_id = d.id").where("name like 'Bob%'")
	if got := sb.String(); got != "select * from Employee e join Department d on e.dept_id = d.id where name like 'Bob%'" {
		t.Errorf("expected join+where, got %v", got)
	}

	sb = NewSelectBuilder("Employee e").orderBy("name")
	if got := sb.String(); got != "select * from Employee e order by name" {
		t.Errorf("expected order by, got %v", got)
	}

	sb = NewSelectBuilder("Employee e").orderBy("name desc").orderBy("age")
	if got := sb.String(); got != "select * from Employee e order by name desc, age" {
		t.Errorf("expected double order, got %v", got)
	}

	sb = NewSelectBuilder("Employee").where("name like 'Bob%'").orderBy("age")
	if got := sb.String(); got != "select * from Employee where name like 'Bob%' order by age" {
		t.Errorf("expected where+order, got %v", got)
	}

	sb = NewSelectBuilder("Employee").where("id = 42").forUpdate()
	if got := sb.String(); got != "select * from Employee where id = 42 for update" {
		t.Errorf("expected for update, got %v", got)
	}
}

func TestSelectBuilder_Limits(t *testing.T) {
	sb := NewSelectBuilder().from("test_table").column("a").column("b").limit(10)
	if got := sb.String(); got != "select a, b from test_table limit 10" {
		t.Errorf("expected limit, got %v", got)
	}

	sb = sb.limit(10, 4)
	if got := sb.String(); got != "select a, b from test_table limit 10, 4" {
		t.Errorf("expected limit offset, got %v", got)
	}
}

func TestSelectBuilder_Unions(t *testing.T) {
	sb := NewSelectBuilder().
		column("a").
		column("b").
		from("Foo").
		where("a > 10").
		orderBy("1")

	sb.union(NewSelectBuilder().
		column("c").
		column("d").
		from("Bar"))

	if got := sb.String(); got != "select a, b from Foo where a > 10 union select c, d from Bar order by 1" {
		t.Errorf("expected union, got %v", got)
	}
}