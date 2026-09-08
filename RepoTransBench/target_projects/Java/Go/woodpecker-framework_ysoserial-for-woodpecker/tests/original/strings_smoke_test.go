package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	yso "woodpecker-framework-ysoserial"
)

func TestStringsSmoke_IsEmpty(t *testing.T) {
	assert.True(t, yso.StringsIsEmpty(nil))
	assert.True(t, yso.StringsIsEmpty(""))
	assert.False(t, yso.StringsIsEmpty("abc"))
}

func TestStringsSmoke_IsNotEmpty(t *testing.T) {
	assert.False(t, yso.StringsIsNotEmpty(nil))
	assert.False(t, yso.StringsIsNotEmpty(""))
	assert.True(t, yso.StringsIsNotEmpty("value"))
}

func TestStringsSmoke_Repeat(t *testing.T) {
	assert.Equal(t, "", yso.StringsRepeat("x", 0))
	assert.Equal(t, "xxx", yso.StringsRepeat("x", 3))
	assert.Equal(t, "foobarfoobar", yso.StringsRepeat("foobar", 2))
}