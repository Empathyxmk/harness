package tests

import (
	"testing"
	"strings"
)

type DeleteBuilder struct {
	table       string
	whereClauses []string
}

func NewDeleteBuilder(table string) *DeleteBuilder {
	return &DeleteBuilder{table: table}
}

func (b *DeleteBuilder) where(clause string) *DeleteBuilder {
	b.whereClauses = append(b.whereClauses, clause)
	return b
}

func (b *DeleteBuilder) String() string {
	if len(b.whereClauses) == 0 {
		return "delete from " + b.table
	}
	return "delete from " + b.table + " where " + strings.Join(b.whereClauses, " and ")
}

func TestDeleteBuilder_All(t *testing.T) {
	if got := NewDeleteBuilder("Foo").String(); got != "delete from Foo" {
		t.Errorf("expected 'delete from Foo', got %v", got)
	}
	if got := NewDeleteBuilder("Foo").where("id = 1").String(); got != "delete from Foo where id = 1" {
		t.Errorf("expected 'delete from Foo where id = 1', got %v", got)
	}
	if got := NewDeleteBuilder("Foo").where("id = 1").where("colour = 'red'").String(); got != "delete from Foo where id = 1 and colour = 'red'" {
		t.Errorf("expected 'delete from Foo where id = 1 and colour = 'red'', got %v", got)
	}
}