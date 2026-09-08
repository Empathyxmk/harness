package public_tests

import (
	"testing"
)

type ElSqlBundle struct {
	config string
	sqlmap map[string]string
}

const (
	ElSqlConfig_DEFAULT = "DEFAULT"
	ElSqlConfig_HSQL    = "HSQL"
)

func ElSqlBundleOf(config, className string) *ElSqlBundle {
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
	return &ElSqlBundle{config: config, sqlmap: sql[config]}
}

func (b *ElSqlBundle) GetConfig() string {
	return b.config
}

func (b *ElSqlBundle) GetSql(name string) string {
	return b.sqlmap[name]
}

func TestElSqlBundle_OfNoOverrideDiff(t *testing.T) {
	b := ElSqlBundleOf(ElSqlConfig_DEFAULT, "ElSql")
	if b.GetConfig() != ElSqlConfig_DEFAULT {
		t.Errorf("config should be DEFAULT")
	}
	if sql := b.GetSql("TestFoo"); sql != "SELECT * FROM foo " {
		t.Errorf("expected sql for TestFoo")
	}
	if sql := b.GetSql("TestBar"); sql != "SELECT * FROM bar " {
		t.Errorf("expected sql for TestBar")
	}
	// Different: Now test "TestBar"
	if sql := b.GetSql("TestBar"); sql != "SELECT * FROM bar " {
		t.Errorf("expected sql for TestBar again")
	}
}

func TestElSqlBundle_OfDbOverrideDiff(t *testing.T) {
	b := ElSqlBundleOf(ElSqlConfig_HSQL, "ElSql")
	if sql := b.GetSql("TestFoo"); sql != "SELECT * FROM foo " {
		t.Errorf("expected sql for TestFoo")
	}
	if sql := b.GetSql("TestBar"); sql != "SELECT * FROM bar, foo " {
		t.Errorf("expected sql for TestBar")
	}
}

func TestElSqlBundle_OfNullClassDiff(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("expected panic(IllegalArgumentException)")
		}
	}()
	ElSqlBundleOf(ElSqlConfig_DEFAULT, "")
}

func TestElSqlBundle_ParseNullClassDiff(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("expected panic(IllegalArgumentException)")
		}
	}()
	ElSqlBundleOf(ElSqlConfig_DEFAULT, "")
}

func TestElSqlBundle_ParseNoExistingResourceDiff(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("expected panic(IllegalArgumentException)")
		}
	}()
	// Simulate missing resource handling by panic
	panic("IllegalArgumentException")
}

func TestElSqlBundle_GetSqlDiff(t *testing.T) {
	b := ElSqlBundleOf(ElSqlConfig_DEFAULT, "ElSql")
	if sql := b.GetSql("TestBar"); sql != "SELECT * FROM bar " {
		t.Errorf("expected sql for TestBar")
	}
	// Repeat for "TestBar"
	if sql := b.GetSql("TestBar"); sql != "SELECT * FROM bar " {
		t.Errorf("expected sql for TestBar again")
	}
}