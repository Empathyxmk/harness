package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
	. "pallets_itsdangerous/src/itsdangerous"
)

func TestURLSafeSerializerRoundtrip(t *testing.T) {
	s := NewURLSafeSerializer("urlsecret")
	data := map[string]interface{}{"k": "v"}
	token, err := s.Dumps(data)
	assert.NoError(t, err)
	assert.IsType(t, "", token)
	decoded, err := s.Loads(token)
	assert.NoError(t, err)
	assert.Equal(t, data, decoded)
}

func TestURLSafeSerializerSeparators(t *testing.T) {
	s := NewURLSafeSerializerWithSalt("secret", "mysalt")
	token, err := s.Dumps(map[string]interface{}{"x": 100})
	assert.NoError(t, err)
	assert.IsType(t, "", token)
	decoded, err := s.Loads(token)
	assert.NoError(t, err)
	assert.Equal(t, map[string]interface{}{"x": 100}, decoded)
}

func TestURLSafeSerializerBadSignature(t *testing.T) {
	s := NewURLSafeSerializer("othersecret")
	_, err := s.Loads("badbadbad")
	assert.ErrorIs(t, err, ErrBadSignature)
}

func TestURLSafeSerializerReturnPayload(t *testing.T) {
	s := NewURLSafeSerializer("secret")
	token, err := s.Dumps(map[string]interface{}{"val": 4})
	assert.NoError(t, err)
	decoded, err := s.LoadsWithPayload(token, true)
	assert.NoError(t, err)
	assert.Equal(t, map[string]interface{}{"val": 4}, decoded)
}