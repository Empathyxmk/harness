package public_tests

import (
	"testing"
	"softvar_json2html/json2html"
)

func TestPublicConvertSimpleDict(t *testing.T) {
	data := map[string]interface{}{"animal": "Elephant", "region": "Africa"}
	html := json2html.Convert(data)
	if !contains(html, "<th>animal</th>") {
		t.Errorf("Missing animal header: %q", html)
	}
	if !contains(html, "<td>Elephant</td>") {
		t.Errorf("Missing Elephant value")
	}
	if !contains(html, "<th>region</th>") {
		t.Errorf("Missing region header")
	}
	if !contains(html, "<td>Africa</td>") {
		t.Errorf("Missing Africa value")
	}
}

func TestPublicConvertListOfNumbers(t *testing.T) {
	data := []int{400, 500, 600}
	html := json2html.Convert(data)
	if len(html) < 4 || html[:4] != "<ul>" {
		t.Errorf("Expected <ul> start in output: %q", html)
	}
	if !contains(html, "<li>400</li>") || !contains(html, "<li>500</li>") || !contains(html, "<li>600</li>") {
		t.Errorf("List values not found in html: %q", html)
	}
}

func TestPublicConvertNestedDictList(t *testing.T) {
	data := map[string]interface{}{
		"cars": []map[string]interface{}{
			{"make": "Toyota", "year": float64(2010)},
			{"make": "Ford", "year": float64(2015)},
		},
	}
	html := json2html.Convert(data)
	if !contains(html, "Toyota") || !contains(html, "Ford") || !contains(html, "year") || !contains(html, "make") {
		t.Errorf("Expected make/year/Ford/Toyota in output: %q", html)
	}
}

func TestPublicConvertJsonString(t *testing.T) {
	jsonStr := `{"genre": "Jazz", "artist": "Miles Davis"}`
	html := json2html.Convert(jsonStr)
	if !contains(html, "<th>genre</th>") ||
		!contains(html, "<td>Jazz</td>") ||
		!contains(html, "Miles Davis") {
		t.Errorf("Expected genre/artist/Jazz/Miles Davis: %q", html)
	}
}

func TestPublicConvertEscapeHtml(t *testing.T) {
	data := map[string]interface{}{"malicious": "<img src='evil'>"}
	html := json2html.Convert(data)
	if !contains(html, "&lt;img") {
		t.Errorf("Expected html escape for img tag")
	}
}

func TestPublicConvertBadJsonString(t *testing.T) {
	badJson := `{"foo": bar`
	html := json2html.Convert(badJson)
	if s, ok := html.(string); !ok {
		t.Fatalf("Expected string result for invalid json")
	} else if !contains(s, `{&quot;foo&quot;: bar`) {
		t.Errorf("Expected HTML-escaped bad json, got: %q", s)
	}
}

func TestPublicConvertEmptyObject(t *testing.T) {
	data := map[string]interface{}{}
	html := json2html.Convert(data)
	if html != "" {
		t.Errorf("Expected empty string for empty dict")
	}
}

func TestPublicConvertEmptyList(t *testing.T) {
	data := []interface{}{}
	html := json2html.Convert(data)
	if html != "" {
		t.Errorf("Expected empty string for empty list")
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