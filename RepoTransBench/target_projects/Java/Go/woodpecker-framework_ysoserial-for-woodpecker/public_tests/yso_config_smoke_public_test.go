package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	yso "woodpecker-framework-ysoserial"
)

func TestYsoConfigSmokePublic_DefaultCompressFlag(t *testing.T) {
	conf := yso.NewYsoConfig()
	assert.False(t, conf.IsCompress())
}

func TestYsoConfigSmokePublic_SetCompressToTrue(t *testing.T) {
	conf := yso.NewYsoConfig()
	conf.SetCompress(true)
	assert.True(t, conf.IsCompress())
}

func TestYsoConfigSmokePublic_SetCompressToFalse(t *testing.T) {
	conf := yso.NewYsoConfig()
	conf.SetCompress(true)
	conf.SetCompress(false)
	assert.False(t, conf.IsCompress())
}