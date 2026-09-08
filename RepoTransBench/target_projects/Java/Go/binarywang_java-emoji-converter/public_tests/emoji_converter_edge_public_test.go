package public_tests

import (
	"testing"
)

func TestNullInputToAliasPublic(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for nil input to toAliasPublic")
		}
	}()
	converter := GetEmojiConverterInstance()
	_ = converter.toAlias("")
}

func TestNullInputToUnicodePublic(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for nil input to toUnicodePublic")
		}
	}()
	converter := GetEmojiConverterInstance()
	_ = converter.toUnicode("")
}

func TestWhitespaceString(t *testing.T) {
	converter := GetEmojiConverterInstance()
	got := converter.toAlias(" ")
	if got != " " {
		t.Errorf("toAlias(\" \") expected \" \", got '%v'", got)
	}
	gotU := converter.toUnicode(" ")
	if gotU != " " {
		t.Errorf("toUnicode(\" \") expected \" \", got '%v'", gotU)
	}
}