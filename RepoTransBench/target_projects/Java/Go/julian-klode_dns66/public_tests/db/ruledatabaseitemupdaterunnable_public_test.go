package db

import "testing"

func TestRuleDatabaseItemSetEnabledPublic(t *testing.T) {
	type RuleDatabaseItem struct {
		enabled bool
		url     string
		title   string
		typ     int
	}
	const TYPE_ALLOWLIST = 2
	item := RuleDatabaseItem{
		enabled: true,
		url:     "public_test_url",
		title:   "PublicTitle",
		typ:     TYPE_ALLOWLIST,
	}
	if !item.enabled {
		t.Error("item should be enabled after set enabled")
	}
	if item.url != "public_test_url" {
		t.Errorf("expected url public_test_url, got %q", item.url)
	}
	if item.title != "PublicTitle" {
		t.Errorf("expected title PublicTitle, got %q", item.title)
	}
	if item.typ != TYPE_ALLOWLIST {
		t.Errorf("expected type TYPE_ALLOWLIST (%d), got %d", TYPE_ALLOWLIST, item.typ)
	}
}