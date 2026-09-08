package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
	. "pallets_itsdangerous/src/itsdangerous/encoding"
)

func TestWantBytesTypeCoercion(t *testing.T) {
	assert.Equal(t, []byte("abc"), WantBytes([]byte("abc")))
	assert.Equal(t, []byte("abc"), WantBytes("abc"))
	assert.Equal(t, []byte("zzz"), WantBytes([]byte("zzz")))
}

func TestBase64Roundtrip(t *testing.T) {
	raw := []byte("foobar")
	encoded := Base64Encode(raw)
	decoded, err := Base64Decode(encoded, "raise")
	assert.NoError(t, err)
	assert.Equal(t, raw, decoded)
}

func TestBase64DecodeError(t *testing.T) {
	_, err := Base64Decode([]byte("!!!"), "raise")
	assert.Error(t, err)
}