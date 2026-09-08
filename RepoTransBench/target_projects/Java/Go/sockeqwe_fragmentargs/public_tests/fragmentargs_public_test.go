package public_tests

import (
	"testing"
)

type alternateDummyInjector struct {
	invoked bool
}

func (a *alternateDummyInjector) Inject(target interface{}) {
	if target != nil {
		a.invoked = true
	}
}

func TestInjectWithNoAutoMappingClassDifferentInput(t *testing.T) {
	FragmentArgs{}.inject("publicDummyString")
}

func TestInjectWithAutoMappingInjectorPresentDifferentInjector(t *testing.T) {
	altInjector := &alternateDummyInjector{}
	autoMappingInjector = altInjector

	FragmentArgs{}.inject(2024)

	if !altInjector.invoked {
		t.Errorf("Expected injector to be invoked")
	}
	autoMappingInjector = nil
}