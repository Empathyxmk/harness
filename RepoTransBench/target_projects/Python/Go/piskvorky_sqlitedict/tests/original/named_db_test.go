package original

import (
	"testing"
	. "piskvorky_sqlitedict"
)

func TestInMemorySqliteDict(t *testing.T) {
	d, err := NewSqliteDict(":memory:", &SqliteDictOptions{Autocommit: true})
	if err != nil {
		t.Fatalf("NewSqliteDict: %v", err)
	}
	defer d.Close()
	d.Set("abc", "def")
	v, _ := d.Get("abc")
	if v != "def" {
		t.Errorf("abc = %v, want def", v)
	}
}

func TestNamedSqliteDict(t *testing.T) {
	name := "tests/db/sqlitedict-with-def.sqlite"
	d, _ := NewSqliteDict(name, nil)
	defer d.Close()
	_ = d // The actual datafile should exist
}

func TestCreateNewSqliteDict(t *testing.T) {
	name := "tests/db/sqlitedict-with-n-flag.sqlite"
	d, _ := NewSqliteDict(name, &SqliteDictOptions{Flag: "n"})
	defer d.Close()
}

func TestStartsWithEmptySqliteDict(t *testing.T) {
	name := "tests/db/sqlitedict-with-w-flag.sqlite"
	d, _ := NewSqliteDict(name, &SqliteDictOptions{Flag: "w"})
	defer d.Close()
}

func TestSqliteDictAutocommitNamed(t *testing.T) {
	name := "tests/db/sqlitedict-autocommit.sqlite"
	d, _ := NewSqliteDict(name, &SqliteDictOptions{Autocommit: true})
	defer d.Close()
}