package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestSomethingSimplePublic(t *testing.T) {
	a := 8
	b := 15
	assert.Equal(t, a+b, 23)

	s := "redisPublic"
	assert.True(t, len(s) >= 3 && s[:3] == "red")
	assert.False(t, len(s) >= 4 && s[len(s)-4:] == "lock")
}