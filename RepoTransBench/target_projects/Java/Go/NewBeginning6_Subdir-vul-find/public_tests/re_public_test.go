package public_tests

import (
	"testing"
	"newbeginning6subdir/org/example"
)

func TestEscapeAndPatternPublic(t *testing.T) {
	input := "x.y$^"
	escaped := example.ReEscape(input)
	if escaped == "" {
		t.Errorf("ReEscape(%q) returned empty string", input)
	}

	pattern := "\\d+"
	if !example.RePattern(pattern, "2024") {
		t.Errorf("RePattern did not match valid string")
	}
	if example.RePattern(pattern, "test") {
		t.Errorf("RePattern matched invalid string")
	}
	if example.RePattern("abc.*", "xyz") {
		t.Errorf("RePattern matched wrong pattern (abc.* vs xyz)")
	}
}

func TestContainsPublic(t *testing.T) {
	if !example.ReContains("Goodbye moon", "moon") {
		t.Errorf("ReContains did not find substring")
	}
	if example.ReContains("Goodbye", "sun") {
		t.Errorf("ReContains should not find non-existent substring")
	}
	if example.ReContains("", "def") {
		t.Errorf("ReContains should be false for empty haystack")
	}
	if example.ReContains("def", "") {
		t.Errorf("ReContains should be false for empty needle")
	}
	if example.ReContains("", "") {
		t.Errorf("ReContains with both empty should be false")
	}
}