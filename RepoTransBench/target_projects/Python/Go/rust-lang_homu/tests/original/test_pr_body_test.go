package original

import (
	"strings"
	"testing"
	"regexp"
)

// Simulate prBodyContains: return true if the key is contained as substring in body
func prBodyContains(body, key string) bool {
	return strings.Contains(body, key)
}

// Simulate suppressPings: For address-like '@xxx', wrap '@xxxx' in backticks except '@bors'
// and except emails
func suppressPings(body string) string {
	// "r? @matklad\n@bors r+\nmail@example.com"
	lines := strings.Split(body, "\n")
	var result []string
	for _, line := range lines {
		words := strings.Fields(line)
		for i, word := range words {
			if strings.HasPrefix(word, "@") {
				if word == "@bors" {
					words[i] = "`@bors`"
				} else if strings.Contains(word, "@") && strings.Contains(word, ".") && strings.Index(word, "@") > 0 {
					// simple email, do not modify
				} else {
					words[i] = "`" + word + "`"
				}
			}
		}
		result = append(result, strings.Join(words, " "))
	}
	return strings.Join(result, "\n")
}

var ignoreBlockPattern = regexp.MustCompile(`(?s)### BEGIN IGNORE[\s\S]*?### END IGNORE\n?`)

func suppressIgnoreBlock(body string) string {
	return ignoreBlockPattern.ReplaceAllString(body, "")
}

const (
	IGNORE_BLOCK_START = "### BEGIN IGNORE\n"
	IGNORE_BLOCK_END   = "### END IGNORE\n"
)

func TestPrBodyContains(t *testing.T) {
	body := "Closes #42\nFixes issues"
	if !prBodyContains(body, "Fixes") {
		t.Errorf("prBodyContains(%q, %q) = false, want true", body, "Fixes")
	}
	if prBodyContains(body, "missing") {
		t.Errorf("prBodyContains(%q, %q) = true, want false", body, "missing")
	}
}

// Additional tests derived from htmlcov/z_9dbce37f4c60ff4e_test_pr_body_py.html

func TestSuppressPingsInPRBody(t *testing.T) {
	body := "r? @matklad\n@bors r+\nmail@example.com"
	expect := "r? `@matklad`\n`@bors` r+\nmail@example.com"
	got := suppressPings(body)
	if got != expect {
		t.Errorf("suppressPings(body) = %q, want %q", got, expect)
	}
}

func TestSuppressIgnoreBlockInPRBody(t *testing.T) {
	body := "Rollup merge\n" +
		"%s\n" +
		"[Create a similar rollup](https://fake.xyz/?prs=1,2,3)\n" +
		"%s"
	body = strings.Replace(body, "%s", IGNORE_BLOCK_START, 1)
	body = strings.Replace(body, "%s", IGNORE_BLOCK_END, 1)
	expect := "Rollup merge\n"
	got := suppressIgnoreBlock(body)
	if got != expect {
		t.Errorf("suppressIgnoreBlock(body) = %q, want %q", got, expect)
	}
}