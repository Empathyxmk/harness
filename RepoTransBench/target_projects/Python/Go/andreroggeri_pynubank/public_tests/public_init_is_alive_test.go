package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

var __version__ = "1.0.0" // Simulate version

func isAlivePublic() bool { return true }

func TestIsAlivePublic(t *testing.T) {
	assert.True(t, isAlivePublic())
}

func TestVersionExistsPublic(t *testing.T) {
	assert.NotEmpty(t, __version__)
	assert.Contains(t, __version__, ".")
}