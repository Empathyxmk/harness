package public_tests

import (
	"os"
	"testing"

	"github.com/stretchr/testify/assert"
)

type ThunderbirdMailStorage struct {
	file *os.File
}

func NewThunderbirdMailStorage(filename string) (*ThunderbirdMailStorage, error) {
	f, err := os.CreateTemp("", "pubmailbox")
	if err != nil {
		return nil, err
	}
	return &ThunderbirdMailStorage{file: f}, nil
}

func TestCanCreateFromDifferentFile(t *testing.T) {
	storage, err := NewThunderbirdMailStorage("/tmp/pubmailbox")
	assert.NoError(t, err)
	assert.NotNil(t, storage)
}