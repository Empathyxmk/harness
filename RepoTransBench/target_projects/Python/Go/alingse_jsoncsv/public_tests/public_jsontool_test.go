package public_tests

import (
	"bytes"
	"reflect"
	"testing"

	"alingse_jsoncsv/jsoncsv"
)

func TestPublicExpandAndRestore_String(t *testing.T) {
	s := "public_string"
	exp := jsoncsv.Expand(s)
	_s := jsoncsv.Restore(exp)
	if s != _s {
		t.Errorf("expected %v, got %v", s, _s)
	}
}

func TestPublicExpandAndRestore_List(t *testing.T) {
	s := []interface{}{"alpha", "beta", 99, 42, []interface{}{"public"}}
	exp := jsoncsv.Expand(s)
	_s := jsoncsv.Restore(exp)
	if !reflect.DeepEqual(s, _s) {
		t.Errorf("expected %v, got %v", s, _s)
	}
}

func TestPublicExpandAndRestore_Dict(t *testing.T) {
	s := map[string]interface{}{
		"foo":  123,
		"bar":  321,
		"nested": map[string]interface{}{
			"sub":    10,
			"level2": map[string]interface{}{"deep": "blue"},
		},
	}
	exp := jsoncsv.Expand(s)
	_s := jsoncsv.Restore(exp)
	if !reflect.DeepEqual(s, _s) {
		t.Errorf("expected %v, got %v", s, _s)
	}
}

func TestPublicExpandAndRestore_Complex(t *testing.T) {
	s := []interface{}{
		map[string]interface{}{"x": 100},
		map[string]interface{}{"y": []interface{}{"v", map[string]interface{}{"a": "b"}}},
		7, "z", []interface{}{"y", "h", 0},
	}
	exp := jsoncsv.Expand(s)
	_s := jsoncsv.Restore(exp)
	for i := range s {
		if !reflect.DeepEqual(s[i], _s.([]interface{})[i]) {
			t.Fatalf("Mismatch at index %d: %+v != %+v", i, s[i], _s.([]interface{})[i])
		}
	}
}

func TestPublicIsArrayIndex(t *testing.T) {
	if !jsoncsv.IsArrayIndex([]interface{}{4, 2, 0, 1, 3}) {
		t.Error("expected true")
	}
	if !jsoncsv.IsArrayIndex([]interface{}{"2", "1", "0"}) {
		t.Error("expected true")
	}
	if !jsoncsv.IsArrayIndex([]interface{}{"0", "1", "2", "11", "5", "4", "6", "7", "8", "9"}) {
		t.Error("expected true")
	}
	if jsoncsv.IsArrayIndex([]interface{}{1, 3, 5}) {
		t.Error("expected false")
	}
	if jsoncsv.IsArrayIndex([]interface{}{"0", 1, "2"}) {
		t.Error("expected false")
	}
}

func TestPublicUnicode(t *testing.T) {
	data := []interface{}{
		map[string]interface{}{"城市": "北京", "面积": "16000平方千米"},
		map[string]interface{}{"城市": "上海", "面积": "6000平方千米"},
	}
	expObj := jsoncsv.Expand(data)
	if expObj == nil {
		t.Errorf("Expect expanded object to not be nil")
	}
}

func TestPublicExpandWithSafe(t *testing.T) {
	data := map[string]interface{}{
		"example.com": map[string]interface{}{"rt": 200, "p99": 23},
		"api.site.com": map[string]interface{}{"rt": 201, "p999": 145, "err": 9},
	}
	expObj := jsoncsv.ExpandSafe(data)
	if expObj["api.site.com\\.p999"] != 145 || expObj["api.site.com\\.err"] != 9 {
		t.Errorf("safe key not found or incorrect value")
	}
	origin := jsoncsv.RestoreSafe(expObj)
	if !reflect.DeepEqual(origin, data) {
		t.Errorf("expected %#v, got %#v", data, origin)
	}
}

func TestPublicExpandAndRestore_More(t *testing.T) {
	data := []interface{}{"red", "orange", "blue", "red", "orange", "blue", "red", "orange", "blue"}
	expObj := jsoncsv.Expand(data)
	if expObj["0"] != "red" || expObj["1"] != "orange" {
		t.Errorf("unexpected expanded")
	}
	origin := jsoncsv.Restore(expObj)
	if !reflect.DeepEqual(data, origin) {
		t.Errorf("expected %v, got %v", data, origin)
	}
}

func TestPublicConvertExpand(t *testing.T) {
	input := `{"x":{"y":88}}
{"x":{"z":99}}
`
	expected := `{"x.y":88}
{"x.z":99}
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

func TestPublicConvertWithUnicode(t *testing.T) {
	input := `{"国家":{"首都":1}}
{"国家":{"人口":"11亿"}}
`
	expected := `{"国家.首都":1}
{"国家.人口":"11亿"}
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

func TestPublicConvertRestore(t *testing.T) {
	input := `{"u.v":88}
{"u.w":99}
`
	expected := `{"u":{"v":88}}
{"u":{"w":99}}
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

func TestPublicConvertExpandJSONArray(t *testing.T) {
	input := `[{"foo":{"bar":5}},{"foo":{"baz":6}}]`
	expected := `{"foo.bar":5}
{"foo.baz":6}
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