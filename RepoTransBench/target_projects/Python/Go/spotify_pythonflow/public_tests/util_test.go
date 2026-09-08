package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func AddInts(a, b int) int {
	return a + b
}

func TestAddIntsPublic(t *testing.T) {
	assert.Equal(t, 4, AddInts(1, 3))
	assert.Equal(t, 0, AddInts(-2, 2))
}