package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestMultiplicationIsCorrect(t *testing.T) {
	assert.Equal(t, 15, 3*5)
}