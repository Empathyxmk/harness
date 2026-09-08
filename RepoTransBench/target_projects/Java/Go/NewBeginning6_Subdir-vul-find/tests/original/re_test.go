package original

import (
	"testing"
	"newbeginning6subdir/org/example"
)

func TestEscapeAndPattern(t *testing.T) {
	input := "a+b*c"
	escaped := example.ReEscape(input)
	if escaped == "" {
		t.Errorf("ReEscape(%q) returned empty string", input)
	}

	pattern := "[a-z]+"
	if !example.RePattern(pattern, "hello") {
		t.Errorf("RePattern did not match valid string")
	}
	if example.RePattern(pattern, "123") {
		t.Errorf("RePattern matched invalid string")
	}
	if example.RePattern(".*", "") {
		t.Errorf("RePattern matched empty string when should be false")
	}
}

func TestContains(t *testing.T) {
	if !example.ReContains("Hello world", "world") {
		t.Errorf("ReContains failed to find substring")
	}
	if example.ReContains("Hello", "bye") {
		t.Errorf("ReContains found non-existent substring")
	}
	if example.ReContains("", "abc") {
		t.Errorf("ReContains should be false for empty haystack")
	}
	if example.ReContains("abc", "") {
		t.Errorf("ReContains should be false for empty needle")
	}
	if example.ReContains("", "") {
		t.Errorf("ReContains with both empty should be false")
	}
}