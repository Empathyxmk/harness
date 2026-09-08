package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// Simulate polymorphic key-based resolution.
type PolyFeather struct{}

type PolyFoo interface{}
type PolyFooA struct{}
type PolyFooB struct{}

func (f *PolyFeather) Instance(name string) PolyFoo {
	switch name {
	case "A":
		return &PolyFooA{}
	case "B":
		return &PolyFooB{}
	default:
		return nil
	}
}

func TestMultipleImplementations(t *testing.T) {
	feather := &PolyFeather{}
	assert.IsType(t, &PolyFooA{}, feather.Instance("A"))
	assert.IsType(t, &PolyFooB{}, feather.Instance("B"))
}