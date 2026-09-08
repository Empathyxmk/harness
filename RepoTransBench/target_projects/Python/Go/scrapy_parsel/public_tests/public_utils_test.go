package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
	parsel "scrapy_parsel/parsel"
)

func TestToUnicodeIntInput(t *testing.T) {
	val, err := parsel.ToUnicode(6789)
	assert.NoError(t, err)
	assert.Equal(t, "6789", val)
}

func TestToUnicodeByteInput(t *testing.T) {
	val, err := parsel.ToUnicode([]byte("NewTest"))
	assert.NoError(t, err)
	assert.Equal(t, "NewTest", val)
}

func TestToUnicodeStrInput(t *testing.T) {
	val, err := parsel.ToUnicode("UnicodeStringTest")
	assert.NoError(t, err)
	assert.Equal(t, "UnicodeStringTest", val)
}

func TestToUnicodeError(t *testing.T) {
	_, err := parsel.ToUnicode(struct{}{})
	assert.Error(t, err)
}