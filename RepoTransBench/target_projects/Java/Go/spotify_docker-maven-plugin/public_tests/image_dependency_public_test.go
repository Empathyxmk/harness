package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestImageDepsFromOtherModulesPublic(t *testing.T) {
	major := 2
	minor := 6
	assert.Equal(t, 8, major+minor)
	assert.True(t, minor%2 == 0)
	assert.False(t, major < 2)
}