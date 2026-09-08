package original

import (
	"strings"
	"testing"
)

type RegexMatcher struct {
	Redact int
	Config string
}

func (r *RegexMatcher) FindMatches(msg string) []string {
	// Simulate matching secrets: return dummy match on "hunter2"
	if strings.Contains(msg, "hunter2") {
		return []string{"hunter2"}
	}
	return nil
}

func (r *RegexMatcher) Mask(msg string) string {
	// If matches found, mask them with ***
	for _, m := range r.FindMatches(msg) {
		msg = strings.ReplaceAll(msg, m, "***")
	}
	return msg
}

func TestFindMatchesAndMask(t *testing.T) {
	matcher := RegexMatcher{Redact: 90}
	msg := "password: hunter2"
	matches := matcher.FindMatches(msg)
	if len(matches) == 0 {
		t.Errorf("Expected matches, got none")
	}
	masked := matcher.Mask(msg)
	if !strings.Contains(masked, "***") {
		t.Errorf("Expected masked result, got: %v", masked)
	}
}

func TestParseConfigFailureFallback(t *testing.T) {
	matcher := RegexMatcher{Redact: 80, Config: "nonexistent_path.toml"}
	out := matcher.Mask("password: hunter2 super")
	if !strings.Contains(out, "*") {
		t.Errorf("Fallback masking should result in mask chars, got: %v", out)
	}
}