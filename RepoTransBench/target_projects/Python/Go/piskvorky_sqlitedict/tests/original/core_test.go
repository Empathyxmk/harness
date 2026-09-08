package original

import (
	"testing"
	. "piskvorky_sqlitedict"
)

func TestCoreSanity(t *testing.T) {
	// Minimal core test: can create a dict and store/retrieve values
	d, err := NewSqliteDict(":memory:", nil)
	if err != nil {
		t.Errorf("NewSqliteDict: %v", err)
	}
	defer d.Close()
	d.Set("ping", "pong")
	v, err := d.Get("ping")
	if err != nil || v != "pong" {
		t.Errorf("Get ping: %v, want pong", v)
	}
}