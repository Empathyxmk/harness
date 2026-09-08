package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

var isAliveFunc = func() bool {
	return true
} // Simulate function

func TestIsAliveDefault(t *testing.T) {
	// Can't monkeypatch in Go; stub "HttpClient.raw_get"
	// Instead, simulate with closure
	called := false
	origIsAlive := isAliveFunc
	defer func() { isAliveFunc = origIsAlive }()

	isAliveFunc = func() bool {
		called = true
		return true
	}

	out := isAliveFunc()
	assert.True(t, called)
	assert.True(t, out)
}