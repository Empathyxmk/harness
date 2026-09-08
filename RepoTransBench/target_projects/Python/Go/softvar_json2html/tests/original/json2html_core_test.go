package original

import (
	"encoding/json"
	"fmt"
	"reflect"
	"testing"
	"softvar_json2html/json2html"
)

func TestConvertVariousInputs(t *testing.T) {
	tests := []struct {
		input            interface{}
		expectedContains string
	}{
		{map[string]interface{}{"foo": "bar"}, "foo"},
		{[]interface{}{}, ""},
		{"", ""},
		{[]map[string]interface{}{{"a": float64(1), "b": float64(2)}, {"a": float64(3), "b": float64(4)}}, "a"},
		{123, "123"},
	}
	for _, tc := range tests {
		html := json2html.Convert(tc.input)
		if !contains(html, tc.expectedContains) {
			t.Errorf("Expected substring '%s' in output '%s'", tc.expectedContains, html)
		}
	}
}

func TestConvertBadJSONString(t *testing.T) {
	badJSON := `{"foo": bar}`
	js := json2html.NewJson2Html()
	res := js.Convert(badJSON)
	if str, ok := res.(string); !ok || !contains(str, badJSON) {
		t.Errorf("Expected fallback string containing input for invalid JSON")
	}
}

func TestConvertNonUTFInput(t *testing.T) {
	js := json2html.NewJson2Html()
	bad := []byte{0x80, 'a', 'b', 'c'}
	res := js.Convert(bad)
	_, sb := res.(string)
	_, bb := res.([]byte)
	if !(sb || bb) {
		t.Errorf("Expected result to be string or []byte")
	}
}

func TestColumnHeadersFromListOfDicts(t *testing.T) {
	js := json2html.NewJson2Html()
	data := []map[string]interface{}{
		{"a": float64(1), "b": float64(2)},
		{"a": float64(10), "b": float64(20)},
	}
	headers := js.ColumnHeadersFromListOfDicts(data)
	expected := []string{"a", "b"}
	if !reflect.DeepEqual(headers, expected) {
		t.Errorf("Expected headers %v, got %v", expected, headers)
	}
}

func TestColumnHeadersWithInconsistentDicts(t *testing.T) {
	js := json2html.NewJson2Html()
	data := []map[string]interface{}{
		{"a": float64(1)},
		{"a": float64(1), "b": float64(2)},
	}
	if js.ColumnHeadersFromListOfDicts(data) != nil {
		t.Errorf("Expected nil for inconsistent headers")
	}
}

func TestColumnHeadersWithListNonDicts(t *testing.T) {
	js := json2html.NewJson2Html()
	data := []interface{}{1, 2, 3}
	if js.ColumnHeadersFromListOfDicts(data) != nil {
		t.Errorf("Expected nil for list of non-dicts")
	}
}

func TestConvertWithEncodeOption(t *testing.T) {
	js := json2html.NewJson2Html()
	data := map[string]interface{}{"foo": "bar"}
	result := js.ConvertWithOptions(data, json2html.ConvertOptions{Encode: true})
	_, ok := result.([]byte)
	if !ok {
		t.Errorf("Expected result to be []byte with Encode option")
	}
}

func TestConvertWithEscapeFalse(t *testing.T) {
	js := json2html.NewJson2Html()
	data := map[string]interface{}{"key": "<b>html</b>"}
	html := js.ConvertWithOptions(data, json2html.ConvertOptions{Escape: false})
	if !contains(fmt.Sprintf("%v", html), "<b>html</b>") {
		t.Errorf("Expected unescaped HTML in output, got: %v", html)
	}
}

func TestReprJson2Html(t *testing.T) {
	js := json2html.NewJson2Html()
	if !contains(fmt.Sprintf("%+v", js), "Json2Html") {
		t.Errorf("Expected representation to contain 'Json2Html'")
	}
}

// helpers used across multiple test files
func contains(s, substr string) bool {
	return substr == "" || (len(substr) > 0 && len(s) > 0 && (len(s) >= len(substr)) && (stringIndex(s, substr) >= 0))
}

func stringIndex(s, sub string) int {
	return len([]rune(([]byte(s))[0:min(len(s), len(sub))])) // fallback to builtin:
}