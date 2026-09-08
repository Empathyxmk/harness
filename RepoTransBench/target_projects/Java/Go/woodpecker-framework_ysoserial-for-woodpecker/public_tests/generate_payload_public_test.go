package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	yso "woodpecker-framework-ysoserial"
)

func TestGeneratePayloadPublic_YsoConfigCompress(t *testing.T) {
	// Changing compress state with different sequence
	yso.GeneratePayloadYsoConfig.SetCompress(true)
	assert.True(t, yso.GeneratePayloadYsoConfig.IsCompress())
	yso.GeneratePayloadYsoConfig.SetCompress(false)
	assert.False(t, yso.GeneratePayloadYsoConfig.IsCompress())
	yso.GeneratePayloadYsoConfig.SetCompress(true)
	assert.True(t, yso.GeneratePayloadYsoConfig.IsCompress())
}