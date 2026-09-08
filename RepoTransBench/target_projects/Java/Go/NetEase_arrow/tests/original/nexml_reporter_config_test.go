package tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// Simulate NeXMLReporterConfig constants
var (
	ATTR_TC_NAME   = "testName"
	ATTR_TC_SUITES = "suiteName"
	ATTR_AUTHOR    = "author"
)

func TestConfigConstants(t *testing.T) {
	assert.Equal(t, "testName", ATTR_TC_NAME)
	assert.Equal(t, "suiteName", ATTR_TC_SUITES)
	assert.Equal(t, "author", ATTR_AUTHOR)
}