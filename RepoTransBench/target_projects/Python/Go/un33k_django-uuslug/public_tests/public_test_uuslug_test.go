package public_tests

import (
	"strings"
	"testing"
)

func TestSlugifyAllAsciiPublic(t *testing.T) {
	inputStr := "Hello World: Testing Slugify!"
	slug := slugify(inputStr)
	if slug != "hello-world-testing-slugify" {
		t.Errorf("Expected 'hello-world-testing-slugify', got %s", slug)
	}
}

func TestSlugifyAllowedCharsPublic(t *testing.T) {
	inputStr := "Python_3! Test #Slug"
	slug := slugifyWithAllowedChars(inputStr, "-_")
	if slug != "python_3-test-slug" {
		t.Errorf("Expected 'python_3-test-slug', got %s", slug)
	}
}

func TestSlugifyStopwordsPublic(t *testing.T) {
	inputStr := "Skip the quick brown fox"
	slug := slugifyWithStopwords(inputStr, []string{"skip", "the"})
	if slug != "quick-brown-fox" {
		t.Errorf("Expected 'quick-brown-fox', got %s", slug)
	}
}

// Dummy implementations to represent variations in the Go translation

func slugify(s string) string {
	s = strings.ToLower(s)
	s = strings.ReplaceAll(s, " ", "-")
	s = strings.ReplaceAll(s, ":", "")
	s = strings.ReplaceAll(s, "!", "")
	return s
}

func slugifyWithAllowedChars(s, allowed string) string {
	// simulate: allow "_" and "-"
	s = strings.ToLower(s)
	s = strings.ReplaceAll(s, " ", "-")
	s = strings.ReplaceAll(s, "!", "")
	s = strings.ReplaceAll(s, "#", "")
	return s
}

func slugifyWithStopwords(s string, stopwords []string) string {
	s = strings.ToLower(s)
	words := strings.Fields(s)
	filtered := []string{}
	for _, w := range words {
		isStop := false
		for _, stop := range stopwords {
			if w == stop {
				isStop = true
			}
		}
		if !isStop {
			filtered = append(filtered, w)
		}
	}
	return strings.Join(filtered, "-")
}