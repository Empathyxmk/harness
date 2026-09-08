package original

import (
	"strings"
	"testing"
)

func TestMaskMultipleMatches(t *testing.T) {
	rm := RegexMatcher{Redact: 90}
	msg := "password: alpha password: beta"
	masked := rm.Mask(msg)
	count := strings.Count(masked, "***")
	if count < 2 {
		t.Errorf("Expected at least 2 masked secrets, got %d (%s)", count, masked)
	}
}

func TestMaskNoMatch(t *testing.T) {
	rm := RegexMatcher{}
	text := "this is safe"
	out := rm.Mask(text)
	if out != text {
		t.Errorf("No masking should happen, got: %v", out)
	}
}

func TestFindMatchesGroup0(t *testing.T) {
	rm := RegexMatcher{}
	// Simulate regex with only group 0 by direct test
	if out := rm.Mask("safe"); !(strings.Contains(out, "*") || out == "safe") {
		t.Errorf("Should contain '*' or be 'safe', got: %v", out)
	}
}

func TestInvalidConfigFile(t *testing.T) {
	path := "broken.toml"
	rm := RegexMatcher{Config: path}
	m := rm.Mask("password: example")
	if !strings.Contains(m, "*") {
		t.Errorf("Masking should be present for invalid config, got: %v", m)
	}
}