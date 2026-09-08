package public

import (
	"testing"
	"strings"
)

type PubUpdateBuilder struct {
	table  string
	sets   []string
	wheres []string
}

func NewPubUpdateBuilder(table string) *PubUpdateBuilder {
	return &PubUpdateBuilder{table: table}
}

func (ub *PubUpdateBuilder) set(expr string) *PubUpdateBuilder {
	ub.sets = append(ub.sets, expr)
	return ub
}

func (ub *PubUpdateBuilder) where(expr string) *PubUpdateBuilder {
	ub.wheres = append(ub.wheres, expr)
	return ub
}

func (ub *PubUpdateBuilder) String() string {
	out := "update " + ub.table
	if len(ub.sets) > 0 {
		out += " set " + strings.Join(ub.sets, ", ")
	}
	if len(ub.wheres) > 0 {
		out += " where " + strings.Join(ub.wheres, " and ")
	}
	return out
}

func TestUpdateBuilderPublic_Basics(t *testing.T) {
	ub := NewPubUpdateBuilder("Profile").set("age = 30").where("username = 'tim'")
	expected := "update Profile set age = 30 where username = 'tim'"
	if got := ub.String(); got != expected {
		t.Errorf("expected %q, got %q", expected, got)
	}
}