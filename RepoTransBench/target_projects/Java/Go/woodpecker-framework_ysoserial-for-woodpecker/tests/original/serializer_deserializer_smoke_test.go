package original

import (
	"bytes"
	"errors"
	"testing"
	"github.com/stretchr/testify/assert"
	yso "woodpecker-framework-ysoserial"
	"io"
)

func TestSerializerSmoke_NullOutputStream(t *testing.T) {
	err := yso.SerializerSerialize(nil, struct{}{})
	assert.Error(t, err)
}

func TestSerializerSmoke_NullObject(t *testing.T) {
	b := new(bytes.Buffer)
	err := yso.SerializerSerialize(b, nil)
	assert.Error(t, err)
}

func TestDeserializerSmoke_NullInputStream(t *testing.T) {
	_, err := yso.DeserializerDeserialize(nil)
	assert.Error(t, err)
}

func TestDeserializerSmoke_BogusData(t *testing.T) {
	bogus := []byte{1, 2, 3, 4}
	b := bytes.NewBuffer(bogus)
	_, err := yso.DeserializerDeserialize(b)
	assert.True(t, errors.Is(err, io.EOF) || err != nil)
}