package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	yso "woodpecker-framework-ysoserial"
)

func TestYsoConfigPublic_CompressFlagToggle(t *testing.T) {
	conf := yso.NewYsoConfig()
	assert.False(t, conf.IsCompress())
	conf.SetCompress(true)
	assert.True(t, conf.IsCompress())
	conf.SetCompress(false)
	assert.False(t, conf.IsCompress())
}

func TestYsoConfigPublic_MultipleToggles(t *testing.T) {
	conf := yso.NewYsoConfig()
	conf.SetCompress(true)
	conf.SetCompress(true)
	assert.True(t, conf.IsCompress())
	conf.SetCompress(false)
	assert.False(t, conf.IsCompress())
	conf.SetCompress(true)
	assert.True(t, conf.IsCompress())
}