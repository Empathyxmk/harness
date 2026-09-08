package original

import (
	"testing"
	"time"
	"github.com/stretchr/testify/assert"
	. "pallets_itsdangerous/src/itsdangerous"
)

func TestTimedSerializerDumpsLoads(t *testing.T) {
	s := NewTimedSerializer("secret-key")
	data := map[string]interface{}{"msg": "timed"}
	dumped, err := s.Dumps(data)
	assert.NoError(t, err)
	loaded, err := s.Loads(dumped)
	assert.NoError(t, err)
	assert.Equal(t, data, loaded)
}

func TestTimedSerializerExpiry(t *testing.T) {
	s := NewTimedSerializer("secret-expiry")
	data := map[string]interface{}{"foo": 1}
	token, err := s.Dumps(data)
	assert.NoError(t, err)
	decoded, err := s.Loads(token)
	assert.NoError(t, err)
	assert.Equal(t, data, decoded)
	_, err = s.LoadsWithMaxAge(token, -1)
	assert.ErrorIs(t, err, ErrSignatureExpired)
}

func TestTimedSerializerTupleLoadingOptions(t *testing.T) {
	s := NewTimedSerializer("secret-key2")
	token, err := s.Dumps(map[string]interface{}{"a": 2})
	assert.NoError(t, err)
	val, timestamp, err := s.LoadsWithTimestamp(token, true)
	assert.NoError(t, err)
	assert.Equal(t, map[string]interface{}{"a": 2}, val)
	assert.IsType(t, float64(0), timestamp)
}

func TestTimedSerializerBadSignature(t *testing.T) {
	s := NewTimedSerializer("secret")
	_, err := s.Loads("bad-token")
	assert.ErrorIs(t, err, ErrBadSignature)

	orig, _ := s.Dumps(map[string]interface{}{"foo": 42})
	tampered := reverseString(orig)
	_, err = s.Loads(tampered)
	assert.ErrorIs(t, err, ErrBadTimeSignature)
}

func reverseString(s string) string {
	runes := []rune(s)
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return string(runes)
}