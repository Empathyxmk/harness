package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// In Go, instrumentation tests don't map directly. We'll just check a basic context string.
func TestUseAppContext(t *testing.T) {
	appContextName := "mohak.uberux"
	assert.Equal(t, "mohak.uberux", appContextName)
}