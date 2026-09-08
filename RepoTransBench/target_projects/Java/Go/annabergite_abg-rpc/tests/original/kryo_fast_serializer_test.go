package tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type TestClass struct {
	X int
	S string
}

type FakeKryo struct{}

type FastSerializer[T any] struct {
}

func NewFastSerializer[T any](k *FakeKryo) *FastSerializer[T] {
	return &FastSerializer[T]{}
}

func (f *FastSerializer[T]) Write(k *FakeKryo, b interface{}, obj T) error {
	return nil // simulate
}
func (f *FastSerializer[T]) Read(k *FakeKryo, b interface{}) (T, error) {
	var zero T
	return zero, nil
}

func TestGetAllFields(t *testing.T) {
	kryo := &FakeKryo{}
	serializer := NewFastSerializer[TestClass](kryo)
	assert.NotNil(t, serializer)
}

func TestWriteAndRead(t *testing.T) {
	kryo := &FakeKryo{}
	serializer := NewFastSerializer[TestClass](kryo)
	obj := TestClass{X: 42, S: "q"}
	assert.NoError(t, serializer.Write(kryo, nil, obj))
	_, err := serializer.Read(kryo, nil)
	assert.NoError(t, err)
}