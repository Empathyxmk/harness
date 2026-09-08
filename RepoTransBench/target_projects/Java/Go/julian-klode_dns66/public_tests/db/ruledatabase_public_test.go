package db

import "testing"

const (
	TYPE_HOSTS     = 0
	TYPE_DNS       = 1
	TYPE_ALLOWLIST = 2
)

type RuleDatabaseItem struct {
	title   string
	enabled bool
	url     string
	typ     int
}

func TestTypeConstantsPublic(t *testing.T) {
	if TYPE_HOSTS != 0 {
		t.Errorf("TYPE_HOSTS should be 0")
	}
	if TYPE_DNS != 1 {
		t.Errorf("TYPE_DNS should be 1")
	}
	if TYPE_ALLOWLIST != 2 {
		t.Errorf("TYPE_ALLOWLIST should be 2")
	}
}

func TestConstructRuleDatabaseItemPublic(t *testing.T) {
	item := RuleDatabaseItem{
		title:   "publicTitle",
		enabled: true,
		url:     "publicUrl",
		typ:     TYPE_DNS,
	}
	if item.title != "publicTitle" {
		t.Errorf("expected publicTitle, got %q", item.title)
	}
	if !item.enabled {
		t.Error("item should be enabled")
	}
	if item.url != "publicUrl" {
		t.Errorf("expected publicUrl, got %q", item.url)
	}
	if item.typ != TYPE_DNS {
		t.Errorf("expected type TYPE_DNS (%d), got %d", TYPE_DNS, item.typ)
	}
}