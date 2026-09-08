package public_tests

import (
	"strings"
	"testing"
)

func stripTrailingSpacesNewlines(s string) string {
	return strings.TrimRight(strings.TrimSpace(s), "\n\t ")
}

func compareFunc(a, b string, ignoreTrailingSpaces bool) bool {
	if ignoreTrailingSpaces {
		a = stripTrailingSpacesNewlines(a)
		b = stripTrailingSpacesNewlines(b)
	}
	return a == b
}

func TestStripTrailingSpacesNewlinesPublic(t *testing.T) {
	s := "hello world    \n  \n\t"
	out := stripTrailingSpacesNewlines(s)
	if out != "hello world" {
		t.Errorf("expected 'hello world', got %q", out)
	}
}

func TestComparePublicEqualNorm(t *testing.T) {
	a := "foo bar   \n"
	b := "foo bar"
	eq := compareFunc(a, b, true)
	if !eq {
		t.Errorf("want true but got false for equal normalize")
	}
}

func TestComparePublicNotEqual(t *testing.T) {
	a := "value1"
	b := "value2"
	eq := compareFunc(a, b, false)
	if eq {
		t.Errorf("Should not be equal")
	}
}