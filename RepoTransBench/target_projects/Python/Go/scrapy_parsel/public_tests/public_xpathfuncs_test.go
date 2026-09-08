package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
	parsel "scrapy_parsel/parsel"
)

func TestTokenizeBasic(t *testing.T) {
	tokens := parsel.Tokenize(" foo-bar baz-qux ")
	assert.Equal(t, []string{"foo-bar", "baz-qux"}, tokens)
}

func TestTokenizeWithCommas(t *testing.T) {
	tokens := parsel.Tokenize("123, test, foo")
	assert.Equal(t, []string{"123,", "test,", "foo"}, tokens)
}

func TestStrToNumber(t *testing.T) {
	n, err := parsel.StrToNumber("4321")
	assert.NoError(t, err)
	assert.Equal(t, 4321, n)
	n2, err2 := parsel.StrToNumber("0x1A")
	assert.NoError(t, err2)
	assert.Equal(t, 26, n2)
}

func TestSplitArgument(t *testing.T) {
	s := parsel.SplitArgument("foo,bar;baz")
	assert.Equal(t, []string{"foo","bar","baz"}, s)
}

func TestHexDigitsError(t *testing.T) {
	_, err := parsel.HexDigits("xyz")
	assert.Error(t, err)
}