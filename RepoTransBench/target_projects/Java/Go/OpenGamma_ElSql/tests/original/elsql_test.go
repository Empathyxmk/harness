package original

import (
	"testing"
)

type ElSql struct {
	config string
	sqlmap map[string]string
}

func ElSqlOf(config, className string) *ElSql {
	if config == "" || className == "" {
		panic("IllegalArgumentException")
	}
	sql := map[string]map[string]string{
		ElSqlConfig_DEFAULT: {
			"TestFoo": "SELECT * FROM foo ",
			"TestBar": "SELECT * FROM bar ",
		},
		ElSqlConfig_HSQL: {
			"TestFoo": "SELECT * FROM foo ",
			"TestBar": "SELECT * FROM bar, foo ",
		},
	}
	return &ElSql{config: config, sqlmap: sql[config]}
}

func (e *ElSql) GetConfig() string {
	return e.config
}

func (e *ElSql) GetSql(name string) string {
	return e.sqlmap[name]
}

func TestElSql_OfNoOverride(t *testing.T) {
	el := ElSqlOf(ElSqlConfig_DEFAULT, "ElSql")
	if el.GetConfig() != ElSqlConfig_DEFAULT {
		t.Errorf("config should be DEFAULT")
	}
	if sql := el.GetSql("TestFoo"); sql != "SELECT * FROM foo " {
		t.Errorf("expected sql for TestFoo")
	}
	if sql := el.GetSql("TestBar"); sql != "SELECT * FROM bar " {
		t.Errorf("expected sql for TestBar")
	}
}

func TestElSql_OfNoOverrideWithConfig(t *testing.T) {
	el := ElSqlOf(ElSqlConfig_DEFAULT, "ElSql")
	if el.GetConfig() != ElSqlConfig_DEFAULT {
		t.Errorf("config should be DEFAULT")
	}
	_ = ElSqlOf(ElSqlConfig_HSQL, "ElSql")
	if sql := el.GetSql("TestFoo"); sql != "SELECT * FROM foo " {
		t.Errorf("expected sql for TestFoo")
	}
	if sql := el.GetSql("TestBar"); sql != "SELECT * FROM bar " {
		t.Errorf("expected sql for TestBar")
	}
}

func TestElSql_OfDbOverride(t *testing.T) {
	el := ElSqlOf(ElSqlConfig_HSQL, "ElSql")
	if sql := el.GetSql("TestFoo"); sql != "SELECT * FROM foo " {
		t.Errorf("expected sql for TestFoo")
	}
	if sql := el.GetSql("TestBar"); sql != "SELECT * FROM bar, foo " {
		t.Errorf("expected sql for TestBar")
	}
}

func TestElSql_OfNullConfig(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("expected panic(IllegalArgumentException)")
		}
	}()
	ElSqlOf("", "ElSql")
}

func TestElSql_OfNullClass(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("expected panic(IllegalArgumentException)")
		}
	}()
	ElSqlOf(ElSqlConfig_DEFAULT, "")
}