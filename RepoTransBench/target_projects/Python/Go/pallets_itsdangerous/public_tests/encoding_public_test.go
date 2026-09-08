package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
	. "pallets_itsdangerous/src/itsdangerous/encoding"
)

func TestWantBytesTypeCoercionPublic(t *testing.T) {
	assert.Equal(t, []byte("xyz"), WantBytes([]byte("xyz")))
	assert.Equal(t, []byte("hello"), WantBytes("hello"))
	assert.Equal(t, []byte("test"), WantBytes([]byte("test")))
}

func TestBase64RoundtripPublic(t *testing.T) {
	raw := []byte("bazqux")
	encoded := Base64Encode(raw)
	decoded, err := Base64Decode(encoded, "raise")
	assert.NoError(t, err)
	assert.Equal(t, raw, decoded)
}

func TestBase64DecodeErrorPublic(t *testing.T) {
	_, err := Base64Decode([]byte("??="), "raise")
	assert.Error(t, err)
}