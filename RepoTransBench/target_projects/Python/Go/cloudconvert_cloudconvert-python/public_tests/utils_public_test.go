package public_tests

import (
	"strings"
	"testing"
)

func joinURLPublic(parts ...string) string {
	var cleaned []string
	for _, part := range parts {
		clean := strings.Trim(part, "/")
		cleaned = append(cleaned, clean)
	}
	return strings.Join(cleaned, "/")
}

func stripNonePublic(input interface{}) interface{} {
	switch v := input.(type) {
	case map[string]interface{}:
		m := make(map[string]interface{})
		for k, val := range v {
			if val != nil {
				m[k] = val
			}
		}
		return m
	case []interface{}:
		var l []interface{}
		for _, val := range v {
			if val != nil {
				l = append(l, val)
			}
		}
		return l
	default:
		return input
	}
}

func dictKeysToCamelCasePublic(d map[string]interface{}) map[string]interface{} {
	r := make(map[string]interface{})
	for k, v := range d {
		r[toCamelCasePublic(k)] = v
	}
	return r
}

func toSnakeCasePublic(s string) string {
	var out []rune
	for i, c := range s {
		if c >= 'A' && c <= 'Z' {
			if i != 0 {
				out = append(out, '_')
			}
			out = append(out, c+'a'-'A')
		} else {
			out = append(out, c)
		}
	}
	return strings.ToLower(string(out))
}

func toCamelCasePublic(s string) string {
	words := strings.Split(s, "_")
	if len(words) == 0 {
		return s
	}
	res := words[0]
	for _, w := range words[1:] {
		if len(w) > 0 {
			res += strings.ToUpper(w[:1]) + w[1:]
		}
	}
	return res
}

func getValuePublic(m map[string]interface{}, key string, fallback interface{}) interface{} {
	if val, ok := m[key]; ok {
		return val
	}
	return fallback
}

func TestJoinURLAlternate(t *testing.T) {
	if got := joinURLPublic("x", "y", "z"); got != "x/y/z" {
		t.Errorf("joinURL x/y/z got %v", got)
	}
	if got := joinURLPublic("x/", "/y/", "z/"); got != "x/y/z" {
		t.Errorf("joinURL with slashes: want x/y/z, got %v", got)
	}
}

func TestStripNoneDictPublic(t *testing.T) {
	d := map[string]interface{}{"foo": 0, "bar": nil, "baz": 2}
	out := stripNonePublic(d).(map[string]interface{})
	if _, ok := out["bar"]; ok {
		t.Errorf("Key 'bar' should not be present")
	}
	if _, ok := out["foo"]; !ok || _, ok := out["baz"]; !ok {
		t.Errorf("foo or baz missing from stripNone result")
	}
}

func TestStripNoneListPublic(t *testing.T) {
	l := []interface{}{nil, 3, 4}
	out := stripNonePublic(l).([]interface{})
	if len(out) != 2 || out[0] != 3 || out[1] != 4 {
		t.Errorf("Expected [3,4], got %v", out)
	}
}

func TestStripNoneOtherPublic(t *testing.T) {
	val := 12345
	if stripNonePublic(val) != 12345 {
		t.Errorf("stripNonePublic should return primitive input as-is")
	}
}

func TestDictKeysToCamelCasePublic(t *testing.T) {
	d := map[string]interface{}{"hello_world": 10, "My_Name_is": 20}
	cd := dictKeysToCamelCasePublic(d)
	if _, ok := cd["helloWorld"]; !ok {
		t.Errorf("Expected helloWorld in camelcase dict")
	}
	if _, ok := cd["myNameIs"]; !ok {
		t.Errorf("Expected myNameIs in camelcase dict")
	}
}

func TestToSnakeCasePublic(t *testing.T) {
	if got := toSnakeCasePublic("BarFooBAT"); got != "bar_foo_bat" {
		t.Errorf("Expected bar_foo_bat, got %v", got)
	}
}

func TestToCamelCasePublic(t *testing.T) {
	if got := toCamelCasePublic("bar_foo_bat"); got != "barFooBat" {
		t.Errorf("Expected barFooBat, got %v", got)
	}
}

func TestGetValuePublic(t *testing.T) {
	d := map[string]interface{}{"x": 100}
	if getValuePublic(d, "x", 99) != 100 {
		t.Errorf("Expected 100, got %v", getValuePublic(d, "x", 99))
	}
	if getValuePublic(d, "unknown", 77) != 77 {
		t.Errorf("Expected 77 fallback, got %v", getValuePublic(d, "unknown", 77))
	}
}