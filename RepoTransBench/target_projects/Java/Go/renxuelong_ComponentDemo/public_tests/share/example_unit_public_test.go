package share

import (
	"strings"
	"testing"
)

func TestDivideIsCorrect(t *testing.T) {
	if 8/2 != 4 {
		t.Errorf("Expected 4, got %d", 8/2)
	}
}

func TestStringStartsWithIsCorrect(t *testing.T) {
	if !strings.HasPrefix("ShareTesting", "Share") {
		t.Error(`Expected "ShareTesting" to start with "Share"`)
	}
}