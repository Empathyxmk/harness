package original

import (
	"testing"
	. "piskvorky_sqlitedict"
)

func TestPickleFallback(t *testing.T) {
	// Go doesn't use Python's import hooks;
	// substitute: try creating SqliteDict, ensure all works
	_, err := NewSqliteDict(":memory:", nil)
	if err != nil {
		t.Fatalf("NewSqliteDict fallback: %v", err)
	}
}