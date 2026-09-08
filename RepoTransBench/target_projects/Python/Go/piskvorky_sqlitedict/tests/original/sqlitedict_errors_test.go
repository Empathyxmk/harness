package original

import (
	"testing"
	. "piskvorky_sqlitedict"
)

func TestInvalidFilenameType(t *testing.T) {
	_, err := NewSqliteDict(12345, nil)
	if err == nil {
		t.Errorf("expected error for non-string filename")
	}
}

func TestInvalidFlag(t *testing.T) {
	name := TempFile(t, "flagerr", ".sqlite")
	_, err := NewSqliteDict(name, &SqliteDictOptions{Flag: "invalid"})
	if err == nil {
		t.Errorf("invalid flag should error")
	}
}

func TestClosedDictOperations(t *testing.T) {
	name := TempFile(t, "closedtest", ".sqlite")
	d, _ := NewSqliteDict(name, nil)
	d.Set("a", 123)
	d.Close()
	if err := d.Set("a", 999); err == nil {
		t.Errorf("should error on Set after close")
	}
	if _, err := d.Get("a"); err == nil {
		t.Errorf("should error on Get after close")
	}
	if err := d.Delete("a"); err == nil {
		t.Errorf("should error on Delete after close")
	}
	if err := d.Update(map[string]interface{}{"b": 1}); err == nil {
		t.Errorf("should error on Update after close")
	}
	_, err := d.Items()
	if err == nil {
		t.Errorf("should error on Items after close")
	}
}

func TestContainsWithClosed(t *testing.T) {
	name := TempFile(t, "c", ".sqlite")
	d, _ := NewSqliteDict(name, nil)
	d.Set("x", "y")
	d.Close()
	_, err := d.Has("x")
	if err == nil {
		t.Errorf("should error on Has after close")
	}
}