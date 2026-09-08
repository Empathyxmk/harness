package tests

import (
	"bytes"
	"errors"
	"io"
	"testing"

	"github.com/stretchr/testify/mock"
)

// TestError is a convenient error for error-case mocks.
var TestError = errors.New("fail")

// DummyMailProvider mocks MailProvider interface for MailProvider tests.
type DummyMailProvider[T any] struct {
	mock.Mock
	Throw bool
	Value T
}

func (d *DummyMailProvider[T]) Get() (T, error) {
	args := d.Called()
	if d.Throw {
		var zero T
		return zero, TestError
	}
	return d.Value, nil
}

// DummyIoProvider mocks IoProvider interface for IoProvider tests.
type DummyIoProvider[T any] struct {
	mock.Mock
	Throw bool
	Value T
}

func (d *DummyIoProvider[T]) Get() (T, error) {
	args := d.Called()
	if d.Throw {
		var zero T
		return zero, TestError
	}
	return d.Value, nil
}

// ReadAll is used in public IoProvider tests.
// Simulates io.ReadAll for public test.
func ReadAll(r io.Reader) ([]byte, error) {
	buf := new(bytes.Buffer)
	_, err := buf.ReadFrom(r)
	return buf.Bytes(), err
}