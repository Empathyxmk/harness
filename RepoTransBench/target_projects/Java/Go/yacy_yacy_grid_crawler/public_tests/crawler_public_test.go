package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
	"yacy_grid_crawler/tests"
)

func TestCrawlerPublic_CRAWLER_SERVICESContainsExpectedClasses_Public(t *testing.T) {
	hasDefaultValues := false
	hasCrawlStart := false
	for _, n := range tests.CRAWLER_SERVICES {
		if len(n) >= 10 && n[len(n)-17:] == "DefaultValuesService" {
			hasDefaultValues = true
		}
		if len(n) >= 8 && n[len(n)-15:] == "CrawlStartService" {
			hasCrawlStart = true
		}
	}
	assert.True(t, hasDefaultValues, "CRAWLER_SERVICES should contain DefaultValuesService")
	assert.True(t, hasCrawlStart, "CRAWLER_SERVICES should contain CrawlStartService")
}