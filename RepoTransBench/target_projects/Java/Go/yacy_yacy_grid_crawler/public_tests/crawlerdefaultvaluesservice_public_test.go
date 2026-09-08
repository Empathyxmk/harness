package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
	"yacy_grid_crawler/tests"
)

func TestCrawlerDefaultValuesServicePublic_GetDefaultTimeout_Public(t *testing.T) {
	defaultTimeout := tests.GetDefaultTimeout()
	assert.True(t, defaultTimeout > 0)
}

func TestCrawlerDefaultValuesServicePublic_DefaultValuesConstants_Public(t *testing.T) {
	depth := tests.DefaultMaxDepth
	links := tests.DefaultMaxLinks
	assert.True(t, depth > 0 && links > 0)
	assert.True(t, depth != 0 && links != 0)
}