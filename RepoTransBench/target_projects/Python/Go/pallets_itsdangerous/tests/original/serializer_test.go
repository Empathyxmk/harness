package original

import (
	"os"
	"testing"
	"github.com/stretchr/testify/assert"
	. "pallets_itsdangerous/src/itsdangerous"
)

func TestSerializerDumpsLoads(t *testing.T) {
	s := NewSerializer("secret-key")
	data := map[string]interface{}{"hello": "world"}
	dumped, err := s.Dumps(data)
	assert.NoError(t, err)
	loaded, err := s.Loads(dumped)
	assert.NoError(t, err)
	assert.Equal(t, data, loaded)
}

func TestSerializerLoadsBadSignature(t *testing.T) {
	s := NewSerializer("secret-key")
	badToken := "bad-token"
	_, err := s.Loads(badToken)
	assert.ErrorIs(t, err, ErrBadSignature)
}

func TestSerializerLoadsPayloadVariants(t *testing.T) {
	s := NewSerializer("secret-key")
	data := map[string]interface{}{"foo": "bar"}
	dumped, err := s.Dumps(data)
	assert.NoError(t, err)
	loaded, err := s.LoadsWithPayload(dumped, false)
	assert.NoError(t, err)
	assert.Equal(t, data, loaded)
	loadedPayload, err := s.LoadsWithPayload(dumped, true)
	assert.NoError(t, err)
	assert.Equal(t, data, loadedPayload)
}

func TestSerializerDumpAndLoadToFile(t *testing.T) {
	s := NewSerializer("secret")
	data := map[string]interface{}{"a": 1, "b": 2}
	filePath := "token.txt"
	f, err := os.Create(filePath)
	assert.NoError(t, err)
	defer os.Remove(filePath)
	defer f.Close()
	err = s.Dump(data, f)
	assert.NoError(t, err)
	f.Close()
	f2, err := os.Open(filePath)
	assert.NoError(t, err)
	defer f2.Close()
	loaded, err := s.Load(f2)
	assert.NoError(t, err)
	assert.Equal(t, data, loaded)
}