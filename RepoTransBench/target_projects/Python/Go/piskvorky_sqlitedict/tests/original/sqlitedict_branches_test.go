package original

import (
	"testing"
	. "piskvorky_sqlitedict"
)

func TestNamedDBBranch(t *testing.T) {
	name := TempFile(t, "named_db", ".sqlite")
	d1, _ := NewSqliteDict(name, &SqliteDictOptions{Tablename: "table1"})
	d2, _ := NewSqliteDict(name, &SqliteDictOptions{Tablename: "table2"})
	d1.Set("a", 1)
	d2.Set("b", 2)
	d1.Commit()
	d2.Commit()
	has, _ := d1.Has("a")
	if !has {
		t.Errorf("a not in d1")
	}
	has, _ = d2.Has("b")
	if !has {
		t.Errorf("b not in d2")
	}
	d1.Close()
	d2.Close()
}

func TestFlagAutocommitBranch(t *testing.T) {
	name := TempFile(t, "auto", ".sqlite")
	d, _ := NewSqliteDict(name, &SqliteDictOptions{Autocommit: true})
	d.Set("x", 1)
	d.Set("y", 2)
	d2, _ := NewSqliteDict(name, nil)
	x, _ := d2.Get("x")
	y, _ := d2.Get("y")
	if x != 1 {
		t.Errorf("x = %v", x)
	}
	if y != 2 {
		t.Errorf("y = %v", y)
	}
	d.Close()
	d2.Close()
}

func TestFlagEncodeKey(t *testing.T) {
	name := TempFile(t, "encode", ".sqlite")
	enc := func(x interface{}) ([]byte, error) {
		return []byte(strings.ToUpper(x.(string))), nil
	}
	dec := func(b []byte) (string, error) {
		return strings.ToLower(string(b)), nil
	}
	d, _ := NewSqliteDictCustom(name, enc, dec)
	d.Set("foo", "bar")
	d.Commit()
	keys, _ := d.Keys()
	if len(keys) != 1 || keys[0] != "foo" {
		t.Errorf("keys = %+v, want [foo]", keys)
	}
	d.Close()
}

func TestFlagDecodeKey(t *testing.T) {
	name := TempFile(t, "decode", ".sqlite")
	enc := func(x interface{}) ([]byte, error) {
		return append([]byte("a"), []byte(x.(string))...), nil
	}
	dec := func(b []byte) (string, error) {
		return string(b[1:]), nil
	}
	d, _ := NewSqliteDictCustom(name, enc, dec)
	d.Set("k", 11)
	d.Commit()
	has, _ := d.Has("k")
	if !has {
		t.Errorf("k not found")
	}
	d.Close()
}

func TestTableNameCollision(t *testing.T) {
	name := TempFile(t, "clash", ".sqlite")
	d1, _ := NewSqliteDict(name, &SqliteDictOptions{Tablename: "t"})
	d2, _ := NewSqliteDict(name, &SqliteDictOptions{Tablename: "t"})
	d1.Set("a", 1)
	d1.Commit()
	val, _ := d2.Get("a")
	if val != 1 {
		t.Errorf("d2 Get(a) = %v, want 1", val)
	}
	d1.Close()
	d2.Close()
}

func TestErrorOnClosed(t *testing.T) {
	name := TempFile(t, "closed", ".sqlite")
	d, _ := NewSqliteDict(name, nil)
	d.Set("a", 5)
	d.Close()
	if err := d.Set("b", 6); err == nil {
		t.Errorf("Set after close should fail")
	}
	if _, err := d.Get("a"); err == nil {
		t.Errorf("Get after close should fail")
	}
}

func TestInOperatorWithMissingKey(t *testing.T) {
	name := TempFile(t, "contain", ".sqlite")
	d, _ := NewSqliteDict(name, nil)
	has, _ := d.Has("zz")
	if has {
		t.Errorf("zz should not be present")
	}
	d.Close()
}