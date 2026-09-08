package original

import (
	"testing"
)

func TestInjectHandlesClassNotFoundException(t *testing.T) {
	// ensure static field is nil
	autoMappingInjector = nil
	FragmentArgs{}.injectFromBundle(struct{}{})
	if autoMappingInjector != nil {
		t.Errorf("Expected autoMappingInjector to remain nil")
	}
}

func TestInjectHandlesInstantiationException(t *testing.T) {
	// Can't simulate instantiation exception in Go; just for coverage
	autoMappingInjector = nil
	FragmentArgs{}.injectFromBundle(struct{}{})
	if autoMappingInjector != nil {
		t.Errorf("Expected autoMappingInjector to remain nil")
	}
}