package original

import (
	"testing"
	"regexp"

	"github.com/stretchr/testify/assert"
	"project/company"
)

func TestRandomString_Length(t *testing.T) {
	assert.Equal(t, 8, len(company.RandomString(8)))
	assert.Equal(t, 1, len(company.RandomString(1)))
	assert.Equal(t, 32, len(company.RandomString(32)))
}

func TestRandomString_Characters(t *testing.T) {
	str := company.RandomString(100)
	matched, _ := regexp.MatchString("^[A-Za-z0-9]{100}$", str)
	assert.True(t, matched, "Random string should be exactly 100 alphanumeric")
}

func TestRandomString_ZeroAndNegativeLength(t *testing.T) {
	assert.Equal(t, "", company.RandomString(0))
	assert.Equal(t, "", company.RandomString(-5))
}