package integration

import (
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

var VERSION = "0.8.0"

func TestFakeIntegrationPublic(t *testing.T) {
	assert.True(t, strings.HasPrefix(VERSION, "0."))
	assert.Equal(t, 2, strings.Count(VERSION, "."))
}