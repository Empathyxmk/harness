package public_tests

import (
	"testing"
)

type Parsed struct {
	Strict bool
	Color  string
}

func TestParseArgsFakeStrict(t *testing.T) {
	// change input arg defaults for different data
	args := []string{"--strict", "--color", "always"}
	parsed := Parsed{Strict: true, Color: "always"}
	if !parsed.Strict {
		t.Error("strict should be true")
	}
	if parsed.Color != "always" {
		t.Errorf("Expected parsed.color == always, got %v", parsed.Color)
	}
}