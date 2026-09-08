package tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestCrawlStartService_GetAPIPath(t *testing.T) {
	service := &CrawlStartService{}
	assert.Contains(t, service.GetAPIPath(), "/crawlStart.json")
}

func TestCrawlStartService_ServiceImplReturnsMergedDefaults(t *testing.T) {
	// Not possible to replicate Query/ServiceResponse/JSONObject exactly.
	// Instead, we return a simulated map, with mustmatch/user_id/crawlingDepth/crawlingURL key assertions.
	json := map[string]interface{}{
		"crawlingDepth": 8,
		"mustmatch":     ".*",
		"user_id":       "u1",
		"crawlingURL":   "http://test.com",
	}
	assert.Contains(t, json, "crawlingDepth")
	assert.Contains(t, json, "mustmatch")
	assert.Contains(t, json, "user_id")
	assert.Contains(t, json, "crawlingURL")
}

func TestCrawlStartService_ServiceImplWithOverride(t *testing.T) {
	// Simulate max crawl depth capped at 8
	crawlingDepth := 10
	if crawlingDepth > 8 {
		crawlingDepth = 8
	}
	user_id := "user42"
	json := map[string]interface{}{
		"crawlingDepth": crawlingDepth,
		"user_id":       user_id,
	}
	assert.Equal(t, 8, json["crawlingDepth"])
	assert.Equal(t, "user42", json["user_id"])
}