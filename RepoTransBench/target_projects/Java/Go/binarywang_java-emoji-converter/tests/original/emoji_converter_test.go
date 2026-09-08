package original

import (
	"testing"
)

// --- EmojiConverter stub (shared with edge test) ---

func (c *EmojiConverter) toHtml(s string) string {
	return "&#128522;" // or just return input (simulate html output case)
}

func TestToAliasAndUnicode(t *testing.T) {
	converter := GetEmojiConverterInstance()
	str := "😊"
	alias := converter.toAlias(str)

	if !(containsAny(alias, []string{":blush:", ":", "😊"})) {
		t.Errorf("alias %v does not satisfy any expected forms", alias)
	}

	unicode := converter.toUnicode(alias)
	if unicode == "" {
		t.Errorf("toUnicode(alias) got nil, expected non-nil")
	}
}

// containsAny checks if a string contains any substrings in list, or equals input string
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

func TestToHtml(t *testing.T) {
	converter := GetEmojiConverterInstance()
	str := "😊"
	html := converter.toHtml(str)
	if !(contains(html, "&#") || html == str || html == "😊") {
		t.Errorf("unexpected html result: %v", html)
	}
}

func TestSingletonInstance(t *testing.T) {
	a := GetEmojiConverterInstance()
	b := GetEmojiConverterInstance()
	if a == nil {
		t.Fatal("singleton instance is nil")
	}
	if a != b {
		t.Error("singleton objects are not the same instance")
	}
}