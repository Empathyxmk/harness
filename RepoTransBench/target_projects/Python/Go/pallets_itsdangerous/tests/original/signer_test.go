package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
	. "pallets_itsdangerous/src/itsdangerous"
)

func TestSignerSignUnsign(t *testing.T) {
	signer := NewSigner("test-secret")
	val := []byte("abc")
	signed := signer.Sign(val)
	unsign, err := signer.Unsign(signed)
	assert.NoError(t, err)
	assert.Equal(t, val, unsign)
}

func TestSignerInvalidSignature(t *testing.T) {
	signer := NewSigner("test-secret")
	bad := []byte("invalid-data")
	_, err := signer.Unsign(append(bad, []byte(".bad")...))
	assert.ErrorIs(t, err, ErrBadSignature)
}

func TestSignerKeyDerivation(t *testing.T) {
	s1 := NewSignerWithSalt("secret", "a")
	s2 := NewSignerWithSalt("secret", "b")
	sig1 := s1.Sign([]byte("data"))
	sig2 := s2.Sign([]byte("data"))
	assert.NotEqual(t, sig1, sig2)
}

func TestSignerSeparates(t *testing.T) {
	s := NewSignerWithSep("test-secret", "--")
	val := []byte("xyz")
	signed := s.Sign(val)
	unsign, err := s.Unsign(signed)
	assert.NoError(t, err)
	assert.Equal(t, val, unsign)
	assert.Equal(t, 1, byteCount(signed, []byte("--")))
}

func byteCount(data []byte, sub []byte) int {
	count := 0
	for i := 0; i+len(sub) <= len(data); i++ {
		if string(data[i:i+len(sub)]) == string(sub) {
			count++
		}
	}
	return count
}

func TestSignerSignatureCheck(t *testing.T) {
	signer := NewSigner("secret")
	value := []byte("foo")
	signed := signer.Sign(value)
	unsign, err := signer.Unsign(signed)
	assert.NoError(t, err)
	assert.Equal(t, value, unsign)

	tampered := make([]byte, len(signed))
	copy(tampered, signed)
	if tampered[len(tampered)-1] != '0' {
		tampered[len(tampered)-1] = '0'
	} else {
		tampered[len(tampered)-1] = '1'
	}
	_, err = signer.Unsign(tampered)
	assert.ErrorIs(t, err, ErrBadSignature)
}