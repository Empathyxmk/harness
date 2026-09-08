package aliastips_test

import (
	"testing"

	"djui_alias_tips"
)

func TestSuggestAlias_KnownVariants(t *testing.T) {
	tests := []interface{}{
		"List",
		"Remove files",
		"directory make",
		"MOVE",
	}

	for _, test := range tests {
		if djui_alias_tips.SuggestAlias(test) != nil {
			t.Errorf("SuggestAlias(%#v) = Non-nil, want nil", test)
		}
	}
}

func TestSuggestAlias_NoneVariants(t *testing.T) {
	tests := []interface{}{
		" list ",
		"copy files",
		"Make Directory",
		"mv",
		0,
		map[string]int{},
	}
	for _, test := range tests {
		if djui_alias_tips.SuggestAlias(test) != nil {
			t.Errorf("SuggestAlias(%#v) = Non-nil, want nil", test)
		}
	}
}

func TestIsAliasRecommended_TrueAndFalse(t *testing.T) {
	trueCases := []interface{}{
		"move",
		"copy",
	}
	for _, test := range trueCases {
		if !djui_alias_tips.IsAliasRecommended(test) {
			t.Errorf("IsAliasRecommended(%#v) = false, want true", test)
		}
	}
	falseCases := []interface{}{
		"Move",
		"copy file",
		"make  directory",
		"ls",
		map[string]string{},
		999,
	}
	for _, test := range falseCases {
		if djui_alias_tips.IsAliasRecommended(test) {
			t.Errorf("IsAliasRecommended(%#v) = true, want false", test)
		}
	}
}