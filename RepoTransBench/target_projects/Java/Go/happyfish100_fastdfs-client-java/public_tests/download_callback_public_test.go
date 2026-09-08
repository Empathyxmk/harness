package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type TestDownloadCallbackPublic struct {
	LastBytes    int
	LastFileSize int64
	LastData     []byte
}

func (cb *TestDownloadCallbackPublic) Recv(fileSize int64, data []byte, bytes int) int {
	cb.LastFileSize = fileSize
	cb.LastData = data
	cb.LastBytes = bytes
	return 0
}

func TestCallbackPublic(t *testing.T) {
	cb := &TestDownloadCallbackPublic{}
	data := []byte{10, 20, 30, 40, 50}
	result := cb.Recv(987654321, data, len(data))
	assert.Equal(t, 0, result)
	assert.Equal(t, int64(987654321), cb.LastFileSize)
	assert.Equal(t, data, cb.LastData)
	assert.Equal(t, len(data), cb.LastBytes)
}