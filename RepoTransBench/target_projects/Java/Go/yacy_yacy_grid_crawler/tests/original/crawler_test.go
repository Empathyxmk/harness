package tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestCRAWLER_SERVICESContainsExpectedClasses(t *testing.T) {
	// Simulate by looking for names in CRAWLER_SERVICES
	hasDefaultValues := false
	hasCrawlStart := false
	for _, n := range CRAWLER_SERVICES {
		if n == "CrawlerDefaultValuesService" {
			hasDefaultValues = true
		}
		if n == "CrawlStartService" {
			hasCrawlStart = true
		}
	}
	assert.True(t, hasDefaultValues, "CRAWLER_SERVICES should contain CrawlerDefaultValuesService")
	assert.True(t, hasCrawlStart, "CRAWLER_SERVICES should contain CrawlStartService")
}