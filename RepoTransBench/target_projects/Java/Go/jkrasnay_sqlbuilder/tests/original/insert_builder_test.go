package tests

import (
	"testing"
	"strings"
)

type InsertBuilder struct {
	table   string
	columns []string
	values  []string
}

func NewInsertBuilder(table string) *InsertBuilder {
	return &InsertBuilder{table: table}
}

func (b *InsertBuilder) set(col, val string) {
	b.columns = append(b.columns, col)
	b.values = append(b.values, val)
}

func (b *InsertBuilder) String() string {
	if len(b.columns) == 0 {
		return "insert into " + b.table + " () values ()"
	}
	return "insert into " + b.table + " (" +
		strings.Join(b.columns, ", ") + ") values (" +
		strings.Join(b.values, ", ") + ")"
}

func TestInsertBuilder_All(t *testing.T) {
	builder := NewInsertBuilder("Employee")
	if got := builder.String(); got != "insert into Employee () values ()" {
		t.Errorf("expected initial insert, got %v", got)
	}

	builder.set("id", "1")
	if got := builder.String(); got != "insert into Employee (id) values (1)" {
		t.Errorf("expected single col insert, got %v", got)
	}

	builder.set("name", "'Bobo'")
	if got := builder.String(); got != "insert into Employee (id, name) values (1, 'Bobo')" {
		t.Errorf("expected double col insert, got %v", got)
	}
}