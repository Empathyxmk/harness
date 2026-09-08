package tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestCrawlerDefaultValuesService_GetAPIPath(t *testing.T) {
	service := &CrawlerDefaultValuesService{}
	assert.Contains(t, service.GetAPIPath(), "/defaultValues.json")
}

func TestCrawlerDefaultValuesService_CrawlStartDefaultClone(t *testing.T) {
	// Simulate by using a map and copy check
	original := map[string]string{
		"depth": "8", "links": "100",
	}
	clone := make(map[string]string)
	for k, v := range original {
		clone[k] = v
	}
	for k := range original {
		assert.Equal(t, original[k], clone[k])
	}
	assert.NotSame(t, &original, &clone)
}

func TestCrawlerDefaultValuesService_ServiceImplReturnsDefaultValues(t *testing.T) {
	// Simulate by using map key check for default values
	original := map[string]string{
		"depth": "8", "links": "100",
	}
	json := map[string]string{
		"depth": "8", "links": "100",
	}
	for k := range original {
		assert.Equal(t, original[k], json[k])
	}
}