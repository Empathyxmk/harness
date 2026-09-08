package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"project/company"
)

func TestReverseIfNotBlank_EmptyStringInput_Public(t *testing.T) {
	assert.Equal(t, "", company.ReverseIfNotBlank(""))
}

func TestIsAllDigits_EmptyStringInput_Public(t *testing.T) {
	assert.False(t, company.IsAllDigits(""))
}