package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"regexp"
	"project/company"
)

func TestRandomString_LengthOne(t *testing.T) {
	s := company.RandomString(1)
	assert.NotNil(t, s)
	assert.Equal(t, 1, len(s))
	matched, _ := regexp.MatchString("^[A-Za-z0-9]$", s)
	assert.True(t, matched, "Should match single alphanumeric")
}

func TestRandomString_LargeLength(t *testing.T) {
	s := company.RandomString(1000)
	assert.NotNil(t, s)
	assert.Equal(t, 1000, len(s))
	matched, _ := regexp.MatchString("^[A-Za-z0-9]{1000}$", s)
	assert.True(t, matched, "Should match 1000 alphanumeric chars")
}