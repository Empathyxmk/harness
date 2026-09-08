package original

import (
	"bytes"
	"os"
	"reflect"
	"testing"
	"github.com/stretchr/testify/assert"
	yso "woodpecker-framework-ysoserial"
	"io"
)

type DummySerializable struct {
	Value string
}

func (d DummySerializable) Equal(o any) bool {
	other, ok := o.(*DummySerializable)
	if !ok {
		return false
	}
	return d.Value == other.Value
}

func TestSerializeAndDeserialize(t *testing.T) {
	testObj := &DummySerializable{"foo"}
	data, err := yso.SerializerSerializeToBytes(testObj)
	assert.NoError(t, err)
	result, err := yso.DeserializerDeserialize(bytes.NewBuffer(data))
	assert.NoError(t, err)
	assert.True(t, reflect.DeepEqual(testObj, result))
}

func TestSerializerCallable(t *testing.T) {
	testObj := &DummySerializable{"bar"}
	s := yso.NewSerializer(testObj)
	data, err := s.Call()
	assert.NoError(t, err)
	res, err := yso.DeserializerDeserialize(bytes.NewBuffer(data))
	assert.NoError(t, err)
	assert.True(t, reflect.DeepEqual(testObj, res))
}

func TestDeserializerCallable(t *testing.T) {
	testObj := &DummySerializable{"baz"}
	s := yso.NewSerializer(testObj)
	data, err := s.Call()
	assert.NoError(t, err)
	d := yso.NewDeserializer(data)
	res, err := d.Call()
	assert.NoError(t, err)
	assert.True(t, reflect.DeepEqual(testObj, res))
}

func TestSerializeToOutputStream(t *testing.T) {
	testObj := &DummySerializable{"baz"}
	buf := new(bytes.Buffer)
	err := yso.SerializerSerialize(buf, testObj)
	assert.NoError(t, err)
	res, err := yso.DeserializerDeserialize(bytes.NewBuffer(buf.Bytes()))
	assert.NoError(t, err)
	assert.True(t, reflect.DeepEqual(testObj, res))
}

func TestDeserializeFromInputStream(t *testing.T) {
	testObj := &DummySerializable{"boo"}
	data, err := yso.SerializerSerializeToBytes(testObj)
	assert.NoError(t, err)
	res, err := yso.DeserializerDeserialize(bytes.NewBuffer(data))
	assert.NoError(t, err)
	assert.True(t, reflect.DeepEqual(testObj, res))
}

func TestMainMethodOfDeserializer(t *testing.T) {
	testObj := &DummySerializable{"mainTest"}
	data, err := yso.SerializerSerializeToBytes(testObj)
	assert.NoError(t, err)

	tmpfile, err := os.CreateTemp("", "serTest.ser")
	assert.NoError(t, err)
	defer os.Remove(tmpfile.Name())
	_, err = tmpfile.Write(data)
	assert.NoError(t, err)
	tmpfile.Close()

	// Simulate os.Stdin redirection and Deserializer main
	origStdin := os.Stdin
	f, err := os.Open(tmpfile.Name())
	assert.NoError(t, err)
	defer f.Close()
	os.Stdin = f
	defer func() { os.Stdin = origStdin }()
	yso.DeserializerMain([]string{})
	// Should not throw error
}

func TestSerializeNullThrows(t *testing.T) {
	_, err := yso.SerializerSerializeToBytes(nil)
	assert.Error(t, err)
}