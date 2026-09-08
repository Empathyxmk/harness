package public

import (
	"testing"
	"strings"
)

type PubSelectBuilder struct {
	columns     []string
	table       string
	whereClause string
}

func NewPubSelectBuilder(table string) *PubSelectBuilder {
	return &PubSelectBuilder{table: table}
}

func (sb *PubSelectBuilder) column(col string) *PubSelectBuilder {
	sb.columns = append(sb.columns, col)
	return sb
}

func (sb *PubSelectBuilder) where(clause string) *PubSelectBuilder {
	sb.whereClause = clause
	return sb
}

func (sb *PubSelectBuilder) String() string {
	cols := "*"
	if len(sb.columns) > 0 {
		cols = strings.Join(sb.columns, ", ")
	}
	query := "select " + cols + " from " + sb.table
	if sb.whereClause != "" {
		query += " where " + sb.whereClause
	}
	return query
}

func TestSelectBuilderPublic_Basics(t *testing.T) {
	sb := NewPubSelectBuilder("UserTable").column("id").column("username")
	if got := sb.String(); got != "select id, username from UserTable" {
		t.Errorf("got %v", got)
	}
	sb = NewPubSelectBuilder("UserTable").where("active = 1")
	if got := sb.String(); got != "select * from UserTable where active = 1" {
		t.Errorf("got %v", got)
	}
}