package public_tests

import (
	"testing"
	"bumpversion/functions"
)

func TestReplaceNumericPostfixDifferentNumber(t *testing.T) {
	out := functions.ReplaceNumericPostfix("abc22xyz", 44)
	if out != "abc44xyz" {
		t.Errorf("Expected 'abc44xyz', got '%v'", out)
	}
}

func TestReplaceNumericPostfixNoDigits(t *testing.T) {
	out := functions.ReplaceNumericPostfix("no_digits_here", 9000)
	if out != "no_digits_here" {
		t.Errorf("Expected 'no_digits_here', got '%v'", out)
	}
}

func TestFirstNumericMatchIndexNew(t *testing.T) {
	start, end, ok := functions.FirstNumericMatchIndex("prefix007suffix")
	if !ok || start != 6 || end != 9 {
		t.Errorf("Expected (6,9), got (%v,%v,ok=%v)", start, end, ok)
	}
}

func TestFirstNumericMatchIndexLeadingNumber(t *testing.T) {
	start, end, ok := functions.FirstNumericMatchIndex("99redballoons")
	if !ok || start != 0 || end != 2 {
		t.Errorf("Expected (0,2), got (%v,%v,ok=%v)", start, end, ok)
	}
}

func TestFirstAlphaPostfix(t *testing.T) {
	if got := functions.FirstAlphaPostfix("xy3z"); got != "z" {
		t.Errorf("Expected 'z', got '%v'", got)
	}
}

func TestFindFirstNumberCustom(t *testing.T) {
	cases := []struct {
		input    string
		expected string
	}{
		{"ABC9", "9"},
		{"a1b2c3", "1"},
		{"no_digits", ""},
	}
	for _, c := range cases {
		result := functions.FindFirstNumber(c.input)
		if result != c.expected {
			t.Errorf("FindFirstNumber(%q) = %q; want %q", c.input, result, c.expected)
		}
	}
}

func TestIncrementStringNumberVariant(t *testing.T) {
	got := functions.IncrementStringNumber("hello109world")
	if got != "hello110world" {
		t.Errorf("Expected 'hello110world', got '%v'", got)
	}
}