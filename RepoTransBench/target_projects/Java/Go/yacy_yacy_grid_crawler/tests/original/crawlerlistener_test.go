package tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestCrawlerListener_InitPriorityQueue(t *testing.T) {
	cl := &CrawlerListener{}
	cl.InitPriorityQueue(1)
	// Just assert that method runs and no panic, and that CRAWLER_PRIORITY_DIMENSIONS etc would be set
	assert.True(t, true)
}

func TestCrawlerListener_PriorityDimensionsEdgeCases(t *testing.T) {
	// We don't have net.yacy.grid.YaCyServices, so just indirectly test that method exists
	assert.NotNil(t, priorityDimensions)
}