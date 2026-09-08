package original

import (
	"os"
	"testing"
	. "piskvorky_sqlitedict"
)

func TestAutocommitExternalScript(t *testing.T) {
	// Simulate an external script writing many entries into a DB, check they're still there
	const dbfile = "tests/db/autocommit.sqlite"
	const N = 1000
	// (This will require the main library to create the DB and add N keys, for the test to pass)
	d, _ := NewSqliteDict(dbfile, nil)
	defer d.Close()
	for i := 0; i < N; i++ {
		v, err := d.Get(i)
		if err != nil || v != i {
			t.Fatalf("key %d: got %v (err %v), want %d", i, v, err, i)
		}
	}
}