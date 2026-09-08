package original

import (
	"strings"
	"testing"
)

// Dummy parser emulating expected logic for structure tests.

func parseCoqStatement(input string) string {
	trimmed := strings.TrimSpace(input)
	// Extremely simple, for test parity: return up to first '.'
	if i := strings.Index(trimmed, "."); i >= 0 {
		return trimmed[:i+1]
	}
	return trimmed
}

func TestParseCoqStatementBasic(t *testing.T) {
	tests := []struct {
		line     string
		expected string
	}{
		{"Lemma foo: True.", "Lemma foo: True."},
		{"admit.", "admit."},
		{"Check nat.", "Check nat."},
		{"Print foo.", "Print foo."},
		{"Goal True.", "Goal True."},
		{"Require Import Bar.", "Require Import Bar."},
	}
	for _, tt := range tests {
		got := parseCoqStatement(tt.line)
		if got != tt.expected {
			t.Errorf("parseCoqStatement(%q) = %q, want %q", tt.line, got, tt.expected)
		}
	}
}

func TestParseCoqStatementMultiline(t *testing.T) {
	inp := "Lemma foo:\nTrue.\nProof.\nadmit.\nQed."
	lines := strings.Split(inp, "\n")
	out := ""
	for _, l := range lines {
		out += parseCoqStatement(l)
	}
	if !strings.Contains(out, "Lemma foo:") {
		t.Errorf("Did not find Lemma in multiline parse: %q", out)
	}
}

func TestParseCoqStatementEdgeCases(t *testing.T) {
	tests := []struct {
		line     string
		expected string
	}{
		{"", ""},
		{"   \n", ""},
		{"No dot here", "No dot here"},
	}
	for _, tt := range tests {
		got := parseCoqStatement(tt.line)
		if got != tt.expected {
			t.Errorf("Edge parse: %q → %q (want %q)", tt.line, got, tt.expected)
		}
	}
}