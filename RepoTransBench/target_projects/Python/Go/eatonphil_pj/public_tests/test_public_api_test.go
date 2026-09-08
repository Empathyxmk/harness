package public_tests

import (
	"reflect"
	"testing"
	"eatonphil_pj/pj"
)

func TestToStringDictDiff(t *testing.T) {
	d := map[string]interface{}{"x": false, "y": 3.14}
	s := pj.ToString(d)
	validStrings := []string{`{"x": false, "y": 3.14}`, `{"y": 3.14, "x": false}`}
	found := false
	for _, v := range validStrings {
		if s == v {
			found = true
			break
		}
	}
	if !found {
		t.Errorf("to_string(dict) unexpected result: %q", s)
	}
	r := pj.FromString(s)
	if !reflect.DeepEqual(r, d) {
		t.Errorf("expected %v, got %v", d, r)
	}
}

func TestToStringListDiff(t *testing.T) {
	arr := []interface{}{10, 99, "foo"}
	s := pj.ToString(arr)
	want := `[10, 99, "foo"]`
	if s != want {
		t.Errorf("expected %q, got %q", want, s)
	}
	r := pj.FromString(`{"b": ` + s + `}`)
	wantMap := map[string]interface{}{"b": arr}
	if !reflect.DeepEqual(r, wantMap) {
		t.Errorf("expected %v, got %v", wantMap, r)
	}
}

func TestToStringStrDiff(t *testing.T) {
	got := pj.ToString("xyz")
	want := `"xyz"`
	if got != want {
		t.Errorf("expected %q, got %q", want, got)
	}
}

func TestToStringBoolDiff(t *testing.T) {
	if pj.ToString(false) != "false" {
		t.Errorf(`expected "false"`)
	}
	if pj.ToString(true) != "true" {
		t.Errorf(`expected "true"`)
	}
}

func TestToStringNullDiff(t *testing.T) {
	if pj.ToString(nil) != "None" {
		t.Errorf(`expected "None"`)
	}
}

func TestToStringNumberDiff(t *testing.T) {
	if pj.ToString(42) != "42" {
		t.Errorf(`expected "42"`)
	}
	if pj.ToString(2.718) != "2.718" {
		t.Errorf(`expected "2.718"`)
	}
}