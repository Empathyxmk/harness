package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"project/company"
)

func TestReverseIfNotBlank_NullInput(t *testing.T) {
	// Java null → Go nil, function should accept nil and return nil, but Go string can't be nil. Let's use a helper to simulate blank/no input.
	result := company.ReverseIfNotBlank("")
	assert.Equal(t, "", result, "ReverseIfNotBlank(\"\") should return \"\"")
}

func TestIsAllDigits_NullInput(t *testing.T) {
	res := company.IsAllDigits("")
	assert.False(t, res, "IsAllDigits(\"\") should return false")
}