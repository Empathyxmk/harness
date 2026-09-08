package original

import (
	"fmt"
	"testing"
	"softvar_json2html/json2html"
)

func TestConvertSimpleDict(t *testing.T) {
	data := map[string]interface{}{"foo": "bar"}
	html := json2html.Convert(data)
	if !contains(html, "foo") || !contains(html, "bar") {
		t.Errorf("Did not find keys/values in html: %s", html)
	}
	if len(html) < 6 || html[:6] != "<table" {
		t.Errorf("Expected output to start with <table, got: %s", html)
	}
}

func TestConvertListOfDicts(t *testing.T) {
	data := []map[string]interface{}{{"foo": "bar"}, {"foo": "baz"}}
	html := json2html.Convert(data)
	if len(html) < 6 || html[:6] != "<table" {
		t.Errorf("Expected output to start with <table, got: %s", html)
	}
	if count := countSubstring(html, "<tr>"); count < 2 {
		t.Errorf("Expected at least two <tr> tags in html, got count = %d HTML: %s", count, html)
	}
}

func TestConvertEmptyInput(t *testing.T) {
	tests := []struct {
		in interface{}
	}{
		{""}, {map[string]interface{}{}}, {[]interface{}{}},
	}
	for _, tc := range tests {
		html := json2html.Convert(tc.in)
		if html != "" {
			t.Errorf("Expected empty output for input %#v, got: %q", tc.in, html)
		}
	}
}

func TestConvertCustomTableAttr(t *testing.T) {
	data := map[string]interface{}{"x": 1}
	html := json2html.ConvertWithOptions(data, json2html.ConvertOptions{TableAttributes: `class="tbl" id="tid"`})
	if !contains(html, `class="tbl"`) || !contains(html, `id="tid"`) {
		t.Errorf("Expected custom table attributes in HTML, got: %s", html)
	}
}

func TestConvertRaisesOnInvalidType(t *testing.T) {
	type Dummy struct{}
	var d Dummy
	out := json2html.Convert(d)
	_, ok := out.(string)
	if !ok {
		t.Errorf("Expected a string output for Dummy object")
	}
}

func TestConvertHandlesTuple(t *testing.T) {
	// Go doesn't have direct python tuple, so simulate with 2-element array
	data := []interface{}{map[string]interface{}{"a": 1}, map[string]interface{}{"b": 2}}
	html := json2html.Convert(data)
	if !contains(html, "a") || !contains(html, "b") {
		t.Errorf("Expected html to contain both 'a' and 'b'")
	}
}

func TestConvertPreservesHtmlEscape(t *testing.T) {
	data := map[string]interface{}{"key": `<script>alert("x")</script>`}
	html := json2html.Convert(data)
	if !(contains(html, "&lt;script&gt;") || contains(html, "&lt;script&gt;alert")) {
		t.Errorf("Expected output to contain &lt;script&gt; or escape for script tags, got: %q", html)
	}
}

func TestJson2HtmlRepr(t *testing.T) {
	js := json2html.NewJson2Html()
	if !contains(fmt.Sprintf("%+v", js), "Json2Html") {
		t.Errorf("Expected 'Json2Html' in representation got=%q", js)
	}
}

func countSubstring(s, match string) int {
	count := 0
	i := 0
	for {
		p := findNext(s, match, i)
		if p < 0 {
			break
		}
		count++
		i = p + len(match)
	}
	return count
}

func findNext(s, sub string, start int) int {
	for i := start; i <= len(s)-len(sub); i++ {
		for j := 0; j < len(sub); j++ {
			if s[i+j] != sub[j] {
				break
			}
			if j == len(sub)-1 {
				return i
			}
		}
	}
	return -1
}