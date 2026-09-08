package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	yso "woodpecker-framework-ysoserial"
)

func TestStringsPublic_IsEmpty(t *testing.T) {
	assert.True(t, yso.StringsIsEmpty(nil))
	assert.True(t, yso.StringsIsEmpty(""))
	assert.False(t, yso.StringsIsEmpty(" "))
	assert.False(t, yso.StringsIsEmpty("测试"))
}

func TestStringsPublic_IsNotEmpty(t *testing.T) {
	assert.False(t, yso.StringsIsNotEmpty(nil))
	assert.False(t, yso.StringsIsNotEmpty(""))
	assert.True(t, yso.StringsIsNotEmpty("something"))
	assert.True(t, yso.StringsIsNotEmpty("1"))
}

func TestStringsPublic_Repeat(t *testing.T) {
	assert.Equal(t, "", yso.StringsRepeat("y", 0))
	assert.Equal(t, "yyyy", yso.StringsRepeat("y", 4))
	assert.Equal(t, "helloworldhelloworldhelloworld", yso.StringsRepeat("helloworld", 3))
}