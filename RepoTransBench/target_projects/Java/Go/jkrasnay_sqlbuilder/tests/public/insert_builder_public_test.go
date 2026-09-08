package public

import (
	"testing"
	"strings"
)

type PubInsertBuilder struct {
	table string
	cols  []string
	vals  []string
}

func NewPubInsertBuilder(table string) *PubInsertBuilder {
	return &PubInsertBuilder{table: table}
}

func (b *PubInsertBuilder) set(col, val string) {
	b.cols = append(b.cols, col)
	b.vals = append(b.vals, val)
}

func (b *PubInsertBuilder) String() string {
	if len(b.cols) == 0 {
		return "insert into " + b.table + " () values ()"
	}
	return "insert into " + b.table + " (" +
		strings.Join(b.cols, ", ") + ") values (" +
		strings.Join(b.vals, ", ") + ")"
}

func TestInsertBuilderPublic_Basics(t *testing.T) {
	b := NewPubInsertBuilder("User")
	b.set("name", "'Alice'")
	if got := b.String(); got != "insert into User (name) values ('Alice')" {
		t.Errorf("expected insert, got %v", got)
	}
}