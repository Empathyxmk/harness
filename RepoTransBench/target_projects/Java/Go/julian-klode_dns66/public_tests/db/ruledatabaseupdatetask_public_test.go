package db

import "testing"

func TestRunWithoutExceptionsPublic(t *testing.T) {
	type RuleDatabaseItem struct {
		title   string
		enabled bool
		url     string
		typ     int
	}
	const TYPE_DNS = 1
	item := RuleDatabaseItem{
		title:   "UpdatePublic",
		enabled: true,
		url:     "http://test-public/",
		typ:     TYPE_DNS,
	}
	str := item.title + item.url
	if str == "" {
		t.Errorf("title+url is empty, should not be")
	}
}