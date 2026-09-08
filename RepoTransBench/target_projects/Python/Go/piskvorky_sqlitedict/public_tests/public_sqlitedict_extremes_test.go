package public_tests

import (
	"os"
	"testing"

	. "piskvorky_sqlitedict"
)

func TestPublicSmallAndLargeKeysAndValues(t *testing.T) {
	d, err := NewSqliteDict(":memory:", nil)
	if err != nil {
		t.Fatalf("NewSqliteDict: %v", err)
	}
	// Trivial
	if err := d.Set("", "z"); err != nil {
		t.Fatalf("Set empty: %v", err)
	}
	val, _ := d.Get("")
	if val != "z" {
		t.Errorf(`Get("") = %#v, want "z"`, val)
	}
	key := ""
	for i := 0; i < 2000; i++ {
		key += "k"
	}
	valstr := ""
	for i := 0; i < 8000; i++ {
		valstr += "v"
	}
	if err := d.Set(key, valstr); err != nil {
		t.Fatalf("Set(long): %v", err)
	}
	got, err := d.Get(key)
	if err != nil || got != valstr {
		t.Errorf("Get(long) = %#v want %#v", got, valstr)
	}
}

func TestPublicLargeNumberOfKeys(t *testing.T) {
	d, _ := NewSqliteDict(":memory:", nil)
	N := 2117
	for i := 0; i < N; i++ {
		d.Set(itoa(i), i*7)
	}
	for i := 0; i < N; i++ {
		val, err := d.Get(itoa(i))
		if err != nil || val != i*7 {
			t.Errorf("Get(%d) = %v, want %d", i, val, i*7)
		}
	}
}

func TestPublicNumericValueTypes(t *testing.T) {
	d, _ := NewSqliteDict(":memory:", nil)
	d.Set("n1", 1.5)
	d.Set("n2", -42)
	d.Set("n3", 1<<30)
	d.Set("n4", 0)
	got1, _ := d.Get("n1")
	if got1 != 1.5 {
		t.Errorf("n1 = %v want 1.5", got1)
	}
	got2, _ := d.Get("n2")
	if got2 != -42 {
		t.Errorf("n2 = %v want -42", got2)
	}
	got3, _ := d.Get("n3")
	if got3 != (1 << 30) {
		t.Errorf("n3 = %v want %d", got3, 1<<30)
	}
	got4, _ := d.Get("n4")
	if got4 != 0 {
		t.Errorf("n4 = %v want 0", got4)
	}
}

func TestPublicUnicodeAndBinary(t *testing.T) {
	d, _ := NewSqliteDict(":memory:", nil)
	k := "unicø∂e"
	v := "välues💡"
	if err := d.Set(k, v); err != nil {
		t.Errorf("Set: %v", err)
	}
	got, _ := d.Get(k)
	if got != v {
		t.Errorf("Get(unicode) = %v, want %v", got, v)
	}
	bk := "\xff\xfe\xfd"
	bv := []byte{0, 1, 2}
	if err := d.Set(bk, bv); err != nil {
		t.Errorf("Set binary key: %v", err)
	}
	val, _ := d.Get(bk)
	b, ok := val.([]byte)
	if !ok || len(b) != 3 || b[0] != 0 || b[1] != 1 || b[2] != 2 {
		t.Errorf("Get(binary) = %v, want [0 1 2]", val)
	}
}

func TestPublicTempDBPersistence(t *testing.T) {
	name := TempFile(t, "pubpersist", ".sqlite")
	d, _ := NewSqliteDict(name, &SqliteDictOptions{Autocommit: true})
	if err := d.Set("foo", "bar"); err != nil {
		t.Fatalf("Set foo: %v", err)
	}
	if err := d.Set("baz", []int{1,2,3}); err != nil {
		t.Fatalf("Set baz: %v", err)
	}
	d.Close()
	d2, _ := NewSqliteDict(name, nil)
	v1, _ := d2.Get("foo")
	if v1 != "bar" {
		t.Errorf("foo = %v want bar", v1)
	}
	v2, _ := d2.Get("baz")
	a, ok := v2.([]int)
	if !ok || len(a) != 3 || a[0] != 1 {
		t.Errorf("baz = %v want [1 2 3]", v2)
	}
	d2.Close()
	os.Remove(name)
}

func itoa(x int) string {
	return fmt.Sprintf("%d", x)
}