package public_tests

import (
	"testing"
	"github.com/example/initstring_linkedin2username"
)

func TestPublicBasicImports(t *testing.T) {
	// In Go, imports are checked by successful compile/import.
	nm := linkedin2username.NewNameMutator("Test Public Import")
	if nm == nil {
		t.Errorf("Expected to find NewNameMutator symbol")
	}
}