package public_tests

import (
	"testing"
)

func TestInjectHandlesClassNotFoundExceptionPublicCase(t *testing.T) {
	autoMappingInjector = nil
	FragmentArgs{}.injectFromBundle("alternatePublicData")
	if autoMappingInjector != nil {
		t.Errorf("Expected autoMappingInjector to remain nil (public case)")
	}
}

func TestInjectHandlesInstantiationExceptionPublic(t *testing.T) {
	autoMappingInjector = nil
	FragmentArgs{}.injectFromBundle(555)
	if autoMappingInjector != nil {
		t.Errorf("Expected autoMappingInjector to remain nil (public case)")
	}
}