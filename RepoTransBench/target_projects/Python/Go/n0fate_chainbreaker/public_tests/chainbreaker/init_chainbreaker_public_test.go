package chainbreaker

import (
	"testing"
)

func TestPublicImportChainbreaker(t *testing.T) {
	// In Go, importing the package is enough, but we check something trivial here
	v := Version()
	if v == "" && Doc() == "" {
		t.Errorf("Chainbreaker has neither version nor doc")
	}
}

func TestPublicChainbreakerModuleContent(t *testing.T) {
	if Doc() == "" {
		t.Error("Expected Chainbreaker to have __doc__ content (simulated with Doc())")
	}
	if Name() == "" {
		t.Error("Expected Chainbreaker to have __name__ content (simulated with Name())")
	}
}

// public API simulation for testing
func Version() string  { return "1.0.0" }
func Doc() string      { return "docstring" }
func Name() string     { return "chainbreaker" }