package original

import (
	"testing"

	"github.com/example/initstring_linkedin2username"
	"reflect"
)

func TestCleanAndSplitNameHtmlcov(t *testing.T) {
	tests := []struct {
		input    string
		expected map[string]string
	}{
		{"John Smith", map[string]string{"first": "john", "second": "smith"}},
		{"Jane D'oe", map[string]string{"first": "jane", "second": "doe"}},
		{"Dr. Ángela Gómez (MBA, PhD)", map[string]string{"first": "angela", "second": "gomez"}},
		{"Mr. François Noël", map[string]string{"first": "francois", "second": "noel"}},
		{"José Niño", map[string]string{"first": "jose", "second": "nino"}},
		{"Joe (CTO) Bloggs", map[string]string{"first": "joe", "second": "bloggs"}},
		{"Alíce O'Conñor (CISO)", map[string]string{"first": "alice", "second": "oconor"}},
		{"Mononym", map[string]string{"first": "mononym", "second": ""}},
	}
	for _, tc := range tests {
		nm := linkedin2username.NewNameMutator(tc.input)
		if !reflect.DeepEqual(nm.Name, tc.expected) {
			t.Errorf("CleanAndSplitName failed for %q: got %+v want %+v", tc.input, nm.Name, tc.expected)
		}
	}
}

func TestCleanAndSplitNameHtmlcovEmpty(t *testing.T) {
	nm := linkedin2username.NewNameMutator("")
	expected := map[string]string{"first": "", "second": ""}
	if !reflect.DeepEqual(nm.Name, expected) {
		t.Errorf("CleanAndSplitName empty: got %+v want %+v", nm.Name, expected)
	}
}

func TestFirstHtmlcov(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"John Smith", "john"},
		{" Jane Smith ", "jane"},
		{"Dr. Ángela Gómez (MBA, PhD)", "angela"},
		{"Mononym", "mononym"},
		{"", ""},
	}
	for _, tc := range tests {
		nm := linkedin2username.NewNameMutator(tc.input)
		got := nm.FirstOne()
		if got != tc.expected {
			t.Errorf("FirstOne(%q) = %q, want %q", tc.input, got, tc.expected)
		}
	}
}

func TestLastHtmlcov(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"John Smith", "smith"},
		{"Jane D'oe", "doe"},
		{"Dr. Ángela Gómez (MBA, PhD)", "gomez"},
		{"Mr. François Noël", "noel"},
		{"José Niño", "nino"},
		{"Joe (CTO) Bloggs", "bloggs"},
		{"Alíce O'Conñor (CISO)", "oconor"},
		{"Mononym", ""},
		{"", ""},
	}
	for _, tc := range tests {
		nm := linkedin2username.NewNameMutator(tc.input)
		got := nm.LastOne()
		if got != tc.expected {
			t.Errorf("LastOne(%q) = %q, want %q", tc.input, got, tc.expected)
		}
	}
}

func TestMutatorsAllVariantsHtmlcov(t *testing.T) {
	nm := linkedin2username.NewNameMutator("John O'Conner (CEO)")
	variants := toSet(nm.Mutators())

	if !variants["johnoconner"] {
		t.Error("Expected variant 'johnoconner'")
	}
	if !variants["joconner"] {
		t.Error("Expected variant 'joconner'")
	}
	// at least one of ["john.o", "johno"] should appear as substring in any variant
	found := false
	for v := range variants {
		if contains(v, "john.o") || contains(v, "johno") {
			found = true
			break
		}
	}
	if !found {
		t.Error("Expected a variant containing 'john.o' or 'johno'")
	}
}

func TestNameWithEmptyStringHtmlcov(t *testing.T) {
	nm := linkedin2username.NewNameMutator("")
	expect := map[string]string{"first": "", "second": ""}
	if !reflect.DeepEqual(nm.Name, expect) {
		t.Errorf("Empty string gives %+v, want %+v", nm.Name, expect)
	}
	mut := nm.Mutators()
	if len(mut) != 0 {
		t.Errorf("Expected no mutators for empty name, got %+v", mut)
	}
}

// -- Helpers used in tests
func toSet(strs []string) map[string]bool {
	m := map[string]bool{}
	for _, s := range strs {
		m[s] = true
	}
	return m
}
// Simple substring helper
func contains(haystack string, needle string) bool {
	return len(needle) > 0 && len(haystack) >= len(needle) && (len(haystack) > 0 && (containsLoop(haystack, needle)))
}
func containsLoop(haystack string, needle string) bool {
	for i := 0; i+len(needle) <= len(haystack); i++ {
		if haystack[i:i+len(needle)] == needle {
			return true
		}
	}
	return false
}