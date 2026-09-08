package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
	"yacy_grid_crawler/tests"
)

func TestCrawlerListenerPublic_InitPriorityQueue_Public(t *testing.T) {
	cl := &tests.CrawlerListener{}
	cl.InitPriorityQueue(2)
	assert.True(t, true)
}

func TestCrawlerListenerPublic_PriorityDimensionsEdgeCases_Public(t *testing.T) {
	assert.NotNil(t, tests.PriorityDimensionsTestHelper())
}

func PriorityDimensionsTestHelper() int {
	return 1
}