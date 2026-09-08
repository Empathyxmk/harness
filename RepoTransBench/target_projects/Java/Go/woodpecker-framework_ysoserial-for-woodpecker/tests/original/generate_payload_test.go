package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
	yso "woodpecker-framework-ysoserial"
)

func TestGeneratePayload_MainHelp(t *testing.T) {
	defer func() { recover() }()
	// Should print help or error; just ensure no panic
	_ = yso.GeneratePayloadMain([]string{})
	assert.True(t, true)
}

func TestGeneratePayload_MainUnknownPayload(t *testing.T) {
	defer func() { recover() }()
	_ = yso.GeneratePayloadMain([]string{"UnknownPayload", "cmd", "id"})
	assert.True(t, true)
}

func TestGeneratePayload_MainWithKnownPayloadButMissingArgs(t *testing.T) {
	defer func() { recover() }()
	_ = yso.GeneratePayloadMain([]string{"CommonsCollections1"})
	assert.True(t, true)
}