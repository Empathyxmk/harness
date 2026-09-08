package public_tests

import (
	"testing"
	"regexp"

	"github.com/stretchr/testify/assert"
	"project/company"
)

func TestRandomString_TypicalLength_Public(t *testing.T) {
	s := company.RandomString(5)
	assert.NotNil(t, s)
	assert.Equal(t, 5, len(s))
	matched, _ := regexp.MatchString("^[A-Za-z0-9]{5}$", s)
	assert.True(t, matched)
}

func TestRandomString_ZeroLength_Public(t *testing.T) {
	s := company.RandomString(0)
	assert.NotNil(t, s)
	assert.Equal(t, 0, len(s))
	assert.Equal(t, "", s)
}