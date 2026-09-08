package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

func numTokensFromString(str string) int {
	// Simulates a token counter, for dummy testing
	if str == "" {
		return 0
	}
	return len(str)
}

func TestNumTokensFromStringBasic(t *testing.T) {
	assert.Equal(t, 3, numTokensFromString("abc"))
}

func TestNumTokensFromStringEmpty(t *testing.T) {
	assert.Equal(t, 0, numTokensFromString(""))
}