package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	yso "woodpecker-framework-ysoserial"
)

func TestStringsSmokePublic_IsEmptySmokeVariants(t *testing.T) {
	assert.True(t, yso.StringsIsEmpty(nil))
	assert.True(t, yso.StringsIsEmpty(""))
	assert.False(t, yso.StringsIsEmpty("null"))
	assert.False(t, yso.StringsIsEmpty("something"))
}

func TestStringsSmokePublic_IsNotEmptySmokeVariants(t *testing.T) {
	assert.False(t, yso.StringsIsNotEmpty(nil))
	assert.False(t, yso.StringsIsNotEmpty(""))
	assert.True(t, yso.StringsIsNotEmpty("123"))
	assert.True(t, yso.StringsIsNotEmpty("xyz"))
}

func TestStringsSmokePublic_RepeatSmokeVariants(t *testing.T) {
	assert.Equal(t, "", yso.StringsRepeat("a", 0))
	assert.Equal(t, "zz", yso.StringsRepeat("z", 2))
	assert.Equal(t, "PQRPQRPQR", yso.StringsRepeat("PQR", 3))
}