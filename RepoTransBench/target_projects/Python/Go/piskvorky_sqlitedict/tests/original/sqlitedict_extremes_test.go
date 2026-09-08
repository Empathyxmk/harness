package original

import (
	"testing"
	. "piskvorky_sqlitedict"
)

func TestSqliteDictAutocommit(t *testing.T) {
	name := TempFile(t, "auto", ".sqlite")
	d, err := NewSqliteDict(name, &SqliteDictOptions{Autocommit: true})
	if err != nil {
		t.Fatalf("create: %v", err)
	}
	defer d.Close()
	if err := d.Set("foo", 42); err != nil {
		t.Fatalf("Set foo: %v", err)
	}
	if err := d.Set("bar", 123); err != nil {
		t.Fatalf("Set bar: %v", err)
	}
	d.Close()
	d2, err := NewSqliteDict(name, nil)
	if err != nil {
		t.Fatalf("open2: %v", err)
	}
	defer d2.Close()
	v, err := d2.Get("foo")
	if err != nil || v != 42 {
		t.Errorf("foo want 42 got %v err=%v", v, err)
	}
	v, err = d2.Get("bar")
	if err != nil || v != 123 {
		t.Errorf("bar want 123 got %v err=%v", v, err)
	}
}