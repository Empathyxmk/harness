package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
	yso "woodpecker-framework-ysoserial"
)

func TestYsoConfig_DefaultIsCompressIsFalse(t *testing.T) {
	conf := yso.NewYsoConfig()
	assert.False(t, conf.IsCompress())
}

func TestYsoConfig_SetCompressTrue(t *testing.T) {
	conf := yso.NewYsoConfig()
	conf.SetCompress(true)
	assert.True(t, conf.IsCompress())
}

func TestYsoConfig_SetCompressFalse(t *testing.T) {
	conf := yso.NewYsoConfig()
	conf.SetCompress(true)
	conf.SetCompress(false)
	assert.False(t, conf.IsCompress())
}