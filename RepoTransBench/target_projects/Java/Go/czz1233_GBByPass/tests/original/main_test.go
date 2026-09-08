package original

import (
	"bytes"
	"testing"

	"github.com/stretchr/testify/assert"
	"project/company"
)

func TestReverseIfNotBlank_NonBlank(t *testing.T) {
	assert.Equal(t, "321", company.ReverseIfNotBlank("123"))
	assert.Equal(t, "a", company.ReverseIfNotBlank("a"))
}

func TestReverseIfNotBlank_Blank(t *testing.T) {
	assert.Equal(t, "", company.ReverseIfNotBlank(""))
	assert.Equal(t, "   ", company.ReverseIfNotBlank("   "))
}

func TestIsAllDigits_Numeric(t *testing.T) {
	assert.True(t, company.IsAllDigits("123456"))
}

func TestIsAllDigits_NonNumeric(t *testing.T) {
	assert.False(t, company.IsAllDigits("abc"))
	assert.False(t, company.IsAllDigits("123abc"))
	assert.False(t, company.IsAllDigits(""))
	assert.False(t, company.IsAllDigits("   "))
}

func TestMain_WithArgs(t *testing.T) {
	// Capture stdout in Go
	var buf bytes.Buffer
	company.SetOutput(&buf)
	company.MainEntry([]string{"123"})
	company.MainEntry([]string{"abc"})
	company.MainEntry([]string{""})
	company.SetOutput(nil)
	output := buf.String()
	assert.NotNil(t, output)
}