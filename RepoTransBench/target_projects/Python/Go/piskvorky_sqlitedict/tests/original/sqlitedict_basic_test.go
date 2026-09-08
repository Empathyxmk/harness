package original

import (
	"os"
	"testing"

	. "piskvorky_sqlitedict"
)

func tempDBFile(t *testing.T) string {
	name := TempFile(t, "sqlitedb", ".sqlite")
	return name
}

func TestSetGetDelLenClear(t *testing.T) {
	name := tempDBFile(t)
	d, _ := NewSqliteDict(name, nil)
	defer d.Close()
	d.Set("a", 1)
	d.Set("b", 2)
	val, _ := d.Get("a")
	if val != 1 {
		t.Errorf("a = %v want 1", val)
	}
	val, _ = d.Get("b")
	if val != 2 {
		t.Errorf("b = %v want 2", val)
	}
	if d.Len() != 2 {
		t.Errorf("len want 2, got %d", d.Len())
	}
	d.Delete("a")
	if has, _ := d.Has("a"); has {
		t.Errorf("deleted key still present")
	}
	if d.Len() != 1 {
		t.Errorf("len want 1, got %d", d.Len())
	}
	d.Clear()
	if d.Len() != 0 {
		t.Errorf("len after clear want 0, got %d", d.Len())
	}
}

func TestContextManager(t *testing.T) {
	name := tempDBFile(t)
	d, _ := NewSqliteDict(name, nil)
	d.Set("foo", "bar")
	out, _ := d.Get("foo")
	if out != "bar" {
		t.Errorf("foo = %v want bar", out)
	}
	d.Close()
}

func TestCommitRemove(t *testing.T) {
	name := tempDBFile(t)
	d, _ := NewSqliteDict(name, nil)
	d.Set("a", 10)
	d.Commit()
	d.Set("b", 20)
	d.Clear()
	if d.Len() != 0 {
		t.Errorf("want 0 after clear, got %d", d.Len())
	}
}

func TestIterMethods(t *testing.T) {
	name := tempDBFile(t)
	d, _ := NewSqliteDict(name, nil)
	for i := 0; i < 5; i++ {
		d.Set(itoa(i), i)
	}
	keys, _ := d.Keys()
	// Convert keys to set
	set := make(map[string]bool)
	for _, k := range keys {
		set[k] = true
	}
	for i := 0; i < 5; i++ {
		if !set[itoa(i)] {
			t.Errorf("missing key %v", i)
		}
	}
	vals, _ := d.Values()
	valset := make(map[int]bool)
	for _, v := range vals {
		if vi, ok := v.(int); ok {
			valset[vi] = true
		}
	}
	for i := 0; i < 5; i++ {
		if !valset[i] {
			t.Errorf("missing val %v", i)
		}
	}
}

func TestGetDefault(t *testing.T) {
	name := tempDBFile(t)
	d, _ := NewSqliteDict(name, nil)
	v, err := d.Get("nonexistent")
	if err == nil && v != nil {
		t.Errorf("want nil for missing key, got %v", v)
	}
	defaultVal := 123
	out := d.GetDefault("nonexistent", defaultVal)
	if out != defaultVal {
		t.Errorf("GetDefault = %v, want %d", out, defaultVal)
	}
}

func TestUpdate(t *testing.T) {
	name := tempDBFile(t)
	d, _ := NewSqliteDict(name, nil)
	m := map[string]int{"x": 1, "y": 2}
	m2 := make(map[string]interface{})
	for k, v := range m {
		m2[k] = v
	}
	d.Update(m2)
	x, _ := d.Get("x")
	y, _ := d.Get("y")
	if x != 1 || y != 2 {
		t.Errorf("update failed: x=%v y=%v", x, y)
	}
}

func TestContains(t *testing.T) {
	name := tempDBFile(t)
	d, _ := NewSqliteDict(name, nil)
	d.Set("present", 1)
	if has, _ := d.Has("present"); !has {
		t.Errorf("present not in d")
	}
	if has, _ := d.Has("missing"); has {
		t.Errorf("missing found in d")
	}
}

func TestRepr(t *testing.T) {
	name := tempDBFile(t)
	d, _ := NewSqliteDict(name, nil)
	out := d.String()
	if out == "" {
		t.Errorf("repr should not be empty")
	}
	d.Close()
}

func TestSqliteDictNonExistingFile(t *testing.T) {
	name := tempDBFile(t)
	d, _ := NewSqliteDict(name, nil)
	d.Set("key", "val")
	d.Commit()
	d.Close()
	if _, err := os.Stat(name); err != nil {
		t.Errorf("file should exist: %s", name)
	}
	os.Remove(name)
}