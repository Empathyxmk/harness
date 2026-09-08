package public_tests

import (
	"regexp"
	"testing"

	"github.com/stretchr/testify/assert"
	"project/company"
)

func TestRandomString_NegativeLength_Public(t *testing.T) {
	val := company.RandomString(-7)
	assert.Equal(t, "", val, "Negative length should return empty string")
}

func TestRandomString_AllValidCharactersMany_Public(t *testing.T) {
	val := company.RandomString(32)
	assert.NotNil(t, val)
	assert.Equal(t, 32, len(val))
	matched, _ := regexp.MatchString("^[A-Za-z0-9]{32}$", val)
	assert.True(t, matched, "Should be all alphanumeric, 32 chars")
}