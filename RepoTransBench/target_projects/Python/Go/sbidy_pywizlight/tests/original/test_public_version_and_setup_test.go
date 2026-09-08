package public_tests

import (
	"regexp"
	"testing"
)

func TestPublicVersionFormat(t *testing.T) {
	version := "1.2.3"
	parts := regexp.MustCompile(`\.`).Split(version, -1)
	if len(parts) != 3 {
		t.Errorf("Expected 3 version parts, got %d", len(parts))
	}
	for _, p := range parts {
		if !regexp.MustCompile(`^[0-9]+$`).MatchString(p) {
			t.Errorf("Expected numeric version component, got %q", p)
		}
	}
}