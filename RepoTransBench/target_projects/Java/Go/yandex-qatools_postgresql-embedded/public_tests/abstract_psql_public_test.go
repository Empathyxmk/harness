package public_tests

import (
	"testing"
)

type DummyPsql struct {
	sql string
}

func NewDummyPsql(sql string) *DummyPsql {
	return &DummyPsql{sql: sql}
}

func (d *DummyPsql) Run() string {
	if len(d.sql) >= 6 && d.sql[:6] == "SELECT" {
		return "OK-PUBLIC"
	}
	return "ERROR-PUBLIC"
}

func TestRunReturnsOkForPublicSelect(t *testing.T) {
	psql := NewDummyPsql("SELECT * FROM bar")
	if psql.Run() != "OK-PUBLIC" {
		t.Errorf("Expected OK-PUBLIC for SELECT, got '%s'", psql.Run())
	}
}

func TestRunReturnsErrorForPublicInsert(t *testing.T) {
	psql := NewDummyPsql("INSERT QQQ")
	if psql.Run() != "ERROR-PUBLIC" {
		t.Errorf("Expected ERROR-PUBLIC for INSERT, got '%s'", psql.Run())
	}
}