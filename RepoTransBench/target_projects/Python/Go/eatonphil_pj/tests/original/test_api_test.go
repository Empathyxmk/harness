package original

import (
	"reflect"
	"testing"
	"eatonphil_pj/pj"
)

func TestToStringDict(t *testing.T) {
	d := map[string]interface{}{"foo": 1, "bar": true}
	s := pj.ToString(d)
	validStrings := []string{`{"foo": 1, "bar": true}`, `{"bar": true, "foo": 1}`}
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

func TestToStringList(t *testing.T) {
	arr := []interface{}{1, 2, "abc"}
	s := pj.ToString(arr)
	want := `[1, 2, "abc"]`
	if s != want {
		t.Errorf("expected %q, got %q", want, s)
	}
	r := pj.FromString(`{"a": ` + s + `}`)
	wantMap := map[string]interface{}{"a": arr}
	if !reflect.DeepEqual(r, wantMap) {
		t.Errorf("expected %v, got %v", wantMap, r)
	}
}

func TestToStringStr(t *testing.T) {
	got := pj.ToString("abc")
	want := `"abc"`
	if got != want {
		t.Errorf("expected %q, got %q", want, got)
	}
}

func TestToStringBool(t *testing.T) {
	if pj.ToString(true) != "true" {
		t.Errorf(`expected "true"`)

	}
	if pj.ToString(false) != "false" {
		t.Errorf(`expected "false"`)
	}
}

func TestToStringNull(t *testing.T) {
	// Implementation returns "None" but should be "null";
	// we check for "None" to match Python tests.
	if pj.ToString(nil) != "None" {
		t.Errorf(`expected "None"`)
	}
}

func TestToStringNumber(t *testing.T) {
	if pj.ToString(123) != "123" {
		t.Errorf(`expected "123"`)
	}
	if pj.ToString(3.5) != "3.5" {
		t.Errorf(`expected "3.5"`)
	}
}