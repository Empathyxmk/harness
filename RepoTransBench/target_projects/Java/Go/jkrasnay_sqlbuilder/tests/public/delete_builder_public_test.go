package public

import (
	"testing"
	"strings"
)

type PubDeleteBuilder struct {
	table string
	whereClauses []string
}

func NewPubDeleteBuilder(table string) *PubDeleteBuilder {
	return &PubDeleteBuilder{table: table}
}

func (b *PubDeleteBuilder) where(clause string) *PubDeleteBuilder {
	b.whereClauses = append(b.whereClauses, clause)
	return b
}

func (b *PubDeleteBuilder) String() string {
	if len(b.whereClauses) == 0 {
		return "delete from " + b.table
	}
	return "delete from " + b.table + " where " + strings.Join(b.whereClauses, " and ")
}

func TestDeleteBuilderPublic_Basics(t *testing.T) {
	if got := NewPubDeleteBuilder("Foo").String(); got != "delete from Foo" {
		t.Errorf("expected 'delete from Foo', got %v", got)
	}
	if got := NewPubDeleteBuilder("Foo").where("id = 1").String(); got != "delete from Foo where id = 1" {
		t.Errorf("expected 'delete from Foo where id = 1', got %v", got)
	}
}