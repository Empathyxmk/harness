package public_tests

import (
	"sync/atomic"
	"testing"

	"github.com/stretchr/testify/assert"
)

type DiscoverListener interface {
	Changed(changedPath string)
}

func TestDiscoverWithDifferentPath(t *testing.T) {
	var called int32
	path := "/public/test/path"

	listener := &mockDiscoverListener{path: path, called: &called}

	// simulate notification
	listener.Changed(path)
	assert.True(t, atomic.LoadInt32(&called) != 0, "Listener should be called with public path")
}

type mockDiscoverListener struct {
	path   string
	called *int32
}

func (m *mockDiscoverListener) Changed(changedPath string) {
	if changedPath == m.path {
		atomic.StoreInt32(m.called, 1)
	}
}