package aliastips_test

import (
	"testing"

	"djui_alias_tips"
)

func TestSuggestAlias_Known(t *testing.T) {
	tests := []struct {
		input    interface{}
		expected string
	}{
		{"list", "ls"},
		{"remove", "rm"},
		{"copy", "cp"},
		{"move", "mv"},
		{"make directory", "mkdir"},
	}

	for _, test := range tests {
		result := djui_alias_tips.SuggestAlias(test.input)
		if result == nil {
			t.Errorf("SuggestAlias(%#v) = nil, want %q", test.input, test.expected)
		} else if *result != test.expected {
			t.Errorf("SuggestAlias(%#v) = %q, want %q", test.input, *result, test.expected)
		}
	}
}

func TestSuggestAlias_None(t *testing.T) {
	tests := []interface{}{
		"unknown",
		"",
		nil,
		123,
		[]string{},
	}

	for _, test := range tests {
		result := djui_alias_tips.SuggestAlias(test)
		if result != nil {
			t.Errorf("SuggestAlias(%#v) = %q, want nil", test, *result)
		}
	}
}

func TestIsAliasRecommended_True(t *testing.T) {
	trueCases := []interface{}{
		"list",
		"remove",
		"copy",
		"move",
		"make directory",
	}
	for _, test := range trueCases {
		if !djui_alias_tips.IsAliasRecommended(test) {
			t.Errorf("IsAliasRecommended(%#v) = false, want true", test)
		}
	}
}

func TestIsAliasRecommended_False(t *testing.T) {
	falseCases := []interface{}{
		"something else",
		"",
		nil,
		123,
		[]string{},
	}
	for _, test := range falseCases {
		if djui_alias_tips.IsAliasRecommended(test) {
			t.Errorf("IsAliasRecommended(%#v) = true, want false", test)
		}
	}
}