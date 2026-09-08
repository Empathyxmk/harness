package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type ProviderB struct{}

type ProviderA struct {
	provider func() *ProviderB
}

type ProviderFeather struct{}

func (f *ProviderFeather) Instance(t string) interface{} {
	switch t {
	case "A":
		return &ProviderA{
			provider: func() *ProviderB { return &ProviderB{} },
		}
	default:
		return nil
	}
}

func TestProviderInjected(t *testing.T) {
	feather := &ProviderFeather{}
	a := feather.Instance("A").(*ProviderA)
	assert.NotNil(t, a.provider())
}