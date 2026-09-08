package original

import (
	"testing"
	. "piskvorky_sqlitedict"
)

func TestReadonlyFlag(t *testing.T) {
	name := TempFile(t, "ro", ".sqlite")
	d, _ := NewSqliteDict(name, nil)
	d.Set("k", "val")
	d.Commit()
	d.Close()

	d2, _ := NewSqliteDict(name, &SqliteDictOptions{Flag: "r"})
	v, _ := d2.Get("k")
	if v != "val" {
		t.Errorf("k = %v, want val", v)
	}
	if err := d2.Set("set_fail", 123); err == nil {
		t.Errorf("expected error for readonly Set")
	}
	d2.Close()
}

func TestKeysValuesItems(t *testing.T) {
	name := TempFile(t, "kv", ".sqlite")
	d, _ := NewSqliteDict(name, nil)
	mp := map[string]int{"abc": 1, "def": 2}
	m := make(map[string]interface{})
	for k, v := range mp {
		m[k] = v
	}
	d.Update(m)
	d.Commit()
	keys, _ := d.Keys()
	vals, _ := d.Values()
	items, _ := d.Items()
	for _, k := range keys {
		if _, ok := mp[k]; !ok {
			t.Errorf("extra key %s", k)
		}
	}
	valMatches := 0
	for _, v := range vals {
		for _, want := range mp {
			if v == want {
				valMatches++
				break
			}
		}
	}
	if valMatches < len(mp) {
		t.Errorf("not all vals found: %v", vals)
	}
	_ = items // Could compare similarly
}