package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
	. "pallets_itsdangerous/src/itsdangerous"
)

func TestSerializerRoundtripPublic(t *testing.T) {
	s := NewSerializer("a_different_key")
	d := map[string]interface{}{"gamma": 13, "zeta": []interface{}{5, 4}}
	token, err := s.Dumps(d)
	assert.NoError(t, err)
	assert.IsType(t, "", token)
	decoded, err := s.Loads(token)
	assert.NoError(t, err)
	assert.Equal(t, d, decoded)
}

func TestSerializerRoundtripWithCustomSerializerPublic(t *testing.T) {
	// Custom serializer example is not portable; see TODO in implementation.
}

func TestSerializerInvalidPayloadPublic(t *testing.T) {
	s := NewSerializer("testkey")
	_, err := s.Loads("$%anotherinvalidpayload$%")
	assert.ErrorIs(t, err, ErrBadSignature)
}

func TestSerializerBadSignaturePublic(t *testing.T) {
	s := NewSerializer("keyxxx")
	_, err := s.Loads("totallyinvalidsignature-publictest")
	assert.ErrorIs(t, err, ErrBadSignature)
}