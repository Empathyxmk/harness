package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestAdditionIsCorrectPublic(t *testing.T) {
	assert.Equal(t, 10, 7+3)
}