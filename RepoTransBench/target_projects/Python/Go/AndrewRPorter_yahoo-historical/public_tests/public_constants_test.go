package public_tests

import (
	"strings"
	"testing"
	"yahoo-historical-go/yah"
)

func TestConstantsFieldsPublic(t *testing.T) {
	c := yah.Constants{}
	if !c.Has("API_URL") {
		t.Error("Constants missing API_URL")
	}
	if !c.Has("DATE_INTERVALS") {
		t.Error("Constants missing DATE_INTERVALS")
	}
	if !c.Has("ONE_DAY_INTERVAL") {
		t.Error("Constants missing ONE_DAY_INTERVAL")
	}
	dateInts, ok := c.GetByKey("DATE_INTERVALS").([]string)
	if !ok {
		t.Fatal("DATE_INTERVALS is not []string")
	}
	found := false
	for _, s := range dateInts {
		if s == "1d" {
			found = true
		}
	}
	if !found {
		t.Error("'1d' not in DATE_INTERVALS")
	}
	if v, ok := c.GetByKey("ONE_DAY_INTERVAL").(string); !ok || v != "1d" {
		t.Errorf("ONE_DAY_INTERVAL must be '1d', got: %v", c.GetByKey("ONE_DAY_INTERVAL"))
	}
}

func TestApiUrlFormatPublic(t *testing.T) {
	c := yah.Constants{}
	apiUrlTpl, ok := c.GetByKey("API_URL").(string)
	if !ok {
		t.Fatalf("API_URL is not a string")
	}
	url := strings.Replace(apiUrlTpl, "%s", "TSLA", 1)
	url = strings.Replace(url, "%d", "1610000000", 1)
	url = strings.Replace(url, "%d", "1610020000", 1)
	url = strings.Replace(url, "%s", "1d", 1)
	url = strings.Replace(url, "%s", "history", 1)
	if !strings.Contains(url, "TSLA") || !strings.Contains(url, "16100") || !strings.Contains(url, "1d") {
		t.Error("API_URL formatting failed")
	}
	if pos := strings.Index(url, "history"); pos <= 0 {
		t.Error("'history' not found in URL, or at invalid position")
	}
}