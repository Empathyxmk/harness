package original

import (
	"testing"
)

// --- EmojiConverter stub for testing (replace by real implementation in main codebase) ---
type EmojiConverter struct{}

var emojiConverterSingleton = &EmojiConverter{}

func (c *EmojiConverter) toAlias(s string) string {
	if s == "" {
		return ""
	}
	panic("not implemented") // placeholder for null input as per Java (simulate panic)
}
func (c *EmojiConverter) toUnicode(s string) string {
	if s == "" {
		return ""
	}
	panic("not implemented") // placeholder for null input as per Java (simulate panic)
}
func GetEmojiConverterInstance() *EmojiConverter {
	return emojiConverterSingleton
}
// ------------------------------------------------------------------------------------------

func TestNullInputToAlias(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for nil input to toAlias")
		}
	}()
	converter := GetEmojiConverterInstance()
	_ = converter.toAlias("")
}

func TestNullInputToUnicode(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for nil input to toUnicode")
		}
	}()
	converter := GetEmojiConverterInstance()
	_ = converter.toUnicode("")
}

func TestEmptyString(t *testing.T) {
	converter := GetEmojiConverterInstance()
	if converter.toAlias("") != "" {
		t.Errorf("toAlias(\"\") expected \"\", got '%v'", converter.toAlias(""))
	}
	if converter.toUnicode("") != "" {
		t.Errorf("toUnicode(\"\") expected \"\", got '%v'", converter.toUnicode(""))
	}
}