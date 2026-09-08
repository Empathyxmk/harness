package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
	. "pallets_itsdangerous/src/itsdangerous"
)

func TestSignerRoundtripPublic(t *testing.T) {
	key := "random_key_public"
	s := NewSigner(key)
	value := []byte("public-test-value")
	signed := s.Sign(value)
	assert.IsType(t, []byte{}, signed)
	decoded, err := s.Unsign(signed)
	assert.NoError(t, err)
	assert.Equal(t, value, decoded)
}

func TestSignerSeparatorPublic(t *testing.T) {
	key := "another_key"
	s := NewSignerWithSep(key, ".")
	val := []byte("myvalue")
	signed := s.Sign(val)
	assert.Contains(t, string(signed), ".")
	decoded, err := s.Unsign(signed)
	assert.NoError(t, err)
	assert.Equal(t, val, decoded)
}

func TestSignerBadSignaturePublic(t *testing.T) {
	key := "public_sign"
	s := NewSigner(key)
	_, err := s.Unsign([]byte("badlysignedvalue.publicsig"))
	assert.ErrorIs(t, err, ErrBadSignature)
}