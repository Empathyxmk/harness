package public_tests

import (
	"bytes"
	"testing"

	"github.com/stretchr/testify/assert"
	yso "woodpecker-framework-ysoserial"
)

type testObj struct {
	N int
}

func TestSerializerDeserializerSmokePublic_IntSerialization(t *testing.T) {
	obj := &testObj{N: 9876}
	out := new(bytes.Buffer)
	err := yso.SerializerSerialize(out, obj)
	assert.NoError(t, err)
	in := bytes.NewBuffer(out.Bytes())
	o, err := yso.DeserializerDeserialize(in)
	assert.NoError(t, err)
	val, ok := o.(*testObj)
	assert.True(t, ok)
	assert.Equal(t, 9876, val.N)
}