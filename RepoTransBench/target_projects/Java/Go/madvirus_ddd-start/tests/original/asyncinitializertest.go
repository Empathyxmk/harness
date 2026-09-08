package original

import (
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
)

var initialized bool

func asyncInit() {
	// Simulates asynchronous initialization.
	go func() {
		initialized = false
		time.Sleep(50 * time.Millisecond)
		initialized = true
	}()
}

func TestAsyncInitializer(t *testing.T) {
	initialized = false
	asyncInit()
	time.Sleep(100 * time.Millisecond)
	assert.True(t, initialized, "Should be initialized after asyncInit")
}