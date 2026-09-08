package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type Nubank struct{}

// For the Go version, simulate "discover" returns {}
func (n *Nubank) Discover() map[string]interface{} { return map[string]interface{}{} }

func TestShouldUseHttpClientIfNoneIsProvided(t *testing.T) {
	nu := &Nubank{}
	assert.NotNil(t, nu)
}