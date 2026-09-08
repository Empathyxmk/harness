package original

import (
	"strings"
	"testing"
)

// Simulated stripMention removes the first @mention (case-insensitive "homu") and leading/trailing spaces, returns rest
func stripMention(s string) string {
	trimmed := strings.TrimSpace(s)
	lower := strings.ToLower(trimmed)
	if strings.HasPrefix(lower, "@homu") {
		return strings.TrimSpace(trimmed[len("@homu"):])
	}
	tokens := strings.Fields(trimmed)
	if len(tokens) > 0 && strings.HasPrefix(strings.ToLower(tokens[0]), "@homu") {
		return strings.TrimSpace(strings.Join(tokens[1:], " "))
	}
	if strings.HasPrefix(trimmed, "@") {
		// Remove first word
		toks := strings.Fields(trimmed)
		if len(toks) > 1 {
			return strings.Join(toks[1:], " ")
		}
		return ""
	}
	return trimmed
}

func TestStripMention(t *testing.T) {
	msg := "@homu r+"
	expected := "r+"
	if got := stripMention(msg); got != expected {
		t.Errorf("stripMention(%q) = %q, want %q", msg, got, expected)
	}
	msg = " @Homu  approve please! "
	expected = "approve please!"
	if got := stripMention(msg); got != expected {
		t.Errorf("stripMention(%q) = %q, want %q", msg, got, expected)
	}
}