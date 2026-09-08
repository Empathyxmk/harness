package tests

import (
	"testing"
	"strings"
)

type UpdateBuilder struct {
	table    string
	sets     []string
	wheres   []string
}

func NewUpdateBuilder(table string) *UpdateBuilder {
	return &UpdateBuilder{table: table}
}

func (ub *UpdateBuilder) set(expr string) *UpdateBuilder {
	ub.sets = append(ub.sets, expr)
	return ub
}

func (ub *UpdateBuilder) where(expr string) *UpdateBuilder {
	ub.wheres = append(ub.wheres, expr)
	return ub
}

func (ub *UpdateBuilder) String() string {
	out := "update " + ub.table
	if len(ub.sets) > 0 {
		out += " set " + strings.Join(ub.sets, ", ")
	}
	if len(ub.wheres) > 0 {
		out += " where " + strings.Join(ub.wheres, " and ")
	}
	return out
}

func TestUpdateBuilder_All(t *testing.T) {
	ub := NewUpdateBuilder("Employee")
	if got := ub.String(); got != "update Employee" {
		t.Errorf("expected 'update Employee', got %v", got)
	}
	ub.set("name = 'Bobo'")
	if got := ub.String(); got != "update Employee set name = 'Bobo'" {
		t.Errorf("expected 'update Employee set name = 'Bobo'', got %v", got)
	}
	ub.set("age = 37")
	if got := ub.String(); got != "update Employee set name = 'Bobo', age = 37" {
		t.Errorf("expected more sets, got %v", got)
	}
	ub.where("name = 'Arnold'")
	if got := ub.String(); got != "update Employee set name = 'Bobo', age = 37 where name = 'Arnold'" {
		t.Errorf("expected where, got %v", got)
	}
	ub.where("age = 17")
	if got := ub.String(); got != "update Employee set name = 'Bobo', age = 37 where name = 'Arnold' and age = 17" {
		t.Errorf("expected multiple wheres, got %v", got)
	}
}