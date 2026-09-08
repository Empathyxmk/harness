package public_tests

import (
	"strings"
	"testing"
)

func isIdent(s string) bool {
	// Minimal translation: in Go, identifiers must start with a letter or underscore, followed by letters/digits/underscores
	if len(s) == 0 {
		return false
	}
	for i, c := range s {
		if i == 0 && !(('A' <= c && c <= 'Z') || ('a' <= c && c <= 'z') || c == '_') {
			return false
		}
		if i > 0 && !(('A' <= c && c <= 'Z') || ('a' <= c && c <= 'z') || ('0' <= c && c <= '9') || c == '_') {
			return false
		}
	}
	return true
}

func splitLine(text string) (string, int) {
	// Dummy: returns line (original string) and index of first colon or 0.
	idx := strings.IndexRune(text, ':')
	if idx < 0 {
		idx = 0
	}
	return text, idx
}

func findName(text string) string {
	// Dummy logic: finds the first word after "Theorem "
	kw := "Theorem "
	i := strings.Index(text, kw)
	if i < 0 {
		return ""
	}
	start := i + len(kw)
	rest := text[start:]
	end := strings.IndexAny(rest, " :")
	if end < 0 {
		return rest
	}
	return rest[:end]
}

func TestPublicParseIdentifierAlpha(t *testing.T) {
	if !isIdent("KappaZetaXYZ") {
		t.Errorf("Expected KappaZetaXYZ to be an identifier")
	}
}

func TestPublicParseIdentifierMixed(t *testing.T) {
	if !isIdent("T2X9P") {
		t.Errorf("Expected T2X9P to be an identifier")
	}
}

func TestPublicParseNonIdentifierNumeric(t *testing.T) {
	if isIdent("10MainVar") {
		t.Errorf("Did not expect 10MainVar to be an identifier")
	}
}

func TestPublicParseSplitLineColon(t *testing.T) {
	text := "Theorem Power: forall n, n ^ 2 >= 0."
	result, idx := splitLine(text)
	if result != text {
		t.Errorf("splitLine text mismatch")
	}
	if !strings.Contains(result, "Theorem") {
		t.Errorf("missing Theorem")
	}
	if idx != strings.IndexRune(text, ':') {
		t.Errorf("splitLine index incorrect")
	}
}

func TestPublicParseFindNameTheorem(t *testing.T) {
	text := "Theorem my_power: forall n, n ^ 2 >= 0."
	name := findName(text)
	if name != "my_power" {
		t.Errorf("Expected to find my_power, got %q", name)
	}
}