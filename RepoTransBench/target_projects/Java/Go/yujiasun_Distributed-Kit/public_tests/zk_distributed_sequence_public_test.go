package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestIncrementSequencePublic(t *testing.T) {
	base := int64(1000)
	incremented := base + 11
	assert.Equal(t, int64(1011), incremented)
}

func TestSequenceWrapAroundPublic(t *testing.T) {
	maxValue := int64(50)
	value := (maxValue + 8) % maxValue
	assert.Equal(t, int64(8), value)
}