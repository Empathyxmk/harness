package original

import (
	"testing"
	. "piskvorky_sqlitedict"
)

func TestCreateSqliteDict(t *testing.T) {
	d, err := NewSqliteDict("", nil)
	if err != nil {
		t.Fatalf("NewSqliteDict failed: %v", err)
	}
	defer d.Close()
	if _, ok := any(d).(interface{ Get(string) (interface{}, error) }); !ok {
		t.Fatalf("not a SqliteDict type")
	}
	if items, err := d.Items(); err != nil || len(items) != 0 {
		t.Errorf("expected no items, got %v, err %v", items, err)
	}
	if keys, err := d.Keys(); err != nil || len(keys) != 0 {
		t.Errorf("expected no keys, got %v, err %v", keys, err)
	}
	if n := d.Len(); n != 0 {
		t.Errorf("expected len 0, got %d", n)
	}
}

func TestAssignValues(t *testing.T) {
	d, _ := NewSqliteDict("", nil)
	defer d.Close()
	if err := d.Set("abc", "edf"); err != nil {
		t.Fatalf("Set: %v", err)
	}
	val, _ := d.Get("abc")
	if val != "edf" {
		t.Errorf("abc = %v want edf", val)
	}
	if d.Len() != 1 {
		t.Errorf("len want 1, got %d", d.Len())
	}
}

func TestClearData(t *testing.T) {
	d, _ := NewSqliteDict("", nil)
	defer d.Close()
	d.Update(map[string]interface{}{"a": 1, "b": 2, "c": 3})
	if d.Len() != 3 {
		t.Errorf("want 3, got %d", d.Len())
	}
	d.Clear()
	if d.Len() != 0 {
		t.Errorf("want 0 after clear, got %d", d.Len())
	}
}

func TestManageOneRecord(t *testing.T) {
	d, _ := NewSqliteDict("", nil)
	defer d.Close()
	val := ""
	for i := 0; i < 100; i++ {
		val += "rsvp"
	}
	d.Set("abc", val)
	out, _ := d.Get("abc")
	if out != val {
		t.Errorf("long abc: %v", out)
	}
	d.Set("abc", "lmno")
	out, _ = d.Get("abc")
	if out != "lmno" {
		t.Errorf("abc updated: %v", out)
	}
	if d.Len() != 1 {
		t.Errorf("should still be 1 record, got %d", d.Len())
	}
	err := d.Delete("abc")
	if err != nil {
		t.Errorf("Delete abc: %v", err)
	}
	if d.Len() != 0 {
		t.Errorf("should be empty, got %d", d.Len())
	}
}

func TestManageFewRecords(t *testing.T) {
	d, _ := NewSqliteDict("", nil)
	defer d.Close()
	d.Set("abc", "lmno")
	d.Set("xyz", "pdq")
	if d.Len() != 2 {
		t.Errorf("len want 2, got %d", d.Len())
	}
	items, _ := d.Items()
	mp := map[string]interface{}{}
	for _, kv := range items {
		if arr, ok := kv.([2]interface{}); ok {
			mp[arr[0].(string)] = arr[1]
		}
	}
	if v, ok := mp["abc"]; !ok || v != "lmno" {
		t.Errorf("items abc wrong: %v", v)
	}
	if v, ok := mp["xyz"]; !ok || v != "pdq" {
		t.Errorf("items xyz wrong: %v", v)
	}
	if keys, _ := d.Keys(); len(keys) != 2 || (keys[0] != "abc" && keys[1] != "xyz") {
		t.Errorf("keys mismatch: %v", keys)
	}
}

func TestUpdateRecords(t *testing.T) {
	d, _ := NewSqliteDict("", nil)
	defer d.Close()
	d.Update(map[string]interface{}{"v": "w", "p": "x", "q": "y", "r": "z"})
	if d.Len() != 4 {
		t.Errorf("want 4, got %d", d.Len())
	}
	items, _ := d.Items()
	want := map[string]string{"v": "w", "p": "x", "q": "y", "r": "z"}
	mp := map[string]string{}
	for _, kv := range items {
		if arr, ok := kv.([2]interface{}); ok {
			mp[arr[0].(string)] = arr[1].(string)
		}
	}
	for k, v := range want {
		if mp[k] != v {
			t.Errorf("for k=%q, want %q got %q", k, v, mp[k])
		}
	}
}

func TestHandlingErrors(t *testing.T) {
	d, _ := NewSqliteDict("", nil)
	defer d.Close()
	if err := d.Delete("abc"); err == nil {
		t.Errorf("expected key error for delete of nonexistent")
	}
	_, err := d.Get("abc")
	if err == nil {
		t.Errorf("expected key error for get of nonexistent")
	}
}