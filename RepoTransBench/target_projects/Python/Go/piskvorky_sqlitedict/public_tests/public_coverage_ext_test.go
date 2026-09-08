package public_tests

import (
	"os"
	"testing"

	. "piskvorky_sqlitedict"
)

func TestPublicOpenCloseReopen(t *testing.T) {
	name := TempFile(t, "public", ".sqlite")
	d, err := NewSqliteDict(name, &SqliteDictOptions{Autocommit: true})
	if err != nil {
		t.Fatalf("open: %v", err)
	}
	if err := d.Set("foo", "bar"); err != nil {
		t.Fatalf("Set: %v", err)
	}
	if err := d.Set("baz", 45); err != nil {
		t.Fatalf("Set: %v", err)
	}
	d.Close()

	d2, err := NewSqliteDict(name, &SqliteDictOptions{Autocommit: true})
	if err != nil {
		t.Fatalf("open2: %v", err)
	}
	defer d2.Close()
	val, err := d2.Get("foo")
	if err != nil || val != "bar" {
		t.Errorf("Get(foo): got %v want bar", val)
	}
	val, err = d2.Get("baz")
	if err != nil || val != 45 {
		t.Errorf("Get(baz): got %v want 45", val)
	}
	d2.Close()
	os.Remove(name)
}

func TestPublicTableSeparation(t *testing.T) {
	name := TempFile(t, "publictbl", ".sqlite")
	d1, err := NewSqliteDict(name, &SqliteDictOptions{Tablename: "A", Autocommit: true})
	if err != nil {
		t.Fatalf("NewSqliteDict A: %v", err)
	}
	d2, err := NewSqliteDict(name, &SqliteDictOptions{Tablename: "B", Autocommit: true})
	if err != nil {
		t.Fatalf("NewSqliteDict B: %v", err)
	}
	if err := d1.Set("x1", "fooA"); err != nil {
		t.Fatalf("Set: %v", err)
	}
	if err := d2.Set("x1", "fooB"); err != nil {
		t.Fatalf("Set: %v", err)
	}
	d1.Close()
	d2.Close()

	d1b, err := NewSqliteDict(name, &SqliteDictOptions{Tablename: "A"})
	if err != nil {
		t.Fatalf("open A2: %v", err)
	}
	d2b, err := NewSqliteDict(name, &SqliteDictOptions{Tablename: "B"})
	if err != nil {
		t.Fatalf("open B2: %v", err)
	}
	val, _ := d1b.Get("x1")
	if val != "fooA" {
		t.Errorf("A x1 = %v, want fooA", val)
	}
	val, _ = d2b.Get("x1")
	if val != "fooB" {
		t.Errorf("B x1 = %v, want fooB", val)
	}
	d1b.Close()
	d2b.Close()
	os.Remove(name)
}

func TestPublicBasicSetGetDelAutocommit(t *testing.T) {
	d, err := NewSqliteDict(":memory:", &SqliteDictOptions{Autocommit: true})
	if err != nil {
		t.Fatalf("NewSqliteDict: %v", err)
	}
	if err := d.Set("xyz", 678); err != nil {
		t.Fatalf("Set: %v", err)
	}
	val, err := d.Get("xyz")
	if err != nil || val != 678 {
		t.Errorf("Get xyz = %v want 678", val)
	}
	if err := d.Delete("xyz"); err != nil {
		t.Errorf("Delete: %v", err)
	}
	has, err := d.Has("xyz")
	if err != nil {
		t.Errorf("Has: %v", err)
	}
	if has {
		t.Errorf("xyz still exists after delete")
	}
}

func TestPublicLenAndClear(t *testing.T) {
	d, err := NewSqliteDict(":memory:", nil)
	if err != nil {
		t.Fatalf("NewSqliteDict: %v", err)
	}
	keys := []string{"a", "b", "c", "d", "e", "f"}
	vals := []int{10, 11, 12, 13, 14, 15}
	for i, k := range keys {
		d.Set(k, vals[i])
	}
	if n := d.Len(); n != 6 {
		t.Errorf("Len() = %d want 6", n)
	}
	d.Clear()
	if n := d.Len(); n != 0 {
		t.Errorf("Len() after Clear = %d want 0", n)
	}
}

func TestPublicContainsPopAndKeys(t *testing.T) {
	d, _ := NewSqliteDict(":memory:", nil)
	d.Set("k1", 333)
	d.Set("k2", 444)
	d.Set("k3", 555)
	has, _ := d.Has("k1")
	if !has {
		t.Error("k1 not in d")
	}
	val, err := d.Pop("k2")
	if err != nil {
		t.Fatalf("Pop: %v", err)
	}
	if val != 444 {
		t.Errorf("Pop(k2) = %v want 444", val)
	}
	all, err := d.Keys()
	if err != nil {
		t.Fatalf("Keys: %v", err)
	}
	set := map[string]bool{}
	for _, k := range all {
		set[k] = true
	}
	if !(set["k1"] && set["k3"] && len(set) == 2) {
		t.Errorf("Keys = %+v, want only k1,k3", all)
	}
}