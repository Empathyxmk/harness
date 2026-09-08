package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
	"yacy_grid_crawler/tests"
)

func TestCrawlStartServicePublic_ParseTimeout_Public(t *testing.T) {
	params := map[string][]string{
		"timeout": {"90"},
	}
	result := tests.ParseTimeout(params, 250)
	assert.Equal(t, 90, result)
}

func TestCrawlStartServicePublic_ParseTimeout_Defaults_Public(t *testing.T) {
	params := map[string][]string{}
	result := tests.ParseTimeout(params, 60)
	assert.Equal(t, 60, result)
}

func TestCrawlStartServicePublic_ParseTimeout_Invalid_Public(t *testing.T) {
	params := map[string][]string{
		"timeout": {"invalid"},
	}
	result := tests.ParseTimeout(params, 15)
	assert.Equal(t, 15, result)
}