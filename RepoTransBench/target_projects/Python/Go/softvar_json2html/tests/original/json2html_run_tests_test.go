package original

import (
	"bytes"
	"errors"
	"os"
	"path/filepath"
	"regexp"
	"reflect"
	"testing"
	"softvar_json2html/json2html"
)

func TestEmptyJson(t *testing.T) {
	expect := ""
	got := json2html.Convert("")
	if got != expect {
		t.Errorf("Expected empty string, got: %#v", got)
	}
	if json2html.Convert([]interface{}{}) != expect {
		t.Errorf("Expected empty string for empty slice")
	}
	if json2html.Convert(map[string]interface{}{}) != expect {
		t.Errorf("Expected empty string for empty map")
	}
}

func TestInvalidJsonException(t *testing.T) {
	jsonStr := "{'name'}"
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected a JSON error for single-quoted invalid string")
		}
	}()
	_ = json2html.Convert(jsonStr)
}

func TestFunkyObjects(t *testing.T) {
	type objectyClass2 struct{}
	func (o objectyClass2) String() string { return "blübidö" }
	type objectyClass4 struct{}
	func (o objectyClass4) String() string { return "blübidöbidü" }

	objectyFunky1, objectyFunky3 := struct{}{}, struct{}{}
	objectyFunky2 := objectyClass2{}
	objectyFunky4 := objectyClass4{}
	funkyNonJsonObj := []interface{}{
		map[string]interface{}{"blib": []interface{}{"blüb", "ـث‎"}, "ـث‎": 1e-3},
		"blub",
		map[int]interface{}{
			1: objectyFunky1,
			2: objectyFunky2,
			3: objectyFunky3,
			4: objectyFunky4,
		},
		[]interface{}{objectyFunky1, objectyFunky2, objectyFunky3, objectyFunky4},
	}
	converted := json2html.Convert(funkyNonJsonObj)
	for _, exp := range []string{"ـث‎", "blüb", "blübidö", "blübidöbidü", "object", "object"} {
		if !contains(converted, exp) {
			t.Errorf("Expected substring %q in output: %q", exp, converted)
		}
	}
}

func TestDictLikeObjects(t *testing.T) {
	type binaryDict struct {
		One, Two interface{}
	}
	// Implement dict-like via map
	single := map[string]interface{}{"one": []interface{}{1, 2}, "two": "blübi"}
	expect := `<table border="1"><tr><th>one</th><td><ul><li>1</li><li>2</li></ul></td></tr><tr><th>two</th><td>blübi</td></tr></table>`
	got := json2html.Convert(single)
	gotNorm := stripWhitespace(got)
	if gotNorm != expect {
		t.Errorf("Expected:\n%s\nGot:\n%s", expect, gotNorm)
	}
	slice := []map[string]interface{}{single}
	expect2 := `<table border="1"><thead><tr><th>one</th><th>two</th></tr></thead><tbody><tr><td><ul><li>1</li><li>2</li></ul></td><td>blübi</td></tr></tbody></table>`
	got2 := json2html.Convert(slice)
	got2Norm := stripWhitespace(got2)
	if got2Norm != expect2 {
		t.Errorf("Expected:\n%s\nGot:\n%s", expect2, got2Norm)
	}
}

func TestBoolAndNone(t *testing.T) {
	expect := "True"
	got := json2html.Convert(true)
	if got != expect {
		t.Errorf("Expected bool True, got: %q", got)
	}
	expectNone := ""
	gotNone := json2html.Convert(nil)
	if gotNone != expectNone {
		t.Errorf("Expected empty string for nil input, got: %q", gotNone)
	}
}

func TestXSS(t *testing.T) {
	expect := "&lt;script&gt;&lt;/script&gt;"
	got := json2html.Convert("<script></script>")
	if got != expect {
		t.Errorf("Expected escaped script, got: %q", got)
	}
	html := json2html.ConvertWithOptions("<script></script>", json2html.ConvertOptions{Escape: false})
	if html != "<script></script>" {
		t.Errorf("Expected unescaped script, got: %q", html)
	}
}

// Utility
func stripWhitespace(s string) string {
	re := regexp.MustCompile(`[\r\n\t]*`)
	return re.ReplaceAllString(s, "")
}