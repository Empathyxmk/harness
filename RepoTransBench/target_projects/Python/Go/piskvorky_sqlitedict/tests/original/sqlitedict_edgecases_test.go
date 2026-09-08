package original

import (
	"testing"
	. "piskvorky_sqlitedict"
)

func TestIterationAndClear(t *testing.T) {
	name := TempFile(t, "iterclear", ".sqlite")
	d, _ := NewSqliteDict(name, nil)
	for i := 0; i < 10; i++ {
		d.Set(itoa(i), i)
	}
	d.Commit()
	keys, _ := d.Keys()
	if len(keys) != 10 {
		t.Errorf("keys len want 10, got %d", len(keys))
	}
	d.Clear()
	keys, _ = d.Keys()
	if len(keys) != 0 {
		t.Errorf("clear: still keys: %v", keys)
	}
	d.Close()
}

func TestPopAndUpdate(t *testing.T) {
	name := TempFile(t, "popupdate", ".sqlite")
	d, _ := NewSqliteDict(name, nil)
	d.Set("a", 10)
	d.Set("b", 20)
	d.Commit()
	val, _ := d.Pop("a")
	if val != 10 {
		t.Errorf("Pop a = %v want 10", val)
	}
	has, _ := d.Has("a")
	if has {
		t.Errorf("a not deleted")
	}
	m := map[string]interface{}{"c": 30, "d": 40}
	d.Update(m)
	c, _ := d.Get("c")
	if c != 30 {
		t.Errorf("c = %v want 30", c)
	}
	d.Close()
}

func TestDelitem(t *testing.T) {
	name := TempFile(t, "delitem", ".sqlite")
	d, _ := NewSqliteDict(name, nil)
	d.Set("x", 5)
	d.Commit()
	err := d.Delete("x")
	if err != nil {
		t.Errorf("Delete x: %v", err)
	}
	_, err = d.Get("x")
	if err == nil {
		t.Errorf("expected error after delete")
	}
	d.Close()
}

func TestLenAndContains(t *testing.T) {
	name := TempFile(t, "lencontains", ".sqlite")
	d, _ := NewSqliteDict(name, nil)
	d.Set("k1", 11)
	d.Set("k2", 22)
	d.Commit()
	if d.Len() != 2 {
		t.Errorf("len want 2")
	}
	has, _ := d.Has("k1")
	if !has {
		t.Errorf("k1 not found")
	}
	has, _ = d.Has("notkey")
	if has {
		t.Errorf("notkey should not exist")
	}
	d.Close()
}

func TestReprEdge(t *testing.T) {
	name := TempFile(t, "repr", ".sqlite")
	d, _ := NewSqliteDict(name, nil)
	d.Set("r", "v")
	s := d.String()
	if s == "" {
		t.Errorf("repr should not be empty")
	}
	d.Close()
}

func TestContextManagerEdge(t *testing.T) {
	name := TempFile(t, "ctx", ".sqlite")
	d, _ := NewSqliteDict(name, nil)
	d.Set("foo", "bar")
	d.Commit()
	d.Close()
	d2, _ := NewSqliteDict(name, nil)
	val, _ := d2.Get("foo")
	if val != "bar" {
		t.Errorf("foo = %v want bar", val)
	}
}

func TestFromDict(t *testing.T) {
	name := TempFile(t, "fromdict", ".sqlite")
	d, _ := NewSqliteDict(name, nil)
	d.Update(map[string]interface{}{"one": 1, "two": 2})
	d.Commit()
	got := map[string]interface{}{}
	keys, _ := d.Keys()
	for _, k := range keys {
		got[k], _ = d.Get(k)
	}
	if got["one"] != 1 || got["two"] != 2 {
		t.Errorf("fromdict got %v", got)
	}
	d.Close()
}

func TestCloseTwice(t *testing.T) {
	name := TempFile(t, "close2", ".sqlite")
	d, _ := NewSqliteDict(name, nil)
	d.Set("foo", 42)
	d.Close()
	if err := d.Close(); err != nil {
		t.Errorf("second close: %v", err)
	}
}