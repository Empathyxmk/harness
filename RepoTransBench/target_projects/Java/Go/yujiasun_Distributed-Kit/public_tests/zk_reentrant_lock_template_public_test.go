package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestBasicLockingPublic(t *testing.T) {
	x := 42
	y := 58
	assert.Equal(t, x+y, 100)
	assert.NotEqual(t, x, y)
}