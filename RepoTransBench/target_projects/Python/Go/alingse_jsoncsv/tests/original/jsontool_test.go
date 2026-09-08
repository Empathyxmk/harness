package original

import (
	"bytes"
	"encoding/json"
	"io"
	"reflect"
	"testing"

	"alingse_jsoncsv/jsoncsv"
)

func TestExpandAndRestore_String(t *testing.T) {
	s := "sss"
	exp := jsoncsv.Expand(s)
	_s := jsoncsv.Restore(exp)
	if s != _s {
		t.Errorf("expected %v, got %v", s, _s)
	}
}

func TestExpandAndRestore_List(t *testing.T) {
	s := []interface{}{"sss", "ttt", 1, 2, []interface{}{"3"}}
	exp := jsoncsv.Expand(s)
	_s := jsoncsv.Restore(exp)
	if !reflect.DeepEqual(s, _s) {
		t.Errorf("expected %v, got %v", s, _s)
	}
}

func TestExpandAndRestore_Dict(t *testing.T) {
	s := map[string]interface{}{
		"s": 1,
		"w": 5,
		"t": map[string]interface{}{
			"m": 0,
			"x": map[string]interface{}{
				"y": "z",
			},
		},
	}
	exp := jsoncsv.Expand(s)
	_s := jsoncsv.Restore(exp)
	if !reflect.DeepEqual(s, _s) {
		t.Errorf("expected %v, got %v", s, _s)
	}
}

func TestExpandAndRestore_Complex(t *testing.T) {
	s := []interface{}{
		map[string]interface{}{"s": 0},
		map[string]interface{}{"t": []interface{}{"2", map[string]interface{}{"x": "z"}}},
		0,
		"w",
		[]interface{}{"x", "g", 1},
	}
	exp := jsoncsv.Expand(s)
	_s := jsoncsv.Restore(exp)
	for i := range s {
		if !reflect.DeepEqual(s[i], _s.([]interface{})[i]) {
			t.Fatalf("Mismatch at index %d: %+v != %+v", i, s[i], _s.([]interface{})[i])
		}
	}
}

func TestIsArrayIndex(t *testing.T) {
	tt := []struct {
		in   interface{}
		want bool
	}{
		{[]interface{}{0, 1, 2, 3}, true},
		{[]interface{}{"0", "1", "2", "3"}, true},
		{[]interface{}{"0", "1", "10", "2", "3", "4", "5", "6", "7", "8", "9"}, true},
		{[]interface{}{1, 2, 3}, false},
		{[]interface{}{"0", 1, 2}, false},
	}
	for i, tc := range tt {
		got := jsoncsv.IsArrayIndex(tc.in)
		if got != tc.want {
			t.Errorf("test %d: expected %v, got %v", i, tc.want, got)
		}
	}
}

func TestUnicode(t *testing.T) {
	data := []interface{}{
		map[string]interface{}{"河流名字": "长江", "河流长度": "6000千米"},
		map[string]interface{}{"河流名字": "黄河", "河流长度": "5000千米"},
	}
	expObj := jsoncsv.Expand(data)
	if expObj == nil {
		t.Errorf("Expect expanded object to not be nil")
	}
}

func TestExpandWithSafe(t *testing.T) {
	data := map[string]interface{}{
		"www.a.com": map[string]interface{}{"qps": 100, "p95": 20},
		"api.a.com": map[string]interface{}{"qps": 100, "p95": 20, "p99": 100},
	}
	expObj := jsoncsv.ExpandSafe(data)
	if expObj["api.a.com\\.p95"] != 20 || expObj["api.a.com\\.p99"] != 100 {
		t.Errorf("safe key not found or incorrect value")
	}
	origin := jsoncsv.RestoreSafe(expObj)
	if !reflect.DeepEqual(origin, data) {
		t.Errorf("expected %v, got %v", data, origin)
	}
}

func TestExpandAndRestore_More(t *testing.T) {
	data := []interface{}{"a", "ab", "b", "a", "ab", "b", "a", "ab", "b", "a", "ab", "b"}
	expObj := jsoncsv.Expand(data)
	if expObj["0"] != "a" || expObj["1"] != "ab" {
		t.Errorf("unexpected expanded")
	}
	origin := jsoncsv.Restore(expObj)
	if !reflect.DeepEqual(data, origin) {
		t.Errorf("expected %v, got %v", data, origin)
	}
}

// Sub-tests for convert_json functionality
func TestConvertExpand(t *testing.T) {
	input := `{"a":{"b":3}}
{"a":{"c":4}}
`
	expected := `{"a.b":3}
{"a.c":4}
`
	out := new(bytes.Buffer)
	if err := jsoncsv.ConvertJSON(bytes.NewBufferString(input), out, jsoncsv.Expand, false); err != nil {
		t.Fatal(err)
	}
	got := out.String()
	if got != expected {
		t.Errorf("expected %q, got %q", expected, got)
	}
}

func TestConvertWithUnicode(t *testing.T) {
	input := `{"河流":{"长度":3}}
{"河流":{"名字":"长江"}}
`
	expected := `{"河流.长度":3}
{"河流.名字":"长江"}
`
	out := new(bytes.Buffer)
	if err := jsoncsv.ConvertJSON(bytes.NewBufferString(input), out, jsoncsv.Expand, false); err != nil {
		t.Fatal(err)
	}
	got := out.String()
	if got != expected {
		t.Errorf("expected %q, got %q", expected, got)
	}
}

func TestConvertRestore(t *testing.T) {
	input := `{"a.b":3}
{"a.c":4}
`
	expected := `{"a":{"b":3}}
{"a":{"c":4}}
`
	out := new(bytes.Buffer)
	if err := jsoncsv.ConvertJSON(bytes.NewBufferString(input), out, jsoncsv.Restore, false); err != nil {
		t.Fatal(err)
	}
	got := out.String()
	if got != expected {
		t.Errorf("expected %q, got %q", expected, got)
	}
}

func TestConvertExpandJSONArray(t *testing.T) {
	input := `[{"a":{"b":3}},{"a":{"c":4}}]`
	expected := `{"a.b":3}
{"a.c":4}
`
	out := new(bytes.Buffer)
	if err := jsoncsv.ConvertJSON(bytes.NewBufferString(input), out, jsoncsv.Expand, true); err != nil {
		t.Fatal(err)
	}
	got := out.String()
	if got != expected {
		t.Errorf("expected %q, got %q", expected, got)
	}
}