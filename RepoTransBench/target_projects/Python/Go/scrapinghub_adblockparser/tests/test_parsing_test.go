package tests

import (
	"testing"

	"scrapinghub_adblockparser/adblockparser"
)

func TestEmptyRules(t *testing.T) {
	rules := adblockparser.NewAdblockRules([]string{"adv", "", " \t", "adv2"})
	if len(rules.Rules) != 2 {
		t.Errorf("Expected length 2, got %d", len(rules.Rules))
	}
}

func TestEmptyRegexpRulesFails(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for empty regexp rules")
		}
	}()
	_ = adblockparser.NewAdblockRules([]string{"adv", "/", "//"})
}