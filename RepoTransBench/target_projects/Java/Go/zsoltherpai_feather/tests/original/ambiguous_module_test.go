package original

import (
	"testing"
)

type AmbiguousFeather struct{}

func (f *AmbiguousFeather) New(mod *AmbiguousModule) error {
	// Simulates error on ambiguous module (multiple providers for the same type)
	return &FeatherException{}
}

type AmbiguousModule struct{}

func TestAmbiguousModule(t *testing.T) {
	feather := &AmbiguousFeather{}
	err := feather.New(&AmbiguousModule{})
	if err == nil {
		t.Fatal("Expected FeatherException but got nil")
	}
}