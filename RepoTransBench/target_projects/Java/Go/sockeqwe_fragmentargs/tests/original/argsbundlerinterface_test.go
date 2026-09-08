package original

import (
	"testing"
)

type Bundle map[string]interface{}

type ArgsBundler[T any] interface {
	Put(key string, value T, bundle Bundle)
	Get(key string, bundle Bundle) T
}

type StringArgsBundler struct{}

func (s *StringArgsBundler) Put(key string, value string, bundle Bundle) {
	bundle[key] = nil // just exercising the interface
}

func (s *StringArgsBundler) Get(key string, bundle Bundle) string {
	return ""
}

func TestCustomImplementation(t *testing.T) {
	bundler := &StringArgsBundler{}
	bundler.Put("foo", "bar", Bundle{})
	bundler.Get("foo", Bundle{})
}