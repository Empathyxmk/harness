package original

import (
	"regexp"
	"testing"

	"github.com/stretchr/testify/assert"
	"project/company"
)

func TestRandomStringWithZeroLength(t *testing.T) {
	result := company.RandomString(0)
	assert.NotNil(t, result)
	assert.Equal(t, 0, len(result))
}

func TestRandomStringWithNegativeLength(t *testing.T) {
	result := company.RandomString(-1)
	assert.NotNil(t, result)
	assert.Equal(t, 0, len(result))
}

func TestRandomStringWithHighLength(t *testing.T) {
	result := company.RandomString(100)
	assert.NotNil(t, result)
	assert.Equal(t, 100, len(result))
}

func TestRandomStringIsAlphanumeric(t *testing.T) {
	result := company.RandomString(20)
	matched, _ := regexp.MatchString("^[A-Za-z0-9]+$", result)
	assert.True(t, matched || len(result) == 0, "RandomString(20) should be alphanumeric or empty")
}

// The following methods are commented out in original because in Java RandomUtil doesn't implement them.