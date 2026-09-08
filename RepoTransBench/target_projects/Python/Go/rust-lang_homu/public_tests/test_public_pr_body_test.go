package public_tests

import (
	"strings"
	"testing"
)

func prBodyContains(body, key string) bool {
	return strings.Contains(body, key)
}

func TestPrBodyContainsDiffKey(t *testing.T) {
	body := "Closes #99\nExtra: refactor code"
	if !prBodyContains(body, "refactor") {
		t.Errorf("prBodyContains(%q, %q) = false, want true", body, "refactor")
	}
}

func TestPrBodyNotContainsDiffKey(t *testing.T) {
	body := "Implements feature X.\nNone found."
	if prBodyContains(body, "security") {
		t.Errorf("prBodyContains(%q, %q) = true, want false", body, "security")
	}
}