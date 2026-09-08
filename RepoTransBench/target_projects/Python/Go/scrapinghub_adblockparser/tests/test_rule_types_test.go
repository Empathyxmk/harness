package tests

import (
	"reflect"
	"testing"

	"scrapinghub_adblockparser/adblockparser"
)

var commentRules = []string{
	"[Adblock Plus 2.0]",
	"! Checksum: nVIXktYXKU6M+cu+Txkhuw",
	"!/cb.php?sub$script,third-party",
	"!@@/cb.php?sub",
	"!###ADSLOT_SKYSCRAPER",
	"! *** easylist:easylist/easylist_whitelist_general_hide.txt ***",
}

var htmlRules = []string{
	"###ADSLOT_SKYSCRAPER",
	"@@###ADSLOT_SKYSCRAPER",
	"##.adsBox",
	"eee.se#@##adspace_top",
	"domain1.com,domain2.com#@##adwrapper",
	"edgesuitedomain.net#@##ad-unit",
	"mydomain.com#@#.ad-unit",
	`##a[href^="http://affiliate.sometracker.com/"]`,
}

func TestIsComment(t *testing.T) {
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

func TestIsHtmlRule(t *testing.T) {
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