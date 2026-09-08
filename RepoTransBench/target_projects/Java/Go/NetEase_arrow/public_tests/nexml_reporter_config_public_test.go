package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// Simulate NeXMLReporterConfig constants as in original
var (
	ATTR_TC_NAME   = "testName"
	ATTR_TC_SUITES = "suiteName"
	ATTR_AUTHOR    = "author"
)

func TestConfigConstantsWithDifferentAccessPattern(t *testing.T) {
	assert.True(t, ATTR_AUTHOR == "author")
	assert.Equal(t, "testName", ATTR_TC_NAME)
	assert.Equal(t, "suiteName", ATTR_TC_SUITES)
}