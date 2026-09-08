package public_tests

import (
	"testing"
	"regexp"

	"github.com/stretchr/testify/assert"
	"project/company"
)

func TestRandomString_LengthTwo_Public(t *testing.T) {
	s := company.RandomString(2)
	assert.NotNil(t, s)
	assert.Equal(t, 2, len(s))
	matched, _ := regexp.MatchString("^[A-Za-z0-9]{2}$", s)
	assert.True(t, matched)
}

func TestRandomString_MediumLength_Public(t *testing.T) {
	s := company.RandomString(50)
	assert.NotNil(t, s)
	assert.Equal(t, 50, len(s))
	matched, _ := regexp.MatchString("^[A-Za-z0-9]{50}$", s)
	assert.True(t, matched)
}