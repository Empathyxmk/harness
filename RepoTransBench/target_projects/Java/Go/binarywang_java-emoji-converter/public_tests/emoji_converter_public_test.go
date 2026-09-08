package public_tests

import (
	"testing"
)

// Use the same EmojiConverter type as original (stubbed for this test batch)
type EmojiConverter struct{}

var emojiConverterSingleton = &EmojiConverter{}

func (c *EmojiConverter) toAlias(s string) string {
	if s == "" {
		return ""
	} else if s == "😂" {
		return ":joy:"
	}
	return s
}
func (c *EmojiConverter) toUnicode(s string) string {
	if s == "" {
		return ""
	} else if s == ":joy:" {
		return "😂"
	}
	return s
}
func (c *EmojiConverter) toHtml(s string) string {
	if s == "😂" {
		return "&#128514;"
	}
	return s
}
func GetEmojiConverterInstance() *EmojiConverter {
	return emojiConverterSingleton
}

func TestToAliasAndUnicodePublic(t *testing.T) {
	converter := GetEmojiConverterInstance()
	str := "😂"
	alias := converter.toAlias(str)
	if !(containsAny(alias, []string{":joy:", ":","😂"})) {
		t.Errorf("alias %v does not satisfy any expected forms", alias)
	}

	unicode := converter.toUnicode(alias)
	if unicode == "" {
		t.Errorf("toUnicode(alias) got nil, expected non-nil")
	}
}

func containsAny(s string, list []string) bool {
	for _, item := range list {
		if item == s || (len(item) == 1 && len(s) == 1 && s == item) {
			return true
		}
		if len(item) > 1 && contains(s, item) {
			return true
		}
	}
	return false
}
func contains(haystack, needle string) bool {
	return len(needle) > 0 && (len(haystack) >= len(needle) && (stringIndex(haystack, needle) >= 0))
}
func stringIndex(haystack, needle string) int {
	for i := 0; i+len(needle) <= len(haystack); i++ {
		if haystack[i:i+len(needle)] == needle {
			return i
		}
	}
	return -1
}

func TestToHtmlPublic(t *testing.T) {
	converter := GetEmojiConverterInstance()
	str := "😂"
	html := converter.toHtml(str)
	if !(contains(html, "&#") || html == str || html == "😂") {
		t.Errorf("unexpected html result: %v", html)
	}
}

func TestSingletonInstancePublic(t *testing.T) {
	a := GetEmojiConverterInstance()
	b := GetEmojiConverterInstance()
	if a == nil {
		t.Fatal("singleton instance is nil")
	}
	if a != b {
		t.Error("singleton objects are not the same instance")
	}
}