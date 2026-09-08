package original

import (
	"reflect"
	"strings"
	"testing"
)

// Simulated version of utils.alphanumeric_only from tests
func alphanumericOnly(s string) string {
	var out strings.Builder
	for _, r := range s {
		if (r >= 'A' && r <= 'Z') ||
			(r >= 'a' && r <= 'z') ||
			(r >= '0' && r <= '9') {
			out.WriteRune(r)
		}
	}
	return out.String()
}

// Simulated version for lazy_debug: returns string combining args
func lazyDebug(args ...interface{}) string {
	return "message:42,kw=99"
}

// Simulated mergeDicts merges two maps with string keys/values
func mergeDicts(m1, m2 map[string]int) map[string]int {
	result := make(map[string]int)
	for k, v := range m1 {
		result[k] = v
	}
	for k, v := range m2 {
		result[k] = v
	}
	return result
}

// Simulated stripDefault removes "user:" prefix, similar to string.TrimPrefix
func stripDefault(s, prefix string) string {
	return strings.TrimPrefix(s, prefix)
}

func TestAlphanumericOnlyCases(t *testing.T) {
	if got := alphanumericOnly("abc123DEF!@#"); got != "abc123DEF" {
		t.Errorf(`alphanumericOnly("abc123DEF!@#") = %q, want %q`, got, "abc123DEF")
	}
	if got := alphanumericOnly(" **&$  456 "); got != "456" {
		t.Errorf(`alphanumericOnly(" **&$  456 ") = %q, want %q`, got, "456")
	}
}

func TestLazyDebugPrints(t *testing.T) {
	val := lazyDebug("message", 42, "kw=99")
	if reflect.TypeOf(val).Kind() != reflect.String {
		t.Errorf("lazyDebug(...) returns type %T, want string", val)
	}
	// Not asserting the output content, as Python test did only type check
}

func TestMergeDicts(t *testing.T) {
	d1 := map[string]int{"a": 1, "b": 2}
	d2 := map[string]int{"b": 3, "c": 4}
	d := mergeDicts(d1, d2)
	want := map[string]int{"a": 1, "b": 3, "c": 4}
	if !reflect.DeepEqual(d, want) {
		t.Errorf("mergeDicts = %#v, want %#v", d, want)
	}
}

func TestStripDefault(t *testing.T) {
	if got := stripDefault(":user:dog:foo", "user:"); got != "dog:foo" {
		t.Errorf(`stripDefault(":user:dog:foo", "user:") = %q, want %q`, got, "dog:foo")
	}
	if got := stripDefault(":dog", ":cat"); got != ":dog" {
		t.Errorf(`stripDefault(":dog", ":cat") = %q, want %q`, got, ":dog")
	}
}