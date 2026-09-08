package original

import (
	"strings"
	"testing"
)

// Implementing basic versions of the utils for test coverage

func joinURL(parts ...string) string {
	var cleaned []string
	for _, part := range parts {
		clean := strings.Trim(part, "/")
		cleaned = append(cleaned, clean)
	}
	return strings.Join(cleaned, "/")
}

func stripNone(input interface{}) interface{} {
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

func dictKeysToCamelCase(d map[string]interface{}) map[string]interface{} {
	r := make(map[string]interface{})
	for k, v := range d {
		r[toCamelCase(k)] = v
	}
	return r
}

func toSnakeCase(s string) string {
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

func toCamelCase(s string) string {
	// e.g., foo_bar_baz -> fooBarBaz
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

func getValue(m map[string]interface{}, key string, fallback interface{}) interface{} {
	if val, ok := m[key]; ok {
		return val
	}
	return fallback
}

func TestJoinURLBasic(t *testing.T) {
	if got := joinURL("a", "b", "c"); got != "a/b/c" {
		t.Errorf("joinURL a/b/c failed, got %v", got)
	}
	if got := joinURL("a/", "/b/", "c/"); got != "a/b/c" {
		t.Errorf("joinURL a/b/c with slashes failed, got %v", got)
	}
}

func TestStripNoneDict(t *testing.T) {
	in := map[string]interface{}{"a": 1, "b": nil, "c": 0}
	out := stripNone(in).(map[string]interface{})
	if _, ok := out["b"]; ok {
		t.Errorf("Key 'b' should be removed by stripNone")
	}
	if _, ok := out["a"]; !ok {
		t.Errorf("Key 'a' should be present after stripNone")
	}
	if _, ok := out["c"]; !ok {
		t.Errorf("Key 'c' should be present after stripNone")
	}
}

func TestStripNoneList(t *testing.T) {
	l := []interface{}{1, nil, 2}
	out := stripNone(l).([]interface{})
	if len(out) != 2 || out[0] != 1 || out[1] != 2 {
		t.Errorf("stripNone on list: expected [1,2], got %v", out)
	}
}

func TestStripNoneOther(t *testing.T) {
	val := "foo"
	if stripNone(val) != "foo" {
		t.Errorf("stripNone should return value unchanged if not slice/dict")
	}
}

func TestDictKeysToCamelCase(t *testing.T) {
	d := map[string]interface{}{"foo_bar": 1, "BarBaz_qux": 2}
	cd := dictKeysToCamelCase(d)
	if _, ok := cd["fooBar"]; !ok {
		t.Errorf("Expected fooBar in camelcase dict")
	}
	if _, ok := cd["barBazQux"]; !ok {
		t.Errorf("Expected barBazQux in camelcase dict")
	}
}

func TestToSnakeCase(t *testing.T) {
	if got := toSnakeCase("fooBarBAZ"); got != "foo_bar_baz" {
		t.Errorf("Expected foo_bar_baz from fooBarBAZ, got %v", got)
	}
}

func TestToCamelCase(t *testing.T) {
	if got := toCamelCase("foo_bar_baz"); got != "fooBarBaz" {
		t.Errorf("Expected fooBarBaz, got %v", got)
	}
}

func TestGetValue(t *testing.T) {
	d := map[string]interface{}{"a": 1}
	if v := getValue(d, "a", "fallback"); v != 1 {
		t.Errorf("Expected 1, got %v", v)
	}
	if v := getValue(d, "z", "fallback"); v != "fallback" {
		t.Errorf("Expected fallback, got %v", v)
	}
}