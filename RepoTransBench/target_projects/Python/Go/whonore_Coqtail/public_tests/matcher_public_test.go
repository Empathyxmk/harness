package public_tests

import (
	"testing"
)

func matchTokens(patterns []string, words []string) bool {
	// Minimal: match if lengths and contents are equal
	if len(patterns) == 0 {
		return true
	}
	if len(patterns) != len(words) {
		return false
	}
	for i := range patterns {
		if patterns[i] != words[i] {
			return false
		}
	}
	return true
}

func TestPublicMatchTokensDiff(t *testing.T) {
	pat := []string{"cat", "dog"}
	text := "cat bird"
	words := []string{"cat", "bird"}
	if matchTokens(pat, words) {
		t.Error("Expected result to be false")
	}
}

func TestPublicMatchTokensContained(t *testing.T) {
	pat := []string{"tree", "leaf"}
	words := []string{"tree", "root", "leaf"}
	// Simulate "contained" - requires all tokens in words in same order, but not contiguous
	found := false
	for i := 0; i <= len(words)-len(pat); i++ {
		match := true
		for j := 0; j < len(pat); j++ {
			if pat[j] != words[i+j] {
				match = false
				break
			}
		}
		if match {
			found = true
			break
		}
	}
	if !found {
		t.Error("Expected pattern contained")
	}
}

func TestPublicMatchTokensSuccess(t *testing.T) {
	pat := []string{"sun", "light"}
	words := []string{"sun", "light"}
	if !matchTokens(pat, words) {
		t.Error("Expected tokens to match")
	}
}

func TestPublicMatchTokensTooLong(t *testing.T) {
	pat := []string{"alpha", "beta", "gamma"}
	words := []string{"alpha", "beta", "gamma", "delta"}
	if matchTokens(pat, words) {
		t.Error("Expected no match if too long")
	}
}

func TestPublicMatchTokensEmptyPattern(t *testing.T) {
	pat := []string{}
	words := []string{"x", "y", "z"}
	result := matchTokens(pat, words)
	if !result {
		t.Error("Empty pattern must always return true")
	}
}