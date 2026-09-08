package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"project/company"
)

func TestReverseIfNotBlank_NonBlank_Public(t *testing.T) {
	assert.Equal(t, "edcba", company.ReverseIfNotBlank("abcde"))
	assert.Equal(t, "Z", company.ReverseIfNotBlank("Z"))
}

func TestReverseIfNotBlank_Blank_Public(t *testing.T) {
	assert.Equal(t, "\t", company.ReverseIfNotBlank("\t"))
	assert.Equal(t, "    ", company.ReverseIfNotBlank("    "))
}

func TestIsAllDigits_Numeric_Public(t *testing.T) {
	assert.True(t, company.IsAllDigits("987654"))
}

func TestIsAllDigits_NonNumeric_Public(t *testing.T) {
	assert.False(t, company.IsAllDigits("def"))
	assert.False(t, company.IsAllDigits("789ghi"))
	assert.False(t, company.IsAllDigits(""))
	assert.False(t, company.IsAllDigits("    "))
}

func TestMain_WithArgs_Public(t *testing.T) {
	// Different args for coverage
	company.SetOutput(nil) // Default to stdout
	company.MainEntry([]string{"456"})
	company.MainEntry([]string{"def"})
	company.MainEntry([]string{" "})
}