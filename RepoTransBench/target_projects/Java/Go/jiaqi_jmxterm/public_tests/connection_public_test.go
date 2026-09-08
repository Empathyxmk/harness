package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type Connection interface {
	IsClosed() bool
	Close()
}

type testConnection struct {
	closed bool
}

func (c *testConnection) IsClosed() bool { return c.closed }
func (c *testConnection) Close()         { c.closed = true }

func TestIsClosedInitially(t *testing.T) {
	connection := &testConnection{}
	assert.False(t, connection.IsClosed(), "A new connection should not be closed")
	connection.Close()
	assert.True(t, connection.IsClosed(), "After closing, connection should be closed")
}

func TestMultipleCloseCalls(t *testing.T) {
	connection := &testConnection{}
	connection.Close()
	connection.Close()
	assert.True(t, connection.IsClosed(), "Connection should remain closed after multiple closes")
}