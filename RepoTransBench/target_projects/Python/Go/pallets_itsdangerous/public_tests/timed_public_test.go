package public_tests

import (
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	. "pallets_itsdangerous/src/itsdangerous"
)

func TestTimedSerializerRoundtripPublic(t *testing.T) {
	s := NewTimedSerializer("pubtimedkey")
	data := map[string]interface{}{"index": 333}
	token, err := s.Dumps(data)
	assert.NoError(t, err)
	assert.IsType(t, "", token)
	decoded, err := s.Loads(token)
	assert.NoError(t, err)
	assert.Equal(t, data, decoded)
}

func TestTimedSerializerWithMaxAgePublic(t *testing.T) {
	s := NewTimedSerializer("pubtimedkey")
	data := map[string]interface{}{"val": 17}
	token, err := s.Dumps(data)
	assert.NoError(t, err)
	decoded, err := s.LoadsWithMaxAge(token, 3)
	assert.NoError(t, err)
	assert.Equal(t, data, decoded)
}

func TestTimedSerializerBadSignaturePublic(t *testing.T) {
	s := NewTimedSerializer("pubk2")
	_, err := s.Loads("definitely_invalid_token")
	assert.ErrorIs(t, err, ErrBadSignature)
}

func TestTimedSignatureExpiredPublic(t *testing.T) {
	s := NewTimedSerializer("expirepub")
	data := map[string]interface{}{"test": true}
	token, err := s.Dumps(data)
	assert.NoError(t, err)
	time.Sleep(1 * time.Second)
	_, err = s.LoadsWithMaxAge(token, 0)
	assert.ErrorIs(t, err, ErrSignatureExpired)
}