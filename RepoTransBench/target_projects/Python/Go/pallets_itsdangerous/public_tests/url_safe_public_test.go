package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
	. "pallets_itsdangerous/src/itsdangerous"
)

func TestURLSafeSerializerRoundtripPublic(t *testing.T) {
	s := NewURLSafeSerializer("urlsecretpublic")
	data := map[string]interface{}{"foo": "bar"}
	token, err := s.Dumps(data)
	assert.NoError(t, err)
	assert.IsType(t, "", token)
	decoded, err := s.Loads(token)
	assert.NoError(t, err)
	assert.Equal(t, data, decoded)
}

func TestURLSafeSerializerSeparatorsPublic(t *testing.T) {
	s := NewURLSafeSerializerWithSalt("publicsecret", "othersalt")
	token, err := s.Dumps(map[string]interface{}{"y": 303})
	assert.NoError(t, err)
	assert.IsType(t, "", token)
	decoded, err := s.Loads(token)
	assert.NoError(t, err)
	assert.Equal(t, map[string]interface{}{"y": 303}, decoded)
}

func TestURLSafeSerializerBadSignaturePublic(t *testing.T) {
	s := NewURLSafeSerializer("newsecret")
	_, err := s.Loads("notavalidtoken")
	assert.ErrorIs(t, err, ErrBadSignature)
}

func TestURLSafeSerializerReturnPayloadPublic(t *testing.T) {
	s := NewURLSafeSerializer("differentsecret")
	token, err := s.Dumps(map[string]interface{}{"val": 7})
	assert.NoError(t, err)
	decoded, err := s.LoadsWithPayload(token, true)
	assert.NoError(t, err)
	assert.Equal(t, map[string]interface{}{"val": 7}, decoded)
}