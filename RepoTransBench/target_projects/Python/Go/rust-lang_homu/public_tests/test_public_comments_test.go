package public_tests

import (
	"strings"
	"testing"
)

// Public stripMention implementation
func stripMention(s string) string {
	trimmed := strings.TrimSpace(s)
	if strings.HasPrefix(trimmed, "@") {
		words := strings.Fields(trimmed)
		if len(words) > 1 {
			return strings.TrimSpace(strings.Join(words[1:], " "))
		}
	}
	return trimmed
}

func TestStripMentionFromMessage(t *testing.T) {
	msg := "@botuser please test"
	expected := "please test"
	if got := stripMention(msg); got != expected {
		t.Errorf("stripMention(%q) = %q, want %q", msg, got, expected)
	}
	msg = "  @dev hello Homu!**  "
	expected = "hello Homu!**"
	if got := stripMention(msg); got != expected {
		t.Errorf("stripMention(%q) = %q, want %q", msg, got, expected)
	}
}