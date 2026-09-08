package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type TestDownloadCallback struct {
	LastBytes    int
	LastFileSize int64
	LastData     []byte
}

func (cb *TestDownloadCallback) Recv(fileSize int64, data []byte, bytes int) int {
	cb.LastFileSize = fileSize
	cb.LastData = data
	cb.LastBytes = bytes
	return 0
}

func TestRecv(t *testing.T) {
	cb := &TestDownloadCallback{}
	data := []byte{1, 2, 3}
	result := cb.Recv(123, data, len(data))
	assert.Equal(t, 0, result)
	assert.Equal(t, int64(123), cb.LastFileSize)
	assert.Equal(t, data, cb.LastData)
	assert.Equal(t, len(data), cb.LastBytes)
}