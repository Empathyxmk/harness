package public_tests

import (
	"bytes"
	"testing"

	"github.com/stretchr/testify/assert"
	yso "woodpecker-framework-ysoserial"
)

type dummy struct {
	Value string
}

func TestSerializerDeserializerPublic_SerializeDeserializeSimple(t *testing.T) {
	d := &dummy{Value: "public_test_1"}
	out := new(bytes.Buffer)
	err := yso.SerializerSerialize(out, d)
	assert.NoError(t, err)
	in := bytes.NewBuffer(out.Bytes())
	obj, err := yso.DeserializerDeserialize(in)
	assert.NoError(t, err)
	val, ok := obj.(*dummy)
	assert.True(t, ok)
	assert.Equal(t, "public_test_1", val.Value)
}

func TestSerializerDeserializerPublic_SerializeDeserializeNull(t *testing.T) {
	out := new(bytes.Buffer)
	err := yso.SerializerSerialize(out, nil)
	assert.NoError(t, err)
	in := bytes.NewBuffer(out.Bytes())
	obj, err := yso.DeserializerDeserialize(in)
	assert.NoError(t, err)
	assert.Nil(t, obj)
}