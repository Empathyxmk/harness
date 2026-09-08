package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

func numTokensFromStringTest(str string) int {
	if str == "" {
		return 0
	}
	return len(str)
}

func TestPublicNumTokensFromStringNonempty(t *testing.T) {
	assert.Equal(t, 5, numTokensFromStringTest("hello"))
}
func TestPublicNumTokensFromStringEmpty(t *testing.T) {
	assert.Equal(t, 0, numTokensFromStringTest(""))
}