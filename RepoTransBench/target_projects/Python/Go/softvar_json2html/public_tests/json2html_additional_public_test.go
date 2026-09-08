package public_tests

import (
	"testing"
	"softvar_json2html/json2html"
	"fmt"
)

func TestPublicJson2HtmlInstanceConversion(t *testing.T) {
	j2h := json2html.NewJson2Html()
	data := map[string]interface{}{"fruit": "banana", "quantity": 12}
	html := j2h.Convert(data)
	if !contains(html, "banana") || !contains(html, "quantity") {
		t.Errorf("banana/quantity not in html: %q", html)
	}
}

func TestPublicJson2HtmlFunctionConversion(t *testing.T) {
	data := map[string]interface{}{"planet": "Mars", "distance": 225}
	html := json2html.Convert(data)
	if !contains(html, "Mars") || !contains(html, "distance") {
		t.Errorf("Mars/distance not in html: %q", html)
	}
}

func TestPublicConvertDictWithNone(t *testing.T) {
	data := map[string]interface{}{"exists": nil, "name": "test"}
	html := json2html.Convert(data)
	if !(contains(html, "None") || contains(html, "none")) {
		t.Errorf("Expected 'None' or 'none' for nil value")
	}
}

func TestPublicConvertBoolValues(t *testing.T) {
	data := map[string]interface{}{"sunny": true, "rainy": false}
	html := json2html.Convert(data)
	if !contains(html, "True") || !contains(html, "False") {
		t.Errorf("Expected capitalized True/False in html, got: %q", html)
	}
}

func TestPublicConvertListWithDictsAndStrings(t *testing.T) {
	// list: [{"animal": "dog"}, "cat", {"animal": "bird"}]
	data := []interface{}{
		map[string]interface{}{"animal": "dog"},
		"cat",
		map[string]interface{}{"animal": "bird"},
	}
	html := json2html.Convert(data)
	if !contains(html, "dog") || !contains(html, "cat") || !contains(html, "bird") {
		t.Errorf("Expected dog, cat, bird in html output: %q", html)
	}
}

func TestPublicJson2HtmlCustomTableAttributes(t *testing.T) {
	data := map[string]interface{}{"val": 40}
	html := json2html.ConvertWithOptions(data, json2html.ConvertOptions{TableAttributes: `id="public_test_table" class="newtab"`})
	if !contains(html, `id="public_test_table"`) || !contains(html, `class="newtab"`) {
		t.Errorf("Custom table attributes missing: %q", html)
	}
}

func TestPublicJson2HtmlListOfDictsDiff(t *testing.T) {
	data := []map[string]interface{}{
		{"model": "A", "year": float64(1990)},
		{"model": "B", "year": float64(2020)},
	}
	html := json2html.Convert(data)
	for _, s := range []string{"model", "A", "B", "1990", "2020"} {
		if !contains(html, s) {
			t.Errorf("Did not find '%s' in output html: %q", s, html)
		}
	}
}

func TestPublicJson2HtmlEscapeScript(t *testing.T) {
	data := map[string]interface{}{"x": `<script>alert('a')</script>`}
	html := json2html.Convert(data)
	if !contains(html, "&lt;script&gt;") || !contains(html, "alert") {
		t.Errorf("Expected HTML-escaped script and alert content, got: %q", html)
	}
}

func contains(s, sub string) bool {
	return sub == "" || (len(sub) > 0 && len(s) > 0 && (len(s) >= len(sub)) && (stringIndex(s, sub) >= 0))
}

func stringIndex(s, sub string) int {
	for i := 0; i <= len(s)-len(sub); i++ {
		if s[i:i+len(sub)] == sub {
			return i
		}
	}
	return -1
}