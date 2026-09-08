package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"project/company"
)

func TestReverseIfNotBlank_WithNumbersAndLetters_Public(t *testing.T) {
	assert.Equal(t, "Ba98", company.ReverseIfNotBlank("89aB"))
}

func TestReverseIfNotBlank_WithSpecialCharacters_Public(t *testing.T) {
	assert.Equal(t, "!@#", company.ReverseIfNotBlank("#@!"))
}

func TestIsAllDigits_WithSpacesAndDigits_Public(t *testing.T) {
	assert.False(t, company.IsAllDigits(" 789 "))
}

func TestIsAllDigits_WithDash_Public(t *testing.T) {
	assert.False(t, company.IsAllDigits("123-456"))
}