package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// Simulates the Java @Named string mappings
type NamedFeather struct{}

func (f *NamedFeather) Instance(key string) interface{} {
	switch key {
	case "hello":
		return "Hello!"
	case "hi":
		return "Hi!"
	default:
		return nil
	}
}

func TestNamedInstanceWithModule(t *testing.T) {
	feather := &NamedFeather{}
	assert.Equal(t, "Hello!", feather.Instance("hello"))
	assert.Equal(t, "Hi!", feather.Instance("hi"))
}