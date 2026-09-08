package public_tests

import (
	"reflect"
	"testing"

	"scrapinghub_adblockparser/adblockparser"
)

var commentRules = []string{
	"! This is a comment line",
	"! Title: Example Filter List",
	"! Expires: 4 days",
	"! Homepage: https://example.com/",
	"[Adblock]",
	"!#include another_list.txt",
}

var htmlRules = []string{
	"##.bannerAd",
	"@@##.sponsoredContent",
	"mysite.com#@##sidebar",
	"@@##.cookieBar",
	"example.net,example.org#@##promo",
	"##a[href^='https://tracker.example.com/']",
	"##img[src$=\".ads.png\"]",
}

func TestPublicIsComment(t *testing.T) {
	for _, text := range commentRules {
		rule := adblockparser.NewAdblockRule(text)
		if !rule.IsComment {
			t.Errorf("Expected IsComment true for %q", text)
		}
		if rule.IsHtmlRule {
			t.Errorf("Expected IsHtmlRule false for %q", text)
		}
		if rule.IsException {
			t.Errorf("Expected IsException false for %q", text)
		}
		if !reflect.DeepEqual(rule.Options, map[string]interface{}{}) {
			t.Errorf("Expected Options={} for %q, got: %#v", text, rule.Options)
		}
		if rule.Regex != nil {
			t.Errorf("Expected Regex nil for %q", text)
		}
	}
}

func TestPublicIsHtmlRule(t *testing.T) {
	for _, text := range htmlRules {
		rule := adblockparser.NewAdblockRule(text)
		if !rule.IsHtmlRule {
			t.Errorf("Expected IsHtmlRule true for %q", text)
		}
		if rule.IsComment {
			t.Errorf("Expected IsComment false for %q", text)
		}
	}
}