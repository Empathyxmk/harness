package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

type TableFactory interface {
	ToString() string
}

type NexmarkTableSourceFactory struct{}

func (f NexmarkTableSourceFactory) ToString() string { return "NexmarkTableSourceFactory" }

func TestFactoryClassType(t *testing.T) {
	var factory TableFactory = NexmarkTableSourceFactory{}
	_, ok := factory.(NexmarkTableSourceFactory)
	assert.True(t, ok)
}

func TestFactoryToStringNotNull(t *testing.T) {
	var factory TableFactory = NexmarkTableSourceFactory{}
	assert.NotEmpty(t, factory.ToString())
}